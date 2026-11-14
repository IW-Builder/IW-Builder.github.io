# World stats page

[iw-builder.github.io/stats/](https://iw-builder.github.io/stats/) turns the CSV export from a world's **World Stats** page in Infinite Worlds into charts. Load one file or several (one per world) to compare worlds. The page runs entirely in your browser: files are never uploaded. No build step and no libraries; `index.html` is the whole tool.

What it shows:

- **At a glance:** turns, games, players, credits per turn (weighted by turns across worlds) and a side-by-side table, including the share of players still playing at turns 5, 10, 21, 51 and 100.
- **Turns played each day**, **How far they get** (as a share of each world's players) and **Where players found it**, one colour per world.
- **Per world:** who they play as, versions, keyword instruction blocks, how games ended and every trigger (games it fired in and times fired), with zero-fire triggers listed separately.
- **Stats markers:** worlds built with the IW-Builder house kit carry hidden one-shot triggers named `Stats: …`. The page groups them: `Stats: Started` (the denominator), each setting (`Stats: <setting> = <option>`) with a check that the options add up to Started, `Reached …` milestones and `Turn …` as funnels, and `Model …` with games and turns.

How to read it:

- `Stats: Started` counts games on versions that carry the markers. IW's Games figure also counts older versions and saved copies, so marker shares use Started.
- A setting whose options don't add up to Started is flagged. More than Started means a multi-select, several slots counted together, or a mid-game switch; fewer means some games never reached the choice.
- A trigger or marker at 0 has usually not been reached yet. Check it against "How far they get" before calling it a bug.
- IW counts triggers by ID, so a trigger rebuilt with a new ID shows up twice. The page adds duplicate `Stats:` markers together.
- IW hides counts under 5 players; they show as a faint bar labelled "under 5".
- A second export of the same world replaces the older one; the date in the file name (`<World> stats YYYY-MM-DD.csv`) decides.
