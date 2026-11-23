# Playthrough stats page

[iw-builder.github.io/playthrough/](https://iw-builder.github.io/playthrough/) turns your Infinite Worlds **credit activity** export (`credit-activity-YYYY-MM-DD.csv`) into stats for one playthrough of one world. It runs entirely in your browser: the file is never uploaded. No build step and no libraries; `index.html` is the whole tool.

Pick a world (most recently played first), then a playthrough (the longest is picked for you), or all of a world's playthroughs together.

What it shows:

- **At a glance:** average cost per turn (and per paid turn), credits spent, turns played and the turn reached, retries, free turns, start and end date, turns per day played and per calendar day, main model.
- **Cost per turn:** every turn as billed, in the order played, colored by model.
- **Cost per turn in 10% blocks:** the turns from first to last split into ten equal parts, with the average, the change against the whole playthrough and the model mix in each. Shown from 20 turns; under 100 turns each block is small, and the page says so.
- **Models used:** share of turns per model, with credits and cost per paid turn.
- **Turns per day:** every calendar day from start to finish.
- **Images:** turns with an image you made yourself, and the list of turns without one.

How it reads the export:

- **Playthroughs.** The export names the world and turn number of each turn, but not the save. A new playthrough starts when a world goes back to Turn 1 after a later turn. Retries of a turn, and going back to an earlier save, stay in the same playthrough. Two games of the same world played at the same time would be mixed together.
- **Turns played** counts every billed turn row, so a retried turn counts each time. "Reached" is the highest turn number.
- **Images.** The picture IW makes with each turn is billed inside the turn's cost, and the export doesn't say whether it was made. The export lists only images you make yourself (`N images`, 4 credits each) with no world or turn named. The page credits each to the last turn played before it (any world), if that turn was within 2 hours, and says how many it couldn't place. So "turns without an image" means turns with no image you made yourself.
- **Dates** use the export's own date column (your time zone when you downloaded it).
- Several exports can be loaded together; rows found in more than one are counted once.

The Theme button is shared with the [World Stats](../stats/) page. For stats across your whole account, see [IW analyzer](https://iwstats.netlify.app/).
