# Trigger capability catalog

Read this overview before saying a trigger cannot do something. It lists all condition/effect kinds currently identified in the kit and observed editor, not a guarantee about future additions. User-facing labels describe purpose; exact picker wording can vary. Use tracker/trigger Names with users, reserving the JSON identifiers below for implementation or requested technical detail.

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
| Modify tracked item details | `effectModifyTrackedItemDetails` | Change Name, description, visibility, automatic updating and update instructions using matching override flags. Yes: autoUpdate can change, from the next turn; not alongside Request Input (below). |
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

Native startup payload examples: [background](../examples/effect-effectChangeBackground.json), [first action](../examples/effect-effectChangeFirstAction.json), and Other Character [Add](../examples/effect-effectChangeOtherCharacters-add.json), [Modify](../examples/effect-effectChangeOtherCharacters-modify.json), [Delete](../examples/effect-effectChangeOtherCharacters-delete.json). Their verification limits are stated in each example; the [payload cookbook](../examples/Payloads.md) includes the complete effect nodes.

## Changing automatic updating

**Modify tracked item details** can turn automatic updating on or off. Set `overrideAutoUpdate: true` and the desired `autoUpdate` value. Equivalent override flags select changes to Name, description, visibility and update instructions. Changing a field without its matching override does not apply it. This changes future update behavior; it does not undo an earlier write in the current turn, so plan an explicit handoff point between AI and script ownership and inspect the next turn.

Verified live (probe P37): on and off both work, repeatedly. A switch on turn N affects the AI from turn N+1, because triggers run after the AI's tracker update. Re-sending update instructions is unnecessary. **Never put this effect in a trigger that also has Request Input**: the change is silently lost while messages and scripts there still run. Give it its own trigger with the same condition (works on the same turn). Present Choice is untested; treat it the same. It can also reveal a hidden tracker. Visibility restrictions still matter. With `overrideVisibility: true`, the observed visibility values are everyone, player_only, ai_only, hidden, ai_only_boring and hidden_boring. They survive editor import, and live effects apply the expected player-visible/hidden grouping.

This capability is already represented by the schema and [native example](../examples/effect-effectModifyTrackedItemDetails.json); no example needs to be read merely to discover that it exists. Read [Schema](Schema.md) and the specific payload only when implementing. The schema is a partial compatibility profile, not the definition of all platform capabilities. Do not infer nonexistent Evaluation, Summary or image-change effects from similarly named effects.

---

END OF DOCUMENT: reference/Trigger-Catalog.md
