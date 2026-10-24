# Trackers and memory

Trackers: `name` is the display label, `id` connects native references, and `variableName` supplies the PawScript root.

“Coins” can have display name `Coins`, variable name `coins`, a unique tracker ID, initial value "10", and `autoUpdate: false`. PawScript reads $coins; native effects target the tracker ID. Purchases change the live value, while the base world's initial value remains the starting configuration.

## Storage, visibility and ownership

Use the dataType vocabulary `text`, `number`, `yaml`, `xml`; do not emit an invented boolean/list dataType. Structured booleans/lists can live inside YAML. UI terminology and storage types are not automatically identical.

Tracker `initialValue` is a JSON STRING even for numbers and YAML: `"10"`, or `"held: 0\nuses: 3\n"`. YAML content inside that string has its own parsed numbers, strings, lists and records. IW text entry does not enforce numeric-only input, but a mathematical tracker should start from an actual numeric literal. This does NOT make the entire export string-valued: JSON booleans, arrays and numeric fields elsewhere retain schema types.

Initialize every mechanical path explicitly. Distinguish 0, false, empty text, an empty list, an absent key and null. Define each value's meaning consistently; numeric 0/1 is one practical flag convention. Narration must not reinterpret a stored value to justify a conflicting story. Treat missing required data as malformed/denied unless the design explicitly defines a fallback. Enforce format does not prevent all malformed manual/script writes; use explicit shape and semantic checks before accepting generated state. Native path adjustment and script assignment have different missing-path behavior, and independent random expressions can disagree, so cache shared choices.

Ownership:

| Tracker role | autoUpdate | Typical use |
| --- | --- | --- |
| Mechanics | false | Inventory flags, money, HP, counters, access, scores, RNG results |
| AI request record | true | Current-turn classification of what the player explicitly requested |
| Soft narrative memory | true | Introductions/observed scenery, when needed and bounded |
| Script staging/cache | false | Prepared active-block text, temporary results, status |

Do not let the AI and scripts compete to rewrite the same mechanical YAML document. Consolidating related flags in a YAML tracker reduces editor clutter; it does not by itself reduce trigger count or guarantee lower token cost. Large AI-visible YAML and duplicative logs still cost context. Keep hidden cache text out of the storyteller unless needed.

Visibility values include everyone (player and AI), ai_only and ai_only_boring (AI-only), player_only, hidden and hidden_boring (hidden from player and AI in supplied uses). Do not infer additional UI highlighting behavior from the suffix alone. The editor clears "Hide in Storyteller mode" when player visibility is enabled. Do not invent contradictory UI combinations. Exports can include hidden trackers and secret information when Storyteller Mode is enabled; select those export options when collecting diagnostics. Visibility is not script access control: hidden values remain script-usable at runtime.

[RUNTIME] Extra-hidden values remain visible in the Storyteller tracker editor even when Include Extra-hidden is off. Import normalizes automatic updating off for hidden, hidden_boring and player_only; everyone, ai_only and ai_only_boring can retain automatic updates. UI visibility does not establish full AI prompt inclusion.

Modify tracked item details accepts all six visibility values with overrideVisibility: true, and can change future automatic updating with overrideAutoUpdate and autoUpdate. The live player-visible/hidden lists reflect a visibility change even when the live-design export retains the original visibility.

Starting values:

- initialValueBasedOnPC same: one initialValue for all PCs.
- character: per-character initialTrackedItemValues entries target the TRACKER ID. Fixed initialPCValue is a string. A fixed single-choice list is an array of strings. A script-generated list uses initialPCValueChoicesScript with initialPCValue empty, as illustrated in ../examples/character-starting-values.json. The expression is evaluated at game start with initial trackers and that PC's skills available, per editor description.
- player: the tracker itself defines a player-chosen startup value. ../examples/optional-block.json exports initialValueBasedOnPC: "player", initialValue: "On", and initialValueChoices: ["On", "Off"]. These are tracker-level fields, independent of per-character initialTrackedItemValues. Use this for an offered startup preference; autoUpdate false prevents AI rewriting it. The user can edit the live preference later. For unconstrained player input or an unusual type, do not assume the choice-list example establishes every corresponding UI control; obtain a representative export only for that additional variant.
- Never combine arbitrary fixed/list/script modes and guess precedence. Do not assume formatSchema is JSON Schema or enforces semantic intent; its exact enforcement language is not established by our sample fields.

Name/handle drift: The editor does not compare Name and variableName as case-sensitive literal strings. Normal generated differences such as Win Path / win_path need no acknowledgement. Use driftAcknowledgedForName for an intentionally different handle when the editor reports a mismatch; its value is the current display Name. It does not rename the variable or change script references. Preserve existing metadata during unrelated edits; do not rename handles or fill null acknowledgements merely because capitalization, spaces or separators differ. The complete normalization algorithm is not specified here.

## Memory, continuity and context cost

Recent story text, summaries, active instructions and tracker values serve different roles. Summaries compress history; they can omit incidental details or distort elapsed time. Use summaryRequest to preserve categories important to this particular world, and trackers for persistent facts that need a stable home. Avoid duplicating the whole story in a growing tracker. Set useful bounds on journals and cast records.

If a bad turn establishes a false fact, adding an instruction may leave conflicting history in place. Where the player's tools permit, editing or rewinding that turn can be cleaner than asking later prose to reconcile it. No correction engine is required by default.

Native trigger changes can affect runtime instructions without changing the base editor definition. Inspect active instruction contents and trigger/debug results when troubleshooting; a base-world export alone does not show everything the model received. Base and live worlds are separate copies.

Keep loaded instructions and AI-visible tracker names, descriptions, update rules and values purposeful. Prefer concise shared rules over repetition, keyword activation for occasional lore, and PawScript for exact calculations. Large AI-updated records can be expensive to rewrite. Inspect actual state and rendered instructions rather than assuming hidden prompt contents. Summary compression follows a six-turn cadence beginning at turn eight, as confirmed by the user; exact summary contents remain unavailable.

Alternate selectable protagonists can also have NPC cards if unchosen protagonists should appear in the story. A selected player sharing an Other Character name can use information from that entry. Internal identity merging or exclusion is not visible; do not promise automatic same-name NPC exclusion.

See [Editor-UI](Editor-UI.md) for current-value editing and [Verified-Behavior](Verified-Behavior.md) for forms, initialization and retention results.

---

END OF DOCUMENT: reference/Trackers.md
