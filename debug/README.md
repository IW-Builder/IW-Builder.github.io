# IW Debug Exporter

The debug counterpart of IW's Export story. For every turn of the open game it
saves what World debug tools shows: the evaluation, thinking (on models that
think), triggers fired, active instruction blocks (rendered), matched lore,
every PawScript condition and effect with its status and error, and the long
term memory the storyteller used on that turn, plus the image instructions
(the wrench under the image) on turns that generated an image. Downloads a
readable `.txt` and a `.json`.

**Install:** open [the install page](https://iw-builder.github.io/debug/) and
drag the button to your bookmarks bar, or use the console method it offers.

**Use:** open or load the game on infiniteworlds.app, wait until no turn is
generating, then click the bookmark. When the status box says Done, both files
download and the game is back on the turn you were viewing.

## Files

- `index.html`: the install page. Built by
  `npm i --no-save terser@5 && node debug/build.js` from `index.template.html`
  and the source; don't edit it by hand. The `Build debug exporter page`
  workflow (`.github/workflows/build-debug.yml`) runs this on GitHub whenever
  the source, template or build script is pushed, and commits the result. The build minifies the exporter, then
  deflates and base64-encodes it inside a small loader that unpacks it with
  `DecompressionStream` and runs it with `Function`. The bookmark is about 6,000
  characters, because Edge's favorites editor cuts bookmarks off at about
  10,000 (Chrome's editor only hides the rest). If a site ever blocks
  `Function`, the bookmark says so, and the page's console method still works:
  it copies the minified exporter to paste into DevTools.
- `IW-Debug-Exporter-bookmarklet.js`: readable source of the bookmarklet.

## How it works

The debug data isn't fetched when you open World debug tools; it arrives with
each turn's view. The **Previous turn** / **Next turn** buttons call
`get_ui_info` with `change_to_turns_ago`, relative to the turn the server is
showing (1 = back one, -1 = forward one). The exporter borrows the site's
WebSocket (it waits for the next message the page sends, usually a keep-alive
within 30 seconds), reads the current turn, steps back to turn 1, walks forward
to the last turn, then steps back to where you were. It consumes the replies to
its own requests, so the page never sees them.

A turn's reply is a list of fields; the exporter finds the debug object by its
keys (`fired_triggers`, `script_evaluations`) and checks that the turn numbers
are where it expects, so a format change in IW stops it with a message instead
of producing bad data. Fields used: 0 action, 3 turn, 4 last turn, 11 title,
12 character, 5 image, 24 evaluation, 25 thinking, and the debug object (26 as of
2026-11-01).

**Image instructions.** Field 5 (found by its keys `imagePromptInfo` and
`ageOfImageInTurnsBeforeRequestedTurn`) is the image in effect on that turn;
age 0 means the turn generated it, otherwise it is carried over and skipped
(as is a file already exported for the turn before). The caption's turn
number is IW's own text and can lag (a turn-4 image captioned "3:...").
From `imagePromptInfo` the export keeps the five fields the wrench panel
shows: `illustrationSubject` (the caption), `illustrationAppearance`,
`illustrationClothing` (Character data), `illustrationExpression` and
`illustrationSetting` (Situation data). In the JSON they are
`image_instructions` (`image_url`, `caption`, `appearance`, `clothing`, `expression`,
`setting`), or null on turns without a new image.

**Long term memory.** World debug tools > Long term memory doesn't come with
the turn's view: the panel asks for it with `get_turn_long_term_memory`
(`game_uuid`, `turn_number`). The game id is `gameUuid` in field 8 of each turn's
reply. The answer holds `summary` (story, current_situation, key_moments,
characters, plot_threads, secrets, lore, future_notes) and `summary_turn` (0 =
the starting memory, before the first summary). The memory changes only when IW
writes a summary, so the JSON keeps it in full on the turn it first appears and
`{"same_as_turn": n}` after that; the text file prints it once and then
"(unchanged since turn n)". Games still on the old memory system have no memory
to read: the export says so once and carries on without it.

It is read-only: it takes no game actions and sends nothing anywhere else.
Tested 2026-11-01 on a 25-turn Dolphin game (complete, view restored from both
the latest turn and turn 23), and 2026-11-13 with long term memory on a 6-turn
game and a 42-turn game whose memory was migrated (summaries at turns 8, 14,
20, 26, 32 and 38, each printed once).
