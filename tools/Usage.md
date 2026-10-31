# Tool usage and validation reference

Run commands from the package root. Python reads and writes package files explicitly as UTF-8. No tool here submits a game turn, imports a world or publishes content; none executes IW or PawScript.

## Validate an authored world

```sh
python tools/validate_iw_export.py WORLD.json --json
python tools/validate_iw_export.py WORLD.json --diff ORIGINAL.json --json
```

Install jsonschema for full schema coverage:

```sh
python -m pip install jsonschema
```

Without jsonschema, the validator reports schema-validation-unavailable and uses limited type/requiredness guards before checking references and lint. This is deliberately reduced coverage, not a substitute implementation of JSON Schema. Read the coverage object in JSON output. Exit status is 0 when no errors were found (warnings may remain), 1 for validation errors, and 2 for unreadable files/invalid JSON. No output certifies import or gameplay success.

### What it checks

- Full structural types/constraints when jsonschema is present.
- Explicit tracker, block, trigger, PC and skill references; duplicate IDs and wrapper/payload mismatches.
- Likely undeclared roots in Run Script, conditions, startup-choice expressions and <<...>> templates throughout the export. Declared tracker variableName values, script locals, $game and $player are accounted for. Video-context placeholders are reported separately where applicable.
- Likely borrowed operators and block syntax outside quoted literals/comments, and common string-plus concatenation mistakes.
- Recognizable library editing placeholders. Generic comments and intentional runtime notation should not be removed just to silence warnings.
- Searchable content-substitution markers, reported as review warnings rather than import errors; reconcile them with the separate Authoring report.
- A trailing newline in the actual input file.
- Native string turn thresholds, the editor-recognized first-action/Other Character effects and the turn_number root are accepted. Exact Scenario mismatches are errors when a registry is present; an absent registry produces migration guidance, since import populates it. Non-alphanumeric tracker IDs, a tracker without `description` and a value effect without `replaceWith` produce import-risk advisories. Findings identify the owning tracker/trigger Name where available; JSON paths remain technical coordinates.
- In --diff mode, added/removed/changed object IDs, ordering changes and changed field paths. Long string values are summarized with length and hash; the files remain the authoritative complete values.

### Limitations and warning review

Static lint is heuristic. It does not parse all PawScript, resolve arbitrary dynamic paths, model control flow, evaluate templates, or validate the full formatSchema language. Script locals are recognized lexically; declaration order and every branch scope are not proven. A root warning can expose a missing tracker or a context-specific engine variable; investigate it rather than inventing a tracker automatically. New syntax can produce false positives.

The module library deliberately contains authoring slots and alternative dependency sets, so placeholder/root warnings there are expected until the selected modules are adapted. Finished worlds should have no unexplained warnings. A native YAML path can be semantically wrong even when all static checks pass; compare it with the intended runtime structure.

The validator's review advisories cover repeat accumulation, separate script transaction boundaries, computed choice domains, multiple-choice storage and independently evaluated random expressions. They are prompts to inspect intent, never hard prohibitions or proof that a guard is missing; an existing guard can legitimately trigger a review notice.

A diff proves what changed, not whether those changes are authorized or correct. Reordered arrays can generate positional changes while the object-ID summary remains easier to read.

## Compare a source world with its native re-export

```sh
python tools/import_audit.py source.json imported.json
```

The report includes source hashes, complete structural differences, possible tracker-ID changes and references still pointing at removed tracker targets. Possible identity changes require a unique Name/variable-handle candidate; ambiguity is reported, never automatically repaired. Array changes remain visible even when positional reordering makes them noisy. No input is modified. Full schema coverage depends on jsonschema; source hashes and comparison do not. Import normalization and what to check afterwards are described in [Editor and UI](../reference/Editor-UI.md#import-export-and-preserving-work).

## Portable data and full-content reports

`data_bank.py` exports selected native content or the entire world into a readable text bank with authoritative JSON and an integrity hash. It also packs/unpacks editable bank JSON and restores unchanged complete-world reports. It does not automatically integrate entries or infer their dependencies. See [Portable-Banks.md](../reference/Portable-Banks.md) for commands, tags, bundles, PC/NPC conversion and preservation rules. No third-party dependencies are required. Output files are never silently overwritten.

## Sort characters, triggers and trackers

`iw_sort.py` reorders a world's Player Characters, Other Characters, Triggers and Trackers through a plain text list, so you can sort them by cutting and pasting lines instead of dragging items in the editor. Standard library only.

The simplest way is to copy `iw_sort.py` into the folder with your world JSON and double-click it, or run `python iw_sort.py` there with no arguments. The first run writes `WORLD.order.txt`: a `[Player Characters]`, `[Other Characters]`, `[Triggers]` and `[Trackers]` section, each with one name per line. Move lines within their section and save, then run it again: it finds the world and its text file and writes `WORLD.sorted.json`. The input world is never changed.

With no arguments it sorts a world that has a matching `WORLD.order.txt` or `WORLD.txt`, otherwise exports a lone world, and otherwise lists the worlds and asks (a path can also be typed or dragged in). It skips its own `.sorted.json` outputs and asks before replacing an existing output. Delete the text file to export afresh.

The modes can also be named:

```sh
python tools/iw_sort.py export WORLD.json
python tools/iw_sort.py apply WORLD.json WORLD.order.txt
```

Use `-o` to name the output and `--force` to overwrite an existing one; without `--force` these never overwrite.

- Nothing is dropped. An item left out of the list stays at the end of its section, with a warning. A line that matches nothing is reported and ignored, and a section left out is left as it is.
- Duplicate names are matched in their original order. Blank names appear as `<unnamed>`. Lines starting with `#` are ignored.
- `positionInList` is renumbered to the new order. Indentation and line endings follow the input, so an unedited list gives a byte-identical file.
- Trigger order is execution order (see [Triggers](../reference/Triggers.md)), so moving triggers can change how a world plays. The tool warns when it does.

Unedited round trips are byte-identical and shuffled worlds pass the validator. After importing a sorted world, confirm that the editor shows the new order.

## Extract story text without silently resolving ambiguity

These commands operate on files, not the live game. They do not infer hidden character records or certify narrative consistency.

```sh
python tools/story_export.py plan story.txt --world world.json --session my-session --branch main > plan.json
```

The plan proposes turn, section and tracker line ranges using the world's tracker Names. Review the actual source at those ranges, correct any boundary mistaken for prose/data, resolve reviewIssues, and set reviewed to true. A human or an AI with access to the source can perform this review. This is a data-review requirement, not a request to rerun the story. Duplicate tracker Names cannot be safely represented as a Name-keyed state map; resolve that ambiguity before extraction.

Native story text has no escaping contract for headings. An embedded marker that looks exactly like a real turn or section can be indistinguishable by syntax alone. The source hash locks a plan to the reviewed bytes; review is an operator assertion, not an authenticated platform identity or a proof of automatic parsing correctness. Unknown prose headings are retained, and detected duplicate/out-of-order known boundaries are rejected.

Then run:

```sh
python tools/story_export.py build plan.json --output new-extraction
python tools/story_export.py verify new-extraction
```

Output includes original source bytes, reviewed plans, story.json and a SHA-256 manifest. Tracker values remain raw text, preserving nested YAML and multiline content rather than inventing typed structure. Blank separators may remain in raw value spans. Section text and original bytes provide the complete source representation. Line ranges are one-based and inclusive.

The output path must be new. Publication uses a fresh sibling staging directory, validates its hashes and renames the completed directory into place. Existing output is never reused or deleted, preventing stale files from masquerading as new state. Read only manifest-listed files; verify checks their hashes and ignores unrelated files.

### Merge only an explicitly selected history

Supply multiple reviewed plans to build. Every plan must declare the same nonempty session and branch. Neither title, player Name, timestamp nor overlap proves identity. Identical overlapping turn content and extraction can deduplicate, retaining all source provenance. Any conflicting overlap is rejected, independent of file modification time or input order.

Select a single coherent branch before building conflicting history; the tool offers no latest-file winner and does not combine downstream turns from divergent branches automatically. Complete histories require turn one and no gaps. --partial permits a contiguous later range and labels it partial; it does not permit holes or silently promote partial history to complete.

## Plot compiler

`tools/plot_compile.py` is a local authoring tool, not a platform API. It accepts a deliberately bounded plan: title and nodes; each node has an internal lowercase identifier, a user-facing Name, a literal Scenario, optional all-of prerequisites and a nonnegative integer award. It builds a fresh world, never modifies an existing one. See [example plan](example-plot-plan.json).

```sh
python tools/plot_compile.py tools/example-plot-plan.json
python tools/plot_compile.py tools/example-plot-plan.json --output new-world.json
```

Without output, it reports dependency order, roots, structurally reachable nodes and shared Scenarios. With output, it also validates and writes a new world; existing files are refused. Full schema checks need `jsonschema`; otherwise the report explicitly identifies reduced coverage.

Generation puts prerequisite triggers before their dependents. A single script guards both completion and award and commits them together, allowing retry when a script has not completed. The resulting world uses literal Scenarios and a script-owned Plot progress tracker. Two eligible nodes sharing a Scenario may both complete in one turn; no hidden priority or fairness rule is implied. Later narration sees committed state according to platform timing; the compiler does not rewrite narration retrospectively.

Unknown prerequisites, cycles, duplicate identifiers, dynamic Scenario templates and unsupported plan fields are rejected. This compiler supports prerequisite DAGs, not arbitrary cyclic plots, mutually exclusive branches or all possible IW worlds. Independent nodes retain author order. It does not infer events from prose or prove that the AI will recognize a Scenario, that a scene is achievable, or that every player's route is possible. Connectivity is not narrative satisfiability. The generated composition is structurally checked, not live-certified.

## Maintainer commands

These are repository maintenance tasks, not requirements for authoring worlds:

```sh
python -m unittest discover -s tools -p "test_*.py"
python tools/check_package.py
python tools/build_distribution.py
```

`check_package.py` validates every example world, checks local Markdown links, runs a few negative checks, and measures hedge density: the number of caveat phrases (the families listed in its `HEDGES` table) per thousand words in each AI-facing document. A document above 3 per thousand is listed under `hedgeWarnings` in its report and output. The rule behind the check: a kit-wide caveat is stated once, at the top of reference/Verified-Behavior.md, and a sentence elsewhere states what is true instead of warning against a misreading; a scope statement ("one world, Dolphin") or a real unknown is kept.

`build_distribution.py` uses its own location in `/tools` to find the repository, so it needs no arguments and works from any working directory. It uses only Python's standard library. It updates the END OF DOCUMENT markers in AI-facing Markdown documents, generates `index.html` from `Authoring-Prompt.md`, synchronizes the checker's embedded validator/schema, writes the combined chat TXT files and `chat/sources.json`, generates `llms.txt` and the folder index pages from its descriptions table, then hashes the finished files into root `manifest.json`. It does not run validation or rebuild ZIP archives: run `check_package.py` before building when worlds or tools changed, and repackage `full-package.zip` after the build when distributing a new archive. Required sources are checked before output begins; a missing source or checker embedding stops the build with an error. Repeated builds with unchanged inputs preserve output bytes and the manifest timestamp.

`IW-Tools.txt` carries the authoring tools only: this usage guide, the validator, static checks, JSON schema, data-bank utility, import audit, story-export tool and plot compiler. Builders, regression tests, package reports, human READMEs and the world sorter (a hands-on editing tool) stay in the repository but are omitted from that model-facing bundle.

The root manifest records repository-relative paths, byte lengths and SHA-256 hashes for the authoring sources and supported files under reference, library, examples, tools, chat, cost and checker, plus the homepage and root guide/template/license. It excludes itself, ZIP archives, sample histories, hidden files and caches. Hash original bytes, never a browser's rendered/extracted text. A mismatch may mean the manifest is stale; investigate apparent missing content without treating every mismatch as damage. A match establishes the recorded bytes, not freshness or runtime correctness.

END OF DOCUMENT markers are added only to AI-facing Markdown and the generated chat documents, not to JSON, scripts, the native default Evaluation text or other directly reusable content. They are documentation boundaries, not world instructions to copy into a story.

---

END OF DOCUMENT: tools/Usage.md
