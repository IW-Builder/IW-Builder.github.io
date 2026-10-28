#!/usr/bin/env python3
"""Fast custom sorting for Infinite Worlds world JSON files.

Two modes:

  export  world.json [-o order.txt]
      Write a plain text file listing the names in each sortable category:
      Player Characters, Other Characters, Triggers and Trackers.

  apply   world.json order.txt [-o sorted.json]
      Reorder those categories in the world to match the (edited) text file
      and write the result to a new world file.

Edit the text file by cutting and pasting lines to new positions inside
their section. Nothing is ever dropped: anything left out of the text file
is kept, after the listed items, and the script warns about it. Names that
do not match anything are reported and ignored.

Standard library only. Python 3.8 or later.
"""

import argparse
import json
import os
import sys
from collections import defaultdict, deque

# (section header in the text file, key in the world JSON)
CATEGORIES = [
    ("Player Characters", "possibleCharacters"),
    ("Other Characters", "NPCs"),
    ("Triggers", "triggerEvents"),
    ("Trackers", "trackedItems"),
]
HEADER_TO_KEY = {header.lower(): key for header, key in CATEGORIES}

# Shown in the text file for an item whose name is blank.
UNNAMED = "<unnamed>"

INTRO = """\
# Sort order for: {title}
#
# Move names up and down inside their [section] by cutting and pasting
# whole lines. Then run:  python iw_sort.py apply <world.json> <this file>
#
# Lines starting with # are ignored, as are blank lines.
# Names left out are kept at the end of their section. A name that appears
# more than once in the world is matched in its original order: the first
# line with that name takes the first item with it, and so on.
# Trigger order is execution order: moving a trigger can change how it plays.
"""


def warn(message):
    print("warning: " + message, file=sys.stderr)


def item_name(item):
    name = item.get("name") if isinstance(item, dict) else None
    if not isinstance(name, str):
        name = "" if name is None else str(name)
    return name


def display_name(item):
    name = item_name(item)
    if not name.strip():
        return UNNAMED
    # A name must fit on one line of the text file.
    return " ".join(name.splitlines()).strip()


def load_world(path):
    # newline="" keeps CRLF visible, so the output can match the input.
    with open(path, encoding="utf-8-sig", newline="") as f:
        text = f.read()
    try:
        world = json.loads(text)
    except json.JSONDecodeError as e:
        sys.exit("error: {} is not valid JSON: {}".format(path, e))
    if not isinstance(world, dict):
        sys.exit("error: {} is not a world JSON (top level is not an object)".format(path))
    if not any(key in world for _, key in CATEGORIES):
        sys.exit("error: {} has none of the sortable lists ({})".format(
            path, ", ".join(key for _, key in CATEGORIES)))
    return world, text


def detect_indent(text):
    """Return the indent the file uses, so the output diffs cleanly."""
    for line in text.splitlines()[1:]:
        stripped = line.lstrip(" \t")
        if stripped and len(stripped) < len(line):
            indent = line[: len(line) - len(stripped)]
            return "\t" if indent.startswith("\t") else len(indent)
    return None  # minified


def check_positions(header, items):
    positions = [item.get("positionInList") for item in items if isinstance(item, dict)]
    if positions and all(isinstance(p, int) for p in positions):
        if positions != list(range(len(positions))):
            warn("{}: positionInList does not match the list order in the file; "
                 "the text file follows the file's list order".format(header))


# ---------------------------------------------------------------- export

def export(world_path, out_path, force):
    world, _ = load_world(world_path)
    lines = [INTRO.format(title=world.get("title") or os.path.basename(world_path))]
    for header, key in CATEGORIES:
        items = world.get(key)
        if not isinstance(items, list):
            continue
        check_positions(header, items)
        lines.append("[{}]".format(header))
        lines.extend(display_name(item) for item in items)
        lines.append("")
        counts = defaultdict(int)
        for item in items:
            name = display_name(item)
            counts[name] += 1
            if name.startswith("#") or (name.startswith("[") and name.endswith("]")):
                warn("{}: '{}' looks like a comment or header in the text file and "
                     "cannot be sorted; it will stay at the end".format(header, name))
        for name, n in counts.items():
            if n > 1:
                warn("{}: '{}' appears {} times; duplicates keep their relative order".format(
                    header, name, n))

    write_new_file(out_path, "\n".join(lines), force)
    print("wrote {}".format(out_path))


# ---------------------------------------------------------------- apply

def parse_order(path):
    """Return {json key: [names in order]} for each section in the text file."""
    with open(path, encoding="utf-8-sig") as f:
        raw_lines = f.read().splitlines()
    sections = {}
    current = None
    for number, line in enumerate(raw_lines, 1):
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        if text.startswith("[") and text.endswith("]"):
            header = text[1:-1].strip()
            key = HEADER_TO_KEY.get(header.lower())
            if key is None:
                warn("line {}: unknown section [{}]; its lines are ignored".format(number, header))
            elif key in sections:
                warn("line {}: section [{}] appears twice; its lines are added to the first".format(
                    number, header))
            else:
                sections[key] = []
            current = key
            continue
        if current is None:
            warn("line {}: '{}' is outside any section; ignored".format(number, text))
            continue
        sections[current].append(text)
    return sections


def reorder(header, items, wanted):
    """Return (new item list, changed?) following the names in `wanted`."""
    pools = defaultdict(deque)
    for index, item in enumerate(items):
        pools[display_name(item)].append(index)

    order = []
    for name in wanted:
        if pools.get(name):
            order.append(pools[name].popleft())
        elif name in pools:
            warn("{}: '{}' is listed more times than it exists; extra line ignored".format(
                header, name))
        else:
            warn("{}: '{}' is not in the world; ignored".format(header, name))

    used = set(order)
    leftovers = [i for i in range(len(items)) if i not in used]
    for i in leftovers:
        warn("{}: '{}' was missing from the text file; kept at the end".format(
            header, display_name(items[i])))
    order.extend(leftovers)

    # Every item exactly once, or something has gone badly wrong.
    assert sorted(order) == list(range(len(items)))
    return [items[i] for i in order], order != list(range(len(items)))


def apply(world_path, order_path, out_path, force):
    world, text = load_world(world_path)
    sections = parse_order(order_path)
    if not sections:
        sys.exit("error: {} has no recognised [section] headers".format(order_path))

    for header, key in CATEGORIES:
        items = world.get(key)
        if not isinstance(items, list):
            if key in sections:
                warn("[{}] is in the text file but the world has no {} list; ignored".format(
                    header, key))
            continue
        if key not in sections:
            print("{}: not in the text file, left as is".format(header))
            continue
        new_items, changed = reorder(header, items, sections[key])
        # Keep positionInList in step with the new order where items carry it.
        for position, item in enumerate(new_items):
            if isinstance(item, dict) and "positionInList" in item:
                if item["positionInList"] != position:
                    item["positionInList"] = position
                    changed = True
        world[key] = new_items
        print("{}: {} ({} items)".format(header, "reordered" if changed else "unchanged",
                                         len(new_items)))
        if changed and key == "triggerEvents":
            warn("trigger order is execution order; test the world after moving triggers")

    indent = detect_indent(text)
    if indent is None:
        output = json.dumps(world, ensure_ascii=False, separators=(",", ":"))
    else:
        output = json.dumps(world, ensure_ascii=False, indent=indent)
    if text.endswith("\n"):
        output += "\n"
    if "\r\n" in text:
        output = output.replace("\n", "\r\n")
    write_new_file(out_path, output, force)
    print("wrote {}".format(out_path))


# ---------------------------------------------------------------- helpers

def write_new_file(path, content, force):
    if os.path.exists(path) and not force:
        sys.exit("error: {} already exists; pick another name with -o or add --force".format(path))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def default_path(world_path, suffix):
    base, _ = os.path.splitext(world_path)
    return base + suffix


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Sort an Infinite Worlds world's Player Characters, Other Characters, "
                    "Triggers and Trackers through an editable text file.")
    sub = parser.add_subparsers(dest="mode", required=True)

    p = sub.add_parser("export", help="write the names in a world to a text file")
    p.add_argument("world", help="world JSON exported from Infinite Worlds")
    p.add_argument("-o", "--output", help="text file to write (default: <world>.order.txt)")
    p.add_argument("--force", action="store_true", help="overwrite the output if it exists")

    p = sub.add_parser("apply", help="reorder a world to match an edited text file")
    p.add_argument("world", help="world JSON to reorder (it is not changed)")
    p.add_argument("order", help="text file made by export, then edited")
    p.add_argument("-o", "--output", help="world JSON to write (default: <world>.sorted.json)")
    p.add_argument("--force", action="store_true", help="overwrite the output if it exists")

    args = parser.parse_args(argv)
    if args.mode == "export":
        export(args.world, args.output or default_path(args.world, ".order.txt"), args.force)
    else:
        out = args.output or default_path(args.world, ".sorted.json")
        if os.path.abspath(out) == os.path.abspath(args.world):
            sys.exit("error: the output would replace the input world; choose another -o")
        apply(args.world, args.order, out, args.force)


if __name__ == "__main__":
    main()
