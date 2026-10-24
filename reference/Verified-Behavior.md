# Consolidated behavior reference

Results current through 2026-10-23. Evidence labels follow [Evidence](Evidence.md). **[RUNTIME]** means observed behavior within the stated scope, **[DOCUMENTED]** means editor/export guidance, **[PATTERN]** means an authoring choice, and **[UNKNOWN]** means unresolved. Import success, rendered instructions and narration answer different questions; none is a complete view of hidden engine state. This reference contains conclusions, not research procedures.

## Triggers and Scenarios

- [RUNTIME] Ordinary triggers with no conditions do not fire automatically. Start-gated empty-condition triggers can fire at startup. An eligible trigger with no effects still records firing and can satisfy prerequisites.
- [RUNTIME] Fire random trigger bypasses target conditions, including empty or false conditions. Consumed one-shot targets do not execute again; nested dispatch works. Duplicate-pool weighting remains unresolved.
- [RUNTIME] A failing Run Script rolls back that script's writes. Separate earlier and later effects can commit. The trigger can count as fired and consume one-shot eligibility despite failure. Prerequisites mean firing, not successful completion.
- [PATTERN] Set completion flags only after successful work. Order producers before consumers when same-turn consumption is intended. Later triggers see earlier committed writes; reversing order can defer dependent work.
- [RUNTIME] Start+Mid+Repeat can execute before the opening and again during ordinary play. Repeat does not require a false-to-true condition transition. Start=false makes the stored Mid flag inert.
- [RUNTIME] Give information to AI is ignored with Start enabled, including subsequent Start+Mid activations. It differs from Tell the AI what should happen next turn. Computed information can appear in Secret Info; full prompt delivery is not visible.
- [RUNTIME] Background replacement affects startup in Start-only mode. Ordinary background/first-action effects do not rewrite the opening. Start+Mid did not apply background replacement. Fire random trigger dispatches in ordinary mode but did not dispatch with Start enabled. A containing trigger firing does not guarantee every stored effect executes.
- [DOCUMENTED] Change first action and Change other characters appear among startup-related choices. Full runtime character-record mutation is not observable through the current UI.
- [RUNTIME] Scenario binding requires exact registry strings, including case, spaces and punctuation. Preserved JSON can still be unbound. Say Scenarios in prose; the top-level JSON field is `conditions`.
- [RUNTIME] Add Scenario has a ten-entry editor creation cap. Imported worlds containing twelve bound Scenarios retained them through reopening and executed them. This is neither a universal runtime maximum of ten nor unlimited-support evidence.
- [RUNTIME/UNKNOWN] Dynamic Scenario text works in some single-slot arrangements but fails in multi-slot, cyclic and parallel arrangements where literal Scenarios work. Adding resolved registry entries does not repair this. Blank slot text is not reliable deactivation. Prefer literal Scenarios with explicit state gates; the internal cause remains unresolved.
- [RUNTIME] Independent plot gates can advance together; a shared gate restricts them according to authored policy. Character-specific conditions follow the selected source character rather than exchanging eligibility after display-name changes.

## Import and native payloads

- [RUNTIME] Tracker IDs containing underscore, hyphen, plus, slash, dot, space, colon or accented characters were regenerated on import, while paired trigger IDs were retained. Tracker references were not remapped. ASCII alphanumeric tracker IDs were preserved. Use this conservative convention for new IDs; preserve existing valid IDs and audit imported references. No universal character-set rule for every entity is established.
- [RUNTIME] Missing/blank PawScript condition data and legacy bare-array prerequisite/blocker data can be omitted from exports while problematic objects remain in imported editor state. Export omission is not proof of deletion. Use current object-shaped gate payloads.
- [RUNTIME] PawScript conditions require true/false, not numeric truthiness. Unknown handles produce missing-variable diagnostics.
- [RUNTIME] Numeric tracker conditions retain nonempty `textComparison` even when hidden in the UI; preserve it. Turn-at-least values can be native strings or numbers. Do not reject native exports solely for that representation.
- [RUNTIME] Nested And/Or/None Of logic executes from its node tree even where `advancedLogic` is absent or false. Use the enabled flag for new native logic. Duplicate leaf/effect IDs can survive and execute, but general collision/editing safety is unresolved; prefer unique IDs.
- [RUNTIME] Item-level and per-character initial-value scopes must agree. Import can remove incompatible entries and materialize defaults on a later round trip. Fixed text and array-based choices have different meanings; preserve their native shapes.

## Tracker writes and PawScript

- [RUNTIME] Native numeric effects within one trigger can overwrite rather than accumulate. Text additions accumulate and text removal removes matching occurrences. Sequential scripts are preferable for dependent arithmetic.
- [RUNTIME] Native YAML paths support set/remove/append/adjust, one-based list indexes and interpolation. Record append stores structured data and permits duplicates. Numeric adjustment can create a missing parent/leaf. Whole-value replacement overrides stale path/action fields: interpret `updateMode` first.
- [RUNTIME] Native And/Or and PawScript boolean expressions short-circuit in order. Place existence guards before dependent reads. This establishes skipped evaluation, not measured speedup.
- [RUNTIME] Plain nested assignments and runtime-key `.item` writes can create paths. Scalar parents can reject child writes and roll back the script. Missing-path compound arithmetic differs from assignment. Supported `try`, fallback item access and guarded reads handle missing values; `first_available` preserves zero/false and skips empty text.
- [RUNTIME] Locals do not cross Run Script effect boundaries. Executed branch locals and the last binding of a nonempty loop remain available later in that script. Filter bare fields resolve per row. Empty-loop/shadowing behavior is not fully characterized.
- [RUNTIME/UNKNOWN] `current()` is rejected in Run Script even inside `try`; the diagnostic limits it to List Update Target/Value. A supported positive legacy context is unavailable in the current editor.
- [RUNTIME] Enforce format is not a universal write-validation boundary: malformed manual/script values can persist. Hidden AI repair is not inspectable. Validate shape and semantic invariants explicitly when required.
- [RUNTIME] Comparisons/arithmetic can coerce YAML types, and Boolean-expression writes may serialize as quoted text. Rendered values and collapsed summaries do not prove strict types. Duplicate inventory records are not automatically prevented.
- [RUNTIME] Initial text of 10,014 characters and script-written text of 20,014 characters can be retained exactly. These are observed supported sizes, not maximum limits.
- [PATTERN] Separate generated candidates from accepted state, immutable definitions from mutable state, and archive storage from active context. Validate identity and entry types before freezing; a list-length check is insufficient. Explicit archive/reactivation can preserve state without duplicate transitions.
- [PATTERN] Choose turn time, story time or hybrid clocks intentionally. Consume milestone crossings and guard rewards. Counter order changes the first firing boundary. Shared arbitration and priority are authored policies, not automatic fairness.

## Instructions, visibility and memory

- [RUNTIME] Hidden and extra-hidden values remain script-accessible. Extra-hidden is display filtering, not protection against Storyteller inspection. The tracker editor can expose them with the debug display override off.
- [RUNTIME] Import normalizes automatic updating off for hidden, hidden_boring and player_only. Everyone, ai_only and ai_only_boring retain supported updates. Extra-hidden AI-only filtering does not stop updating. UI visibility does not prove full prompt inclusion.
- [RUNTIME] Direct active templates reevaluate. Ordinary interpolation installed through Modify instruction block snapshots its value; deferred `<=...=>` references remain live in that destination. Nested expression text is not generally evaluated recursively.
- [RUNTIME] Empty/whitespace replacement clears content while headings can remain. Malformed expressions may stay literal; an unclosed delimiter can affect a following block. Active instructions is current rendered state, not a historical full prompt.
- [RUNTIME] Independent random expressions can differ within/across blocks and effects. Cache a choice when consumers must agree. Hidden storage and rendered selection do not prove complete exclusion of unselected content.
- [RUNTIME] Selector case matters for observed equality/choose behavior; provide explicit fallbacks. AI-managed dependencies can see same-turn updates despite tracker order. Use staging for prior-turn values; hidden generation architecture is unresolved.
- [RUNTIME] Keyword matching accepts case variants, surrounding punctuation and authored alternate keywords; embedded substrings and a simple plural did not match. Activation persists through the matching turn and three following turns without refresh. Actions, completed narration and Secret Info can contribute; the complete tokenizer/scanned-field set is unspecified.
- [DOCUMENTED] Other Character Summary precedes fuller detail according to editor help, which describes availability from the turn after name/location mention. Repeat essential Summary facts in Character detail. This is not live-database visibility.
- [RUNTIME] A selected player sharing an Other Character name can use information from that entry. Unchosen player options authored separately as Other Characters can also provide information. Internal identity merging, exclusion and mutation remain unresolved; do not assert automatic same-name NPC exclusion.
- [RUNTIME] Secret Info and narration can disagree or misattribute knowledge. Characters can fail to learn disclosures; hidden facts can become player knowledge in prose. Separate direct knowledge, reports and sources. Anti-omniscience prose alone is not enforcement.
- [DOCUMENTED, user-confirmed] Summary compression follows a six-turn cadence beginning at turn eight. Later recall is possible; exact summary contents and their contribution versus persistent context remain hidden.
- [RUNTIME/UNKNOWN] Ordinary paragraph requests and strong priority-overriding wording did not reliably achieve requested longer output, including with richer lore. No reliable length-control recipe or hidden maximum is established. A shorter version is not validated.

## Forms, images and endings

- [RUNTIME] Bound Choice/Request Input answers are available to subsequent triggers in the same turn. Multiple-choice min/max constrain submission. Newline-delimited selections store text, not automatically a YAML list. Optional blank input clears the destination while preserving siblings; required blank input is rejected. Multiline input preserves line breaks at nested paths.
- [RUNTIME] Preset back-fill is order-sensitive. Fill missing fields without overwriting nonblank choices. Starting-value customization is distinct from live-state editing permission.
- [RUNTIME] Source/live-design initial-value changes do not migrate current values. Fresh games use new source starting values. Renaming a display Name with Ignore preserves the variable handle and ID.
- [RUNTIME] Dedicated Other Character image fields can populate Illustration details independently of narrative appearance. Appearance/clothing edits affect images and can be reversed. Alias-associated clothing drift can occur; repeated-name stability does not establish cache identity rules.
- [RUNTIME/UNKNOWN] Character/scenery results followed `imageStyle*Pre/Post` text opposed to `illustrationStyle*HighPriority`. Exact assembly and universal precedence remain hidden. Preserve imported fields and author using current style controls.
- [RUNTIME] Model-filtered blocks follow the selected active model; All blocks remain active. Available models are a dated UI roster, not a fixed schema enum.
- [RUNTIME] Ends game `data: true` offers Continue game and restores actions after confirmation. False removes action/continuation controls but leaves history/regeneration available. This is not irreversible deletion or proof of built-in ending-checker timing.

## Tooling conclusions

The reviewed external story parser can split nested YAML into false tracker entries, mishandle delimiters, merge branches according to file order/time and retain stale outputs. Preserve raw exports and require validated parsing with explicit branch identity. The external implementation remains unchanged. IW-Builder now supplies a separate reviewed-boundary extractor and conflict-rejecting merge; see [Story tools](Story-Tools.md). A local capture/export harness is also supplied; its authenticated standalone connection, capture and refresh-verified editor export are verified. Gameplay recovery and server persistence remain unverified. See [Engineering tools](Engineering-Tools.md) for its bounded capabilities. Reloading during generation can leave the latest turn unretained; streamed prose is not persistence.

See [Editor and UI](Editor-UI.md), [Known limits](Known-Limits.md) and [Roadmap](Roadmap.md).

---

END OF DOCUMENT: reference/Verified-Behavior.md
