# Examples to explore

Want to see what a feature can do before adding it to your world? These small worlds show individual features and combinations you can try in IW or ask your AI to adapt.

Each JSON file is a complete world. Import it into a separate world to explore it without replacing your own work. Some are demonstrations rather than finished adventures, and not every example has been tested through a full playthrough.

## Start with a story

- [Vendemmia](narrative-vendemmia.json): A vineyard story with three potential love interests and different relationships to explore.
- [Seven Nights](narrative-seven-nights.json): A fantasy relationship story built around promises, character motives and a small cast.
- [Velvet Wager](narrative-velvet-wager.json): An adult villa setting focused on intimate character dynamics.
- [The Glass Ledger](showcase-glass-ledger.json): A more involved example combining a crew, choices, purchases, a countdown and endings.

The relationship-focused examples include mature material. Pick one close to the kind of experience you want, rather than treating any of them as a required template.

## Try a useful combination

| Example | What to explore |
| --- | --- |
| [A purchase with a receipt](recipe-request-commit.json) | Check funds, make a purchase and report what changed. |
| [A choice that changes the goal](recipe-choice-followup.json) | Let the player's answer guide what comes next. |
| [Unlock something through progress](recipe-threshold-unlock.json) | Open up new content when a tracked value reaches a threshold. |
| [An optional story setting](optional-block.json) | Let the player switch an extra feature on or off. |
| [Different character starting values](character-starting-values.json) | Give characters fixed values or a choice of starting options. |
| [Characters, lore, portraits and endings](npc-keyword-portrait-ending.json) | See several familiar world-building features together. |
| [Combining conditions](logic-groups.json) | Make an event depend on several requirements or alternatives. |
| [Changing text](native-text-operations.json) | Add, remove or replace parts of a text tracker. |
| [Changing structured data](yaml-path-operations.json) | Update individual parts of a YAML tracker. |
| [Skills demonstration](probe-skills.json) | Inspect skill changes and their limits. |
| [When values appear in text](probe-template-timing.json) | Compare changing values with text saved at a particular moment. |

## Explore one feature at a time

These examples are useful when you know what you want to happen but are unsure which IW feature handles it.

### When should something happen?

- [React to a story situation](condition-triggerOnEvent.json)
- [Let chance decide](condition-triggerOnRandomChance.json)
- [Vary events by player character](condition-triggerOnCharacter.json)
- [React to a tracked value](condition-triggerOnTrackedItem.json)
- [Wait for an earlier event](condition-triggerPrereqs.json)
- [Prevent conflicting events](condition-triggerBlockers.json)
- [Check a scripted rule](condition-triggerOnPawScript.json)
- [Wait until a turn](condition-triggerOnTurn.json)

### What should happen?

- [Show a message](effect-effectShowMessage.json)
- [Guide the next scene](effect-effectTellAIWhatToDo.json)
- [Give the storyteller background information](effect-effectGiveInfo.json)
- [Change a tracked value](effect-effectSetTrackedItemValue.json)
- [Change tracker settings](effect-effectModifyTrackedItemDetails.json)
- [Rename the player character](effect-effectChangePCName.json)
- [Change the player description](effect-effectChangePCDescription.json)
- [Adjust a skill](effect-effectChangePCSkill.json)
- [Change the goal](effect-effectChangeObjective.json)
- [Change the victory conditions](effect-effectChangeVictoryCondition.json)
- [Change the defeat conditions](effect-effectChangeDefeatCondition.json)
- [Change story instructions](effect-effectChangeMainInstructions.json)
- [Switch an instruction block](effect-effectModifyInstructionBlock.json)
- [Change keyword-triggered lore](effect-effectModifyKeywordBlock.json)
- [Change the writing style](effect-effectChangeAuthorStyle.json)
- [Change scene-description guidance](effect-effectChangeDescriptionInstructions.json)
- [Offer a choice](effect-effectPresentChoice.json)
- [Ask for a written answer](effect-effectRequestInput.json)
- [Choose a random event](effect-effectFireRandomTrigger.json)
- [Run a script](effect-effectRunScript.json)
- [End the game](effect-effectEndsGame.json)

## Look under the hood

The [feature recipes](../reference/Recipes.md) explain how these approaches work and when to use them. [Payloads.md](Payloads.md) contains smaller technical snippets, and [index.json](index.json) records the scope and testing status of the examples.

[Back to the main guide](https://iw-builder.github.io/guide/)

The [guarded state recipes](../reference/Recipes.md) include completion awards, candidate acceptance, archive/reactivation, cached randomness, consumed timers, choice-domain checks and a compiled prerequisite graph. Their exact compositions are structurally checked patterns, not newly live-certified worlds.
