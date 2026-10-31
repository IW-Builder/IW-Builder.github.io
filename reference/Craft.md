# Narrative craft

The storyteller performs from what the world gives it, and it mirrors the specificity and register of that material. Label-style cards ("kind but guarded") produce generic narration; a card with a concrete want, a sample line and a physical tell produces scenes. Write what the storyteller performs from (NPC cards, firstInput, authorStyle, lore) as specific prose. Write rules (instructions, blocks, tracker updates) as short, plain statements.

When effort is limited, spend it here first, in this order: NPC one_liners; one voice line and one tell per recurring NPC; each NPC's stance toward the player and what changes it; firstInput; authorStyle.

## What goes where

| Field | Job | Avoid |
| --- | --- | --- |
| description | Player-facing hook, one or two sentences | Lore summary |
| background | Facts true at the start: place, situation, household, stakes, adult status | Secrets; a backstory novel |
| instructions | How to run the story: premise in play, agency, who can do what, boundaries, tracker use | Prose style; character essays |
| authorStyle | How prose sounds: POV, tense, sensory focus, length, how turns end, phrases to avoid | Mechanics |
| firstInput | First scene: place and time, who is present and what the player notices about them, the immediate situation, what not to decide | Introducing everyone; resolving the premise |
| objective | Direction | A script |
| NPC one_liner | Everything needed before first mention: name, age, role, one or two visual anchors, behavior, stance toward player | Adjectives only |
| NPC detail | Essentials repeated, then labeled lines: Wants, Voice (with sample line), Tells, Toward you, Friction; for romance also Desire, In intimacy, Afterward | Biography |
| appearance | Body, face, movement, distinguishing marks | Current outfit; verdicts like "beautiful" |
| img_appearance / img_clothing | Short visual tags; default outfit | Personality |
| secret_info | One or two facts that change relationships when revealed | Plot schedule |
| Keyword lore | Optional depth behind distinctive words | Essential opening facts |
| Instruction blocks | Persistent rules: time header, world laws, intimate-scene craft | Duplicated main instructions |
| AI trackers | Bounded memory of what changes: stance, agreements, outfits, promises | Unbounded journals |
| mature / nsfw / contentWarnings | Content settings matching the audience; the template sets both flags true | Treating them as the prose policy: write the boundaries in instructions |

## Opening

A strong opening gives the player an immediate, legible situation rather than an encyclopedia. firstInput names the place and time, who is present and one or two things the player notices about each, the immediate situation, and what the storyteller must not decide. Introduce two or three people at most; let the rest arrive through play. Define what is interesting about success, failure and doing nothing.

For a mystery, track who knows each clue; for a social story, give relationships room to change; for a simulation, make recurring decisions and their consequences legible. Describe setting-specific deviations from common knowledge, not every ordinary object. Test the first turn as carefully as the machinery: does it introduce the right player, place, people and options without resolving the premise?

## Characters

Write `detail` as labeled lines; they are easy for the storyteller to use and hard to leave empty.

- Essentials, repeated from the one_liner. The storyteller may see only the one_liner until the character is first mentioned.
- Wants: something they pursue whether or not the player shows up.
- Voice: rhythm, vocabulary, habits, and one sample line in quotes. One person corrects estimates before discussing feelings; another answers concern with an offer of food.
- Tells: two or three physical behaviors, specific to this character, that reveal state.
- Toward you: starting stance, what raises it, what cools it, how it shows.
- Friction: a relationship with someone else in the cast, so scenes have more than one axis.

`appearance` describes body, face and movement in plain, specific facts: build, height, notable features, how they stand and move. "Broad-hipped, soft stomach, freckled shoulders" gives the storyteller something to use; "beautiful", "curvy" and "perfect" do not. Vary bodies across the cast. Put the default outfit in img_clothing and track current clothing separately if it changes.

Reveal secret_info through opportunity (a late conversation, a mistake, a bargain), never exposition. Minor characters need only a one_liner and a few lines; spend detail where the player will spend time.

## Romance, desire and adult worlds

Apply this section only when the brief includes romance or sexual content.

- Attraction is individual. State each romantic NPC's orientation and what attracts them. Not everyone wants the player, or at the same time, or in the same way; universal instant attraction makes desire meaningless.
- Flirting is not wanting. Some characters flirt with everyone; others never flirt and must be asked. Say which.
- Stance is state. Keep an AI-updated tracker per romantic NPC: a stage from a fixed ladder and a one-sentence concrete cause. Each card describes how that character shows the stages.
- Match the tracker to the premise's heat. A courtship ladder (`wary -> curious -> warm -> drawn -> wanting -> involved`, moving one step per scene) fits slow-burn romance where intimacy is slow earned.
- For erotica-first, kink, or power-exchange worlds, do not time-gate sex: instead track **escalation and dynamic** (for example `heat` from 1 to 5, `control` as `dominant / even / yielding / undone`, active rules/forfeits, and boundaries pushed so far).
- Pace explicit scenes across turns. In high-heat worlds, tell the storyteller never to start and finish a sexual encounter in the same turn: let undressing, foreplay, the act, and the aftermath unfold across turns, and allow explicit scenes to expand in paragraph count so physical detail and position changes are not rushed.
- Gates differ. Vary what each love interest needs: respect earned through competence; easy physical intimacy but slow emotional intimacy; never initiates but answers a plain question honestly; desire that can only be offered, never taken. Different gates make different stories.
- Personality persists. Desire changes a character's tempo, not who they are. Describe how each one is in intimacy (talkative, commanding, giggly, silent, precise) and what they want but will not ask for. Without this, every intimate scene converges on the same generic partner.
- Afterward is a scene. Say how each behaves the morning after and in front of others. Aftermath is where relationships change.
- The cast is a system. NPCs notice each other's interest in the player: jealousy, teasing, rivalry, protectiveness. Give NPCs histories with each other.
- Bodies and clothes stay present: heat, sweat, wet hair, stains, what is worn and its state. An AI wardrobe tracker keeps clothing continuous through scene changes and undressing.
- Consent lives in the fiction. Characters ask, tease, check in, refuse in character, and change their minds through events, never pressure. World rules can make consent part of the drama: a debt that cannot compel the body; a boss who will not while a vote is open. Put boundaries in instructions, not disclaimers in narration.
- No contrived interruptions. Near-misses should come from characters' choices. Tell the storyteller never to interrupt a scene both parties are clearly continuing.
- The player's character is theirs. Never decide their words, feelings or desires; sensations a scene plainly causes are fine. Their body is whatever the player has established. Enable name and description editing when players are expected to bring their own character.
- Content settings. Set mature, nsfw and contentWarnings to match. State in instructions that all characters are adults, and give ages in cards. Put the explicitness level in one clear line of an always-on block, for example "write sex on-page and explicitly when the player continues into it" or "fade out at the bedroom door and resume the next morning". List any hard limits the user requested.

## Weak and strong

one_liner
- Weak: "Captain Reyes commands the ship. She is tough but fair."
- Strong: "Captain Ines Reyes, 41, commands the salvage tug Marrow: shaved head, burn-scarred left hand, gravel voice; rations praise, never coffee; treats you as cargo until you prove otherwise."

Voice
- Weak: "He is witty and flirtatious."
- Strong: "Answers every question with a compliment aimed slightly beside it: 'Directions? For you I'd draw a map on my own back.' When he means something, he stops joking and says it once."

Toward you
- Weak: "She is secretly in love with the player."
- Strong: "Starts wary: you replaced her friend on the crew. Warms when you take night shifts unasked or admit a mistake first; cools if you pull rank. Drawn shows as checking your work twice and pretending she didn't."

appearance
- Weak: "A gorgeous woman with a perfect figure and long flowing hair."
- Strong: "Short and broad-shouldered, heavy-thighed and soft at the belly, with a swimmer's back; cropped bleached hair growing out dark; a gold ring through one eyebrow; a ragged thumbnail she bites while thinking."

In intimacy
- Weak: "Passionate and loving."
- Strong: "Talks throughout, asks what you like and actually listens; gets giggly when nervous and has to stop to laugh; goes silent and fierce only once she trusts you."

secret_info
- Weak: "He has a dark past."
- Strong: "He sold the crew's route to raiders last year and has sent his share, every month since, to the widow of the man who died."

firstInput
- Weak: "You arrive at the station. Introduce the crew and the mystery."
- Strong: "Docking ring C, 03:10 station time. The airlock has cycled twice and still won't open. Reyes is on the comm asking whether I'm armed; through the porthole the mechanic, Teo, a big man in a grease-black vest, pries at the panel and grins at me. Begin with Reyes's question. Show Teo through one detail and one line. Don't explain the derelict or decide my answer."

authorStyle
- Weak: "Immersive, descriptive, emotional."
- Strong: "Second person, present tense. Close, physical prose; one or two specific details per person, never a head-to-toe inventory. Dialogue carries subtext; each character sounds like their card. Three to six paragraphs; end on a line or action that hands the moment to the player."

## Prose and authorStyle

authorStyle describes how sentences sound: POV and tense, sensory focus, scene length, how turns end, how characters stay distinct, and how to describe people (a detail or two at a time, through the player's attention). A style anchor ("closer to Angela Carter than a greeting card") can help. Length rules belong here: a cap in authorStyle outweighs the same text in descriptionRequest.

A short avoid-list counters common AI phrasing: 'a mix of X and Y', 'ministrations', 'barely above a whisper', 'eyes darkening', 'a testament to', 'something shifted'. Keep it short and always say what to do instead; long lists can prime the very phrases they ban in weaker storyteller models.

## Names

Choose names from the setting's language, era and class. Avoid names language models overuse (Elara, Lyra, Seraphina, Aria, Luna, Kael, Thorne, Zephyr, Vex, Chen as a default surname). Give recurring characters different initials and syllable counts so neither the player nor the storyteller confuses them.

## Peoples, expeditions and platonic relationships

Make unfamiliar peoples usable in scenes: connect a physical trait to a practical capability, a limit and ordinary habits of work or care. Distinguish physiology from culture and individual temperament. Include differing people of the same ancestry; do not make one companion represent everyone's values. Offer other ways to solve a problem so an ancestry is not the only key.

For an expedition, establish spatial relationships, available tools and visible risks before asking for action. Let companions contribute expertise, admit uncertainty and disagree for concrete reasons. Friendship, mentorship, care and professional respect need their own motives and consequences; they do not require romantic progression. Support retreat or a partial repair when the situation makes either credible.

## Horror and bounded uncertainty

Separate fixed underlying facts from testimony, interpretation and unresolved meaning. Define what a threat can perceive and affect, and how the player can discover those limits. Escalate only when events enable it; do not grant new powers merely because the player found a sensible solution.

Use corroborating clues, ordinary intervals and independent channels of help. Keep descriptions reliable even when speakers lie or imitate others. A failed investigation should leave another route to essential evidence. Preserve successful containment; uncertainty can survive in the meaning of events without making every practical success false. AI-managed trackers support continuity but do not mechanically enforce these rules.

## Examples

| Example | Shape | Demonstrates |
| --- | --- | --- |
| [The Road That Must Be Asked](../examples/narrative-listening-road.json) | Non-romantic high-fantasy expedition | Distinct peoples with internal variation; platonic teamwork; fixed facts; repair, negotiation and retreat |
| [The Address After Midnight](../examples/narrative-address-after-midnight.json) | Contained contemporary horror | Limited threat capabilities; reliable evidence; conditional escalation; independent verification and valid containment |
| [Vendemmia](../examples/narrative-vendemmia.json) | Contemporary ensemble, three love interests | Different attraction gates; stance ladder with agreements; wardrobe continuity; stakes each NPC experiences differently; sensory keyword lore |
| [Seven Nights](../examples/narrative-seven-nights.json) | Fantasy: central partner, foil, late rival | World-rules block; consent built into the fiction; non-human tells; player-visible promise ledger; minimal card for a minor character |
| [Velvet Wager](../examples/narrative-velvet-wager.json) | High-heat erotica & power-exchange trio | Immediate heat from turn 1; escalation & control tracker instead of courtship gates; multi-turn sex pacing; kinetic body descriptions; light state triggers |

For narrative worlds, read the example closest to the requested genre and relationship structure. Borrow structure, never content: do not reuse example names, premises or signature details. These are authoring patterns; the expedition and horror examples are structurally validated only.

## Existing worlds

Preserve IDs and unrelated fields, report intended changes, validate the complete output and test the affected behavior. A live copy and its base world are separate. When diagnosing a discrepancy, compare active blocks, Evaluation, trigger counts, PawScript errors and tracker values for the same turn; a rendered story alone cannot identify which stage failed.

---

END OF DOCUMENT: reference/Craft.md
