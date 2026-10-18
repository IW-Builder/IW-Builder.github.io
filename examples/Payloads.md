# Compact native payload cookbook

[DOCUMENTED] Exact payload shapes, extracted from the complete example worlds. These are snippets, not independently importable worlds. Read ../reference/Schema.md for field semantics and ../reference/Triggers.md for timing. Copy the node into triggerConditions or triggerEffects as appropriate, assign a unique node ID, and declare/remap every target. For a coherent transaction, choose one complete recipe rather than concatenating unrelated snippets.

Every authored trigger also needs an id, name, conditions/effects arrays and explicit triggerOnStartOfGame, triggerMidGame and canTriggerMoreThanOnce flags. Conditions normally AND together. Scripts are bare code strings; messages may contain templates. String payload values remain JSON strings.

## triggerBlockers

Suppress an event if another trigger fired this turn or earlier in the game. Full world: [condition-triggerBlockers.json](condition-triggerBlockers.json).

```json
{
  "category": "condition",
  "type": "triggerBlockers",
  "data": {
    "blockers": [
      "trg-anchor"
    ],
    "firedThisTurn": true
  },
  "id": "node-condition-triggerBlockers-3"
}
```

Dependencies: triggerEvents trg-anchor (Anchor).

## triggerOnCharacter

Limit an event to selected player characters. Full world: [condition-triggerOnCharacter.json](condition-triggerOnCharacter.json).

```json
{
  "category": "condition",
  "type": "triggerOnCharacter",
  "data": [
    "pc-visitor"
  ],
  "id": "node-condition-triggerOnCharacter-1"
}
```

Dependencies: possibleCharacters pc-visitor (Avery).

## triggerOnEvent

Recognize an AI-judged narrative Scenario; define it once in root conditions. Full world: [condition-triggerOnEvent.json](condition-triggerOnEvent.json).

```json
{
  "category": "condition",
  "type": "triggerOnEvent",
  "data": "The player explicitly asks the clerk for a receipt.",
  "id": "node-condition-triggerOnEvent-1"
}
```

Dependencies: root conditions must include the Scenario text.

## triggerOnPawScript

Evaluate a deterministic state predicate. Full world: [condition-triggerOnPawScript.json](condition-triggerOnPawScript.json).

```json
{
  "category": "condition",
  "type": "triggerOnPawScript",
  "data": "$coins >= 10",
  "id": "node-condition-triggerOnPawScript-1"
}
```

Dependencies: script/template roots: $coins.

## triggerOnRandomChance

Apply a percentage chance to an otherwise eligible trigger. Full world: [condition-triggerOnRandomChance.json](condition-triggerOnRandomChance.json).

```json
{
  "category": "condition",
  "type": "triggerOnRandomChance",
  "data": "50",
  "id": "node-condition-triggerOnRandomChance-1"
}
```

## triggerOnTrackedItem

Compare a tracker with a threshold or text condition. Full world: [condition-triggerOnTrackedItem.json](condition-triggerOnTrackedItem.json).

```json
{
  "category": "condition",
  "type": "triggerOnTrackedItem",
  "data": {
    "trackedItemID": "o8pvrgyOL",
    "inequality": "at_least",
    "requiredValue": "10",
    "textComparison": "contains"
  },
  "id": "node-condition-triggerOnTrackedItem-1"
}
```

Dependencies: trackedItems o8pvrgyOL (Coins).

## triggerOnTurn

Run at a specified turn. Full world: [condition-triggerOnTurn.json](condition-triggerOnTurn.json).

```json
{
  "category": "condition",
  "type": "triggerOnTurn",
  "data": 2,
  "id": "node-condition-triggerOnTurn-1"
}
```

## triggerPrereqs

Require another trigger to have fired this turn or earlier in the game. Full world: [condition-triggerPrereqs.json](condition-triggerPrereqs.json).

```json
{
  "category": "condition",
  "type": "triggerPrereqs",
  "data": {
    "prereqs": [
      "trg-anchor"
    ],
    "firedThisTurn": true
  },
  "id": "node-condition-triggerPrereqs-3"
}
```

Dependencies: triggerEvents trg-anchor (Anchor).

## effectChangeAuthorStyle

Change the requested prose style. Full world: [effect-effectChangeAuthorStyle.json](effect-effectChangeAuthorStyle.json).

```json
{
  "type": "effectChangeAuthorStyle",
  "data": "Use short paragraphs and dry, understated humor.",
  "id": "node-effect-effectChangeAuthorStyle-2"
}
```

## effectChangeDefeatCondition

Replace the native defeat criterion/message. Full world: [effect-effectChangeDefeatCondition.json](effect-effectChangeDefeatCondition.json).

```json
{
  "type": "effectChangeDefeatCondition",
  "data": {
    "condition": "The player has explicitly abandoned the demonstration.",
    "text": "The demonstration ends unfinished.",
    "alreadyFired": false
  },
  "id": "node-effect-effectChangeDefeatCondition-2"
}
```

## effectChangeDescriptionInstructions

Change Description specialist instructions. Full world: [effect-effectChangeDescriptionInstructions.json](effect-effectChangeDescriptionInstructions.json).

```json
{
  "type": "effectChangeDescriptionInstructions",
  "data": "Write a concise second-person scene grounded in the guild office. Keep the player's intentions intact.",
  "id": "node-effect-effectChangeDescriptionInstructions-2"
}
```

## effectChangeMainInstructions

Replace main storyteller instructions. Full world: [effect-effectChangeMainInstructions.json](effect-effectChangeMainInstructions.json).

```json
{
  "type": "effectChangeMainInstructions",
  "data": "Continue a short guild-office scene. Mara is the clerk. Respect the tracker values; the player decides what to do next.",
  "id": "node-effect-effectChangeMainInstructions-2"
}
```

## effectChangeObjective

Replace the current story objective. Full world: [effect-effectChangeObjective.json](effect-effectChangeObjective.json).

```json
{
  "type": "effectChangeObjective",
  "data": "Learn why the silver seal is missing.",
  "id": "node-effect-effectChangeObjective-2"
}
```

## effectChangePCDescription

Change the active player character description. Full world: [effect-effectChangePCDescription.json](effect-effectChangePCDescription.json).

```json
{
  "type": "effectChangePCDescription",
  "data": "Avery Reed is a courier newly recognized by the guild.",
  "id": "node-effect-effectChangePCDescription-2"
}
```

## effectChangePCName

Change the active player character name. Full world: [effect-effectChangePCName.json](effect-effectChangePCName.json).

```json
{
  "type": "effectChangePCName",
  "data": "Avery Reed",
  "id": "node-effect-effectChangePCName-2"
}
```

## effectChangePCSkill

Increase/decrease a named skill with a level boundary. Full world: [effect-effectChangePCSkill.json](effect-effectChangePCSkill.json).

```json
{
  "type": "effectChangePCSkill",
  "data": {
    "name": "Observation",
    "amount": 2,
    "minmax": 4,
    "increase": true
  },
  "id": "node-effect-effectChangePCSkill-2"
}
```

## effectChangeVictoryCondition

Replace the native victory criterion/message. Full world: [effect-effectChangeVictoryCondition.json](effect-effectChangeVictoryCondition.json).

```json
{
  "type": "effectChangeVictoryCondition",
  "data": {
    "condition": "The player has explicitly asked to finish the demonstration.",
    "text": "The demonstration is complete.",
    "alreadyFired": false
  },
  "id": "node-effect-effectChangeVictoryCondition-2"
}
```

## effectEndsGame

End the game; boolean data controls whether continuing is allowed. Full world: [effect-effectEndsGame.json](effect-effectEndsGame.json).

```json
{
  "type": "effectEndsGame",
  "data": true,
  "id": "node-effect-effectEndsGame-3"
}
```

## effectFireRandomTrigger

Dispatch a random listed trigger or the nothing sentinel; extra dispatch semantics are bounded. Full world: [effect-effectFireRandomTrigger.json](effect-effectFireRandomTrigger.json).

```json
{
  "type": "effectFireRandomTrigger",
  "data": [
    "trg-child-a",
    "trg-child-b"
  ],
  "id": "node-effect-effectFireRandomTrigger-2"
}
```

Dependencies: triggerEvents trg-child-a (Child A); triggerEvents trg-child-b (Child B).

## effectGiveInfo

Supply background information to the AI. Full world: [effect-effectGiveInfo.json](effect-effectGiveInfo.json).

```json
{
  "type": "effectGiveInfo",
  "data": "Mara has just learned that the courier route is clear.",
  "id": "node-effect-effectGiveInfo-2"
}
```

## effectModifyInstructionBlock

Install, replace or clear a named instruction block. Full world: [effect-effectModifyInstructionBlock.json](effect-effectModifyInstructionBlock.json).

```json
{
  "type": "effectModifyInstructionBlock",
  "data": {
    "id": "blk-guidance",
    "content": "Mara now offers the courier assignment."
  },
  "id": "node-effect-effectModifyInstructionBlock-2"
}
```

Dependencies: instructionBlocks blk-guidance (Guild Guidance).

## effectModifyKeywordBlock

Change a keyword block and its activation keywords. Full world: [effect-effectModifyKeywordBlock.json](effect-effectModifyKeywordBlock.json).

```json
{
  "type": "effectModifyKeywordBlock",
  "data": {
    "id": "kw-guild",
    "keywords": [
      "silver seal",
      "crescent"
    ],
    "content": "The silver seal has a crescent engraving and is kept in the clerk's desk."
  },
  "id": "node-effect-effectModifyKeywordBlock-2"
}
```

Dependencies: loreBookEntries kw-guild (Guild Seal).

## effectModifyTrackedItemDetails

Change selected tracker settings through explicit override flags. Full world: [effect-effectModifyTrackedItemDetails.json](effect-effectModifyTrackedItemDetails.json).

```json
{
  "type": "effectModifyTrackedItemDetails",
  "data": {
    "trackedItemID": "SRdpskbWh",
    "overrideName": false,
    "overrideDescription": false,
    "overrideVisibility": true,
    "overrideAutoUpdate": true,
    "overrideUpdateInstructions": true,
    "name": "Note",
    "description": "",
    "updateInstructions": "Record one brief observation about the guild each turn.",
    "visibility": "everyone",
    "autoUpdate": true
  },
  "id": "node-effect-effectModifyTrackedItemDetails-2"
}
```

Dependencies: trackedItems SRdpskbWh (Note).

## effectPresentChoice

Ask the player to select from defined options and store the result. Full world: [effect-effectPresentChoice.json](effect-effectPresentChoice.json).

```json
{
  "id": "node-effect-effectPresentChoice-2",
  "data": {
    "path": "",
    "valueDelimiter": "newline",
    "updateMode": "replace",
    "minSelections": null,
    "choices": "Courier\nArchivist",
    "maxSelections": null,
    "targetTrackedItemId": "GJlIgehdL",
    "selectionMode": "single",
    "message": "Choose your guild assignment."
  },
  "type": "effectPresentChoice"
}
```

Dependencies: trackedItems GJlIgehdL (Answer).

## effectRequestInput

Request text and store it in a tracker. Full world: [effect-effectRequestInput.json](effect-effectRequestInput.json).

```json
{
  "id": "node-effect-effectRequestInput-2",
  "data": {
    "path": "",
    "inputMode": "single",
    "requestText": "What nickname should the clerk use?",
    "requiresInput": true,
    "targetTrackedItemId": "jcbMjWZOx"
  },
  "type": "effectRequestInput"
}
```

Dependencies: trackedItems jcbMjWZOx (Answer).

## effectRunScript

Execute sequential tracker updates in PawScript. Full world: [effect-effectRunScript.json](effect-effectRunScript.json).

```json
{
  "type": "effectRunScript",
  "data": "$coins -= 2\n$flag = 1",
  "name": "Spend Coins and Mark Flag",
  "id": "node-effect-effectRunScript-2"
}
```

Dependencies: script/template roots: $coins, $flag.

## effectSetTrackedItemValue

Set or modify a tracked value with a native operation. Full world: [effect-effectSetTrackedItemValue.json](effect-effectSetTrackedItemValue.json).

```json
{
  "type": "effectSetTrackedItemValue",
  "data": {
    "trackedItemID": "NR2bqLfoi",
    "action": "add",
    "newValue": "2",
    "replaceWith": "",
    "path": "",
    "updateMode": "path",
    "listExpression": "",
    "targetExpression": ""
  },
  "id": "node-effect-effectSetTrackedItemValue-2"
}
```

Dependencies: trackedItems NR2bqLfoi (Coins).

## effectShowMessage

Display an authoritative player-facing result. Full world: [effect-effectShowMessage.json](effect-effectShowMessage.json).

```json
{
  "type": "effectShowMessage",
  "data": "The clerk has recorded your visit.",
  "id": "node-effect-effectShowMessage-2"
}
```

## effectTellAIWhatToDo

Guide subsequent narration. Full world: [effect-effectTellAIWhatToDo.json](effect-effectTellAIWhatToDo.json).

```json
{
  "type": "effectTellAIWhatToDo",
  "data": "On the next scene, have Mara ask which assignment interests the player.",
  "id": "node-effect-effectTellAIWhatToDo-2"
}
```

