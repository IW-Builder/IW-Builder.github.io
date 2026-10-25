# Triggers and effects

A trigger combines eligibility rules with effects. Its conditions are checked in a processing pass; if they pass and its repeat/prerequisite rules allow it, its effects run. Ordinary triggers are processed in triggerEvents array order. Repeat lets a trigger fire again whenever it is eligible; the condition does not have to become false in between. "HP below 5" with repeat enabled fires every turn while HP stays low, not once when it crosses below 5.

## Composition and sequencing

Each trigger has id, name, triggerConditions, triggerEffects, and explicit timing/repeat flags. Conditions are a list of nodes combined with AND; nested logic groups (and, or, none_of) are separate nodes, not leaves with type "or". Node shapes, payloads and comparator vocabulary are in [Schema.md](Schema.md) and [Payloads.md](../examples/Payloads.md). Scripts change trackers; native effects change instructions, objectives and other system properties.

Use a combined PawScript condition and sequential script when they make calculation or transaction clearer. Simple native conditions and effects remain appropriate. Keep separate triggers for phase boundaries or cross-effect dependencies. Give Scripts meaningful names describing effect; avoid generic "Update State." The owning trigger's name is useful when it describes effect. Clear script names make error reports easier.

A one-time reward can require quest_complete = 1 AND reward_claimed = 0. Its effects grant the reward and set reward_claimed = 1. An OR group could instead accept either of two qualifying quests. none_of passes when none of its child conditions pass. A state guard prevents repeated grants even if the trigger is repeatable; a one-shot trigger additionally records that it has already fired.

### Timing guidance:

| Intent | Start | Mid Game | Repeat | Conditions |
| --- | --- | --- | --- | --- |
| One-time setup before opening | true | false | false | None, or a setup predicate |
| Setup and every ordinary turn | true | true | true | None, or predicates checked on each pass |
| Fire once when eligible, including setup | true | true | false | Required predicates |
| Fire once when eligible after opening | false | false | false | Required predicates |
| Fire repeatedly when eligible after opening | false | false | true | Required predicates; add state guards where needed |
| Saved/inactive trigger | false | false | As intended | None; explicit dispatch is separate |

Start enables pre-opening evaluation; additional conditions still apply except for the incompatible condition types noted below. Mid Game extends a Start-enabled trigger to ordinary turns. With Start disabled, ordinary conditional triggers do not require Mid Game.

Start + Mid Game + Repeat can execute before the opening and again during turn 1, so guard counters and other effects that should run only once per turn.

With Start false, Mid Game has no effect; a stored true value requires no warning or repair. A trigger with no conditions and Start false does not fire automatically, but can remain available for explicit dispatch.

- Prerequisites/blockers with firedThisTurn true are ordered this-turn checks, resetting on subsequent turns; false uses game history. Order matters. The editor disallows requiring and blocking the same trigger; do not generate that conflict.
- Defaults are not a contract: always serialize canTriggerMoreThanOnce and the timing flags intentionally. Use repeatable commit triggers with idempotent state guards where appropriate, and true one-shot events when required.
- Restriction: Do not combine Start of Game with Scenario or minimum-turn conditions. The editor warns that these conditions are ignored; minimum-turn bypass is confirmed during both startup and mid-game execution. Use a separate startup trigger and leave Start off on the conditional trigger. Scenario runtime behavior remains unverified.

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

## Start-of-game effect restrictions

[RUNTIME] Some effects behave differently when Start of Game is enabled:

- **Give information to AI** (`effectGiveInfo`) is ignored with Start enabled, including later ordinary activations of a Start+Mid trigger. Put opening context in background or an instruction block, or use a separate ordinary-play trigger. Tell the AI what should happen next turn (`effectTellAIWhatToDo`) is a different effect and is not covered by this restriction. The validator warns for `effectGiveInfo` whenever Start is enabled.
- **Change background** replaces the opening background in Start-only mode. With Start+Mid it did not apply, and ordinary-play background or first-action changes do not rewrite an opening already shown.
- **Fire random trigger** dispatches in ordinary play but did not dispatch with Start enabled.

A trigger counting as fired does not guarantee that every stored effect executed.


## Capability discovery and reliable gating

Read [Trigger-Catalog](Trigger-Catalog.md) for every identified condition and effect, including **Modify tracked item details**, which changes a tracker's definition (Name, description, visibility, automatic updating, update instructions) rather than its value.

Eligible no-effect triggers record firing. Random dispatch bypasses target conditions but not a consumed one-shot. A failing script can still consume its containing one-shot and satisfy prerequisites; explicit successful-completion flags are therefore distinct from firing history. Native And/Or groups and PawScript expressions short-circuit in order. See [consolidated behavior](Verified-Behavior.md) for supported boundaries.

### Scenarios

Say Scenarios when talking to users; the root JSON field is `conditions`, referenced by `triggerOnEvent`. Binding requires an exact registry string, including case, spaces and punctuation; preserved JSON can still be unbound, so check the selector after import. Use literal Scenarios with explicit state gates. Dynamic Scenario text works in some single-slot arrangements but fails in multi-slot, cyclic and parallel ones, and blank slot text is not dependable deactivation. The editor stops adding Scenarios at ten entries, but imported registries of twelve were retained and executed; ten is not a runtime maximum.

---

END OF DOCUMENT: reference/Triggers.md
