# IW Cost Exporter

Downloads your full Infinite Worlds credit history as CSV and JSON: every
transaction with its UTC timestamp, world, turn, model, total cost, the
input/output cost breakdown, and your balance after it.

**Install:** open [the install page](https://iw-builder.github.io/cost/) and
drag the button to your bookmarks bar.

**Use:** on infiniteworlds.app, open Credit activity (click your credit balance
at the top), then click the bookmark. A status box counts the transactions.
When it says Done, both files download. **Stop and save** ends early and keeps
what was collected.

## Files

- `index.html`: the install page.
- `IW-Cost-Exporter-bookmarklet.js`: readable source of the bookmarklet.
  The install page's bookmark is this file, URL-encoded.

## How it works

It waits for the site's own credit-history request, then requests further
pages over the same connection until IW returns an empty page. There's no
record limit. The bookmarklet consumes the replies to its own requests itself,
so IW doesn't log "Got response for unknown request ID". Timestamps arrive
beside each reply as typed objects and are written into each record's
`datetime` field. A slow reply is retried up to 4 times with smaller batches;
if it still fails, the bookmarklet saves what it has and says why
(`"complete": false` in the JSON).

It is read-only: it reads your own history through your logged-in session,
sends nothing anywhere else and takes no game actions.

## Spreadsheet tips

With the timestamp in A2:

- Date (UTC): `=DATE(LEFT(A2,4),MID(A2,6,2),MID(A2,9,2))`
- Time (UTC): `=TIMEVALUE(MID(A2,12,8))`
- Local date and time: add both, then subtract your UTC offset, e.g. `-4/24`
  for New York in daylight saving time.
