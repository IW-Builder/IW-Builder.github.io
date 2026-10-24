# Infinite Worlds export reference

Compatibility and evidence scope: [Evidence.md](Evidence.md).

This reference describes arbitrary IW worlds. The schema and validator contain no required action engine, region graph, game-specific trackers, inventory rules, scores or narrative-control framework. Optional features remain optional. The authoring prompt explains how to choose features for the user's idea.

## Scope and validation

`../tools/iw-export.schema.json` is a JSON Schema Draft 2020-12 profile of native exported structure, not an official exhaustive importer contract. Known fields have characterized types. Unknown fields, values and condition/effect discriminators remain permissive and produce warnings where the validator can identify them. Observed vocabularies are not necessarily exhaustive enums.

At least one skill is required, in the editor. Other sparse `required` declarations do not prove that a skills-only object is a sufficient usable import. The neutral `../World-Template.json` supplies a conservative envelope; it intentionally requires the author to fill the story rather than supplying a game design.

The validator checks explicit tracker, trigger, PC, NPC, block and skill wiring. It does not parse or execute PawScript or template strings, enforce a particular narrative architecture, validate every reference hidden in text, test AI instruction compliance, or prove importer/runtime acceptance.

Structural errors are returned before reference traversal; fix them and rerun. Exit codes: 0 means no errors with warnings permitted; 1 means validation errors; 2 means an input/dependency problem. Read each warning. Known opaque-code warnings are not the same as unknown payloads or unresolved targets.

## Field and editor groups

|Editor purpose|Native fields|
|-|-|
|Introducing the story|title, description, background, firstInput, objective, charSelectText; preview image metadata|
|Main instructions|instructions, authorStyle, mature, nsfw, contentWarnings; instructionBlocks|
|Specialist instructions|evaluationRequest, descriptionRequest, summaryRequest, videoPromptInstructions|
|Image style|imageModel, imageStyle, illustrationStyle\* and imageStyle\* controls|
|Player character options|skills, possibleCharacters; PC skill/portrait/start-value data|
|Victory and defeat|victoryCondition, defeatCondition|
|Other characters|NPCs|
|Keyword instruction blocks|loreBookEntries|
|Tracked items|trackedItems|
|Triggers|triggerEvents, conditions|
|Permissions|permissionsOnceShared, allowChangeCharacter\*|
|Metadata/advanced controls|schemaVersion, favorite, hideSkillSystem, autoAdvanceVersion, version, designNotes, showPawScriptButtons|

These groups map purpose; they do not assert every UI label or control is bijective. `recommendedAIModel` is obsolete/export-only with no current editor selector. Keep it null if retained. `driftAcknowledgedForName` is null or the display name for which the variable-name mismatch alert was dismissed. Normal capitalization and separator differences such as Win Path / win_path are not drift and do not require acknowledgement. It is editor metadata, not a script alias. Metadata is not automatically story context: put necessary instructions in actual AI-facing fields.

## Trackers

Tracker definitions use an ID, display name, explicit variableName, dataType, visibility, initial-value fields and optional AI-update/format instructions. Use unique IDs and variable names. A variable name is not the same as a target ID.

Tracker dataType values: text, number, yaml, xml. Lists/boolean values can exist inside structured YAML; do not infer a separate native boolean/list dataType. `initialValue` is a JSON string even for numeric or structured content; parsed YAML values inside that string retain their own types. The editor does not enforce numeric-only typing in Number input controls. Use meaningful numeric literals when calculations depend on them.

Visibility values include everyone, player\_only, ai\_only, ai\_only\_boring, hidden and hidden\_boring. The latter variants are characterized by the supplied usage; do not infer unverified UI highlighting distinctions from their names. Player visibility clears the separate hide-in-Storyteller checkbox. Hidden trackers may be read by scripts and are omitted from ordinary player exports.

AI updating can be enabled for ordinary story-driven facts, relationships, appearance and other evolving information. Script/native effects can instead own values where exact control is useful. Neither is universally required. If combining them, specify the intended division to avoid competing writes.

`formatExample` and `formatSchema` are strings. The library demonstrates YAML-like schema notation, including text/number, optional-key and open-content forms. This is not evidence that formatSchema accepts JSON Schema, nor does the supplied JSON validator enforce its full grammar or AI semantic intent.

### Starting values: platform modes

|Mode|Native shape|Intended use|
|-|-|-|
|Same for all characters|Tracker initialValueBasedOnPC same plus initialValue string|Shared initial value|
|Character-defined fixed value|Tracker character mode; per-PC initialTrackedItemValues entry targets tracker ID and contains initialPCValue string|Different value for each predefined PC|
|Character-defined fixed selection|Same per-PC entry with initialPCValue array of strings|Choose one supplied option for that character|
|Character-defined script selection|Same per-PC entry with initialPCValue empty and initialPCValueChoicesScript string|Script generates that character's choices at startup|
|Player-defined selection|Tracker initialValueBasedOnPC player, initialValue string, initialValueChoices array of strings|Player chooses a startup preference independently of PC-specific values|

The optional-block export supplies the concrete player form: initialValue On, initialValueChoices \[On, Off], player mode and autoUpdate false. Those are tracker-level fields; do not put this list into a per-PC initialTrackedItemValues entry unless that is the intended character-defined mode. The player can change the live preference later to affect a following turn.

The script-choice editor description says choices are evaluated at game start from initial tracker values, including that character's values and skills. This is a platform capability rather than a game-specific rule. Arbitrary combinations of conflicting initialization fields, and player-mode UI behavior for every unconstrained input type, are not established by the selection examples; request a targeted export only if that additional variation matters.

## Conditions and effects

Conditions use category condition with a type/data leaf, or category logic with operator and a data child array. Normal condition lists are AND. Logic operators include and, or, none\_of. Effects use type and data. IDs are opaque but importer preservation is entity-specific. Some punctuation/non-ASCII tracker IDs are regenerated without remapping references; use ASCII alphanumeric IDs for new trackers. Field case matters: trackedItemID, targetTrackedItemId and characterId are different native spellings.

|Condition|Payload|
|-|-|
|triggerOnEvent|Scenario string evaluated by AI; root conditions lists Scenarios reusable by multiple triggers; the editor creation cap is ten, not a verified runtime maximum|
|triggerOnPawScript|Bare expression string|
|triggerOnRandomChance|Success percentage string: numeric literal, variable or PawScript expression; "50" means 50%|
|triggerOnTurn|Native string threshold or numeric threshold|
|triggerOnCharacter|Array of PC IDs|
|triggerOnTrackedItem|Tracker target/comparison object|
|triggerPrereqs / triggerBlockers|Trigger-ID arrays in prereqs/blockers plus firedThisTurn boolean|

Native tracked comparisons include is\_exactly, at\_least, not\_equal, at\_most; text comparisons include contains and does\_not\_contain. Value effects include set/add/subtract/replace. Native numeric and text controls are type-aware despite text-entry fields. Wrapper fields can repeat payload metadata; precedence is not established, and disagreement is an error. Preserve a coherent convention from the relevant sample rather than creating conflicting duplicates.

Native effects can show messages, guide/give information to the storyteller, edit tracker values/definitions, modify main/ordinary/keyword instructions, change PC name/description/skills, change objective/style/endings, present choices/request input, dispatch random triggers, run scripts and end the game. Use their exact schema payloads; do not infer additional effect types from similar names.

`effectEndsGame.data` is the "Player can choose to continue the game" boolean, not an enabled checkbox. True permits continuation after the game-over message; false does not. Native ending definitions have their own shapes. Null victoryCondition/defeatCondition is an exported disabled configuration.

## Payload catalog

Condition payload quick reference (all nodes still need category/type/id):

|type|data shape and intent|
|-|-|
|triggerOnPawScript|Bare expression STRING, without `<< >>`; deterministic check of current state|
|triggerOnEvent|Scenario STRING interpreted by AI; flexible but subject to false positives/negatives; include it in root conditions registry. The editor stops adding at ten entries; larger imported registries can persist and execute. Multiple triggers can reuse each Scenario|
|triggerOnTrackedItem|Object: trackedItemID, inequality, requiredValue, textComparison; target uses tracker ID, not variable name|
|triggerOnTurn|Native string or numeric turn threshold|
|triggerOnCharacter|Array of possibleCharacters characterId references|
|triggerPrereqs|Object: prereqs array of trigger IDs, firedThisTurn boolean|
|triggerBlockers|Object: blockers array of trigger IDs, firedThisTurn boolean|
|triggerOnRandomChance|Success percentage as a STRING: numeric literal, variable or PawScript expression; "50" means a 50% chance|

Native numeric comparison vocabulary: is\_exactly, at\_least, not\_equal, at\_most. Text comparisons: contains, does\_not\_contain. Do not extrapolate arbitrary comparison strings. Native wrappers can duplicate trackedItemID/inequality outside data; preserve a supplied export's consistent convention, never create mismatches. PawScript conditions are another option when useful, not a requirement to replace native conditions.

Effects by purpose:

|Effect|Authoring guidance|
|-|-|
|effectRunScript|Bare multiline script STRING; changes tracker values only|
|effectShowMessage|Text STRING rendered to player; use for authoritative results/status|
|effectTellAIWhatToDo|Guidance STRING influencing subsequent narration; not a state mutation or guaranteed repair|
|effectGiveInfo|AI background-information STRING; distinct from player output|
|effectSetTrackedItemValue|Object includes trackedItemID, action, newValue, replaceWith, path, updateMode, listExpression, targetExpression; use exact schema shape, not invented targeting modes|
|effectModifyTrackedItemDetails|Changes Name, description, visibility, automatic updating (autoUpdate), and update instructions; matching override booleans select changes|
|effectModifyInstructionBlock|`{id: instruction-block-ID, content: text}`|
|effectModifyKeywordBlock|`{id: keyword-block-ID, keywords: string-array, content: text}`|
|effectPresentChoice|Native inline choice form; correctly bound single-answer persistence is verified; choices is a STRING, targetTrackedItemId is a tracker ID; single/multiple modes and string limits as schema describes|
|effectRequestInput|Native input request; requestText, targetTrackedItemId, inputMode, requiresInput, path; do not assume it is equivalent to ordinary next-turn input|
|effectFireRandomTrigger|Array of trigger IDs; literal nothing is a sentinel. Target conditions are bypassed but consumed one-shot eligibility remains enforced. Duplicate weighting is unresolved.|
|effectChangePCSkill|Declared skill display name, integer amount and minmax, increase boolean. Levels and minmax are 0–5; minmax is the upper/lower boundary according to increase. See Capabilities.md for outcomes|
|effectEndsGame|Boolean data is "player may continue": true allows continuation, false does not. It is not an enabled flag.|

Other schema-defined effects change PC name/description, objective, main instructions, author style, Description instructions and victory/defeat definitions. Consult their exact payloads. A Run Script cannot directly edit those system properties; stage tracker text and use the appropriate native effect. Do not invent change-evaluation/summary/image effects because a similar Description effect exists.

In the native choice payload, choices is newline-separated text (`"Take road\\nTake ferry"`), single selection uses selectionMode single with null limits, and multiple selection uses string limits such as "1" and "3" with valueDelimiter newline. Those are export examples, not proof of every modal timing or selection-storage detail. Use real target tracker IDs and an empty path for whole-value targeting where appropriate. Nested-path writes and newline-delimited multi-selection text are supported within the observed scope. Native forms constrain answers and correctly bound single-answer targets update immediately; later triggers can react in the same turn.

## Comparator fields

For Number trackers, inequality selects is\_exactly, at\_least, not\_equal or at\_most. For Text trackers, textComparison selects contains or does\_not\_contain. Exports may retain both fields; do not interpret them as two simultaneous predicates. Use PawScript for structured YAML field checks rather than guessing how text comparison applies to a whole document. Native wrappers can repeat trackedItemID/inequality; keep wrapper and payload consistent.

## Assets and persistence

Do not invent image URLs, data-URI support or preset identifiers. Image style fields can require editor save/reload before their export reflects changes. Preview strings can persist with no attached image; empty settings can auto-populate. Preserve intentional whitespace rather than inventing universal default strings. Nonempty portrait metadata has characterized string fields for appearance, clothes, expression/position and setting.

Editor workflow: enable Show optional feature, expand Misc advanced features (optional), enable Show raw JSON, copy the full box to export. To import, overwrite the full box, avoid an extra trailing newline, and click Import JSON to world. Acknowledge the dialogs and wait for the editor rebuild before reopening raw JSON and refreshing. Import may persist independently of a later Discard changes action. The trailing-newline issue is an importer quirk, not invalid JSON syntax.

Playing creates an independent live world copy. Base edits/deletion do not affect existing games; live edits do not change the base. Save as new world or export live JSON and import it over the intended base to preserve/reuse changes. schemaVersion can be inspected in raw JSON; it is not a visible application release number.

## Remaining limits

The profile does not establish every importer-required field, every future vocabulary/preset, all path/list-expression targeting modes, arbitrary initialization-field precedence, random-child dispatch/duplicate weighting, complete system skill slug normalization, or a general performance/trigger limit. Collect targeted evidence only when an additional behavior is required. These limits do not require imposing a restrictive game architecture on ordinary world authoring.

## Authoring context

background, firstInput and objective feed AI context and direct play; objective also has a native update effect. They are not merely player-facing metadata. `<#...#>` are IW comment delimiters; sample authoring slots inside them should be filled, while genuine comments can remain. The sample Time and Location (whereWhen) block is a soft default for visible chronology. whereWhen is runtime output vocabulary, not an additional root export field.

Skill levels in possibleCharacters are integers from 0 through 5. effectChangePCSkill.minmax is a level boundary in that same range. The editor-provided Evaluation uses skill, difficulty, character context and common sense, including PARTIAL\_SUCCESS; there is no established numeric success-probability formula. See Capabilities.md.



Native path fields are unchecked editor inputs. Review target structure and operation together; JSON validation alone cannot establish runtime path meaning. See Import-Integrity.md.

## Native value effects

|Field / operation|Meaning and safe use|
|-|-|
|trackedItemID|Target tracker ID|
|action set|Replace target value with newValue|
|action add|Numeric addition or text append according to target type|
|action subtract|Numeric subtraction; the native text-removal operation uses this serialized action|
|action replace|Replace matched text newValue with replaceWith|
|newValue|String payload; numeric content is still serialized as text|
|path|Plain dotted path, e.g. wallet.coins; empty targets the whole tracker|
|updateMode|`path` edits a selected path; `replace` replaces the whole YAML value|
|action append|Add a value to the list at path; distinct from numeric/text add|
|listExpression / targetExpression|Empty in the current export; preserve when importing, but do not use them to invent a currently unsupported editor workflow|

Text adds accumulate and preserve literal quotation marks; text removal removes all matching occurrences. Numeric repeated writes within one trigger have different semantics. The cookbook supplies separate native text and number examples.

The current YAML editor offers Replace Value, Path, and "Do Something Complicated"; the last directs authors to Run Script. There is no separately exposed List Update workflow in this editor. Path offers Set a Value, Remove Value, Add to a list and Change Number By. Set uses YAML text with optional <<...>> interpolation, including whole-structure injection. The append export uses action append. Remove Value serializes as action remove; Change Number By as action adjust. Both use updateMode path. Do not confuse these YAML operations with native text subtract or numeric add/subtract.

Adding one list member is different from updating every member. To refill each character's HP, use a script:

```text
for each $member in $test\_party
  $member.hp = $member.max\_hp
```

For structured append payloads, a leading `-` describes a list, while `name: Frank` with sibling fields describes one record. Flow-style YAML record append stores structured data and permits duplicates. Arbitrary list flattening/nesting and coercion remain unresolved; do not infer automatic deduplication. Use Run Script for list-wide transformations.

Modify Tracked Item Details uses override flags. A value only changes when its matching override flag is enabled. This can reveal a tracker or hand future updates between AI and scripts. Changing autoUpdate after generation cannot undo a write already made this turn. Include an explicit handoff point and inspect the next turn.

Present Choice includes message, newline-separated choices, targetTrackedItemId, selectionMode, updateMode, limits, delimiter and path. Request Input uses requestText, targetTrackedItemId, inputMode, requiresInput and path. Correctly bound single-answer forms work: narration streams, the inline form waits for submission, the answer tracker updates immediately, and following triggers can fire in the same turn. The tested follow-up message is rendered ABOVE the question/answer receipt, followed by normal story options. Rendered placement does not imply execution before submission. The tested required forms offer no cancellation or forced focus.

Multiple choice exports selectionMode multiple, string min/maxSelections (for example "1" and "2"), and valueDelimiter newline or comma. Text input exports inputMode single or multi and requiresInput true or false. YAML Request Input exposes a dotted path. [RUNTIME] Multiple-choice bounds constrain selection; newline-delimited answers store text, not an automatic YAML list. Optional blank input clears its destination while preserving sibling keys. Required blank input is rejected, and multiline/nested-path writes preserve submitted line breaks. Arbitrary delimiter variants remain outside this result.

Correct target binding is required. Preserve IDs and verify that targetTrackedItemId names the intended tracker. The supplied single-choice world preserves its IDs and binding through a fresh import and works without retargeting. See Import-Integrity.md.

### Background replacement

`effectChangeBackground` uses string `data` payload including template e.g. `<<$opening\_assembly>>`. Represented in [layered opening](../examples/recipe-layered-opening.json) for startup assembly. Changes background through native effect; not script-writable. Mid-game history behavior not established.


## First-pass capability overview

[Trigger-Catalog](Trigger-Catalog.md) lists every currently identified condition/effect without requiring examples. It includes editor-recognized Change first action and Change other characters, now represented in the schema; character-database mutation remains unverified. Use the catalog to discover capabilities and obtain current native payloads before implementing beyond this profile. The roadmap tracks tooling alignment separately from verified runtime conclusions.

---

END OF DOCUMENT: reference/Schema.md
