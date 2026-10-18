# Cookbook: complete, independent exports

Every linked JSON is a whole world with declared targets, not a fragment to paste into a random array. The purpose is to make native shapes copyable. Structural/reference checks do not prove execution. This is an authoring reference. index.json records example scope and verification status; ../reference/Known-Limits.md describes remaining platform boundaries. Rename/remap IDs when combining examples. Sample-library modules remain separate because they require creative and dependency adaptation.

For lightweight payload lookup, use [Payloads.md](Payloads.md). Full files below remain standalone imports.

## Native conditions and effects

### Conditions

| Example | Demonstrates |
| --- | --- |
| [triggerOnEvent](condition-triggerOnEvent.json) | Recognize an AI-judged narrative Scenario; define it once in root conditions. |
| [triggerOnRandomChance](condition-triggerOnRandomChance.json) | Apply a percentage chance to an otherwise eligible trigger. |
| [triggerOnCharacter](condition-triggerOnCharacter.json) | Limit an event to selected player characters. |
| [triggerOnTrackedItem](condition-triggerOnTrackedItem.json) | Compare a tracker with a threshold or text condition. |
| [triggerPrereqs](condition-triggerPrereqs.json) | Require another trigger to have fired this turn or earlier in the game. |
| [triggerBlockers](condition-triggerBlockers.json) | Suppress an event if another trigger fired this turn or earlier in the game. |
| [triggerOnPawScript](condition-triggerOnPawScript.json) | Evaluate a deterministic state predicate. |
| [triggerOnTurn](condition-triggerOnTurn.json) | Run at a specified turn. |

### Effects

| Example | Demonstrates |
| --- | --- |
| [effectShowMessage](effect-effectShowMessage.json) | Display an authoritative player-facing result. |
| [effectTellAIWhatToDo](effect-effectTellAIWhatToDo.json) | Guide subsequent narration. |
| [effectGiveInfo](effect-effectGiveInfo.json) | Supply background information to the AI. |
| [effectSetTrackedItemValue](effect-effectSetTrackedItemValue.json) | Set or modify a tracked value with a native operation. |
| [effectModifyTrackedItemDetails](effect-effectModifyTrackedItemDetails.json) | Change selected tracker settings through explicit override flags. |
| [effectChangePCName](effect-effectChangePCName.json) | Change the active player character name. |
| [effectChangePCDescription](effect-effectChangePCDescription.json) | Change the active player character description. |
| [effectChangePCSkill](effect-effectChangePCSkill.json) | Increase/decrease a named skill with a level boundary. |
| [effectChangeObjective](effect-effectChangeObjective.json) | Replace the current story objective. |
| [effectChangeVictoryCondition](effect-effectChangeVictoryCondition.json) | Replace the native victory criterion/message. |
| [effectChangeDefeatCondition](effect-effectChangeDefeatCondition.json) | Replace the native defeat criterion/message. |
| [effectChangeMainInstructions](effect-effectChangeMainInstructions.json) | Replace main storyteller instructions. |
| [effectModifyInstructionBlock](effect-effectModifyInstructionBlock.json) | Install, replace or clear a named instruction block. |
| [effectModifyKeywordBlock](effect-effectModifyKeywordBlock.json) | Change a keyword block and its activation keywords. |
| [effectChangeAuthorStyle](effect-effectChangeAuthorStyle.json) | Change the requested prose style. |
| [effectChangeDescriptionInstructions](effect-effectChangeDescriptionInstructions.json) | Change Description specialist instructions. |
| [effectPresentChoice](effect-effectPresentChoice.json) | Ask the player to select from defined options and store the result. |
| [effectRequestInput](effect-effectRequestInput.json) | Request text and store it in a tracker. |
| [effectFireRandomTrigger](effect-effectFireRandomTrigger.json) | Dispatch a random listed trigger or the nothing sentinel; extra dispatch semantics are bounded. |
| [effectRunScript](effect-effectRunScript.json) | Execute sequential tracker updates in PawScript. |
| [effectEndsGame](effect-effectEndsGame.json) | End the game; boolean data controls whether continuing is allowed. |

## Combined recipes and other fixtures

- [logic-groups](logic-groups.json): Nested logic nodes with native shape.
- [native-text-operations](native-text-operations.json): Append, remove all matches and replace text.
- [character-starting-values](character-starting-values.json): Fixed, fixed-choice and script-choice per-PC values.
- [npc-keyword-portrait-ending](npc-keyword-portrait-ending.json): NPC, keyword, portrait descriptors and natural-language endings.
- [recipe-request-commit](recipe-request-commit.json): Optional precise transaction using a fresh AI request and script receipt.
- [recipe-choice-followup](recipe-choice-followup.json): Answer-dependent objective using a later ordered trigger.
- [recipe-threshold-unlock](recipe-threshold-unlock.json): State threshold grants access and modifies content once.
- [probe-skills](probe-skills.json): Editor-baseline Evaluation installed explicitly; capped skill effects and runtime readout.
- [probe-template-timing](probe-template-timing.json): Compare live block interpolation with effect-installed interpolation.
- [showcase-glass-ledger](showcase-glass-ledger.json): Integrated cast, alternate PCs, planning choice, precise transactions, countdown, optional prose, Scenario and script-triggered endings.

## Request -> deterministic commit [PATTERN]

Use `recipe-request-commit.json` when an AI-interpreted purchase needs exact state accounting. The example offers one guild ticket for 5 coins; its intentionally small event catalog is not a requirement for other worlds.

1. AI writes Request every turn: `turn` copies CURRENT TURN from the permanent Turn Context block and `event` is BUY_TICKET or NONE. Instructions classify the current request, not narrated success.
2. The first ordered trigger resets the receipt for the current turn. It does **not** erase the AI request before consumption.
3. A following trigger requires the fresh turn stamp and purchase event. One script checks ownership/funds, deducts coins and grants the ticket together, or writes the rejection reason.
4. A later conditional effect displays the receipt and totals only for a fresh non-NONE request, then clears the request. A persistent receipt supplies next-turn continuity.
5. Narration describes a purchase attempt until the receipt is available. It then continues from the authoritative result next turn.

The turn stamp protects against reuse, not misclassification. A model can still classify a vague input incorrectly or invent prose; this is not a perfect parser. Correctly bound native menus provide constrained answers that subsequent triggers can consume in the same turn. Native thresholds and timed effects need no AI request layer at all.

## Choice → follow-up

Correctly bound single-answer forms update their target immediately, and a later trigger can update the objective or show a receipt in the same turn. Use consistent target IDs. The single-choice example supports a fresh import without retargeting; ../reference/Import-Integrity.md explains reference checks for composed worlds.

## Threshold unlock

`recipe-threshold-unlock.json` establishes a reputation threshold, records a persistent flag and installs an instruction block. The flag makes the operation idempotent even though the trigger is repeatable. It does not require region switching, an action catalog or any particular movement system.

## Showcase scope

`showcase-glass-ledger.json` combines two player characters, Skills, a crew, keyword lore, a player-selected startup plan, an exact purchase/recovery sequence, a countdown, a player-optional prose block, a Scenario and endings. It is an integration example, not an action-engine requirement for other worlds. The showcase selects its approach through a player-controlled startup tracker.

It intentionally excludes unrelated demonstrations such as renaming the PC mid-game, switching all specialist rules, and dispatching random inactive triggers. Those have their own isolated examples. Video is not made a required dependency before its context variables are characterized. The showcase composition is structurally validated; runtime verification of an adapted world should focus on its actual feature dependencies.

## Optional verification

The cookbook is supplied to the authoring AI as examples. You do not need to play every world. index.json records the examples' purpose and verification scope. ../reference/Known-Limits.md identifies behavior that needs checking only when a design depends on it. Structural validation and a successful runtime check are separate claims.


For reference integrity and importing, see ../reference/Import-Integrity.md.

## YAML path operations

[yaml-path-operations.json](yaml-path-operations.json) demonstrates set, remove, append and adjust on separate turns. Its paths match the declared YAML structure. This composition is structurally validated; its full runtime sequence is not certified.

## Narrative-first example

[narrative-last-ferry.json](narrative-last-ferry.json) demonstrates a focused opening, distinct NPC voices, optional lore and bounded AI memory without a custom action engine. [PATTERN]: structurally checked, not a runtime-qualified benchmark.
