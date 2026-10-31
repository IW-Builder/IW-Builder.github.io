# Skills, player characters, NPC cards and keyword blocks

The structured character data IW works from: Skills and the Evaluation that uses them, player-character entries, Other Character cards and keyword lore. How to write the prose inside these fields is in [Craft.md](Craft.md).

## Skills and player characters

Root `skills` is a list of display names. Each possibleCharacters entry has a `skills` object keyed by those names, with integer levels from 0 through 5. Define focused skills with distinct jobs (Observation, Persuasion, Engineering); the AI selects the available skill whose name best matches the attempted action, so overlapping names make that choice ambiguous. A neutral generic skill is appropriate when the story does not need skill distinctions. PC `description` establishes identity, abilities and context for the storyteller, not only the selection page. `charSelectText` introduces the available choices to the player. The allowChangeCharacter* flags control which parts players may customize ([Editor-UI.md](Editor-UI.md#permissions-and-specialist-destinations)).

Keep at least one skill. For generated JSON, use `hideSkillSystem: false` when Skills should be visible; an unchecked editor option omits the field, which is the normal visible-skills state. `hideSkillSystem` hides the skill system's presentation only.

PawScript exposes `$player.skills`, `$player.skills_and_levels`, `$game.skill_map`, `$game.skill_list`, `$game.skill_example`, `$game.difficulty_list` and `$game.difficulty_example`. The skill map connects runtime slugs to display names; read it rather than deriving slugs from names. The difficulty names are Trivial, Easy, Medium, Hard and Legendary. Skills not raised default to level 3; set every authored PC level explicitly. [PawScript reference](https://infiniteworlds.app/pawscript-reference)

Native `effectChangePCSkill` uses the declared display name. `amount` is an integer magnitude; `increase: true` increases toward `minmax` as an upper cap; false decreases toward it as a lower bound. Each effect caps: two successive triggers increasing a level initially 2 by 2 up to 4, then by 1 up to 4, finish at 4. ../examples/probe-skills.json exercises increases, decreases and boundary cases.

Use the numeric skill values for mechanical checks; generated skill labels and Evaluation descriptions can disagree with them.

## Evaluation

`Default-Evaluation.txt` is the editor's prefilled Evaluation text, verbatim: the baseline IW uses when evaluationRequest is empty and the starting point for a custom one. It asks for a brief assessment, a skill and difficulty, and DENIED, SUCCESS, FAILURE or PARTIAL_SUCCESS. Trivial uncomplicated actions succeed and impossible assertions are denied without further evaluation; otherwise proficiency, difficulty, character history, instructions and common sense inform the judgment. Partial success covers incomplete achievement, failure with a silver lining, or success with drawbacks. There is no numerical success-probability table. The Script Library's Storymaster override defines its own caveat labels; keep it distinct from the baseline.

## NPC cards

NPC field purpose and activation guidance are [DOCUMENTED]; the keyword matching and retention below are [RUNTIME].

| NPC field | Authoring purpose |
| --- | --- |
| id | Stable card identity |
| name | Canonical character name |
| names | Recognition names/aliases; comma-separated in the editor; use distinctive forms |
| one_liner | The Summary: compact identity and role; put essential identity here |
| detail | Fuller personality, motives, history, behavior and relationships |
| appearance | Narrative appearance description |
| location | Short starting location (two words at most), an activation cue; not a movement lock |
| secret_info | Hidden character facts; instructions still govern who knows them |
| img_appearance / img_clothing | Visual identity and clothing for image generation; inspect with the wrench under a character image |
| positionInList | Ordering metadata; preserve existing values; use sequential integers for new lists |

Only Name is required in the NPC editor; storytelling and image information are independent optional sections. The brief summary is the only character information available to the storyteller until the turn after the character or their location is first mentioned; characters can activate by name with no location. Detail retrieval is unreliable even then, and the narrator can invent a substitute that history then repeats, or introduce named NPCs into an opening that says the player is alone. Put facts that must surface in one_liner or always-on text and repeat them in detail; correct a wrong invented detail early by editing the turn. For an opening scene, do not depend on card or keyword activation at all: there is no prior context to activate them, so put essential opening facts in firstInput or always-on instructions and give starting NPCs useful brief summaries without duplicating their entire cards. Mentioning footwear in image fields encourages full-body framing, per editor help.

IW permits a character among both player choices and Other Characters under the same name; the selected player can retrieve information from that entry, while the internal merging is not visible. Unchosen player options are not NPCs unless also added as Other Characters. Author the intended relationship explicitly where it matters. PC/NPC conversion is available in Data mode: preserve the source and map relevant fields into the destination type ([Portable-Banks.md](Portable-Banks.md)).

World Debug does not show NPC activation or static character context. Secret fields are a convention the instructions enforce, not a barrier: see the knowledge findings in [Notable-Findings.md](Notable-Findings.md#characters-knowledge-and-memory).

## Keyword blocks

Keyword entries have id, name, keywords (string array) and content. They load through mention matching in recent context, rather than location checks. Matching is case-insensitive and whole-word: quartzbadger and QUARTZBADGER match; prequartzbadgerpost does not, and neither does a simple plural. Surrounding punctuation and authored alternate keywords match. A match keeps the block active on the matching turn and three more: a turn-3 match is active on turn 6 and inactive on turn 7 unless matched again. Player actions, completed narration and Secret Info all contribute to matching, from the next generated turn. The complete tokenizer, multiword behavior and full set of scanned fields are not characterized; there are no matching operators or regex syntax.

Choose distinct phrases and relevant aliases; broad terms such as "man" activate irrelevant lore. A short persistent rule can be always-on while its detailed lore stays keyword-triggered. Choose NPC cards, keyword blocks and always-on blocks by intended activation: make locations or characters dynamically loaded only where the world benefits, and remember that native character and image bookkeeping can matter even when the narrative could be described in an ordinary block.

---

END OF DOCUMENT: reference/Characters.md
