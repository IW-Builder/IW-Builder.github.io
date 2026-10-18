# Narrative craft

## Opening and cast

A strong opening gives the player an immediate, legible situation rather than an encyclopedia. Put deep backstory in relevant cards/lore, keep firstInput actionable, and let early choices expose the setting. Define what is interesting about success, failure and doing nothing. Distinct NPC motives create better choices than merely different appearances. For a mystery, track who knows each clue; for a social story, give relationships room to change; for a simulation, make recurring decisions and their consequences legible.

Write a few observable voice cues rather than labels alone: an impatient engineer interrupts with practical questions; a guarded diplomat answers indirectly. Describe setting-specific deviations from common knowledge, not every ordinary object. Keep instructions consistent with examples. Test the first turn as carefully as the machinery: does it introduce the right player, place, people and viable options without prematurely resolving the premise?

For an existing world, preserve IDs and unrelated fields, report intended changes, validate the complete output and test the affected behavior. A live copy and its base world are separate. Compare active blocks, Evaluation, trigger counts, PawScript errors and tracker values for the same turn when diagnosing a discrepancy. A rendered story alone cannot identify which stage failed.


## Distinct characters
Give each recurring NPC a want, a voice, a point of friction and at least one physical or behavioral distinction. A voice is more useful than a stock adjective: one person corrects estimates before discussing feelings, another answers concern with an offer of food. Put essential opening facts in firstInput or an always-on block, with concise NPC summaries. Reveal secrets through opportunities rather than an opening exposition dump.

## Naming preference

Offer this soft default during initial design unless a preference is already supplied. If accepted, apply it while authoring and install a separate Naming instruction block for characters introduced during play:

> Wherever creating any name, first or last, create five valid possible choices. Eliminate the four most common and choose the fifth. Keep choices appropriate to the setting and naming culture. Preserve established and user-supplied names. Output only the selected name.

"Most common" is a model judgment, not a measured ranking. Adapt or omit the technique at the user's request. It applies to fictional names, not tracker variables, IDs or schema fields. A shared PC/NPC identity keeps the same canonical name.

## Content agreements and substitutions

Preserve requested tone, relationships and mature themes within the authoring model's content limits. Identify specific portions that cannot be provided and discuss acceptable alternatives; continue unaffected work. Never quietly remove, sanitize or weaken permitted content to avoid the discussion. Do not change mature/nsfw settings or unrelated content as an incidental side effect.

When proceeding with a substitution, preserve its narrative and mechanical role where feasible. Otherwise disclose the behavioral difference. Use unique searchable references, with playable replacement text outside IW comments:

```text
<#REPLACE01#>
Jane invites the player to a private conversation. Completing it advances the relationship milestone.
<#END_REPLACE01#>
```

Comments mark the span but do not carry its playable instructions. Use markers in AI-facing prose, not inside script syntax, IDs, variable names or numeric fields. For substitutions to such fields, record exact paths in the separate report instead. Preserve valid native types and references. Do not embed prohibited content or instructions to reconstruct it in markers; a replacement is an allowed alternative, not a hidden completion request.

Deliver a separate Authoring report with: reference; brief non-graphic description of the affected request; implemented replacement; object ID and JSON path; any mechanical difference. Keep that discussion outside the world. Preserve markers across edits unless the corresponding substitution is deliberately resolved or changed.

Before delivery, compare the world to the agreed brief and substitution register. Check tone, character roles, relationships, prerequisites, rewards, objectives and endings; flag unintended differences and preserve unrelated content. Every REPLACE marker needs a report entry, and every reported substitution needs an identifiable location. Markers are review notices, not import errors. Do not claim that a substitute exactly fulfills the original request when it does not.

## Player-facing opportunities
Give a concrete immediate problem with several reasonable approaches. Describe what the player can notice; reserve hidden facts for discovery. Allow ordinary social and exploratory actions without demanding a mechanical event for everything. Use failure and partial success to change the situation without erasing agency. A bounded ending needs clear accomplishment criteria; an ongoing world needs recurring tensions and evolving relationships.

See ../examples/narrative-last-ferry.json for a narrative-first world with a focused opening, distinct voices, optional lore and bounded AI memory. It is an authoring example, not a runtime-qualified benchmark.
