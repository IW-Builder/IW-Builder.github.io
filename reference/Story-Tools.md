# Story extraction and import diagnostics

These local tools operate on files, not the live game. They do not infer hidden character records, run PawScript or certify narrative consistency.

## Compare a source world with its native re-export

Run:

```sh
python tools/import_audit.py source.json imported.json
```

The report includes source hashes, complete structural differences, possible tracker-ID changes and references still pointing at removed tracker targets. Possible identity changes require a unique Name/variable-handle candidate; ambiguity is reported, never automatically repaired. Array changes remain visible even when positional reordering makes them noisy. No input is modified.

The validator supports native string turn thresholds, the editor-recognized first-action/Other Character effects, and the verified turn_number root. Exact Scenario mismatches are errors when a registry is present; an absent registry produces migration guidance, since import populates it. Non-alphanumeric tracker IDs, a tracker without `description` and a value effect without `replaceWith` produce import-risk advisories. Findings identify the owning tracker/trigger Name where available; JSON paths remain technical coordinates.

## Extract story text without silently resolving ambiguity

Run:

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

## Merge only an explicitly selected history

Supply multiple reviewed plans to build. Every plan must declare the same nonempty session and branch. Neither title, player Name, timestamp nor overlap proves identity. Identical overlapping turn content and extraction can deduplicate, retaining all source provenance. Any conflicting overlap is rejected, independent of file modification time or input order.

Select a single coherent branch/revision before building conflicting history; the tool offers no latest-file winner and does not combine downstream turns from divergent branches automatically. Complete histories require turn one and no gaps. --partial permits a contiguous later range and labels it partial; it does not permit holes or silently promote partial history to complete.

The tool is a conservative IW-Builder implementation. It does not patch the separate external parser.

---

END OF DOCUMENT: reference/Story-Tools.md
