# Validator and maintainer tools

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

These are not steps a world author must run:

```sh
python tools/test_validator.py
python tools/test_data_bank.py
python tools/check_package.py
python tools/build_chat_edition.py
```

The validator regression tests exercise static diagnostics, reduced-coverage operation and diff reporting. They are not an IW or model qualification suite. The package checker validates distributed world files and links and writes Validation-Report.json. build_chat_edition.py assembles the source files without independent edits; rerun it after changing source documents or examples.

The chat-edition generator also emits IW-Tools.txt, including tool source, schema, documentation and packaged reports. It does not execute validation.
