# Trigger capability catalog

Read this overview before saying a trigger cannot do something. It lists every condition and effect kind in the current editor. User-facing labels describe purpose; exact picker wording can vary. Use tracker/trigger Names with users, reserving the JSON identifiers below for implementation or requested technical detail.

## Trigger gates and composition

Start of game, Or mid-game, repeat eligibility and advanced logic are trigger settings, not additional effect types. The effect picker changes with Start mode: Start offers background, first-action and Other Character changes and omits Give information and Fire random trigger. Normal condition lists are And; nested groups support And, Or and None Of. Native And/Or and PawScript boolean expressions short-circuit. Empty ordinary condition lists do not run automatically. Start compatibility is effect-specific; see [Triggers](Triggers.md).

## Conditions

| Capability | JSON type | Scope |
| --- | --- | --- |
| Scenario | `triggerOnEvent` | AI-interpreted narrative situation; exact registry binding required. |
| PawScript condition | `triggerOnPawScript` | Bare expression returning true/false. |
| Random chance | `triggerOnRandomChance` | Success percentage; native string/expression payload. |
| Turn at least | `triggerOnTurn` | Minimum turn threshold; native string or numeric representation. |
| Chosen character | `triggerOnCharacter` | Selected source player character, independent of customized display Name. |
| Tracked item / player action comparison | `triggerOnTrackedItem` | Native numeric/text comparisons; text Contains is ASCII case-insensitive. Preserve hidden comparator fields: a missing textComparison drops the condition. |
| Prerequisite triggers | `triggerPrereqs` | Required trigger firing, this turn or historical. |
| Blocking triggers | `triggerBlockers` | Exclude after specified trigger firing, this turn or historical. |

## Effects

| Capability | JSON type | Scope |
| --- | --- | --- |
| Run script | `effectRunScript` | Sequential tracker calculations and structured changes; not arbitrary system-property writes. |
| Show message | `effectShowMessage` | Player-facing text. |
| Tell AI what should happen next turn | `effectTellAIWhatToDo` | Narrative guidance, not guaranteed state mutation. |
| Give information to AI | `effectGiveInfo` | Information distinct from next-turn guidance; ignored with Start enabled. |
| Set/change tracked item value | `effectSetTrackedItemValue` | Numeric/text updates, whole YAML replacement, path set/remove/append/adjust. |
| Modify tracked item details | `effectModifyTrackedItemDetails` | Change Name, description, visibility, automatic updating and update instructions using matching override flags; applies from the next turn; not in the same trigger as Request Input ([Triggers](Triggers.md#changing-a-trackers-definition-during-play)). |
| Modify extra instruction block | `effectModifyInstructionBlock` | Replace block content; template installation timing matters. |
| Modify keyword instruction block | `effectModifyKeywordBlock` | Change keywords and content. |
| Present choice | `effectPresentChoice` | Single/multiple selection, limits, delimiter and target/path. |
| Request input | `effectRequestInput` | Required/optional single/multiline text into target/path. |
| Fire random trigger | `effectFireRandomTrigger` | Dispatch a pool target, bypassing its conditions but not consumed one-shot eligibility. |
| Change player Name | `effectChangePCName` | Change player display name. |
| Change player description | `effectChangePCDescription` | Change player description. |
| Change player skill | `effectChangePCSkill` | Increase/decrease a declared skill with a level cap. |
| Change objective | `effectChangeObjective` | Replace objective text. |
| Change main instructions | `effectChangeMainInstructions` | Replace main instruction text. |
| Change author style | `effectChangeAuthorStyle` | Replace writing-style guidance. |
| Change Description instructions | `effectChangeDescriptionInstructions` | Replace specialist narration instructions. |
| Change victory condition | `effectChangeVictoryCondition` | Change victory definition. |
| Change defeat condition | `effectChangeDefeatCondition` | Change defeat definition. |
| Change background | `effectChangeBackground` | Startup background replacement; ordinary/combined modes are not equivalent. |
| Change first action | `effectChangeFirstAction` | Editor-recognized startup opening-action replacement; represented structurally in the schema. |
| Change other characters | `effectChangeOtherCharacters` | Add/Modify/Delete Character, offered only in the Start picker. Add uses `character: null`; Modify/Delete name the target by its current name. Runtime mutation unresolved. |
| Ends game | `effectEndsGame` | End ordinary play; data true allows optional continuation, false does not. |

Native startup payload examples: [background](../examples/effect-effectChangeBackground.json), [first action](../examples/effect-effectChangeFirstAction.json), and Other Character [Add](../examples/effect-effectChangeOtherCharacters-add.json), [Modify](../examples/effect-effectChangeOtherCharacters-modify.json), [Delete](../examples/effect-effectChangeOtherCharacters-delete.json). Their verification limits are stated in each example; [Payloads.md](../examples/Payloads.md) includes the complete effect nodes.

## Scope of this catalog

Everything listed is represented in the schema and has a native example under ../examples/; read [Schema](Schema.md) and the specific payload only when implementing. **Modify tracked item details** changes a tracker's definition (Name, description, visibility, automatic updating, update instructions) rather than its value; its rules and the Request Input restriction are in [Triggers](Triggers.md#changing-a-trackers-definition-during-play). There is no effect that changes Evaluation, Summary or image settings; Change Description instructions is the only specialist-request effect.

---

END OF DOCUMENT: reference/Trigger-Catalog.md
