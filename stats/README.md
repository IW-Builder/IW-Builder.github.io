# World stats page

[iw-builder.github.io/stats/](https://iw-builder.github.io/stats/) turns the CSV export from a world's **World Stats** page in Infinite Worlds into charts. Load one file or several (one per world) to compare worlds. The page runs entirely in your browser: files are never uploaded. No build step and no libraries; `index.html` is the whole tool.

What it shows:

- **At a glance:** turns, games, players, credits per turn (weighted by turns across worlds) and a side-by-side table, including the share of players still playing at turns 5, 10, 21, 51 and 100. Worlds with `Stats:` markers also get games reaching Day 1, 3 and 7 (share of Started), the longest game in story time (the furthest `Reached Day`, else `Reached Hour`, marker any game hit) and the top three models by turns.
- **Turns played each day**, **How far they get** (as a share of each world's players) and **Where players found it**, one colour per world.
- **Per world:** who they play as, versions, keyword instruction blocks, how games ended and every trigger (games it fired in and times fired), with zero-fire triggers listed separately.
- **Stats markers:** worlds built with the IW-Builder house kit carry hidden one-shot triggers named `Stats: …`. The page groups them: `Stats: Started` (the denominator), each setting (`Stats: <setting> = <option>`) with a check that the options add up to Started, `Reached …` milestones and `Turn …` as funnels, and `Model …` with games and turns.

How to read it:

- `Stats: Started` counts games on versions that carry the markers. IW's Games figure also counts older versions and saved copies, so marker shares use Started.
- A setting whose options don't add up to Started is flagged. More than Started means a multi-select, several slots counted together, or a mid-game switch; fewer means some games never reached the choice.
- A trigger or marker at 0 has usually not been reached yet. Check it against "How far they get" before calling it a bug.
- IW counts triggers by ID, so a trigger rebuilt with a new ID shows up twice. The page adds duplicate `Stats:` markers together.
- IW hides counts under 5 players; they show as a faint bar labelled "under 5". In "Where players found it", a source a world has no row for shows a faint stub labelled "Not listed".
- A world with no `Stats:` rows at all usually has no published version with markers yet: IW lists a trigger once a published version has it.
- The Theme button switches between your system setting, light and dark.
- A second export of the same world replaces the older one; the date in the file name (`<World> stats YYYY-MM-DD.csv`) decides.

Until you load a file, the page shows example data: three made-up worlds with invented numbers, in [examples/](examples/). One has live `Stats:` markers, one has none, and one has a marker build published but not yet played. Your first file replaces them; Clear all brings them back. The examples load only when the page is served over the web (opened straight from disk, it starts empty).

## Add the markers to your own world

[stats-starter.json](stats-starter.json) is a tiny world that holds only the base markers, ready to copy. Its harbour-town story is a placeholder so it imports and plays. What it carries:

| Marker | Condition | When it fires | What IW's stats show |
| --- | --- | --- | --- |
| `Stats: Started` | `$stats_markers >= 0` (always true) | Start of game, once | Games on versions with markers: the denominator for every share |
| `Stats: Pace = Slow` (and Steady, Fast) | `$pace = "Slow - a week per chapter"` | Start of game or mid-game, once | Which option of a setting players pick. Copy one per option |
| `Stats: Pictures = High` (and Basic, Off) | `$imagetype = "High"` | Start of game or mid-game, **repeating** | Games per picture setting, and turns on each (Fired) |
| `Stats: Reached Day 1` … `Day 300` | `$story_day >= 1` | Mid-game, once | How far games get in story time. Use `>=` so a jump still counts |
| `Stats: Model Dolphin` … `Model Other` | `$game.ai_model = "Dolphin"` | Mid-game, **repeating** | Games and turns on each model: the standard eleven, then Leopard-2, Wampus, Wildcat, `Smilodon-2 (experimental)`, `Smilodon-2 Thinking (experimental)` and `Galaxycat (experimental)` (the display name, which is what `$game.ai_model` returns). Other is `!=` every listed model |

Every marker has the same single effect, a Run Script of `$stats_markers = $stats_markers + 1`, and a hidden Number tracker **Stats Markers** (`stats_markers`, starting at 0) holds the count. Hidden trackers aren't sent to the AI and triggers don't bill, so the markers cost nothing to play.

**Copy them by raw JSON** (fastest, and keeps the IDs):

1. Open your world in the editor: **Show optional features > Misc advanced features > Show raw JSON**, then **Refresh raw JSON** and copy the whole value somewhere safe as a backup.
2. Open `stats-starter.json` in a text editor. Copy the **Stats Markers** object from its `trackedItems` into yours, and every trigger named `Stats: …` from its `triggerEvents` onto the end of yours (they read each turn's final state, so last is best).
3. Point the copied conditions at your own world: change `$pace` and its option texts to your own setting's variable and exact dropdown options (case and punctuation must match), `$imagetype` to your picture setting, and `$story_day` to your day count. Delete the markers you have no use for, and copy a setting's block once per extra setting, giving each copy a new ID (nine letters and digits).
4. Paste the edited JSON back into the box and choose **Import JSON to world**. Remove any final newline first: the text should end at its last brace.

**Or add them by hand** in the trigger editor: a PawScript condition, one Run Script effect, and the boxes from the table (**Trigger at start of game** for Started and settings, **Or mid-game** for all of them, **Allow triggering multiple times** only for Pictures and Model).

Rules that keep the numbers right:

- **Keep marker IDs fixed across versions.** IW counts triggers by ID, so a marker deleted and recreated starts a fresh row. Edit the name or condition freely; don't delete and re-add.
- **Name them `Stats: …`** with ` = ` between a setting and its option, `Reached …` for milestones and `Model …` for models, and this page groups and charts them for you.
- **Markers count only in a public Community World.** Load your next World Stats export here after publishing: Started should match the games on that version, and each setting's options should add up to Started.
- **`Reached …` takes any unit your story keeps.** Days are only the starter's example. For short games, hours work the same way: `Stats: Reached Hour 1` … `Hour 20` on a count of story hours (`$story_hours >= 4`), which needs a time of day the story keeps (the house kit's is a Story Time tracker the AI writes as HH:MM, turned into hours by a script). The page lists `Hour n` first, then `Day n`, then other milestones.
- Other markers fit the same pattern: a ready-made character (`$player.name = "Name"`, plus a `!=` catch-all for custom characters), a story milestone (`$chapter >= 3`), or the first use of a feature.
