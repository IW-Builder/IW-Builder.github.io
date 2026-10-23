# Portable character and data banks

Data mode maintains reusable content independently of a world. It supports extraction, listing, additions, updates, explicit removals and integration into a destination world. A character bank is one use; the same format holds trackers, triggers, instruction/keyword blocks, scripts, specialist instructions or mixed bundles. This is a kit interchange format, not an IW import format.

## Select the operation

Use the user's existing bank or library when supplied. Preserve unrelated entries, unknown fields, native IDs, string contents and value types. Adding something to one world does not update its source bank; omitting a module does not delete it. Remove entries only on explicit request, checking dependent entries first. Do not silently overwrite or deduplicate entries with matching names.

Tags are optional. Ask or infer the stated preference: no tags, supplied tags, or suggested tags. When suggestions are wanted, derive them from the content and follow existing vocabulary/capitalization if desired. Store tags as plain strings and display them as [fantasy] [merchant]. Tags organize the bank; they are not automatically IW keywords or native fields. Do not retag existing entries without a request.

In Build, Edit, Review or Debug, recognize cohesive reusable content and offer extraction when useful. A shop's accounting tracker, instructions and purchase triggers may form a bundle; unrelated nearby objects do not. Explain what belongs together and let the user choose extraction. Prefer one stored component plus included-entry references over duplicating shared dependencies.

## Authoritative data and readable presentation

The `.txt` bank has a generated readable index followed by one authoritative JSON section. Summaries and [tags] make it easy to browse, but never reconstruct native data from summaries. The section is delimited by full lines `<!-- BEGIN IW DATA BANK -->` and `<!-- END IW DATA BANK -->`, contains one `json` code fence, and ends with `SHA256: <hash>` on the following line, or `SHA256: UNVERIFIED` when no code-based hash was computed. The hash covers the canonical authoritative data, not the index. This is transport integrity, not proof of provenance or gameplay correctness.

The authoritative object has `format: "iw-data-bank"`, integer `version: 1`, and an `entries` array. Other metadata is preserved. Each entry contains:

| Field | Purpose |
| --- | --- |
| id | Stable bank identity, separate from every native IW ID |
| title, kind, summary | Human-readable name, content type and optional summary text |
| tags | Optional list of strings; omit when unused |
| dependencies.included | IDs of other entries present in this bank |
| dependencies.external | Required objects, variables or context not included |
| dependencies.unresolved | Concrete questions or remaining dependency review |
| components | One or more objects with kind, optional sourcePath, and complete payload |

`payload` stores the original JSON value, including unknown keys and nested content. A standalone script can use a string payload and metadata identifying its context (Run Script, predicate or template) and required variables. An NPC or tracker stores its complete native object. A bundle stores multiple components; its `kind` is `bundle`. Keep sourcePath as an escaped JSON Pointer when extracted, such as `/NPCs/0` or `/triggerEvents/2`. Paths record provenance, not a command to overwrite that position in another world.

Retain the original native payload during PC/NPC conversion. Create the requested counterpart as a distinct component or entry, mapping appropriate identity, appearance and narrative information into its native fields. PC skills/selection fields and NPC activation/image fields are not interchangeable. Report newly supplied defaults and preserve unmapped source information; do not claim the conversion is a lossless relabeling. IW can offer the same canonical name as both PC and NPC without exclusion prose.

## Dependencies and application

Record dependencies as included, external or unresolved. Native IDs can be checked statically; variable roots, prose references and dynamic paths require review. The export helper does not automatically infer them and marks dependency review as unresolved. A physically complete export is not proof of a self-contained mechanic.

To apply entries, inspect the destination and preserve its unrelated content. Resolve native IDs, variable names, skills, activation requirements, ordering, starting values and referenced blocks. Remap collisions consistently; never run a blind global string replacement. Keep bank IDs unchanged. Report adaptations, additions and unresolved dependencies, and validate the complete destination world. A source bank remains unchanged unless its update was requested.

## Full-content build report

Offer this optional deliverable whenever outputting a world. It is a portable report of all fields and objects, not a prose inventory: export the full world, including metadata and unknown fields, with a restoration layout and source fingerprint. It can later supply selected entries or restore the original world definition. It is separate from the Authoring report containing explanations, substitutions and verification notes.

A complete report retains array ordering, empty containers and root fields. Bundling components does not remove their source paths. Removing or changing components invalidates exact restoration; integrate such edits deliberately rather than changing the fingerprint to conceal differences. This is JSON-data equivalence, not byte-for-byte preservation of whitespace, key formatting or numeric spellings. Scripts and other string contents remain exact.

## Tool workflow

Run from the kit root; no third-party Python dependencies are required:

```sh
# Full-content report; restores the complete world definition.
python tools/data_bank.py export World.json --out Build-Report.txt
python tools/data_bank.py check Build-Report.txt
python tools/data_bank.py restore Build-Report.txt --out Restored-World.json

# Selected objects; repeat --select and optionally --tag.
python tools/data_bank.py export World.json --select /NPCs/0 --out Character-Bank.txt --tag fantasy

# A selected mechanical bundle; review its dependencies before reuse.
python tools/data_bank.py export World.json --select /trackedItems/0 --select /triggerEvents/0 --bundle "Shop system" --out Shop-Bank.txt

# Edit authoritative JSON with tools, then rebuild presentation and hash.
python tools/data_bank.py unpack Character-Bank.txt --out Bank-Edit.json
python tools/data_bank.py pack Bank-Edit.json --out Updated-Bank.txt
```

Output paths must be new; the tool refuses silent overwrite. Check the updated bank, preserve a prior copy, and return the complete new file. For a manual merge, unpack both, retain entries and dependencies, resolve conflicting bank IDs deliberately, then pack the combined data. Do not carry a completeWorld restoration claim into a bank combining different sources; retain relevant source metadata per entry instead.

The helper rejects duplicate JSON keys, checks bank structure and included-entry targets, and verifies hashes for text banks. It preserves arbitrary-precision integers and decimal numbers without float rounding. Its hash check does not validate IW payload schemas, semantic dependencies, tags or prose summaries; use the world validator after integration. Unknown bank metadata is preserved.

Without code execution, use the same `.txt` format with `SHA256: UNVERIFIED`, or return the authoritative `.json` bank source with readable discussion separately. Never fabricate a hash or claim round-trip verification. The helper accepts either form, explicitly distinguishes an absent hash from verified integrity, and computes a hash when packing. Large edits should preserve untouched payloads and be checked with tools before claiming losslessness. An upload does not guarantee persistent storage: keep the latest returned bank for future sessions.

---

END OF DOCUMENT: reference/Portable-Banks.md
