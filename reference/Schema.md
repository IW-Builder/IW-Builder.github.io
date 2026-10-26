# Infinite Worlds export reference

Compatibility and evidence scope: [Evidence.md](Evidence.md). For an overview of every identified condition and effect, including Change first action and Change other characters, read [Trigger-Catalog](Trigger-Catalog.md) first; this file gives their payloads.

This reference describes arbitrary IW worlds. The schema and validator contain no required action engine, region graph, game-specific trackers, inventory rules, scores or narrative-control framework. Optional features remain optional. The authoring prompt explains how to choose features for the user's idea.

## Scope and validation

`../tools/iw-export.schema.json` is a JSON Schema Draft 2020-12 profile of native exported structure, not an official exhaustive importer contract. Known fields have characterized types. Unknown fields, values and condition/effect discriminators are accepted and produce warnings where the validator can identify them. Observed vocabularies are not necessarily exhaustive enums.

At least one skill is required, in the editor. Other sparse `required` declarations do not prove that a skills-only object is a sufficient usable import. `../World-Template.json` supplies a conservative envelope; it intentionally leaves the story for the author to fill rather than supplying a game design.

The validator checks explicit tracker, trigger, PC, NPC, block and skill wiring. It does not execute PawScript or templates, enforce a narrative architecture, validate every reference hidden in text, test AI instruction compliance, or prove importer/runtime acceptance.

Structural errors are returned before reference traversal; fix them and rerun. Exit codes: 0 means no errors with warnings permitted; 1 means validation errors; 2 means an input/dependency problem. Read each warning. Known opaque-code warnings are not the same as unknown payloads or unresolved targets.

## Field and editor groups

|Editor purpose|Native fields|
|-|-|
|Introducing the story|title, description, background, firstInput, objective, charSelectText; preview image metadata|
|Main instructions|instructions, authorStyle, mature, nsfw, contentWarnings; instructionBlocks|
|Specialist instructions|evaluationRequest, descriptionRequest, summaryRequest, videoPromptInstructions|
|Image style|imageModel, imageStyle, `illustrationStyle*` and `imageStyle*` controls|
|Player character options|skills, possibleCharacters; PC skill/portrait/start-value data|
|Victory and defeat|victoryCondition, defeatCondition|
|Other characters|NPCs|
|Keyword instruction blocks|loreBookEntries|
|Tracked items|trackedItems|
|Triggers|triggerEvents, conditions|
|Permissions|permissionsOnceShared, `allowChangeCharacter*`|
|Metadata/advanced controls|schemaVersion, favorite, hideSkillSystem, autoAdvanceVersion, version, designNotes, showPawScriptButtons|

These groups map purpose; not every UI label corresponds one-to-one to a field. `recommendedAIModel` is obsolete/export-only with no current editor selector; keep it null if retained. `driftAcknowledgedForName` is editor metadata for the variable-name mismatch alert, not a script alias; see [Trackers.md](Trackers.md). Metadata is not story context: put necessary instructions in AI-facing fields. schemaVersion is visible in raw JSON; it is not an application release number.

## Trackers

Tracker definitions use an ID, display name, explicit variableName, dataType, visibility, initial-value fields and optional AI-update/format instructions. Use unique IDs and variable names; a variable name is not a target ID. Ownership, visibility behavior, memory and name/handle drift are covered in [Trackers.md](Trackers.md).

dataType values: text, number, yaml, xml. Lists and booleans live inside YAML; there is no native boolean/list dataType. `initialValue` is a JSON string even for numeric or structured content. The editor does not enforce numeric-only input in Number controls, so use numeric literals when calculations depend on them.

visibility values: everyone, player_only, ai_only, ai_only_boring, hidden, hidden_boring. Hidden trackers remain readable by scripts and are omitted from ordinary player exports.

`formatExample` and `formatSchema` are strings. The library demonstrates a YAML-like schema notation with text/number, optional-key and open-content forms. formatSchema is not JSON Schema, and the validator does not enforce its grammar.

### Starting values: platform modes

|Mode|Native shape|Intended use|
|-|-|-|
|Same for all characters|Tracker initialValueBasedOnPC same plus initialValue string|Shared initial value|
|Character-defined fixed value|Tracker character mode; per-PC initialTrackedItemValues entry targets tracker ID and contains initialPCValue string|Different value for each predefined PC|
|Character-defined fixed selection|Same per-PC entry with initialPCValue array of strings|Choose one supplied option for that character|
|Character-defined script selection|Same per-PC entry with initialPCValue empty and initialPCValueChoicesScript string|Script generates that character's choices at startup|
|Player-defined selection|Tracker initialValueBasedOnPC player, initialValue string, initialValueChoices array of strings|Player chooses a startup preference independently of PC-specific values|

The optional-block export supplies the concrete player form: initialValue On, initialValueChoices [On, Off], player mode and autoUpdate false. Those are tracker-level fields; do not put this list into a per-PC initialTrackedItemValues entry unless the character-defined mode is intended. A live change later (through the Storyteller-mode tracker editor) affects the following turn.

Per the editor, script choices are evaluated at game start from initial tracker values, including that character's values and skills. Conflicting combinations of initialization fields, and player-mode controls for unconstrained input types, are not established; request a targeted export if that variation matters.

## Conditions

A condition node is either a leaf (`category: "condition"` with type and data) or a logic group (`category: "logic"`, operator and a data array of child nodes; operators and, or, none_of). Normal condition lists are AND. Every node needs category, type and id. IDs are opaque, and importer preservation is entity-specific: use ASCII alphanumeric IDs for new trackers ([Import-Integrity.md](Import-Integrity.md)). Field case matters: trackedItemID, targetTrackedItemId and characterId are different native spellings.

|type|data shape and intent|
|-|-|
|triggerOnPawScript|Bare expression STRING, without `<< >>`; deterministic check of current state|
|triggerOnEvent|Scenario STRING interpreted by AI; flexible but subject to false positives/negatives. Must match an entry in the root `conditions` registry exactly; multiple triggers can reuse each Scenario. Registry size: see [Triggers.md](Triggers.md)|
|triggerOnTrackedItem|Object: trackedItemID, inequality, requiredValue, textComparison; target uses tracker ID, not variable name. See Comparator fields|
|triggerOnTurn|Native string or numeric turn threshold|
|triggerOnCharacter|Array of possibleCharacters characterId references|
|triggerPrereqs|Object: prereqs array of trigger IDs, firedThisTurn boolean|
|triggerBlockers|Object: blockers array of trigger IDs, firedThisTurn boolean|
|triggerOnRandomChance|Success percentage as a STRING: numeric literal, variable or PawScript expression; "50" means a 50% chance|

PawScript conditions are an option when useful, not a requirement to replace native conditions.

## Comparator fields

For Number trackers, `inequality` selects is_exactly, at_least, not_equal or at_most. For Text trackers, `textComparison` selects contains or does_not_contain. Do not extrapolate other comparison strings. Exports may retain both fields; they are not two simultaneous predicates. Numeric conditions natively carry `textComparison: "contains"`; if it is missing or empty, the condition is dropped from the export and the trigger loses that gate. Text Contains matching is ASCII case-insensitive. Native numeric and text controls are type-aware despite text-entry fields. Use PawScript for structured YAML field checks rather than text comparison over a whole document.

Native wrappers can repeat trackedItemID/inequality outside `data`. Precedence is not established and disagreement is an error: keep wrapper and payload consistent, following the supplied export's convention.

## Effects

|Effect|Authoring guidance|
|-|-|
|effectRunScript|Bare multiline script STRING; changes tracker values only|
|effectShowMessage|Text STRING rendered to player; use for authoritative results/status|
|effectTellAIWhatToDo|Guidance STRING influencing subsequent narration; not a state mutation or guaranteed repair|
|effectGiveInfo|AI background-information STRING; distinct from player output. Ignored with Start of Game enabled ([Triggers.md](Triggers.md))|
|effectSetTrackedItemValue|Object with trackedItemID, action, newValue, replaceWith, path, updateMode, listExpression, targetExpression; see Native value effects|
|effectModifyTrackedItemDetails|Changes Name, description, visibility, automatic updating and update instructions; a value changes only when its matching override boolean is true. See [Trigger-Catalog.md](Trigger-Catalog.md#changing-automatic-updating)|
|effectModifyInstructionBlock|`{id: instruction-block-ID, content: text}`; template timing in [Capabilities.md](Capabilities.md)|
|effectModifyKeywordBlock|`{id: keyword-block-ID, keywords: string-array, content: text}`|
|effectPresentChoice / effectRequestInput|Native forms; see Choice and input forms|
|effectFireRandomTrigger|Array of trigger IDs; literal nothing is a sentinel. Target conditions are bypassed but consumed one-shot eligibility is enforced. Duplicate weighting is unresolved|
|effectChangePCSkill|Declared skill display name, integer amount and minmax, increase boolean. Levels and minmax are 0–5; minmax is the upper or lower boundary according to increase. Outcomes in [Capabilities.md](Capabilities.md)|
|effectChangeBackground|String `data`, which can be a template such as `<<$opening_assembly>>`; see [layered opening](../examples/recipe-layered-opening.json). Startup behavior in [Triggers.md](Triggers.md); mid-game history behavior not established|
|effectEndsGame|Boolean data means "player may continue": true allows continuation after the game-over message, false does not. It is not an enabled flag|

Other schema-defined effects change PC name/description, objective, main instructions, author style, Description instructions and victory/defeat definitions; consult their exact payloads in the schema and [Payloads.md](../examples/Payloads.md). Run Script cannot edit those system properties or the background: stage text in a tracker and apply it with the native effect. Do not invent change-evaluation/summary/image effects because a similar Description effect exists. Native ending definitions have their own shapes; null victoryCondition/defeatCondition is an exported disabled configuration.

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
|listExpression / targetExpression|Empty in current exports; preserve when importing, but do not use them to invent an unsupported editor workflow|
|replaceWith|Always serialize, as "" when unused. An effect missing it was associated with the game failing at the opening|

Text adds accumulate and preserve literal quotation marks; text removal removes all matching occurrences. Repeated numeric writes within one trigger behave differently ([Triggers.md](Triggers.md)). The cookbook supplies separate native text and number examples.

The YAML editor offers Replace Value, Path, and "Do Something Complicated" (which directs authors to Run Script); there is no separate List Update workflow. Path offers Set a Value, Remove Value, Add to a list and Change Number By. Set uses YAML text with optional `<<...>>` interpolation, including whole-structure injection. Add to a list exports action append, Remove Value action remove, and Change Number By action adjust, all with updateMode path. Do not confuse these YAML operations with native text subtract or numeric add/subtract. Path fields are unchecked editor inputs: review target structure and operation together ([Import-Integrity.md](Import-Integrity.md)).

Adding one list member is different from updating every member. To refill each character's HP, use a script:

```text
for each $member in $test_party
  $member.hp = $member.max_hp
```

For structured append payloads, a leading `-` describes a list, while `name: Frank` with sibling fields describes one record. Flow-style YAML record append stores structured data and permits duplicates. List flattening/nesting and coercion are unresolved; do not assume deduplication. Use Run Script for list-wide transformations.

## Choice and input forms

Present Choice includes message, choices, targetTrackedItemId, selectionMode, updateMode, limits, delimiter and path. `choices` is one newline-separated STRING (JSON `"Take road\nTake ferry"`). Single selection uses selectionMode single with null limits; multiple selection uses selectionMode multiple, string min/maxSelections such as "1" and "3", and valueDelimiter newline or comma.

Request Input uses requestText, targetTrackedItemId, inputMode (single or multi), requiresInput (true or false) and path; YAML targets expose a dotted path. Do not treat it as equivalent to ordinary next-turn input.

[RUNTIME] Correctly bound single-answer forms work: narration streams, the inline form waits for submission, the target tracker updates immediately, and following triggers can fire in the same turn. The tested follow-up message renders above the question/answer receipt; placement does not imply execution before submission. Required forms offer no cancellation. Multiple-choice bounds constrain selection, and newline-delimited answers are stored as text, not a YAML list. Optional blank input clears its destination while preserving sibling keys; required blank input is rejected. Multiline and nested-path writes preserve line breaks. Other delimiter variants are untested.

Binding must be correct: targetTrackedItemId must name the intended tracker, using an empty path for whole-value targeting. The supplied single-choice world keeps its IDs and binding through a fresh import. Check bindings after import ([Import-Integrity.md](Import-Integrity.md)).

## Authoring context

background, firstInput and objective feed AI context and direct play; objective also has a native update effect. They are not merely player-facing metadata. `<#...#>` are IW comment delimiters; fill sample authoring slots inside them, while genuine comments can remain. The sample Time and Location (whereWhen) block is a soft default for visible chronology; whereWhen is runtime output vocabulary, not a root export field.

Skill levels in possibleCharacters are integers from 0 through 5. The editor-provided Evaluation uses skill, difficulty, character context and common sense, including PARTIAL_SUCCESS; there is no established numeric success formula. See [Capabilities.md](Capabilities.md).

## Assets and persistence

Do not invent image URLs, data-URI support or preset identifiers. Image style fields can require editor save/reload before their export reflects changes. Preview strings can persist with no attached image; empty settings can auto-populate. Preserve intentional whitespace rather than inventing default strings. Nonempty portrait metadata has string fields for appearance, clothes, expression/position and setting.

Import/export steps are in [Editor-UI.md](Editor-UI.md); the trailing-newline issue is an importer quirk, not invalid JSON. Base worlds and live games are separate copies ([Import-Integrity.md](Import-Integrity.md)).

## Remaining limits

The profile does not establish every importer-required field, future vocabularies or presets, all path/list-expression targeting modes, initialization-field precedence, random-dispatch duplicate weighting, skill slug normalization, or a general performance/trigger limit. Collect targeted evidence only when a design needs one of these. None of this requires imposing a restrictive architecture on ordinary worlds.

---

END OF DOCUMENT: reference/Schema.md
