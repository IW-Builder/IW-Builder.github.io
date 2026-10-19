# Adapting the sample library

`Sample-Blocks.json` is adapted from the unaffiliated [The Script Library](https://infiniteworlds.app/shared/Dxb2ko), world code Dxb2ko. The packaged modules include Time and Location (whereWhen). The source snapshot is identified in ../reference/Evidence.md. The shared world includes additional image-style, content and character blocks and is frequently updated; check whether desired blocks have newer versions before adopting them. It is a collection of reusable instructions, tracker alternatives, examples and updater scripts, not an instruction to copy its entire world into every new story. Use this guide as the dependency reference when selecting modules.

## Feature selection

| Component | Offer when useful | Check before inclusion |
| --- | --- | --- |
| Time and Location (whereWhen) | Soft default for chronology and player reference | Adapt geography/calendar; use one header; account for scene durations |
| Characterization | Character knowledge, voice and agency matter | Adapt universal statements to the requested premise; distinguish player from character knowledge |
| Narrative Craft | Distinct prose and character behavior are desired | Match length/intensity/register; fill or remove non-human feature customization comments |
| Pacing | The user wants more deliberate scene movement | Resolve its Sexual Content reference if that module is omitted; keep appropriate player agency |
| Period Knowledge | Historical/period knowledge limits matter | Fill era and culture; adapt assumptions about travel and wider-world knowledge |
| SecretInfo + Storymaster | Always discuss for a new world unless a preference is already stated; popular, substantial framework, not automatic inclusion | Include/adapt main instructions, authorStyle, specialist requests, reader_profile and story_metadata references |
| Appearance trackers | Visual/wardrobe continuity or images matter | Choose small/large cast or direct/buffered updates; align target variable names |
| Relationship Tracker/Update | Recurring social connections matter | Match identity/aliases, choose complete-record versus patch semantics |
| Reader Profile | Delivery should adapt to demonstrated reader preferences | Meta-player preferences are distinct from PC traits; do not fabricate real personal biography |
| Story Metadata | A stable story identity benefits planning | Populate the current user's genres, core appeal, themes and audience |
| Intimacy Log/Update, Sexual Content | Applicable requested adult/relationship content | Apply to erotic/NSFW worlds; do not modify or sanitize; inform user if beyond content guidelines |
| Model-named bugfixes | The relevant model/behavior is actually targeted | These are user-authored workarounds, not universal official defaults |
| Cover Image script | Preparing the game's cover prompt | Run/adapt as an authoring step; replace title/blurb and keep style separate |

Discuss Storymaster's benefits, supporting instructions and approximate costs before selection. whereWhen remains a soft default; other modules are offered according to the brief. Removing an unused module from one world does not remove it from a personal library. Library maintenance and dependency-aware bundles use Data mode; see [Portable-Banks.md](../reference/Portable-Banks.md).

## Approximate instruction costs

These are source-text reference estimates: decoded characters divided by four, rounded upward to ten tokens. Tokenizers, native comment handling and customization change the result; punctuation-heavy text may differ substantially. Figures exclude dynamic tracker contents, generated planning/output and platform instructions. IW credit costs need not vary directly with tokens. Share the relevant estimates and this caveat when offering modules.

| Instruction block | Approximate tokens |
| --- | ---: |
| Characterization | 250 |
| Pacing | 160 |
| Sexual Content | 260 |
| Period Knowledge | 210 |
| SecretInfo + Storymaster | 1,640 |
| Narrative Craft | 790 |
| Leopard Bugfixes | 140 |
| Caracal Bugfixes | 380 |
| Dolphin Bugfixes | 260 |
| Cover Image script | 480 |
| Time and Location (whereWhen) | 250 |

The Cover Image script is an authoring aid, not a default recurring story block. The Storymaster block alone is not the cost of its configuration. Supporting fields below can enter different requests; do not add them up and advertise a guaranteed per-turn cost. Trackers can also grow and planning adds generated tokens.

| Supporting text | Approximate tokens |
| --- | ---: |
| instructions | 330 |
| authorStyle | 10 |
| evaluationRequest | 2,180 |
| descriptionRequest | 290 |
| summaryRequest | 790 |

Tracker estimates below cover updateInstructions only; descriptions, schemas, state values and update output are additional. Small/large-cast variants and direct/buffered approaches are alternatives, not one required combined configuration.

| Tracker update instructions | Approximate tokens |
| --- | ---: |
| Player Appearance | 390 |
| NPC Appearance small cast | 440 |
| NPC Appearance (large cast) | 460 |
| NPC Appearance Update | 40 |
| Relationship Tracker | 320 |
| Relationship Update | 260 |
| Intimacy Log | 290 |
| Intimacy Update | 250 |
| Reader Profile | 240 |
| Story Metadata | 180 |

## Storymaster variable content

Populate Genres, Core Appeals of Genres, Appeals of this Specific Narrative, Element of Novelty, Tone, Themes, Conflicts and Pacing. Pacing includes ongoing versus bounded length and appropriate scene estimates. These are creative inputs; derive them from the user description or ask targeted questions. The pacing line can include specialized scenes only when relevant.

The source's `[npcAction]`, `[worldAction]`, `[smPlan]` and other output labels are intentional runtime notation. They are not the same as `[LIST GENRES]`, `[DESCRIBE TONE]`, `[Author Style]` or `[title]` editing slots. Resolve nested pacing brackets thoughtfully instead of deleting everything between square brackets.

`<#...#>` are native IW comment delimiters. Resolve sample editing slots into world-specific text or ordinary headings; genuine comments may remain. Execute instructions such as selecting an appearance variant and copying its instructions to the buffer tracker; do not leave those comments for the live storyteller to interpret.

If Storymaster is not selected, rewrite or replace all dependent main/style/specialist text. Do not leave instructions to consult an absent director, tracker, mode or secretInfo section. If it is player-optional, its off configuration needs a consistent fallback for the whole selected family, not just one blank block.

## Structured updater dependencies

The source offers both small- and large-cast appearance trackers. Its appearance merge script targets `$npc_appearance`, which is not automatically the variableName of either variant. Normalize the chosen store's variableName or rewrite all references. The large-cast updater depends on Relationship Tracker significance.

The relationship/intimacy buffers and stores demonstrate an AI-proposed update followed by a script merge. The supplied scripts replace matching records; that is not automatically a field-level patch. Ensure the update contains the required full entry, or deliberately implement a field-preserving merge. This is an integration choice, not a new requirement for every world.

Initial blank list-like trackers in the library are source examples. Where a chosen script requires an actual list, initialize `[]` or ensure the first-use initialization is correct; do not assume blank text and an empty YAML list are interchangeable. The schema checks field storage type but not the nested runtime reference or merge algorithm.

## Optional block recipe

The optional-block recipe is `../examples/optional-block.json`: a player-only On/Off preference, a hidden applied-state cache, and repeatable On/Off triggers. Enabling writes instructions and marks Enabled; disabling clears content and marks Disabled. No trigger runs again while the cached state matches the preference.

An optional cosmetic block can clear its content when disabled. A director such as Storymaster needs fallback instructions and authorStyle appropriate to the disabled state. Choose the behavior required by the selected module. Retain block IDs rather than deleting target entries.

## Module configuration

The library is a menu of adaptable parts, not the cookbook's runnable showcase. Its updater triggers explicitly use Start false, Mid false and repeat true, so these conditional update jobs run in ordinary play rather than being assumed to perform initial setup. Their scripts have descriptive names.

The image-style fields contain selectable alternatives and genre-specific defaults. Resolve all editing brackets, keep only compatible choices, and remove sexualized styling unless requested. The video template depends on video-context variables; see ../reference/Capabilities.md before adopting it. These are intentional adaptation dependencies, not finished-world settings.

Storymaster as a player toggle is an advanced bundle. A simpler off state must replace its dependent main/style/specialist rules, not merely hide the Storymaster block. For example, ordinary narration can use the premise, current facts, character motivations and player input directly, with summary instructions that preserve facts instead of referring to smPlan. Since there are no characterized native change effects for every specialist field, prefer a static coherent conditional instruction design or an always-compatible specialist override; do not invent effects to switch those fields.


## Storymaster dependency checklist


The sample's root instructions, authorStyle ("Written by Storymaster"), Evaluation, Description and Summarization are written around its author/director vocabulary. Evaluation refers to npcAction, worldAction, smPlan, genres/core appeals, reader_profile and story_metadata. Summary refers to particular secretInfo sections. Some craft blocks use Simulation Engine/Narrative Author mode labels or cross-reference other blocks.

If using that family, include or consistently adapt the required blocks/trackers and vocabulary. If omitting it, rewrite or replace those specialist/main/style instructions and any dependent references; do not leave an absent Storymaster, nonexistent tracker or unprovided secretInfo section in the world. It is a library framework, not a built-in IW agent or API. Do not promise its role separation is hard isolation enforced by IW.

When using the Storymaster VARIABLE BLOCK, supply ALL of:

- Genres.
- Core appeals of those genres.
- Appeals of this particular narrative.
- Element of novelty.
- Tone.
- Themes.
- Conflicts.
- Pacing: intended overall length or ongoing format, major/minor scene estimates, and any relevant specialized scene estimates. For an ongoing story, state that plainly rather than inventing a fixed total.

Obtain these from the description or ask targeted creative questions where needed. Keep them coherent with authorStyle, story_metadata and any reader-profile instructions. Do not remove the variable section merely because it contains placeholders.
For template substitution timing, see ../reference/Capabilities.md. For generic optional-block composition, see ../reference/Recipes.md.
