# Import and reference integrity

An importable world needs both valid JSON structure and correctly linked objects. Tracker IDs, display names and PawScript variable names serve different purposes. Native effects target tracker IDs; scripts use variableName. Preserve IDs when editing, and remap every corresponding reference when combining examples.

## Identifier convention

Preserve existing IDs when editing. For new trackers, use a unique nine-character ASCII alphanumeric ID, following the editor-style form used by the import-tested examples. Use explicit descriptive snake_case variableName values in scripts and descriptive display names in the editor. This is the kit's authoring convention, not a claim that other ID formats are invalid or that length alone guarantees import behavior. Generate IDs in code and check collisions; without tools, check each newly introduced ID and reference manually. New triggers/blocks/PCs can use the same convention. When combining worlds, remap every explicit reference consistently.

The supplied single-choice world preserves its IDs and binding through a fresh import. Inspect native target dropdowns after importing a composed world; schema validation cannot predict importer behavior for every construction.

## Before import

- Serialize the complete world as JSON ending at its final closing brace, without a trailing newline.
- Run the validator on that exact file. Resolve missing or duplicate IDs and mismatched target references.
- Review native YAML paths against the tracker's declared initial structure and intended operation. The editor can accept unchecked paths without warning. Removing a nonexistent key or appending to a numeric path may be syntactically valid but semantically wrong. Dynamic paths may require runtime inspection rather than a blanket validation error.
- Review script references separately: structural validation does not execute PawScript or prove its paths exist.

## After import

Save and inspect affected target controls. An invalid-value target is a binding failure even if the original JSON had consistent references. Export the imported world and validate that export when diagnosing discrepancies. Preserve the untouched export before repairing a suspect target so source and imported IDs can be compared.

For a native input, confirm the current target value after submitting an answer. Correctly bound single-answer Choice and Request Input effects update immediately, and subsequent ordered triggers can read the result in the same turn. Their follow-up messages can render above the question/answer receipt. The live-world editor's initialValue remains configuration, not the current runtime value.

## Editing an existing playthrough

Base worlds and live games are separate copies. Changes to player characters or Other Characters in the live-world editor do not affect that playthrough; already-fired effects are not retroactively rewritten. Use Save as new world, or export the live JSON and import it over the intended base, to reuse live-world edits in future games. Image-style changes can require save/reload before their export reflects the editor.

## Read-only source/import comparison

[import_audit.py](../tools/import_audit.py) compares original and native-exported worlds, preserves hashes and reports possible tracker identity changes plus references to removed targets. It never repairs or remaps automatically. See [Story tools](Story-Tools.md) for usage.

---

END OF DOCUMENT: reference/Import-Integrity.md
