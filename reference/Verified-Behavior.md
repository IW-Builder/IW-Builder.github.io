# Consolidated behavior reference

Detailed runtime conclusions for Infinite Worlds, current through 2026-10-26. [Notable findings](Notable-Findings.md) gives the plain-language summary and the list of what remains unknown; this file carries the detail and the evidence labels. Import success, rendered instructions and narration answer different questions.

## Compatibility and evidence

This is an independent, unaffiliated kit. Platform baseline: Infinite Worlds' October 8, 2026 "Save/load system, Image style system and Pawscript update," with editor/runtime information consolidated through October 26, 2026. Export schemaVersion is 2.4. Kit version is 1.6.0; the structural profile is 1.2.0. Neither is an IW application version. The unaffiliated Script Library source snapshot is version 3.16, October 16, 2026; see ../library/Integration.md.

Four evidence labels are used across the kit when a distinction matters; ordinary reference sentences do not carry a tag.

| Label | Meaning |
| --- | --- |
| [DOCUMENTED] | Supported by editor help, a native export shape or cited language documentation. Does not alone establish runtime behavior. |
| [RUNTIME] | The stated behavior was exercised in IW within the described scope. |
| [PATTERN] | An optional authoring design assembled from supported features; not a platform requirement. |
| [UNKNOWN] | A concrete behavior remains unresolved; avoid depending on it without a focused check. |

Kit-wide caveats, not repeated per entry:

- Observed sizes, counts and caps (text lengths, Scenario counts, input counters) are working examples, not platform maxima.
- A tested feature does not certify every composition built from it; test new combinations in play.
- Rendered panels (Active instructions, debug, Secret Info, narration) show what IW displays, not the complete prompt or hidden engine state.
- Credits are not token counts.
- Structural validation is a separate status, not a fifth label: it checks export structure and explicit references. Static lint reports likely mistakes; neither executes PawScript or certifies a story. Do not present generated prose as evidence of tracker state.
- Behavior established only from a user's report is marked "user-confirmed". A "one world" or "one model" note means the result was observed in that scope and has not been repeated elsewhere.

## Triggers and Scenarios

- [RUNTIME] Ordinary triggers with no conditions never fire automatically. Start-gated empty-condition triggers fire at startup. [UNKNOWN] Whether an empty-condition Start+Mid+Repeat trigger also fires on ordinary turns; give every-turn triggers an always-true condition. An eligible trigger with no effects still records firing and can satisfy prerequisites.
- [RUNTIME] Fire random trigger bypasses target conditions, including empty or false conditions. Consumed one-shot targets do not execute again, even on later turns; nested dispatch works. Editor help's "already fired this turn" wording understates this. Duplicate-pool weighting is unresolved.
- [RUNTIME] A failing Run Script rolls back that script's writes. Separate earlier and later effects can commit. The trigger still counts as fired and consumes one-shot eligibility. Prerequisites mean firing, not successful completion.
- [RUNTIME] This-turn prerequisites/blockers see a producer only when it is earlier in triggerEvents. History prerequisites see a later-ordered producer from the next turn. Current-turn gates reset each turn.
- [PATTERN] Set completion flags only after successful work. Order producers before consumers when same-turn consumption is intended. Later triggers see earlier committed writes; reversing order defers dependent work by a turn.
- [RUNTIME] Start+Mid+Repeat executes before the opening and again during ordinary play; trigger history records Start-pass firings as turn 0. Repeat does not require a false-to-true condition transition. Start=false makes the stored Mid flag inert.
- [RUNTIME] Give information to AI is ignored with Start enabled, including later Start+Mid activations; the payload is not stripped. It differs from Tell the AI what should happen next turn. Computed information appears in Secret Info.
- [RUNTIME] Background replacement affects startup in Start-only mode. Ordinary background/first-action effects do not rewrite the opening. Start+Mid did not apply background replacement. Fire random trigger dispatches in ordinary mode but not with Start enabled. A trigger firing does not guarantee every stored effect executes.
- [DOCUMENTED] Change first action and Change other characters appear only in the Start picker. Live character-record mutation is not observable.
- [RUNTIME] Scenario binding requires exact registry strings, including case, spaces and punctuation. Preserved JSON can still be unbound. Say Scenarios in prose; the top-level JSON field is `conditions`.
- [RUNTIME] A Scenario fires only when the event actually occurs in the narrated outcome. The narrator can refuse or substitute a requested action, and then the trigger does not fire. An already-satisfied Scenario does not refire on quiet turns.
- [RUNTIME] Add Scenario stops at ten entries in the editor. Imported registries of twelve bound Scenarios persisted through save/reopen and all fired in one turn; a fourteen-entry registry with unused entries and duplicate references also ran.
- [RUNTIME] Dynamic Scenario text works in some single-slot arrangements but fails in multi-slot, cyclic and parallel arrangements where literal Scenarios work. Adding the resolved literal strings to the registry does not repair it. Blank slot text is not reliable deactivation. Prefer literal Scenarios with explicit state gates; [UNKNOWN] the cause.
- [RUNTIME] Independent plot gates can advance together; a shared gate serializes them according to authored policy. Character-specific conditions follow the selected source character, not its customized display name.

## Import and native payloads

- [RUNTIME] Tracker IDs containing underscore, hyphen, plus, slash, dot, space, colon or accented characters are regenerated on import while paired trigger IDs are kept. Tracker references are not remapped, leaving dangling targets. ASCII alphanumeric tracker IDs are preserved. Use them for new trackers; preserve existing valid IDs and audit references.
- [RUNTIME] A tracker definition without `description` imports with a success dialog, then the editor rebuild fails with a KeyError. Always serialize description, even empty.
- [RUNTIME] An effectSetTrackedItemValue without `replaceWith` survived export, but the game twice failed at the opening with a generic streaming error (charges refunded); removing that one effect fixed it. Always serialize replaceWith, even as "". [UNKNOWN] the mechanism.
- [RUNTIME] Missing/blank PawScript condition data and legacy bare-array prerequisite/blocker data are omitted from exports. The open editor can still hold them (opening such a trigger raised a list-index TypeError), but importing that export elsewhere leaves the gate deleted; a trigger left with no conditions shows "will never fire". Convert legacy gates to object shape before import.
- [RUNTIME] A numeric or text tracked-item condition with `textComparison` missing or "" is dropped from the export and its trigger stays dormant. After re-import, a trigger whose only condition was dropped never fires; one with other conditions loses that gate. Preserve the nonempty native value, which numeric conditions carry even though the UI hides it.
- [RUNTIME] Import fills an absent root `conditions` registry from triggerOnEvent references, and normalizes schemaVersion 2.2 to 2.4 with trigger payloads unchanged.
- [RUNTIME] A round trip of well-formed native JSON was byte-identical, including Unicode, multiline text, quotes, backslashes, nulls and empty arrays. Export adds positionInList to Other Characters that lack it.
- [RUNTIME] PawScript conditions require true/false, not numeric truthiness. Unknown handles produce missing-variable diagnostics. An interpolated comparison such as `<<$x>> >= 0` works in a PawScript condition.
- [RUNTIME] Turn-at-least values can be native strings or numbers; both fire. Do not reject native exports for that representation.
- [RUNTIME] Text Contains/Does not contain is ASCII case-insensitive, unlike Scenario binding and PawScript equality.
- [RUNTIME] Nested And/Or/None Of logic executes from its node tree even where `advancedLogic` is absent or false. Use the enabled flag for new native logic. Duplicate leaf/effect IDs survive and execute, but editing collisions is untested; prefer unique IDs.
- [RUNTIME] Item-level and per-character initial-value scopes must agree. Import removes incompatible entries and materializes defaults on a later round trip. Fixed text and array-based choices have different meanings; preserve their native shapes.
- [RUNTIME] The kit's single-choice example keeps its IDs and binding through a fresh import. Inspect native target dropdowns after importing a composed world; schema validation cannot predict importer behavior for every construction.

## Tracker writes and PawScript

- [RUNTIME] Native numeric effects within one trigger overwrite rather than accumulate (starting at 0, add 2 then add 3 ended at 3; starting at 1, set 5 then add 2 ended at 3). Text additions accumulate and text removal removes matching occurrences. Use sequential scripts for dependent arithmetic; sequential script arithmetic accumulates, nested YAML changes preserve unrelated keys, and separate script effects writing different YAML paths preserve both.
- [RUNTIME] Native YAML paths support set/remove/append/adjust, one-based list indexes and interpolation. Record append stores structured data and permits duplicates. Numeric adjustment creates a missing parent/leaf. Whole-value replacement overrides stale path/action fields: interpret `updateMode` first.
- [RUNTIME] Native And/Or and PawScript boolean expressions short-circuit left to right; debug lists only the deciding condition. Place existence guards before dependent reads. No speed benefit has been measured.
- [RUNTIME] Plain nested assignments and runtime-key `.item` writes create paths. Scalar parents reject child writes and roll back the script. Missing-path compound arithmetic (`+=`) fails where assignment succeeds. `try`, `item(key, fallback)` and `if(x.exists(), x, fallback)` handle missing values; `first_available` preserves zero/false and skips empty text.
- [RUNTIME] Locals do not cross Run Script effect boundaries. Executed branch locals and the last binding of a nonempty loop remain available later in that script. Filter bare fields resolve per row. [UNKNOWN] Empty-loop and shadowing behavior.
- [RUNTIME] `current()` is rejected in Run Script even inside `try`; the diagnostic limits it to List Update Target/Value, which the current editor does not expose.
- [RUNTIME] Enforce format is not a write-validation boundary: malformed manual/script values persist. Hidden AI repair is not inspectable. Validate shape and meaning explicitly.
- [RUNTIME] Comparisons and arithmetic coerce YAML values (see [PawScript](PawScript.md#2-values-trackers-and-scope)), and Boolean-expression writes serialize as quoted text. Rendered values and collapsed summaries do not prove types. Duplicate inventory records are not prevented.
- [RUNTIME] The PawScript sandbox matches the field it opens from: a script field gives a multi-line script box; a single-line field gives a one-line expression box that refuses a multi-line paste, with a Text tab for multi-line `<<expression>>` text. Sandbox trackers can be added, edited and deleted, and runs use those values; nothing changed goes back to the editor or game. From the world editor it loads all base trackers, at fixed initial values or 0/empty for unspecified, player-chosen or character-dependent ones; from debug or from View/edit world design during play, it loads the game state of that turn.
- [RUNTIME] A native tracker condition with requiredValue `$limit` is compared against the live value (changing `$limit` changed when it fired). A random-chance condition written as an expression (`$hi`, `$hi - $lo`) is re-evaluated each turn: 0 never fired, 100 always fired, and swapping the values swapped the pattern. Native numeric subtract with newValue `2d3` removed 2–6, varying by turn. One world, Dolphin.
- [RUNTIME] `$game.ai_model` returns the display name (`Dolphin`, `Puma`, `Smilodon` observed); `$game.ai_model = "dolphin"` is false on Dolphin.
- [RUNTIME] `<<...>>` in a tracker's own update instructions is evaluated each turn: the AI wrote the hidden tracker's value, not the template, and followed a change to it from the next turn.
- [RUNTIME] Initial text of 10,014 characters and script-written text of 20,014 characters were retained exactly.
- [PATTERN] Separate generated candidates from accepted state, immutable definitions from mutable state, and archive storage from active context. Validate identity and entry types before freezing; a list-length check is insufficient. Record assignment copies by value, so an archive is unaffected by later edits to the active record.
- [PATTERN] Choose turn time, story time or hybrid clocks intentionally. Detect crossings (`previous < N and now >= N`), consume them, and guard rewards. Use inequalities for thresholds: a countdown of 1 reduced by 3 is -2, so `= 0` is false. Counter order changes the first firing turn. Shared locks favor the first eligible trigger; priority is authored, not automatic.

## Instructions, visibility and memory

- [RUNTIME] Modify tracked item details with overrideVisibility accepts everyone, player_only, ai_only, hidden, ai_only_boring and hidden_boring and applies the live player-visible/hidden grouping. Live-design exports can retain the original visibility.
- [RUNTIME] Modify tracked item details switches automatic updating on and off at runtime, repeatedly, from the next turn (triggers run after the AI's tracker update in a turn). Re-sending update instructions is unnecessary. In the same trigger as a Request Input effect the change is lost (three trackers across two worlds); in a separate trigger on the same turn it works. Show Message and Run Script effects in that trigger are unaffected. [UNKNOWN] Present Choice in the same trigger.
- [RUNTIME] An unchecked Hide skill system option exports with hideSkillSystem omitted, including after importing false. Omission is normal visible-skills state.
- [RUNTIME] Hidden and extra-hidden values remain script-accessible. Extra-hidden is display filtering, not protection from Storyteller inspection; the tracker editor shows them even with the debug override off.
- [RUNTIME] AI-updated buffers rooted in a YAML list lose updates; a record root (`entries: []`) does not. In one same-world comparison on Dolphin and Puma (14 turns, three copies of the library relationship buffer), list roots landed under half of the expected add/update events while the record root landed nearly all of them. List losses were whole turns with nothing written, or rejected writes whose debug message says the body must be a mapping or that the parent is a list. A buffer instructed to "update only changed fields" received index patches against the already-cleared buffer; these failed in every root shape, repairs dropped the change or appended an unnamed junk entry, and they caused every record-root loss. Ask buffers for complete entries. The storyteller sometimes wrote `entries: []` followed by the items, leaving a stray key beside `entries`.
- [RUNTIME] Import normalizes automatic updating off for hidden, hidden_boring and player_only. Everyone, ai_only and ai_only_boring keep updates. Extra-hidden filtering does not stop updating.
- [RUNTIME] A block reinstalled every turn by Modify instruction block with `<<$v>>`, ordered above the trigger that sets `$v`, showed the value from two turn-ends earlier; the same text written `<=$v=>` showed the latest value. One world, Dolphin.
- [RUNTIME] A list-rooted buffer with "append-only inbox" wording and a library-style merge landed fewer than half of the expected changes over 12 turns on Dolphin, each only after IW's auto-repair. The record-rooted copy with the same wording was clean until the AI wrote two rows as one nested list item, after which its `.entries.any(name.exists())` merge never fired again.
- [RUNTIME] An AI-updated text tag tracker ("judge only this turn; tags or None"), reset to None by a final script, carried no tag into later turns across eight turns.
- [RUNTIME] Direct active templates reevaluate. Ordinary interpolation installed through Modify instruction block snapshots its value; deferred `<=...=>` references stay live. Nested expression text stored in a tracker is not evaluated recursively.
- [RUNTIME] `<<=...=>>` stays literal in messages, installed blocks and trackers. A trigger that sets a tracker to `<=x=>` stores `<<x>>`, which the tracker panel and editor show evaluated each turn; block interpolation of that tracker inserts the raw `<<x>>`. Saving the tracker editor writes displayed values back, freezing such trackers. A hand-typed `<=x=>` becomes `<<x>>` after the next turn and is shown raw. The platform's own name for `<=...=>` is a postponed evaluation expression, intended for a trigger that sets a tracker to it; in testing, the panel, Show changes and the editor agreed on a hand-set tracker's value within a turn.
- [RUNTIME] Empty/whitespace replacement clears content while headings remain. Missing-path, invalid and unclosed expressions stay literal; an unclosed delimiter can break a valid expression in the following block. Active instructions is current rendered state and updates immediately on live-design edits.
- [RUNTIME] Independent random expressions differ within and across blocks and effects, including from a hidden pool. Cache a choice when consumers must agree.
- [RUNTIME] Selector case matters for equality/choose; provide explicit fallbacks. AI-managed dependencies can see same-turn updates despite tracker order. Stage prior-turn values explicitly.
- [RUNTIME] Keyword matching accepts case variants, surrounding punctuation and authored alternate keywords; embedded substrings and a simple plural did not match. Activation lasts the matching turn and three more. Player actions, completed narration and Secret Info contribute, from the next generated turn; the complete scanned-field set is unspecified.
- [DOCUMENTED] Other Character Summary is available before fuller detail, which editor help says becomes available the turn after a name/location mention. Repeat essential Summary facts in detail.
- [RUNTIME] Character detail retrieval is unreliable. A selected player sharing an Other Character name used that entry's facts, but a name-only mention did not surface an authored hobby on two turns; the narrator invented one, and history then reinforced it. The narrator can also introduce named NPCs into an opening that says the player is alone. Internal identity merging and exclusion are unresolved.
- [RUNTIME] Secret Info and narration can disagree or misattribute knowledge. Characters can deny a fact just told to them, and hidden facts can become player knowledge in prose. A general provenance policy showed no clear benefit; explicit correction of the source chain did.
- [RUNTIME] Once a secret reaches narration, removing or emptying its disclosure block does not remove it from later turns.
- [RUNTIME] Summary compression runs after turn 8 and every six turns after that (after turns 8, 14, 20, …), so the turn being written has the 2–7 most recent turns in uncompressed short-term memory (from turn 2 on). The cost breakdown shows LTM from the first compression as STM drops; short and long term memory can be watched turn by turn in any game. Later recall of compressed material is possible; summary contents remain hidden.
- [RUNTIME] Shortening (Dolphin, one world): a cap of at most 2 short paragraphs and 90 words, with priority-override framing, appended to authorStyle averaged 82 words (control 413) and held through a story-beat turn; a plain one-sentence version averaged 96. The same cap in descriptionRequest (mean 118, max 215) or an always-on block (max 226) broke on the story-beat turn. A per-turn Tell AI trigger held later turns but cannot reach the opening. The cap acts as a soft target; credits fell only about 10%.
- [RUNTIME] Lengthening: paragraph-count requests and strong priority-overriding wording did not reliably lengthen narration, even with richer lore. A one-sentence descriptionRequest did not shorten it. [UNKNOWN] Other models for the authorStyle cap.

## Forms, images and endings

- [RUNTIME] Bound Choice/Request Input answers are available to subsequent triggers in the same turn. Multiple-choice min/max constrain submission. Newline-delimited selections store text, not a YAML list. Optional blank input clears the destination while preserving siblings; required blank input is rejected. Multiline input preserves line breaks at nested paths.
- [RUNTIME] One turn combining a malformed-candidate input with a multiline Request Input showed narration without forms and did not persist, though it was charged; each worked alone, and two plain Request Input forms from separate triggers on one turn worked. Prefer one input form per turn. [UNKNOWN] the server-side cause.
- [RUNTIME] Preset back-fill is order-sensitive: a script after the choice fills in the same turn, before it fills nothing. Fill missing fields without overwriting nonblank choices. Starting-value customization is distinct from live editing.
- [RUNTIME] Source/live-design initial-value changes do not migrate current values; fresh games use the new values. Renaming a display Name with Ignore preserves the variable handle and ID.
- [RUNTIME] Dedicated Other Character image fields populate Illustration details independently of narrative appearance. Appearance/clothing edits change images and can be reversed. Alias-associated clothing drift can occur.
- [RUNTIME] Character/scenery results followed `imageStyle*Pre/Post` when opposed to `illustrationStyle*HighPriority`. Exact prompt assembly is hidden. Preserve imported fields and author with current style controls.
- [RUNTIME] Model-filtered blocks follow the selected active model; All blocks stay active.
- [RUNTIME] Ends game `data: true` offers Continue game and restores actions after confirmation, at no charge. False removes action/continuation controls but leaves history/regeneration available. This is not proof of the built-in ending checker's timing.

## Story exports

Native story text has no escaping for headings or nested YAML, so naive parsers split nested YAML into false trackers and mistake embedded markers for turns. Parse with the kit's reviewed-boundary extractor (`tools/story_export.py`, documented in ../tools/Usage.md) and keep raw exports. Reloading during generation can leave the latest turn unretained; streamed prose is not persistence.

See [Editor and UI](Editor-UI.md) for workflows and [Notable findings](Notable-Findings.md) for the summary and the unresolved list.

---

END OF DOCUMENT: reference/Verified-Behavior.md
