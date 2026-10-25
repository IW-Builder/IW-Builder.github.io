# Feature recipes

These are independent recipes. Select, adapt or omit them; none is a required world architecture.

**Narrative instructions plus AI-updated trackers.** A relationship, journal, outfit, reputation or story-preference tracker can update from the ongoing story without an explicit mechanical action parser. Explain what belongs in it, when to add/change/remove entries, and what should remain stable. Match structured entries by stable identity or names/aliases as appropriate, not a list position that may change. Provide a useful format example; sample data must not silently become real world facts.

**A situation followed by a consequence.** Situation-trigger effects follow story generation; guidance does not retroactively rewrite the scene that caused it. If a behavior must shape that scene, provide the rule beforehand in active instructions.  Use triggerOnEvent for a narrative situation the AI recognizes, optionally AND a tracker/turn/prerequisite condition to narrow it. Effects might give background information, show a message, modify a value, change an objective, present a choice or alter an instruction block. Situation classification is probabilistic; use explicit predicates only for requirements that genuinely need exact enforcement. There is no requirement to replace ordinary actions with event codes.

**A threshold or dependency chain.** A relationship threshold can unlock a new characterization block; a turn condition can introduce weather or a letter; a prior event can enable another event. Intentional one-shot/repeat flags and firedThisTurn scope matter. Check order where the later trigger reads an earlier result. Avoid requiring and blocking the same trigger.

**Choice/input plus later effects.** Present a selection or text form targeting a real tracker, then respond with a later ordered trigger. Correctly bound single-answer forms update immediately. Inspect binding after import; use current tracker data rather than initialValue from the live-world editor export.

**AI update buffer plus scripted merge.** The library's update trackers let the AI propose changed structured entries, while a script merges them into a persistent list. This is useful for large casts or expensive long-lived records. Root the buffer in a record (`entries: []`), since list-rooted AI buffers lose updates, and ask for complete entries: the buffer is cleared after each merge, so field-level patches have nothing to apply to. Match records by identity. A script replacing a matched record with a partial entry can lose unchanged fields; the selected updater instructions and implementation must agree. Only use this extra layer when it serves the world.

**Conditional instruction content.** Use a native block-modification effect to add/replace/clear instructions. The source may be fixed text in the effect or text prepared in a tracker by an earlier script trigger. This can control optional image guidance, pacing, prose detail, character behavior or any relevant block. A script changes tracker values; the native effect changes the instruction block. Keep the block ID stable when disabling content so later re-enabling still targets a real block.

**Player-optional block, with no repeated writes.** The companion optional example distills the supplied native demonstration:

1. A player-only text preference has initialValueBasedOnPC player, initialValue On or Off, initialValueChoices [On, Off], autoUpdate false. The player can change this live.
2. A hidden non-AI-updated text tracker records which choice has actually been applied. It is a cache, not another player preference. hidden_boring is used by the source example.
3. A repeatable enabling trigger requires preference On AND cache not Enabled. It writes the enabled block content, then records Enabled.
4. A repeatable disabling trigger requires preference Off AND cache not Disabled. It writes empty content, or a deliberately chosen simpler fallback, then records Disabled.
5. Enable opening and later execution where needed. Initialize the cache empty so the selected startup choice gets applied. Once synchronized, neither trigger fires until the preference changes.

Clearing content is not deleting the instructionBlocks entry. Use `content: ""` as in ../examples/optional-block.json. If disabling a bundle that also changes authorStyle or specialist rules, restore ALL affected behavior to a coherent fallback. For a Storymaster toggle, define an off configuration that uses ordinary narration and no Storymaster-specific specialist or tracker dependencies. The generic toggle example demonstrates the mechanism, not a complete Storymaster toggle bundle.

Player-visible preference trackers may be hidden from the storyteller; the triggers read them deterministically. Describe their effect and potential turn cost to the player. Do not create an AI-updated tracker that changes the player's own choice back.

**More exact mechanics when requested.** Script-owned numbers, independent prerequisite checks, a request-classification tracker or a controlled transaction may be useful for a precise system. They are options for that feature, not default requirements for the world. If used, define who updates each value and avoid competing AI/script ownership of the same data. Freshness stamps matter only if consuming an AI-generated per-turn request; they are not mandatory for ordinary narrative trackers.

**Time and location: a soft default.** Offer the sample's Time and Location (whereWhen) block unless the premise makes a clock/location header unhelpful. Writing the current place and time each turn helps IW maintain chronology and gives the player a reference. Adapt the geography, calendar and precision to the setting; omit irrelevant levels rather than inventing a country or continent. Put exactly one header at the beginning of outcomeDescription, not a second competing heading. This is guidance for runtime output, not a new JSON root field.

**NPCs and keyword blocks.** Native NPC cards provide structured character data and name activation. Keyword blocks load relevant lore based on mentions and recent context. Always-on blocks provide universal guidance. Choose by intended activation, not by habit; do not make all locations or characters dynamically loaded unless the world benefits. Native character/image bookkeeping may matter even when the narrative could be described in a normal block. For an opening scene, do not depend solely on keyword activation: there may be no prior context to activate a card or block. Put essential opening facts in firstInput or always-on instructions and give starting NPCs useful brief summaries. Avoid duplicating their entire cards.

secretInfo, outcomeDescription, whereWhen and option1_text/option2_text/option3_text are runtime output concepts, not arbitrary new root export fields. Their intended use can be described in instructions and specialist requests. secretInfo can legitimately contain secrets, planning and off-screen developments in narrative worlds; the Storymaster family explicitly structures it. Do not impose an empty-secretInfo policy or a reset system unless requested by that world's design. Its contents and purported "memory dumps" remain generated text, not direct access to an engine memory store.

Use ordinary Markdown formatting where appropriate. Tests showed raw span HTML rendered literally, so do not promise arbitrary HTML/CSS styling. Header behavior and special output formatting should be tested in their actual display context. An inline-code style is a platform-rendered style, not a general color API.

## Dynamic content
Native block-modification effects substitute ordinary `<<...>>` templates when the content is installed. For live values, write deferred `<<=...=>>` references in the installed text, use a separate permanent block, or reinstall content when the relevant values change. See Capabilities.md for the interpolation table.

**Player-selected layered openings.** Combine independent choices into meaningful variations using ordered text replacements, then install the result as background. This avoids authoring every full combination; keep fragments compatible and add combination-specific handling where needed. See [layered opening](../examples/recipe-layered-opening.json).

**On-demand generation with retained results.** Install a substantial generation brief only when needed, store a compact result, and clear the brief after a matching completed request. Do not clear merely because a turn elapsed. Prefer infrequent event-driven requests; retained tracker context and AI updates can outweigh the omitted instructions. See [on-demand generation](../examples/recipe-on-demand-generation.json).


## Request and commit example

In [recipe-request-commit.json](../examples/recipe-request-commit.json), the AI records the current requested event and turn stamp. The first trigger resets the receipt, not the unconsumed request. A later trigger checks freshness, then checks funds/ownership and commits a purchase or rejection. A following effect displays the receipt and clears the request; the receipt remains for next-turn continuity. Narration describes an attempt until the committed result is available. A freshness stamp prevents stale reuse, not incorrect classification. This pattern is optional: native choices, thresholds and timed effects do not need an AI request layer.

The [example index](../examples/index.json) records each complete world's purpose and verification scope. [Payloads.md](../examples/Payloads.md) supplies smaller native shapes. Remap IDs when combining worlds and validate the result; structural checks do not certify gameplay. Select examples by feature rather than imposing the showcase's architecture on every world.

## Persistent cast: generated people who stay themselves

[Persistent cast](../examples/recipe-persistent-cast.json) generates recurring people on the fly and protects their personalities from player influence. Prose rules alone ("never skip a stage", "quirks always persist") are requests the storyteller can quietly ignore when the AI owns the tracker that holds them. This pattern moves the guarantees into scripts.

| Tracker | Owner | Job |
| --- | --- | --- |
| Cast Proposals | AI (buffer) | Full core for a person who just became recurring |
| Cast | Scripts only | Locked cores plus current stance, progress, pressure and cooldown |
| Cast Influence | AI (buffer, rewritten each turn) | This turn's attempts to influence Cast members, classified earned or pressure |
| Stance Ladder | Author | Six stance names, lowest first; edit to suit the world |
| Cast Report | Scripts | What changed in the latest pass, shown to the storyteller |

1. **Generate.** The Cast Generation block gives the storyteller a recipe: extras get one line and are never recorded. A person becomes recurring on a second appearance, social importance, or when the player seeks them out, and then gets a full core: role, concrete want, 1-3 values, voice with a sample line, 2 tells, 2-4 habits, friction with another cast member, starting stance and an anchor from 1 (impressionable) to 5 (immovable).
2. **Lock.** Admit Cast Proposals checks each proposal (name not already used, core complete, 2-4 habits, at least one value, cast under 12), copies the fields into Cast and clears the buffer. Rejections are explained in the report. After admission no script writes a core field again.
3. **Resist.** Apply Cast Influence reads this turn's entries (stale turn stamps are ignored). Attempts on the core change nothing. Earned attempts add progress; a person's stance improves only after as many earned turns as their anchor, and never more than one step per turn. Pressure adds nothing, makes them guarded for 1 + anchor turns (pushing a guarded person still counts and extends the guard), and three pressures cost a step. Sincere repair while guarded shortens the guard by one turn but earns nothing. Hurtful acts lower stance one step.
4. **Show.** The Persistent Cast block renders the current turn and the latest report through live templates, so the storyteller plays walls, progress and setbacks from authoritative state. Changes apply from the next turn: narrate the current attempt as an attempt.

Adapting it:

- **Different ladders.** Replace the six stance words with the world's own progression (for example stranger, acquaintance, regular, friend, confidant, family) and the level descriptions in the Persistent Cast block. Keep six levels or change the 0-5 bounds in both scripts.
- **Faster or slower worlds.** The anchor is both resistance and pacing. Lower anchors for impressionable casts; raise the guarded duration or the pressure limit for stubborn ones.
- **Several relationships per person.** Keep one Cast record per person and add fields such as a second level for a rival or partner, applied by the same script with a separate `target` value.
- **Visibility.** Cast is ai_only so players do not see the numbers; switch to everyone if visible progress is part of the design.
- **Buffer shape.** Both AI buffers are rooted in a record (`entries: []`) and the scripts read and clear `.entries`. List-rooted buffers lost most AI updates in a two-model comparison (see Verified-Behavior); keep the record root.
- **Limits.** The cast cap of 12 bounds context cost; raise it deliberately. The storyteller still classifies earned versus pressure, so the guarantee is the pacing and the fixed core, not the classification. A malformed proposal (for example quirks written as a sentence instead of a list) can make the admit script fail and roll back; the proposal then stays in the buffer for correction.

A variant of this pattern (same buffers, admit and apply logic, with hypnosis stages in place of stance) was live-tested in IW on Dolphin: admission, earned progress, pressure while guarded, repair while guarded and the record-rooted buffers behaved as described. This recipe itself is structurally validated; check its two scripts in Sandbox against sample proposals and influence entries before relying on it.

## Guarded state patterns

These optional complete worlds compose known primitives; their exact compositions have not been live-certified. Do not replace a world's design with them automatically.

| Example | Intent and boundary |
| --- | --- |
| [Completion and award](../examples/recipe-completion-award.json) | Set Award state's ready field to 1 through an authored action. Commit the score and completed flag together; trigger firing alone is not successful completion. |
| [Candidate acceptance](../examples/recipe-candidate-acceptance.json) | Keep candidate and accepted records separate. Set submitted to 1 to request acceptance. Checks identity, required field existence and quantity bounds before locking. This is a small semantic gate, not a general YAML type validator; coercion remains possible. |
| [Archive and restore](../examples/recipe-archive-reactivate.json) | Set Active record's request to archive or restore. Copy selected fields explicitly and consume the request. This preserves the record while marking it inactive; it does not prove exclusion from every AI context. |
| [Cached random](../examples/recipe-cached-random.json) | One trigger samples once and both blocks read the stored roll. Before that trigger runs the initial value is 0; reset ready to 0 only when a new draw is intended. This is not a guarantee of same-turn narrative visibility. |
| [Consumed milestone](../examples/recipe-consumed-timer.json) | Increment turn time before checking ticks >= 3; consume the crossing once. This counts ordinary eligible trigger cycles, not elapsed story time. Resetting only the consumed flag permits another award. |
| [Choice domain](../examples/recipe-choice-domain.json) | Accept only Courier or Archivist at consumption. Blank offers the form again; unexpected manual/script values do not commit. Multiple selections need their own delimiter/representation validation. |
| [Compiled plot](../examples/recipe-compiled-plot.json) | Literal Scenarios with ordered prerequisites and guarded awards. See [compiler contract](Engineering-Tools.md). |

The validator's review advisories cover repeat accumulation, separate script transaction boundaries, computed choice domains, multiple-choice storage and independently evaluated random expressions. They are prompts to inspect intent, never hard prohibitions or proof that a guard is missing. Existing guards can legitimately trigger a review notice. Choice menus and Enforce format do not validate all manual/script write paths.

---

END OF DOCUMENT: reference/Recipes.md
