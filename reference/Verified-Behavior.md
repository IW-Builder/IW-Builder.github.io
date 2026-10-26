# Consolidated behavior reference

Results current through 2026-10-26. Labels and kit-wide caveats follow [Evidence](Evidence.md): **[RUNTIME]** observed behavior, **[DOCUMENTED]** editor/export guidance, **[PATTERN]** an authoring choice, **[UNKNOWN]** unresolved. Import success, rendered instructions and narration answer different questions. This reference contains conclusions, not research procedures; [Notable findings](Notable-Findings.md) gives the plain-language summary.

## Triggers and Scenarios

- [RUNTIME] Ordinary triggers with no conditions never fire automatically. Start-gated empty-condition triggers fire at startup. An eligible trigger with no effects still records firing and can satisfy prerequisites.
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
- [RUNTIME/UNKNOWN] Dynamic Scenario text works in some single-slot arrangements but fails in multi-slot, cyclic and parallel arrangements where literal Scenarios work. Adding the resolved literal strings to the registry does not repair it. Blank slot text is not reliable deactivation. Prefer literal Scenarios with explicit state gates; the cause is unresolved.
- [RUNTIME] Independent plot gates can advance together; a shared gate serializes them according to authored policy. Character-specific conditions follow the selected source character, not its customized display name.

## Import and native payloads

- [RUNTIME] Tracker IDs containing underscore, hyphen, plus, slash, dot, space, colon or accented characters are regenerated on import while paired trigger IDs are kept. Tracker references are not remapped, leaving dangling targets. ASCII alphanumeric tracker IDs are preserved. Use them for new trackers; preserve existing valid IDs and audit references.
- [RUNTIME] A tracker definition without `description` imports with a success dialog, then the editor rebuild fails with a KeyError. Always serialize description, even empty.
- [RUNTIME/UNKNOWN] An effectSetTrackedItemValue without `replaceWith` survived export, but the game twice failed at the opening with a generic streaming error (charges refunded); removing that one effect fixed it. Always serialize replaceWith, even as "".
- [RUNTIME] Missing/blank PawScript condition data and legacy bare-array prerequisite/blocker data are omitted from exports. The open editor can still hold them (opening such a trigger raised a list-index TypeError), but importing that export elsewhere leaves the gate deleted; a trigger left with no conditions shows "will never fire". Convert legacy gates to object shape before import.
- [RUNTIME] A numeric or text tracked-item condition with `textComparison` missing or "" is dropped from the export and its trigger stays dormant. After re-import, a trigger whose only condition was dropped never fires; one with other conditions loses that gate. Preserve the nonempty native value, which numeric conditions carry even though the UI hides it.
- [RUNTIME] Import fills an absent root `conditions` registry from triggerOnEvent references, and normalizes schemaVersion 2.2 to 2.4 with trigger payloads unchanged.
- [RUNTIME] A round trip of well-formed native JSON was byte-identical, including Unicode, multiline text, quotes, backslashes, nulls and empty arrays. Export adds positionInList to Other Characters that lack it.
- [RUNTIME] PawScript conditions require true/false, not numeric truthiness. Unknown handles produce missing-variable diagnostics. An interpolated comparison such as `<<$x>> >= 0` works in a PawScript condition.
- [RUNTIME] Turn-at-least values can be native strings or numbers; both fire. Do not reject native exports for that representation.
- [RUNTIME] Text Contains/Does not contain is ASCII case-insensitive, unlike Scenario binding and PawScript equality.
- [RUNTIME] Nested And/Or/None Of logic executes from its node tree even where `advancedLogic` is absent or false. Use the enabled flag for new native logic. Duplicate leaf/effect IDs survive and execute, but editing collisions is untested; prefer unique IDs.
- [RUNTIME] Item-level and per-character initial-value scopes must agree. Import removes incompatible entries and materializes defaults on a later round trip. Fixed text and array-based choices have different meanings; preserve their native shapes.

## Tracker writes and PawScript

- [RUNTIME] Native numeric effects within one trigger overwrite rather than accumulate. Text additions accumulate and text removal removes matching occurrences. Use sequential scripts for dependent arithmetic.
- [RUNTIME] Native YAML paths support set/remove/append/adjust, one-based list indexes and interpolation. Record append stores structured data and permits duplicates. Numeric adjustment creates a missing parent/leaf. Whole-value replacement overrides stale path/action fields: interpret `updateMode` first.
- [RUNTIME] Native And/Or and PawScript boolean expressions short-circuit left to right; debug lists only the deciding condition. Place existence guards before dependent reads. No speed benefit has been measured.
- [RUNTIME] Plain nested assignments and runtime-key `.item` writes create paths. Scalar parents reject child writes and roll back the script. Missing-path compound arithmetic (`+=`) fails where assignment succeeds. `try`, `item(key, fallback)` and `if(x.exists(), x, fallback)` handle missing values; `first_available` preserves zero/false and skips empty text.
- [RUNTIME] Locals do not cross Run Script effect boundaries. Executed branch locals and the last binding of a nonempty loop remain available later in that script. Filter bare fields resolve per row. Empty-loop/shadowing behavior is uncharacterized.
- [RUNTIME/UNKNOWN] `current()` is rejected in Run Script even inside `try`; the diagnostic limits it to List Update Target/Value, which the current editor does not expose.
- [RUNTIME] Enforce format is not a write-validation boundary: malformed manual/script values persist. Hidden AI repair is not inspectable. Validate shape and meaning explicitly.
- [RUNTIME] Comparisons and arithmetic coerce YAML values (see [PawScript](PawScript.md#2-values-trackers-and-scope)), and Boolean-expression writes serialize as quoted text. Rendered values and collapsed summaries do not prove types. Duplicate inventory records are not prevented.
- [RUNTIME] Initial text of 10,014 characters and script-written text of 20,014 characters were retained exactly.
- [PATTERN] Separate generated candidates from accepted state, immutable definitions from mutable state, and archive storage from active context. Validate identity and entry types before freezing; a list-length check is insufficient. Record assignment copies by value, so an archive is unaffected by later edits to the active record.
- [PATTERN] Choose turn time, story time or hybrid clocks intentionally. Detect crossings (`previous < N and now >= N`), consume them, and guard rewards. Use inequalities for thresholds: a countdown of 1 reduced by 3 is -2, so `= 0` is false. Counter order changes the first firing turn. Shared locks favor the first eligible trigger; priority is authored, not automatic.

## Instructions, visibility and memory

- [RUNTIME] Modify tracked item details with overrideVisibility accepts everyone, player_only, ai_only, hidden, ai_only_boring and hidden_boring and applies the live player-visible/hidden grouping. Live-design exports can retain the original visibility.
- [RUNTIME] An unchecked Hide skill system option exports with hideSkillSystem omitted, including after importing false. Omission is normal visible-skills state.
- [RUNTIME] Hidden and extra-hidden values remain script-accessible. Extra-hidden is display filtering, not protection from Storyteller inspection; the tracker editor shows them even with the debug override off.
- [RUNTIME] Import normalizes automatic updating off for hidden, hidden_boring and player_only. Everyone, ai_only and ai_only_boring keep updates. Extra-hidden filtering does not stop updating.
- [RUNTIME] Direct active templates reevaluate. Ordinary interpolation installed through Modify instruction block snapshots its value; deferred `<<=...=>>` references stay live. Nested expression text stored in a tracker is not evaluated recursively.
- [RUNTIME] Empty/whitespace replacement clears content while headings remain. Missing-path, invalid and unclosed expressions stay literal; an unclosed delimiter can break a valid expression in the following block. Active instructions is current rendered state and updates immediately on live-design edits.
- [RUNTIME] Independent random expressions differ within and across blocks and effects, including from a hidden pool. Cache a choice when consumers must agree.
- [RUNTIME] Selector case matters for equality/choose; provide explicit fallbacks. AI-managed dependencies can see same-turn updates despite tracker order. Stage prior-turn values explicitly.
- [RUNTIME] Keyword matching accepts case variants, surrounding punctuation and authored alternate keywords; embedded substrings and a simple plural did not match. Activation lasts the matching turn and three more. Player actions, completed narration and Secret Info contribute, from the next generated turn; the complete scanned-field set is unspecified.
- [DOCUMENTED] Other Character Summary is available before fuller detail, which editor help says becomes available the turn after a name/location mention. Repeat essential Summary facts in detail.
- [RUNTIME] Character detail retrieval is unreliable. A selected player sharing an Other Character name used that entry's facts, but a name-only mention did not surface an authored hobby on two turns; the narrator invented one, and history then reinforced it. The narrator can also introduce named NPCs into an opening that says the player is alone. Internal identity merging and exclusion are unresolved.
- [RUNTIME] Secret Info and narration can disagree or misattribute knowledge. Characters can deny a fact just told to them, and hidden facts can become player knowledge in prose. A general provenance policy showed no clear benefit; explicit correction of the source chain did.
- [RUNTIME] Once a secret reaches narration, removing or emptying its disclosure block does not remove it from later turns.
- [DOCUMENTED, user-confirmed] Summary compression follows a six-turn cadence beginning at turn eight; the cost breakdown first shows LTM about then, as STM drops. Later recall is possible; summary contents remain hidden.
- [RUNTIME] Shortening (Dolphin, one world): a cap of at most 2 short paragraphs and 90 words, with priority-override framing, appended to authorStyle averaged 82 words (control 413) and held through a story-beat turn; a plain one-sentence version averaged 96. The same cap in descriptionRequest (mean 118, max 215) or an always-on block (max 226) broke on the story-beat turn. A per-turn Tell AI trigger held later turns but cannot reach the opening. The cap acts as a soft target; credits fell only about 10%.
- [RUNTIME/UNKNOWN] Lengthening: paragraph-count requests and strong priority-overriding wording did not reliably lengthen narration, even with richer lore. A one-sentence descriptionRequest did not shorten it. Other models are untested for the authorStyle cap.

## Forms, images and endings

- [RUNTIME] Bound Choice/Request Input answers are available to subsequent triggers in the same turn. Multiple-choice min/max constrain submission. Newline-delimited selections store text, not a YAML list. Optional blank input clears the destination while preserving siblings; required blank input is rejected. Multiline input preserves line breaks at nested paths.
- [RUNTIME/UNKNOWN] One turn combining a malformed-candidate input with a multiline Request Input showed narration without forms and did not persist, though it was charged; each worked alone. Prefer one input form per turn.
- [RUNTIME] Preset back-fill is order-sensitive: a script after the choice fills in the same turn, before it fills nothing. Fill missing fields without overwriting nonblank choices. Starting-value customization is distinct from live editing.
- [RUNTIME] Source/live-design initial-value changes do not migrate current values; fresh games use the new values. Renaming a display Name with Ignore preserves the variable handle and ID.
- [RUNTIME] Dedicated Other Character image fields populate Illustration details independently of narrative appearance. Appearance/clothing edits change images and can be reversed. Alias-associated clothing drift can occur.
- [RUNTIME/UNKNOWN] Character/scenery results followed `imageStyle*Pre/Post` when opposed to `illustrationStyle*HighPriority`. Exact prompt assembly is hidden. Preserve imported fields and author with current style controls.
- [RUNTIME] Model-filtered blocks follow the selected active model; All blocks stay active.
- [RUNTIME] Ends game `data: true` offers Continue game and restores actions after confirmation, at no charge. False removes action/continuation controls but leaves history/regeneration available. This is not proof of the built-in ending checker's timing.

## Story exports

Native story text has no escaping for headings or nested YAML, so naive parsers split nested YAML into false trackers and mistake embedded markers for turns. Parse with the kit's reviewed-boundary extractor ([Story tools](Story-Tools.md)) and keep raw exports. Reloading during generation can leave the latest turn unretained; streamed prose is not persistence.

See [Editor and UI](Editor-UI.md) and [Known limits](Known-Limits.md).

---

END OF DOCUMENT: reference/Verified-Behavior.md
