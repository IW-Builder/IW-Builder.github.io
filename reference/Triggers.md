# Triggers and effects

## Composition and sequencing

Each trigger has id, name, triggerConditions, triggerEffects, and explicit timing/repeat flags. Conditions are a list of nodes; the normal list is AND. A leaf uses `category: "condition"`, `type` and `data`. A logic node uses `category: "logic"`, operator and a data ARRAY of child nodes. Known operators: and, or, none_of. A logic group is not a leaf with type "or".

Prefer one combined PawScript expression and one multiline Run Script effect for a coherent mechanical transaction. Keep separate triggers for actual phase boundaries or cross-effect dependencies. Give each Run Script effect a meaningful name describing its effect; avoid generic names such as "Update State." The owning trigger's name is useful when it also describes the effect. Clear script names make error reports easier to locate.

Exact payloads and native comparison vocabulary are in Schema.md and ../examples/Payloads.md.

### Timing guidance:

- Start-only, with no other conditions: opening setup. Additional conditions restrict firing.
- Start + Mid Game permits opening and later eligibility. Multiple triggering must also be enabled for repeated execution; otherwise a once-fired trigger stays consumed.
- Start + Mid Game + multiple, no other conditions: every-turn behavior.
- Ordinary conditional triggers can run later with Start unchecked. Do not rely on undocumented first-turn timing; explicitly enable opening execution when required and test it.
- Mid Game true without Start true is editor-inconsistent; avoid emitting it. Both false can be intentional for ordinary conditional or saved content.
- No conditions + Start unchecked is valid saved/inactive content, not an ordinary automatic trigger. Do not "repair" intentionally disabled content into firing every turn.
- Prerequisites/blockers with firedThisTurn true are ordered this-turn checks, resetting on subsequent turns; false uses game history. Order matters. The editor disallows requiring and blocking the same trigger; do not generate that conflict.
- Defaults are not a contract: always serialize canTriggerMoreThanOnce and the timing flags intentionally. Use repeatable commit triggers with idempotent state guards where appropriate, and true one-shot events when required.
- Restriction: Do not combine Start of Game with Scenario or minimum-turn conditions. The editor warns that these conditions are ignored; minimum-turn bypass is confirmed during both startup and mid-game execution. Use a separate startup trigger and leave Start off on the conditional trigger. Scenario runtime behavior remains unverified.

See Schema.md for native effect payloads and input options. Scripts change trackers; native effects change instructions, objectives and other system properties.

### Execution order and effect semantics:

1. Later triggers see earlier committed writes. AI-updated request trackers were available to that turn's trigger checks. Correctly bound Present Choice/Request Input results are available to subsequent triggers in the same turn. This does not describe every internal generation stage.
2. Native numeric Set/Add effects within ONE trigger do not accumulate normally: starting at 0, add 2 then add 3 ended at 3; starting at 1, set 5 then add 2 ended at 3. Reads can nevertheless see changed values. Do not "explain" this with a universal snapshot rule; internals are unproven.
3. Run Script is different: sequential set/add and repeated arithmetic DID accumulate, nested YAML changes preserved unrelated keys, and separate script effects writing different YAML paths preserved both. Tested script failures rolled back that script's changes. Do not claim a whole-trigger rollback covering earlier successful effects.
4. For dependent operations prefer one script. Otherwise put preparation in one trigger and consumption in a following trigger. Do not assume a later native effect's expression sees an earlier native write merely because it appears lower in the same trigger.
5. Native text additions stacked; removal removed all matches and literal quotes are retained. Do not apply numeric overwrite behavior to text or script statements.
6. First guidance appeared to dominate in limited narrative-only tests. Generate one coherent, mutually exclusive guidance outcome rather than contradictory directives whose priority you hope to control.

## Choosing Implementation:

| Approach | Best suited to | Main trade-off |
|---|---|---|
| Instructions and AI-updated trackers | Narrative judgment, descriptive state and flexible interactions | Outcomes depend on model interpretation; unsuitable for guaranteed arithmetic or enforcement |
| Native conditions and effects | Simple rules, editor-friendly customization and platform operations | Repeated cases can require many entries; native effect sequencing needs care |
| PawScript | Exact calculations, structured state, collection operations and repeated logic | Requires code maintenance; only supported writable values can be changed |
| Hybrid | Calculated outcomes combined with messages, block updates, opening changes or other native operations | Requires explicit ordering between calculation and application |

Native comparisons and PawScript conditions are both evaluated mechanically. Neither inherently makes narration more reliable. Use AI instructions to explain the intended behavior and deterministic conditions/scripts where exact enforcement matters.
Consolidate repeated logic when it improves clarity, but preserve meaningful execution stages and useful debugging boundaries. Consider where content is stored: moving inactive trigger payloads into AI-visible trackers can increase context cost. Performance gains from consolidation require measurement.
