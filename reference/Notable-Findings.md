# Notable findings

The Infinite Worlds behavior most likely to surprise an author or break a world, in plain language. Each entry says what happens and what to do. Details and evidence labels are in [Verified behavior](Verified-Behavior.md); open questions are in [Known limits](Known-Limits.md). Use this page as a checklist when reviewing or debugging a world.

## Triggers

1. **A trigger with no conditions never fires on its own.** It is a saved trigger for Fire random trigger, not an "always" trigger. Start-of-game triggers are the exception: they fire at startup. With Start on, the editor drops its "so it will never fire" warning even when Mid-game and Repeat are also on, but firing on later turns is not established. For an every-turn trigger, add an always-true condition such as `$game.turn_number >= 0`.
2. **Repeat means every eligible turn.** "HP below 5" with Allow triggering multiple times fires every turn HP stays low. Add a state guard for one-time effects.
3. **Start + Mid-game + Repeat runs twice before the player acts:** once before the opening and again on turn 1. Guard counters and rewards.
4. **Give information to AI does nothing on a Start-enabled trigger**, even on its later mid-game activations. Use background, an instruction block or a separate ordinary trigger.
5. **Effects available depend on Start mode.** Background, first-action and Other Character changes are Start-only; Fire random trigger does not dispatch with Start on.
6. **"Fired" does not mean "succeeded".** A script that errors rolls back only its own writes, but its trigger still counts as fired, uses up a one-shot and satisfies prerequisites. Set a completion flag inside the script that does the work.
7. **Order in the trigger list is execution order.** Later triggers see earlier writes; a this-turn prerequisite only sees producers above it. Reversing two triggers can delay an effect by a turn.
8. **Two native number changes to one tracker in one trigger overwrite each other.** Add 2 then add 3 ends at 3. Use one script for dependent arithmetic.
9. **Fire random trigger skips the target's conditions** but will not rerun a one-shot that already fired. Put required checks inside the target's effects.
10. **Thresholds need inequalities.** A countdown that jumps from 1 to -2 never equals 0. Use `<=`/`>=` and consume each crossing once.
11. **Effects run after the narration is written.** A trigger cannot change the scene that caused it. If a rule must shape that scene, put it in active instructions beforehand.
12. **When two guidance effects conflict, the first tends to win.** Generate one coherent outcome instead of competing directives.

## Scenarios

13. **Scenario text must match the registry exactly**: case, spaces and punctuation. A mismatch keeps the text in JSON but the selector shows "Select a situation" and the trigger never fires.
14. **A Scenario fires only when the event really happens in the narration.** The narrator can refuse or alter a requested action.
15. **Dynamic Scenario text (`<<$slot>>`) is unreliable** beyond a single slot: multi-slot, cyclic and parallel setups silently fail. Use literal Scenarios plus state conditions.
16. **The editor's ten-Scenario limit is an editor limit.** Imported worlds with twelve or more work.

## Import and editing

17. **Tracker IDs with punctuation, spaces or accents are replaced on import, and triggers still point at the old ID.** Use letters and digits only for tracker IDs.
18. **Some missing fields break things silently.** A condition without `textComparison` is dropped. A value effect without `replaceWith` was linked to the game failing at the opening. A tracker without `description` makes the editor rebuild fail after a "success" message.
19. **Legacy array-style prerequisites and blank script conditions are dropped on import.** The trigger loses that gate, or never fires if it was the only one.
20. **Import is saved immediately**, even if you later click Discard changes. Keep a backup. Wait for the editor to rebuild before refreshing the raw JSON.
21. **A running game is a separate copy.** Editing the world, its starting values or its characters does not change a game in progress. Edit current tracker values in Storyteller mode, or start a new game.
22. **Renaming a tracker's display Name with Ignore keeps its script handle.** Scripts keep working.

## Trackers and PawScript

23. **Hidden and extra-hidden trackers are not secret.** The storyteller and any Storyteller-mode player can see them; extra-hidden only filters one display.
24. **Hidden and player-only trackers cannot auto-update.** Import turns automatic updating off for them.
25. **Enforce format does not reject bad data** written by scripts or by hand. Validate shape and values in scripts before accepting them.
26. **Random expressions disagree with each other.** Two `random()` calls, even in one block, give different results. Store one roll in a tracker when several things must agree.
27. **Text installed by a block effect freezes its values.** Use a deferred `<=...=>` reference to keep a value live; `<<=...=>>` is inert text, although the editor highlights it as code and shows `<=...=>` as plain text. Saving the tracker editor by hand freezes any tracker holding `<<...>>` at its displayed value.
28. **An unclosed `<<` can break the next instruction block too.** Check delimiters across neighboring blocks.
29. **YAML types are loose.** `yes`/`no` are text, `"007"` counts as 7 in arithmetic, Boolean results are stored as quoted text, and appending to a list allows duplicates.
30. **Reading a missing path stops a script.** Guard with `.exists()` first (`and`/`or` short-circuit), or use `try(...)`, `first_available(...)` or `item(key, fallback)`.
31. **Script variables (`set $x`) vanish between Run Script effects** in the same trigger. Keep dependent work in one script.
32. **Skill effects cap rather than add.** Raising a skill by 2 then by 1, each capped at 4, ends at 4. Skills not raised default to level 3; set every level explicitly.
33. **The sandbox opened from a single-line field is a one-line expression box.** A multi-line paste there is refused and does nothing; its Text tab gives a multi-line box for `<<expression>>` text. To test a multi-line script, open the sandbox from the Paw icon beside a Run Script field, which the world editor always shows. Nothing changed in the sandbox goes back to the editor or game.

## Characters, knowledge and memory

34. **Only the Summary is guaranteed early.** Character detail arrives after a name or location mention, and even then often fails to surface; the narrator invents a substitute that history then repeats. Put must-know facts in the Summary or always-on text and repeat them in detail.
35. **Keyword and character cards cannot activate on the opening turn** without prior context. Put opening facts in firstInput or always-on instructions.
36. **Keyword blocks match whole words, any case, and stay active for the matching turn plus three.** Substrings and plurals do not match.
37. **NPCs get knowledge wrong.** They deny facts they were just told, credit the wrong source, or know secrets they should not. Secret Info can contradict the narration. Anti-omniscience instructions alone do not fix this.
38. **Once a secret is narrated it stays in the story**, even if you remove the block that revealed it.
39. **Memory summaries start at turn 8 and repeat every six turns.** Their contents are hidden. Keep facts that must persist in trackers.
40. **A player character with the same name as an Other Character can draw on that card.** Unchosen player options are not NPCs unless added as Other Characters.

## Narration, images and play

41. **Shorten narration from authorStyle, not descriptionRequest.** A word-and-paragraph cap at the end of authorStyle held output near the stated number (often 10–20% over) even on story-beat turns; the same cap in descriptionRequest or an always-on block broke on those turns. Making narration longer is not established.
42. **Raw HTML renders as literal text.** Use ordinary Markdown.
43. **Short avoid-lists help, long ones backfire** on weaker models by priming the banned phrases.
44. **Image style uses the start/end prompt fields.** The old illustrationStyle priority fields have no current controls and lost to the start/end prompts in testing. Saving Illustration details generates a new image (about 4 credits).
45. **Ends game with continuation allowed offers Continue game at no cost.** Without it, the action box disappears but history and regeneration remain.
46. **Reloading during generation can lose the turn and keep the charge.** Check the export's turn count before resubmitting.
47. **Cost per turn grows with story length** and depends heavily on the model; see [Current-AI-Profiles.json](Current-AI-Profiles.json).
48. **One input form per turn is safest.** A turn with two forms once showed narration without the forms and was not saved. (Two plain Request Input forms from separate triggers on one turn worked in a later probe; the earlier failure combined one with a malformed candidate.)
49. **A tracker-detail change in the same trigger as Request Input is silently lost.** Modify tracked item details (for example switching automatic updating on) does nothing when its trigger also asks for input, while messages and scripts in that trigger still run. Put the change in its own trigger with the same condition. Switching automatic updating on and off otherwise works, from the next turn.
50. **An AI-written buffer whose whole value is a list loses updates.** Root it in a record (`entries: []`) and have scripts read and clear `.entries`. Ask for complete entries of changed characters, not "only changed fields": once the buffer is cleared, a field patch has nothing to apply to.

---

END OF DOCUMENT: reference/Notable-Findings.md
