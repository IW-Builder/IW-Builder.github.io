# Feature recipes

These are independent recipes. Select, adapt or omit them; none is a required world architecture.

**Narrative instructions plus AI-updated trackers.** A relationship, journal, outfit, reputation or story-preference tracker can update from the ongoing story without an explicit mechanical action parser. Explain what belongs in it, when to add/change/remove entries, and what should remain stable. Match structured entries by stable identity or names/aliases as appropriate, not a list position that may change. Provide a useful format example; sample data must not silently become real world facts.

**A situation followed by a consequence.** Situation-trigger effects follow story generation; guidance does not retroactively rewrite the scene that caused it. If a behavior must shape that scene, provide the rule beforehand in active instructions.  Use triggerOnEvent for a narrative situation the AI recognizes, optionally AND a tracker/turn/prerequisite condition to narrow it. Effects might give background information, show a message, modify a value, change an objective, present a choice or alter an instruction block. Situation classification is probabilistic; use explicit predicates only for requirements that genuinely need exact enforcement. There is no requirement to replace ordinary actions with event codes.

**A threshold or dependency chain.** A relationship threshold can unlock a new characterization block; a turn condition can introduce weather or a letter; a prior event can enable another event. Intentional one-shot/repeat flags and firedThisTurn scope matter. Check order where the later trigger reads an earlier result. Avoid requiring and blocking the same trigger.

**Choice/input plus later effects.** Present a selection or text form targeting a real tracker, then respond with a later ordered trigger. Correctly bound single-answer forms update immediately. Inspect binding after import; use current tracker data rather than initialValue from the live-world editor export.

**AI update buffer plus scripted merge.** The library's update trackers let the AI propose changed structured entries, while a script merges them into a persistent list. This is useful for large casts or expensive long-lived records. Match records by identity; choose whether update entries are full replacement records or partial patches. A script replacing a matched record with a partial entry can lose unchanged fields; the selected updater instructions and implementation must agree. Only use this extra layer when it serves the world.

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
Native block-modification effects substitute templates when the content is installed. For live values, use a separate permanent block or reinstall content when the relevant values change. See Capabilities.md for the interpolation table.

**Player-selected layered openings.** Combine independent choices into meaningful variations using ordered text replacements, then install the result as background. This avoids authoring every full combination; keep fragments compatible and add combination-specific handling where needed. See [layered opening](../examples/recipe-layered-opening.json) and its [Cookbook notes](../examples/README.md#player-selected-layered-opening).

**On-demand generation with retained results.** Install a substantial generation brief only when needed, store a compact result, and clear the brief after a matching completed request. Do not clear merely because a turn elapsed. Prefer infrequent event-driven requests; retained tracker context and AI updates can outweigh the omitted instructions. See [on-demand generation](../examples/recipe-on-demand-generation.json) and its [cost and runtime notes](../examples/README.md#on-demand-generation-with-retained-results).
