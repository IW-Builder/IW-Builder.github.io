# IW Debug Exporter

The debug counterpart of IW's Export story. For every turn of the open game it
saves what World debug tools shows: the evaluation, thinking (on models that
think), triggers fired, active instruction blocks (rendered), matched lore, and
every PawScript condition and effect with its status and error. Downloads a
readable `.txt` and a `.json`.

**Install:** open [the install page](https://iw-builder.github.io/debug/) and
drag the button to your bookmarks bar.

**Use:** open or load the game on infiniteworlds.app, wait until no turn is
generating, then click the bookmark. When the status box says Done, both files
download and the game is back on the turn you were viewing.

## Files

- `index.html`: the install page. Built by `node debug/build.js` from
  `index.template.html` and the source; don't edit it by hand.
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
12 character, 24 evaluation, 25 thinking, and the debug object (26 as of
2026-11-01).

It is read-only: it takes no game actions and sends nothing anywhere else.
Tested 2026-11-01 on a 25-turn Dolphin game (complete, view restored from both
the latest turn and turn 23).
