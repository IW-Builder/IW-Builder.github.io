# Tool usage and validation reference

Run commands from the package root. Python reads and writes package files explicitly as UTF-8.

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

## What it checks

- Full structural types/constraints when jsonschema is present.
- Explicit tracker, block, trigger, PC and skill references; duplicate IDs and wrapper/payload mismatches.
- Likely undeclared roots in Run Script, conditions, startup-choice expressions and <<...>> templates throughout the export. Declared tracker variableName values, script locals, $game and $player are accounted for. Video-context placeholders are reported separately where applicable.
- Likely borrowed operators and block syntax outside quoted literals/comments, and common string-plus concatenation mistakes.
- Recognizable library editing placeholders. Generic comments and intentional runtime notation should not be removed just to silence warnings.
- Searchable content-substitution markers, reported as review warnings rather than import errors; reconcile them with the separate Authoring report.
- A trailing newline in the actual input file.
- In --diff mode, added/removed/changed object IDs, ordering changes and changed field paths. Long string values are summarized with length and hash; the files remain the authoritative complete values.

## Limitations and warning review

Static lint is heuristic. It does not parse all PawScript, resolve arbitrary dynamic paths, model control flow, evaluate templates, or validate the full formatSchema language. Script locals are recognized lexically; declaration order and every branch scope are not proven. A root warning can expose a missing tracker or a context-specific engine variable; investigate it rather than inventing a tracker automatically. New syntax can produce false positives.

The module library deliberately contains authoring slots and alternative dependency sets, so placeholder/root warnings there are expected until the selected modules are adapted. Finished worlds should have no unexplained warnings. A native YAML path can be semantically wrong even when all static checks pass; compare it with the intended runtime structure.

A diff proves what changed, not whether those changes are authorized or correct. Reordered arrays can generate positional changes while the object-ID summary remains easier to read. The tool does not execute scripts or verify runtime behavior.

## Portable data and full-content reports

`data_bank.py` exports selected native content or the entire world into a readable text bank with authoritative JSON and an integrity hash. It also packs/unpacks editable bank JSON and restores unchanged complete-world reports. It does not automatically integrate entries or infer their dependencies. See [Portable-Banks.md](../reference/Portable-Banks.md) for commands, tags, bundles, PC/NPC conversion and preservation rules. No third-party dependencies are required. Output files are never silently overwritten.

## Maintainer commands

These are repository maintenance tasks, not requirements for authoring worlds:

```sh
python tools/test_validator.py
python tools/test_data_bank.py
python tools/test_distribution.py
python tools/check_package.py
python tools/build_distribution.py
```

`build_distribution.py` uses its own location in `/tools` to find the repository, so it needs no arguments and works from any working directory. It uses only Python's standard library. Run validation before building when publishing changed worlds or tools.

The builder updates visible EOF markers in AI-facing Markdown documents, generates `index.html` from `Authoring-Prompt.md`, synchronizes the checker's embedded validator/schema, writes the combined chat TXT files and `chat/sources.json`, then hashes the finished files into root `manifest.json`. It does not produce a separate `prompt.txt`, run validation or rebuild ZIP archives. Repackage `full-package.zip` after the build when distributing a new archive.

Required sources are checked before output begins; a missing source or checker embedding stops the build with an error. Repeated builds with unchanged inputs preserve output bytes and the manifest timestamp. A write failure can leave partial outputs; fix it and rerun before publishing.

`IW-Tools.txt` has an explicit authoring-tool list: this usage guide, validator, static checks, JSON schema and data-bank utility. Builders, regression tests and package reports remain in the repository but are omitted from that model-facing bundle. Human READMEs are also omitted from combined technical packages. No model needs the distribution builder to author a world.

The root manifest records repository-relative paths, byte lengths and SHA-256 hashes. It covers the authoring sources and supported files under reference, library, examples, tools, chat and checker, plus the homepage and root guide/template/license. It excludes itself, ZIP archives, sample histories, hidden files and caches. It is separate from the files it hashes to avoid circular dependencies. Hash original bytes, never a browser's rendered/extracted text. A mismatch may mean the manifest is stale; investigate apparent missing content without treating every mismatch as damage. A match establishes the recorded bytes, not freshness or runtime correctness.

EOF markers are added only to AI-facing Markdown and the generated chat documents. They are not added to JSON, scripts, the native default Evaluation text or other directly reusable content. They are documentation boundaries, not world instructions to copy into a story.

---

END OF DOCUMENT: tools/Usage.md
