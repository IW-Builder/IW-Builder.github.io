# Feature recipes

These are independent recipes. Select, adapt or omit them; none is a required world architecture.

**Narrative instructions plus AI-updated trackers.** A relationship, journal, outfit, reputation or story-preference tracker can update from the ongoing story without an explicit mechanical action parser. Explain what belongs in it, when to add/change/remove entries, and what should remain stable. Match structured entries by stable identity or names/aliases as appropriate, not a list position that may change. Provide a useful format example; sample data must not silently become real world facts.

**A situation followed by a consequence.** Situation-trigger effects follow story generation; guidance does not retroactively rewrite the scene that caused it. If a behavior must shape that scene, provide the rule beforehand in active instructions.  Use triggerOnEvent for a narrative situation the AI recognizes, optionally AND a tracker/turn/prerequisite condition to narrow it. Effects might give background information, show a message, modify a value, change an objective, present a choice or alter an instruction block. Situation classification is probabilistic; use explicit predicates only for requirements that genuinely need exact enforcement. There is no requirement to replace ordinary actions with event codes.

**A threshold or dependency chain.** A relationship threshold can unlock a new characterization block; a turn condition can introduce weather or a letter; a prior event can enable another event. Intentional one-shot/repeat flags and firedThisTurn scope matter. Check order where the later trigger reads an earlier result. Avoid requiring and blocking the same trigger.

**Choice/input plus later effects.** Present a selection or text form targeting a real tracker, then respond with a later ordered trigger. Correctly bound single-answer forms update immediately. Inspect binding after import; use current tracker data rather than initialValue from the live-world editor export.

**AI update buffer plus scripted merge.** The library's update trackers let the AI propose changed structured entries, while a script merges them into a persistent list. This is useful for large casts or expensive long-lived records. Root the buffer in a record (`entries: []`); list-rooted AI buffers lose updates, even with "append-only" wording. A record root can still jam: the AI may write rows as one nested list (`entries: [[…]]`), and a merge gated on `.entries.any(name.exists())` then never fires again. Gate on a non-empty inbox, drop or unwrap non-record items, and flag an inbox still full after the merge. Match records by identity and ask for complete entries: the buffer is cleared after each merge, so field patches have nothing to apply to. Only use this extra layer when it serves the world.

**Conditional instruction content.** Use a native block-modification effect to add/replace/clear instructions. The source may be fixed text in the effect or text prepared in a tracker by an earlier script trigger. This can control optional image guidance, pacing, prose detail, character behavior or any relevant block. A script changes tracker values; the native effect changes the instruction block. Keep the block ID stable when disabling content so later re-enabling still targets a real block.

**Player-optional block, with no repeated writes.** The pattern in ../examples/optional-block.json:

1. A player-only text preference has initialValueBasedOnPC player, initialValue On or Off, initialValueChoices [On, Off], autoUpdate false. The player picks it at startup; later changes need the Storyteller-mode tracker editor.
2. A hidden non-AI-updated text tracker (hidden_boring in the example) records which choice has actually been applied. It is a cache, not another player preference.
3. A repeatable enabling trigger requires preference On AND cache not Enabled. It writes the enabled block content, then records Enabled.
4. A repeatable disabling trigger requires preference Off AND cache not Disabled. It writes empty content, or a deliberately chosen simpler fallback, then records Disabled.
5. Enable opening and later execution where needed. Initialize the cache empty so the selected startup choice gets applied. Once synchronized, neither trigger fires until the preference changes.

Clearing content is not deleting the instructionBlocks entry. Use `content: ""` as in ../examples/optional-block.json. If disabling a bundle that also changes authorStyle or specialist rules, restore ALL affected behavior to a coherent fallback. For a Storymaster toggle, define an off configuration that uses ordinary narration and no Storymaster-specific specialist or tracker dependencies. The generic toggle example demonstrates the mechanism; a Storymaster toggle needs that fallback bundle as well.

Player-visible preference trackers may be hidden from the storyteller; the triggers read them deterministically. Describe their effect and potential turn cost to the player. Do not create an AI-updated tracker that changes the player's own choice back.

**More exact mechanics when requested.** Script-owned numbers, independent prerequisite checks, a request-classification tracker or a controlled transaction may be useful for a precise system. They are options for that feature, not default requirements for the world. If used, define who updates each value and avoid competing AI/script ownership of the same data. Freshness stamps are for consuming an AI-generated per-turn request, not for ordinary narrative trackers.

**Time and location: a soft default.** Offer the sample's Time and Location (whereWhen) block unless the premise makes a clock/location header unhelpful. Writing the current place and time each turn helps IW maintain chronology and gives the player a reference. Adapt the geography, calendar and precision to the setting; omit irrelevant levels rather than inventing a country or continent. Put exactly one header at the beginning of outcomeDescription, not a second competing heading. This is guidance for runtime output, not a new JSON root field.

**NPCs, keyword blocks and always-on blocks** are chosen by intended activation; see [Characters.md](Characters.md#keyword-blocks).

## Dynamic content

Native block-modification effects substitute ordinary `<<...>>` templates when the content is installed. For live values, write deferred `<=...=>` references in the installed text, use a separate permanent block, or reinstall content when the relevant values change. A block reinstalled every turn freezes values when its trigger runs, so values set by triggers below it arrive a turn late: order producers above the installer, or use `<=...=>`. See [Runtime.md](Runtime.md#template-interpolation-runtime) for the interpolation table.

**Player-selected layered openings.** Combine independent choices into meaningful variations using ordered text replacements, then install the result as background. This avoids authoring every full combination; keep fragments compatible and add combination-specific handling where needed. See [layered opening](../examples/recipe-layered-opening.json).

**On-demand generation with retained results.** Install a substantial generation brief only when needed, store a compact result, and clear the brief after a matching completed request. Do not clear merely because a turn elapsed. Prefer infrequent event-driven requests; retained tracker context and AI updates can outweigh the omitted instructions. See [on-demand generation](../examples/recipe-on-demand-generation.json).


## Turn-state patterns

Optional patterns; trigger order is execution order.

**Previous-value snapshot.** The last trigger (always true, repeat) copies watched values to script-only trackers: `$prev_lp = $lifepoints`. Triggers above it read this turn's change, such as `$lifepoints < $prev_lp` for a spend. AND a delta with an event condition when the story and the number must agree. Clamps (a maximum loss per turn) also go above the snapshot.

**One-turn AI write window.** To let the AI rewrite a locked tracker once, a trigger switches its automatic updating on (optionally with new update instructions), stamps `$window = $game.turn_number` and tells the AI what to write. A relock trigger ordered above it, on `$window > 0 and $game.turn_number > $window`, switches updating off and zeroes the stamp. The switch applies from the next turn, so the AI writes exactly once, on the turn it receives the instruction. Keep the switch out of triggers with Request Input.

**Periodic AI updates.** Unlock a large, slow-changing tracker on `$game.turn_number % N = k` and relock on `% N = k + 1`; it is rewritten one turn in N.

**Cooldowns.** Stamp the turn in the effect and gate on `$last_x <= 0 or $game.turn_number > $last_x + 3`. A very large stamp disables the trigger for good.

**Per-turn verdict tag.** An AI-updated text tracker asks for tags judging only this turn, or None. Text-contains conditions react to each tag, and a last trigger resets it to None (copy it first to keep a record). Tags stay turn-specific; the classification is still the AI's judgement.

**Wait for a well-formed write.** Gate a follow-up on the shape of an AI-written value (contains `(`, no longer contains the placeholder), not mere change, so a malformed write just waits.

**Per-model text.** `$game.ai_model` returns the display name (`Dolphin`, `Smilodon`) and text `=` is case-sensitive. Templates in a tracker's own update instructions are evaluated live, so `<<if($game.ai_model = "Dolphin", "…", "…")>>` there selects per model. Blocks can use selectedAIProfiles instead.

**Start-up codes.** A player-only text tracker at character select holds typed codes; one one-shot Text-contains trigger (case-insensitive) per code applies each. List the codes in charSelectText.

**Ordinal words.** `choose($e.intensity.lower(), "slight", 1, "mild", 2, "moderate", 3, 0) < 3` compares a word scale, for example to raise an entry to a minimum without lowering it.

## Request and commit example

In [recipe-request-commit.json](../examples/recipe-request-commit.json), the AI records the current requested event and turn stamp. The first trigger resets the receipt, not the unconsumed request. A later trigger checks freshness, then checks funds/ownership and commits a purchase or rejection. A following effect displays the receipt and clears the request; the receipt remains for next-turn continuity. Narration describes an attempt until the committed result is available. A freshness stamp prevents stale reuse, not incorrect classification. This pattern is optional: native choices, thresholds and timed effects do not need an AI request layer.

The [example index](../examples/index.json) records each complete world's purpose and verification scope. [Payloads.md](../examples/Payloads.md) supplies smaller native shapes. Remap IDs when combining worlds and validate the result. Select examples by feature rather than imposing the showcase's architecture on every world.

## Guarded state patterns

These optional complete worlds compose known primitives. Do not replace a world's design with them automatically.

| Example | Intent and boundary |
| --- | --- |
| [Completion and award](../examples/recipe-completion-award.json) | Set Award state's ready field to 1 through an authored action. Commit the score and completed flag together; trigger firing alone is not successful completion. |
| [Candidate acceptance](../examples/recipe-candidate-acceptance.json) | Keep candidate and accepted records separate. Set submitted to 1 to request acceptance. Checks identity, required field existence and quantity bounds before locking. This is a small semantic gate, not a general YAML type validator; coercion remains possible. |
| [Archive and restore](../examples/recipe-archive-reactivate.json) | Set Active record's request to archive or restore. Copy selected fields explicitly and consume the request. This preserves the record while marking it inactive; whether an archived record still reaches the AI depends on the tracker's visibility. |
| [Cached random](../examples/recipe-cached-random.json) | One trigger samples once and both blocks read the stored roll. Before that trigger runs the initial value is 0; reset ready to 0 only when a new draw is intended. The roll is available to narration from the next generation. |
| [Consumed milestone](../examples/recipe-consumed-timer.json) | Increment turn time before checking ticks >= 3; consume the crossing once. This counts ordinary eligible trigger cycles, not elapsed story time. Resetting only the consumed flag permits another award. |
| [Choice domain](../examples/recipe-choice-domain.json) | Accept only Courier or Archivist at consumption. Blank offers the form again; unexpected manual/script values do not commit. Multiple selections need their own delimiter/representation validation. |
| [Compiled plot](../examples/recipe-compiled-plot.json) | Literal Scenarios with ordered prerequisites and guarded awards. See the plot compiler in [tools/Usage.md](../tools/Usage.md#plot-compiler). |

The validator's review advisories (repeat accumulation, script transaction boundaries, choice domains, multiple-choice storage, independent random expressions) are prompts to inspect intent, and an existing guard can trip one; see [tools/Usage.md](../tools/Usage.md). Choice menus and Enforce format do not validate all manual/script write paths.

---

END OF DOCUMENT: reference/Recipes.md
