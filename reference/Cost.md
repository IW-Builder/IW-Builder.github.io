# Estimating cost

How much a turn costs, how it differs by Storyteller model, why two players of the same world can pay very different amounts, and how to make a rough estimate before anyone plays. Credit activity shows the real bill: see [Editor-UI](Editor-UI.md#credits-and-cost) for the cost breakdown and the [IW Cost Exporter](https://iw-builder.github.io/cost/) to download your history.

## What a turn is made of

Each turn is billed in two halves. **Input** is everything IW sends the model: its own prompt, the world's standing text, recent story and summaries. **Output** is what the model writes: the narration, Secret Info, evaluation, tracker updates and, on thinking models, its thinking.

**Standing text** is the part the world author controls. It is billed on every turn it is present, at roughly the same rate per character for each model (K in the table below):

- main instructions, authorStyle and every always-on instruction block, plus any block a trigger has installed;
- AI-visible tracker definitions (name, description, update instructions, format), from turn 1, whether or not the AI updates that tracker [RUNTIME, Dolphin: about 1.7 credits per 1k characters];
- AI-visible tracker values;
- lore entries and NPC cards while they are active (assumed to bill at about the instructions rate; not measured directly).

These cost nothing per turn: hidden (script-only) trackers, triggers and PawScript, and Request Input form text after it has been shown. A long descriptionRequest or evaluationRequest is not billed in full either [RUNTIME: 16k characters added about 3–4 credits a turn]; what it really costs is the narration it causes.

**Narration** is billed as output on the turn it is written, then again as recent story (input) on later turns until IW compresses it into a summary. It is the part players are paying for, so it is not a sensible place to save: a world that cut its narration by about 80% saved only about 10% a turn. Overhead (standing text, extra turns, unused lore) is where savings come from.

## Per-model costs

| Model | Small world, per turn | With 10k more instructions | × Dolphin | K: credits per 1k chars of instructions | Narration, words per turn | Credits per 100 words of narration | Thinking, credits per turn |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lynx | 33 | 47 | 0.66 | 0.99 | 406 | 2.2 | – |
| Caracal | 35 | 49 | 0.70 | 1.08 | 346 | 1.0 | 11 (8–14) |
| Lynx-thinking | 40 | 58 | 0.80 | 0.93 | 420 | 2.3 | 10 (9–11) |
| Puma | 41 | 58 | 0.82 | 1.42 | 303 | 3.0 | – |
| Grimalkin | 48 | 72 | 1.0 | 1.75 | 325 | 3.4 | – |
| **Dolphin** | **49** | **72** | **1.0** | **1.58** | **515** | **2.2** | – |
| Smilodon | 70 | 104 | 1.45 | 1.99 | 435 | 5.4 | – |
| Smilodon-thinking | 74 | 105 | 1.5 | 1.81 | 347 | 5.5 | 14 (13–15) |
| Wampus | 75 | 94 | 1.3–1.5 | 1.75 | 344 | 1.9 | 32 (19–39) |
| Leopard | 98 | 104 | 1.5–2.0 | 1.22 | 334 | 4.8 | 42 (31–49) |
| Massivecat | 114 | 167 | 2.3 | 2.77 | 540 | 8.2 | – |
| Massivecat-thinking | 136 | 196 | 2.75 | 2.78 | 515 | 9.1 | 21 (14–35) |
| Leopard-2 | 187 | 195 | 2.7–3.8 | 1.95 | 443 | 7.0 | 92 (65–107) |

Columns:

- **Small world, per turn:** turn 2 of a tiny world (1.2k characters of instructions, no trackers, lore, NPCs or blocks). This is about the least a turn costs on that model after the opening.
- **With 10k more instructions:** the same world on turns 3–4, after 10k characters of plain text were added to the main instructions.
- **× Dolphin:** each model's cost relative to Dolphin. Where two numbers are given, the first is for the larger world: thinking costs about the same whatever the world's size, so those models' lead narrows as the world grows.
- **K:** the extra credits a turn for each 1,000 characters of standing text. Thinking variants bill instructions like their base model.
- **Narration, words per turn:** how much each model writes when nothing in the world asks for a length. A world that sets a length changes this.
- **Credits per 100 words of narration:** the output cost of the narration alone, on the turn it is written.
- **Thinking:** the model's thinking output, mean and range per turn. It varies a lot from turn to turn and is most of the cost on Leopard-2 (about two-thirds) and Leopard.

Turns took about 35–70 seconds on the models that were timed (Dolphin, Massivecat, Massivecat-thinking, Leopard, Leopard-2). Caracal took 5–8 minutes a turn. Wampus and Leopard-2 are under "Show niche models" in the model picker. Wildcat and the experimental Smilodon-2 models were not measured. For the model behind each name and the picker's typical range, see [Current-AI-Profiles.json](Current-AI-Profiles.json).

### Where these numbers come from

[RUNTIME] One small sample world per model, one game each, played on 2026-10-30 with the same four fixed inputs. The averages come from **three turns** per model (turns 2–4; the opening is left out), and K rests on two of those turns. So treat every figure as a rough guide, not a price list: a second game, another world or another day could move a model's numbers by tens of percent, and thinking costs could move more.

Two checks agree with it. Dolphin's and Massivecat's K match earlier separate measurements (1.6 and 2.7). On a long adventure world measured over 14 turns per model, Puma cost 0.85×, Smilodon 1.5× and Massivecat 2.0× Dolphin, close to the ratios above.

## Why the same world costs different players different amounts

The world sets the starting point; the player decides most of the rest.

- **How many turns they take.** This matters most, because a game's total is turns × cost per turn. A player who talks through every scene, explores side paths or makes small moves may take several times as many turns as one who pushes the story along. One long adventure world took about 125 turns to finish, at about 100 credits a turn on Dolphin.
- **Where they go and who they talk about.** Lore entries and NPC cards load when their keywords appear in the story and stay active for a few turns, so a player in a lore-heavy city or a crowded court pays more per turn than one on an empty road. On one large world, active lore cost 17–29 credits a turn on Dolphin.
- **Which route or phase they reach.** Worlds that install blocks or show trackers for a route make that route cost more or less than others. Story luck can change the route: in two otherwise identical games, one player was captured a turn earlier and moved to a different route.
- **How long the game has run.** Recent story is re-sent every turn, so turns get dearer as the game goes on, until IW compresses older story into a summary (from about turn 8, then every six turns). After that the cost levels off. A small world can double between its first turns and turn 8 or 9; a large one rises less in proportion (about 30% over its first six turns on one 50k-character world).
- **How much the narration runs.** The same model on the same world wrote 451 to 638 words a turn. Big scenes, dialogue-heavy turns and players who ask for detail produce longer replies, which cost more now and again in recent story later.
- **Which model they pick.** Players can switch model mid-game. The table above is the biggest single multiplier.
- **Free turns.** IW gives 3 free turns a day, shared across the whole account rather than per world or per model.

## Rough estimates

### Per turn

1. **Start from the model's small-world turn** in the table.
2. **Add standing text:** K × the thousands of characters of standing text the world sends each turn (instructions, authorStyle, always-on blocks, AI-visible tracker definitions and values, typical active lore). Subtract about 1k for the text the small world already had.
3. **Allow for memory:** add about 30% for a large world, and up to double for a small one, once the game is 6–8 turns in.
4. **Adjust for narration** if the world asks for much more or less than the model's natural length: (words asked − words in the table) ÷ 100 × the narration rate. This is the smallest of the four.

Example (an estimate, not a measurement): a world with 18k characters of standing text, played on Smilodon. 70 + 1.99 × 17 ≈ 104 credits a turn early on, about 115–140 once memory builds up, so about 4,500–5,500 credits for a 40-turn game.

### Broad situations on Dolphin

Multiply by the × Dolphin column for another model. For a heavy world on a thinking model, use the first (smaller) multiplier.

| Situation | Standing text per turn | Dolphin, per turn | Basis |
| --- | --- | --- | --- |
| Small, simple world | under 5k characters | about 40–75 | Measured: 49 on turn 2 of the sample world, rising with memory |
| Mid-sized world | 10–25k characters | about 65–120 | Estimate from the method above |
| Large world with plenty of lore | about 50k characters, plus 15–30 credits of active lore | about 150–210 | Measured on one community world: 152 on turn 1, about 200 a turn by turns 4–6 |
| Long campaign | about 33k characters | about 100 average | Measured on one long adventure world: about 13,000 credits for a full game of about 125 turns, about twice that on Massivecat |

For a whole game, multiply the per-turn estimate by the number of turns you expect, and give a range: players' turn counts vary more than the per-turn cost does.

### Checking an estimate

Play a few turns, then open Credit activity and read the breakdown. If a bucket is far above your estimate, it points to the cause: Instructions for always-on text, Tracked Items for tracker definitions, keyword blocks for lore that is loading more often than intended (an entry keyed on a common word loads almost every turn). On one large world, trimming those three cut the cost of a turn by about 20% without changing the narration: instructions fell 38%, lore 70% and tracker definitions 28%.

See [Trackers](Trackers.md#memory-continuity-and-context-cost) for keeping tracker text lean, and [library/Integration.md](../library/Integration.md) for the size of each library module.

---

END OF DOCUMENT: reference/Cost.md
