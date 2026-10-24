"""IW browser capture, refresh-verified export and recovery inspection. No import or play commands."""
from __future__ import annotations

import argparse
import json
import hashlib
import uuid
import tempfile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def selected_page(browser, index):
    pages = [p for c in browser.contexts for p in c.pages
             if urlparse(p.url).hostname in {"infiniteworlds.app", "www.infiniteworlds.app"}]
    if index is None:
        if len(pages) != 1:
            raise ValueError(f"Found {len(pages)} IW tabs. Run status, then supply --tab INDEX.")
        return pages[0]
    if index < 0 or index >= len(pages):
        raise ValueError("Tab index is outside the IW tab list; run status again.")
    return pages[index]


def fresh_dir(path):
    path = path.resolve()
    path.mkdir(parents=True, exist_ok=False)
    return path


def capture(page, out):
    """Publish complete evidence in a fresh directory; preserve previous captures."""
    out = out.resolve()
    if out.exists(): raise ValueError('Capture destination already exists')
    out.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.iw-capture-', dir=out.parent))
    try:
        (stage / 'page.txt').write_text(page.locator('body').inner_text(), encoding='utf8')
        (stage / 'accessibility.yaml').write_text(page.locator('body').aria_snapshot(), encoding='utf8')
        metadata = {'capturedAt': datetime.now(timezone.utc).isoformat(), 'url': page.url,
                    'title': page.title(), 'scope': 'Rendered panels only; neither saved-turn proof nor a full prompt/character database.'}
        (stage / 'capture.json').write_text(json.dumps(metadata, indent=2), encoding='utf8')
        records = [{'path': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(stage.iterdir())]
        (stage / 'manifest.json').write_text(json.dumps({'files': records}, indent=2), encoding='utf8')
        if out.exists(): raise ValueError('Capture destination appeared during capture')
        stage.rename(out)
    finally:
        # stage is allocated directly under the resolved output parent, never user input.
        if stage.exists():
            if stage.resolve().parent != out.parent or not stage.name.startswith('.iw-capture-'):
                raise ValueError('Refusing cleanup outside staging directory')
            shutil.rmtree(stage)
    return out


def world_boxes(page):
    found = []
    for box in page.locator('textarea').all():
        if not box.is_visible(): continue
        try:
            text = box.input_value(); value = json.loads(text)
        except (ValueError, TypeError): continue
        if isinstance(value, dict) and isinstance(value.get('title'), str) and 'schemaVersion' in value:
            found.append((box, text, value))
    return found


def export_current(page, out, expected_title, attempts=80):
    """Back up raw text, invalidate only that buffer, then require regenerated JSON.

    No import/save calls. The original buffer survives on disk even if disconnected.
    Close/reopen/import operations must have finished before using this command.
    """
    out = out.resolve(); backup = out.with_name(out.name + '.before.json')
    receipt = out.with_name(out.name + '.receipt.json')
    if any(p.exists() for p in (out, backup, receipt)): raise ValueError('Output, backup or receipt already exists')
    button = page.get_by_role('button', name='Refresh raw JSON', exact=True)
    if button.count()!=1 or not button.is_visible(): raise ValueError('Open the intended raw JSON panel first')
    found = world_boxes(page)
    if len(found)!=1: raise ValueError('Expected exactly one visible world JSON buffer')
    box, original, before = found[0]
    if before['title']!=expected_title: raise ValueError('Raw world title does not match --expected-title')
    out.parent.mkdir(parents=True, exist_ok=True)
    with backup.open('x', encoding='utf8', newline='') as f: f.write(original)
    sentinel = 'IW_REFRESH_PENDING_' + uuid.uuid4().hex
    changed = False
    try:
        box.fill(sentinel); changed = True
        if box.input_value()!=sentinel: raise ValueError('Could not establish refresh marker')
        button.click()
        for _ in range(attempts):
            page.wait_for_timeout(250)
            text = box.input_value()
            if text == sentinel: continue
            try: value = json.loads(text)
            except (ValueError, TypeError): continue
            if not isinstance(value,dict) or value.get('title')!=expected_title or 'schemaVersion' not in value:
                raise ValueError('Refreshed data does not match the intended world')
            found = world_boxes(page)
            if len(found)!=1 or found[0][1]!=text: raise ValueError('Ambiguous refreshed raw buffers')
            # Same content as original is legitimate: observing the marker replaced is the freshness evidence.
            with out.open('x',encoding='utf8',newline='') as f: f.write(text)
            with receipt.open('x',encoding='utf8') as f:
                json.dump({'capturedAt':datetime.now(timezone.utc).isoformat(),'title':expected_title,
                           'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
                           'freshness':'Observed replacement of a unique marker after Refresh raw JSON.',
                           'scope':'Editor regeneration only; not server persistence or live-state proof.',
                           'backup':backup.name},f,indent=2)
            return out
        raise ValueError('Refresh did not replace the marker within the deadline; no export published')
    finally:
        # Restore only our marker. Never overwrite a newer UI value or retry after disconnection.
        if changed:
            try:
                if box.input_value()==sentinel: box.fill(original)
            except Exception:
                pass  # The on-disk .before.json is the recovery source if detached/disconnected.


def inspect_capture(directory):
    root = directory.resolve()
    m=json.loads((root/'manifest.json').read_text(encoding='utf8')); seen=set()
    for entry in m['files']:
        name=entry['path'];path=(root/name).resolve()
        if not isinstance(name,str) or name in seen or Path(name).is_absolute() or not path.is_relative_to(root):
            raise ValueError('Unsafe/duplicate capture path')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']: raise ValueError('Capture hash mismatch')
        seen.add(name)
    if not {'page.txt','accessibility.yaml','capture.json'}<=seen:raise ValueError('Incomplete capture')
    return {'verifiedFiles':len(seen),'capture':json.loads((root/'capture.json').read_text(encoding='utf8')),
            'recovery':'Compare retained history and controls with the previous capture. Do not infer saved turns from streamed prose. This tool never resubmits, imports or reloads.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=9222)
    commands = ap.add_subparsers(dest="command", required=True)
    launch = commands.add_parser("launch", help="Open dedicated persistent Chromium; log in yourself")
    launch.add_argument("--profile", type=Path, default=Path.home() / ".iw-builder-browser")
    launch.add_argument("--offline", action="store_true", help="Open about:blank for local smoke testing")
    launch.add_argument("--headless", action="store_true", help="For offline verification only")
    inspect = commands.add_parser("inspect", help="Verify an earlier capture offline; no browser actions")
    inspect.add_argument("directory", type=Path)
    commands.add_parser("status", help="List IW tabs; does not navigate or submit anything")
    for name in ("capture", "export-current"):
        cmd = commands.add_parser(name)
        cmd.add_argument("output", type=Path)
        cmd.add_argument("--tab", type=int)
        if name == "export-current": cmd.add_argument("--expected-title", required=True)
    args = ap.parse_args()
    if not 1024 <= args.port <= 65535:
        ap.error("Use a local port between 1024 and 65535")
    if args.command == "inspect":
        try: print(json.dumps(inspect_capture(args.directory), indent=2)); return
        except (ValueError, OSError, KeyError, TypeError) as exc: ap.exit(1, str(exc)+"\n")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        ap.exit(2, "Install dependencies first: python -m pip install -r requirements.txt\n")
    try:
        with sync_playwright() as pw:
            if args.command == "launch":
                if args.headless and not args.offline:
                    ap.error("Headless launch is only supported with --offline")
                # A fresh dedicated profile avoids disturbing the everyday browser.
                context = pw.chromium.launch_persistent_context(
                    str(args.profile.resolve()), headless=args.headless,
                    args=[f"--remote-debugging-port={args.port}", "--remote-debugging-address=127.0.0.1"],
                )
                page = context.pages[0] if context.pages else context.new_page()
                page.goto("about:blank" if args.offline else "https://infiniteworlds.app/",
                          wait_until="domcontentloaded")
                print(f"Browser ready at http://127.0.0.1:{args.port}", flush=True)
                print("Keep this terminal open. Log in directly in the browser. Press Enter here to close.", flush=True)
                try:
                    input()
                finally:
                    context.close()
                return
            browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{args.port}", timeout=10000)
            if args.command == "status":
                pages = [p for c in browser.contexts for p in c.pages
                         if urlparse(p.url).hostname in {"infiniteworlds.app", "www.infiniteworlds.app"}]
                for i, page in enumerate(pages):
                    print(f"[{i}] {page.title()} — {page.url}")
                if not pages:
                    print("Connected; no IW tab is open.")
                return
            page = selected_page(browser, args.tab)
            if args.command == "capture":
                print(capture(page, args.output))
            else:
                print(export_current(page, args.output, args.expected_title))
            # Stopping this client disconnects; do not close the persistent browser.
    except Exception as exc:
        ap.exit(1, f"{type(exc).__name__}: {exc}\nRun launch in another terminal; verify the selected panel and capture it if a selector failed.\n")


if __name__ == "__main__":
    main()
