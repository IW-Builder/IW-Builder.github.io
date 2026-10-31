# Infinite Worlds export reference

Compatibility baseline and evidence labels: [Verified-Behavior.md](Verified-Behavior.md). For an overview of every identified condition and effect, including Change first action and Change other characters, read [Trigger-Catalog](Trigger-Catalog.md) first; this file gives their payloads.

This reference describes arbitrary IW worlds. The schema and validator contain no required action engine, region graph, game-specific trackers, inventory rules, scores or narrative-control framework. Optional features remain optional. The authoring prompt explains how to choose features for the user's idea.

## Scope and validation

`../tools/iw-export.schema.json` is a JSON Schema Draft 2020-12 profile of the native export structure as observed: known fields have characterized types, and unknown fields, values and condition/effect discriminators are accepted with a warning where the validator can identify them. The vocabularies it lists are the ones observed, so a value outside them is a warning to check, not an error.

The editor requires at least one skill; the schema's other `required` declarations are sparse, so a minimal object that passes is not thereby a usable import. `../World-Template.json` supplies the envelope and leaves the story for the author.

The validator checks explicit tracker, trigger, PC, NPC, block and skill wiring, returns structural errors before reference traversal, and exits 0 with no errors (warnings permitted), 1 with validation errors, or 2 for an input/dependency problem. Read each warning: a known opaque-code warning is a different thing from an unknown payload or an unresolved target. What it cannot check (PawScript execution, references hidden in text, instruction compliance, importer acceptance) is listed in [tools/Usage.md](../tools/Usage.md).

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

These groups map purpose; not every UI label corresponds one-to-one to a field. `recommendedAIModel` is obsolete/export-only with no current editor selector; keep it null if retained. `driftAcknowledgedForName` is editor metadata for the variable-name mismatch alert, not a script alias; see [Trackers.md](Trackers.md). `advancedLogic` accompanies the trigger editor's advanced condition setup: use true for authored nested logic groups and preserve existing values; the logic node tree is what executes. `showPawScriptButtons` stores the editor's PawScript Expression Editor button option. Metadata is not story context: put necessary instructions in AI-facing fields. schemaVersion is visible in raw JSON; it is not an application release number.

## Identifiers

Tracker IDs, display names and PawScript variable names serve different purposes: native effects and conditions target the tracker `id`, scripts use `variableName`, and users see `name`. Preserve existing IDs when editing. For new trackers, use a unique nine-character ASCII alphanumeric ID, the editor-style form used by the import-tested examples; IDs containing punctuation, spaces or accents are regenerated on import while their references are not remapped. Use explicit descriptive snake_case variableName values in scripts and descriptive display names in the editor. This is the kit's authoring convention, not a claim that other ID formats are invalid. Generate IDs in code and check collisions; without tools, check each newly introduced ID and reference manually. New triggers, blocks and PCs can use the same convention. When combining worlds, remap every explicit reference consistently and validate the result.

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

The optional-block example (../examples/optional-block.json) shows the player form: initialValue On, initialValueChoices [On, Off], player mode and autoUpdate false. Those are tracker-level fields; do not put this list into a per-PC initialTrackedItemValues entry unless the character-defined mode is intended. A live change later (through the Storyteller-mode tracker editor) affects the following turn.

Per the editor, script choices are evaluated at game start from initial tracker values, including that character's values and skills. Use one mode per tracker; the precedence of conflicting initialization fields, and player-mode controls for unconstrained input types, are not established.

## Conditions

A condition node is either a leaf (`category: "condition"` with type and data) or a logic group (`category: "logic"`, operator and a data array of child nodes; operators and, or, none_of). Normal condition lists are AND. Every node needs category, type and id. IDs are opaque, and importer preservation is entity-specific: use ASCII alphanumeric IDs for new trackers (see Identifiers above). Field case matters: trackedItemID, targetTrackedItemId and characterId are different native spellings.

|type|data shape and intent|
|-|-|
|triggerOnPawScript|Bare expression STRING, without `<< >>`; deterministic check of current state|
|triggerOnEvent|Scenario STRING interpreted by AI; flexible but subject to false positives/negatives. Must match an entry in the root `conditions` registry exactly; multiple triggers can reuse each Scenario. Registry size: see [Triggers.md](Triggers.md)|
|triggerOnTrackedItem|Object: trackedItemID, inequality, requiredValue, textComparison; target uses tracker ID, not variable name. requiredValue may be a `$variable`, read when checked. See Comparator fields|
|triggerOnTurn|Native string or numeric turn threshold|
|triggerOnCharacter|Array of possibleCharacters characterId references|
|triggerPrereqs|Object: prereqs array of trigger IDs, firedThisTurn boolean|
|triggerBlockers|Object: blockers array of trigger IDs, firedThisTurn boolean|
|triggerOnRandomChance|Success percentage as a STRING: numeric literal, variable or PawScript expression, re-evaluated at each check; "50" means a 50% chance|

Use a PawScript condition where it reads more clearly than native conditions; both are evaluated mechanically.

## Comparator fields

For Number trackers, `inequality` selects is_exactly, at_least, not_equal or at_most. For Text trackers, `textComparison` selects contains or does_not_contain. Do not extrapolate other comparison strings. Exports may retain both fields; they are not two simultaneous predicates. Numeric conditions natively carry `textComparison: "contains"`; if it is missing or empty, the condition is dropped from the export and the trigger loses that gate. Text Contains matching is ASCII case-insensitive. Native numeric and text controls are type-aware despite text-entry fields. Use PawScript for structured YAML field checks rather than text comparison over a whole document.

Native wrappers can repeat trackedItemID/inequality outside `data`. Keep wrapper and payload identical, following the convention of the export you are editing; the validator reports a disagreement as an error.

## Effects

|Effect|Authoring guidance|
|-|-|
|effectRunScript|Bare multiline script STRING; changes tracker values only|
|effectShowMessage|Text STRING rendered to player; use for authoritative results/status|
|effectTellAIWhatToDo|Guidance STRING influencing subsequent narration; not a state mutation or guaranteed repair|
|effectGiveInfo|AI background-information STRING; distinct from player output. Ignored with Start of Game enabled ([Triggers.md](Triggers.md))|
|effectSetTrackedItemValue|Object with trackedItemID, action, newValue, replaceWith, path, updateMode, listExpression, targetExpression; see Native value effects|
|effectModifyTrackedItemDetails|Changes Name, description, visibility, automatic updating and update instructions; a value changes only when its matching override boolean is true. See [Triggers.md](Triggers.md#changing-a-trackers-definition-during-play)|
|effectModifyInstructionBlock|`{id: instruction-block-ID, content: text}`; template timing in [Runtime.md](Runtime.md#template-interpolation-runtime)|
|effectModifyKeywordBlock|`{id: keyword-block-ID, keywords: string-array, content: text}`|
|effectPresentChoice / effectRequestInput|Native forms; see Choice and input forms|
|effectFireRandomTrigger|Array of trigger IDs; literal nothing is a sentinel. Target conditions are bypassed but consumed one-shot eligibility is enforced. Duplicate weighting is unresolved|
|effectChangePCSkill|Declared skill display name, integer amount and minmax, increase boolean. Levels and minmax are 0–5; minmax is the upper or lower boundary according to increase. Outcomes in [Characters.md](Characters.md#skills-and-player-characters)|
|effectChangeBackground|String `data`, which can be a template such as `<<$opening_assembly>>`; see [layered opening](../examples/recipe-layered-opening.json). Startup behavior in [Triggers.md](Triggers.md)|
|effectEndsGame|Boolean data means "player may continue": true allows continuation after the game-over message, false does not. It is not an enabled flag|

Other schema-defined effects change PC name/description, objective, main instructions, author style, Description instructions and victory/defeat definitions; their exact payloads are in the schema and [Payloads.md](../examples/Payloads.md), and the full set of effects is the [Trigger-Catalog](Trigger-Catalog.md): there is no effect for Evaluation, Summary or image settings. Run Script cannot edit these system properties or the background: stage text in a tracker and apply it with the native effect. A null victoryCondition/defeatCondition is an exported disabled ending.

## Native value effects

|Field / operation|Meaning and safe use|
|-|-|
|trackedItemID|Target tracker ID|
|action set|Replace target value with newValue|
|action add|Numeric addition or text append according to target type|
|action subtract|Numeric subtraction; the native text-removal operation uses this serialized action|
|action replace|Replace matched text newValue with replaceWith|
|newValue|String payload; numeric content is still serialized as text. Numeric add/subtract also accepts dice text such as `2d3`, rolled on each execution|
|path|Plain dotted path, e.g. wallet.coins; empty targets the whole tracker|
|updateMode|`path` edits a selected path; `replace` replaces the whole YAML value|
|action append|Add a value to the list at path; distinct from numeric/text add|
|listExpression / targetExpression|Empty in current exports; preserve when importing, but do not use them to invent an unsupported editor workflow|
|replaceWith|Always serialize, as "" when unused. An effect missing it was associated with the game failing at the opening|

Text adds accumulate and preserve literal quotation marks; text removal removes all matching occurrences. Repeated numeric writes within one trigger behave differently ([Triggers.md](Triggers.md)). [Payloads.md](../examples/Payloads.md) has separate native text and number examples.

The YAML editor offers Replace Value, Path, and "Do Something Complicated" (which directs authors to Run Script); there is no separate List Update workflow. Path offers Set a Value, Remove Value, Add to a list and Change Number By. Set uses YAML text with optional `<<...>>` interpolation, including whole-structure injection. Add to a list exports action append, Remove Value action remove, and Change Number By action adjust, all with updateMode path. Do not confuse these YAML operations with native text subtract or numeric add/subtract. Path fields are unchecked editor inputs: review target structure and operation together ([Editor-UI.md](Editor-UI.md#import-export-and-preserving-work)).

Adding one list member is different from updating every member. To refill each character's HP, use a script:

```text
for each $member in $test_party
  $member.hp = $member.max_hp
```

For structured append payloads, a leading `-` describes a list, while `name: Frank` with sibling fields describes one record. Flow-style YAML record append stores structured data and permits duplicates. Duplicates are kept and nested shapes are stored as written; use Run Script for list-wide transformations and deduplication.

## Choice and input forms

Present Choice includes message, choices, targetTrackedItemId, selectionMode, updateMode, limits, delimiter and path. `choices` is one newline-separated STRING (JSON `"Take road\nTake ferry"`). Single selection uses selectionMode single with null limits; multiple selection uses selectionMode multiple, string min/maxSelections such as "1" and "3", and valueDelimiter newline or comma.

Request Input uses requestText, targetTrackedItemId, inputMode (single or multi), requiresInput (true or false) and path; YAML targets expose a dotted path. The answer goes into the tracker, not into the next turn's action.

[RUNTIME] Correctly bound single-answer forms work: narration streams, the inline form waits for submission, the target tracker updates immediately, and following triggers can fire in the same turn. The tested follow-up message renders above the question/answer receipt; placement does not imply execution before submission. Required forms offer no cancellation. Multiple-choice bounds constrain selection, and newline-delimited answers are stored as text, not a YAML list. Optional blank input clears its destination while preserving sibling keys; required blank input is rejected. Multiline and nested-path writes preserve line breaks. Other delimiter variants are untested.

Binding must be correct: targetTrackedItemId must name the intended tracker, using an empty path for whole-value targeting. Check bindings after import ([Editor-UI.md](Editor-UI.md#import-export-and-preserving-work)).

## Authoring context

background, firstInput and objective feed AI context and direct play; objective also has a native update effect. They are not merely player-facing metadata. `<#...#>` are IW comment delimiters; fill sample authoring slots inside them, while genuine comments can remain. The sample Time and Location (whereWhen) block is a soft default for visible chronology; whereWhen is runtime output vocabulary, not a root export field.

Skill levels in possibleCharacters are integers from 0 through 5. The editor-provided Evaluation uses skill, difficulty, character context and common sense, including PARTIAL_SUCCESS; there is no established numeric success formula. See [Characters.md](Characters.md#evaluation).

## Assets and persistence

Image and preview fields hold asset references that IW generates; author the prompts and let the image workflow produce the references ([Images-and-Models.md](Images-and-Models.md)). Image style fields can require editor save/reload before their export reflects changes. Preview strings can persist with no attached image; empty settings can auto-populate. Preserve intentional whitespace. Nonempty portrait metadata has string fields for appearance, clothes, expression/position and setting.

Import/export steps and live copies are in [Editor-UI.md](Editor-UI.md); the trailing-newline issue is an importer quirk, not invalid JSON.

Importer-required fields beyond those observed, the path/list-expression targeting modes, initialization-field precedence, random-dispatch duplicate weighting and skill slug normalization are among the unresolved items in [Notable-Findings.md](Notable-Findings.md#still-unknown).

---

END OF DOCUMENT: reference/Schema.md
