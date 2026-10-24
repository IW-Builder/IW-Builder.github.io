# Browser capture and plot compilation

These are local authoring tools, not platform APIs. They never submit a turn or publish a world. See [Story tools](Story-Tools.md) for export parsing and import comparison.

## Standalone browser harness

`tools/iw_browser.py` uses an optional Playwright dependency and a dedicated local Chromium profile. The in-app browser's login is a separate session. Authenticated standalone connection, rendered-page capture and refresh-verified editor export were verified on 2026-10-23. Exported content matched the preserved original and passed structural validation. This establishes the observed capture/export workflow, not imports, gameplay automation, interrupted-turn recovery or server persistence. A command-runner sandbox may block local debugging sockets even when the browser is running; in that environment, run the harness from your own terminal.

Install into a local virtual environment from the kit root:

```text
python -m venv .venv
.venv/Scripts/python -m pip install -r tools/requirements-browser.txt
.venv/Scripts/python -m playwright install chromium
.venv/Scripts/python tools/iw_browser.py launch
```

Log in directly in the dedicated browser. Keep its launcher terminal open. The profile defaults to `.iw-builder-browser` under your home directory; keep it private. Debugging binds to loopback. The launcher opens a visible interactive browser for login. On non-Windows systems use `.venv/bin/python`.

In a second terminal:

```text
.venv/Scripts/python tools/iw_browser.py status
.venv/Scripts/python tools/iw_browser.py capture captures/before --tab 0
.venv/Scripts/python tools/iw_browser.py export-current exports/world.json --tab 0 --expected-title "My World"
.venv/Scripts/python tools/iw_browser.py inspect captures/before
```

`status` lists only Infinite Worlds hostnames. Multiple tabs require an explicit index. Open the intended editor/raw panel yourself and finish any import/rebuild before export. The exact title check concerns the raw buffer; it is not authentication or a server identity check.

Export preserves the current raw buffer as `world.json.before.json`, then temporarily replaces only that raw text with a unique invalid-JSON marker and clicks Refresh raw JSON. Do not interact with the editor during this operation. It never clicks Import or Save. It requires the marker to be replaced by valid JSON of the expected title; unchanged final content is valid when regeneration was observed. A timeout is failure, not permission to reuse old raw text. A successful export has a hash/freshness receipt. This establishes editor regeneration, not server persistence or complete live state.

After failure, the original raw text is restored only if the buffer still contains the tool's marker. If disconnected, the backup remains available; manually restore it after reconnecting if needed. A failed receipt write can leave the exported JSON without a receipt: treat it as incomplete and inspect it, then use a new output path. Existing export/backup/receipt names are never overwritten.

Capture writes page text, accessibility text, metadata and hashes into a new directory. Partial capture staging is removed on failure; earlier captures remain untouched. `inspect` verifies listed files offline. Closed panels, historical prompts and live character records are outside its scope. Captures can contain story material; review before sharing.

Recovery is observational: reconnect, run status, choose the intended tab and capture again. Check retained history and controls before deciding whether any action needs retrying. This harness never reloads, regenerates or resubmits a turn automatically. A future unattended gameplay runner needs a separate supported persistence/completion signal; streamed narration is insufficient.

## Literal-Scenario plot compiler

`tools/plot_compile.py` accepts a deliberately bounded plan: title and nodes; each node has an internal lowercase identifier, a user-facing Name, a literal Scenario, optional all-of prerequisites and a nonnegative integer award. It builds a fresh world, never modifies an existing one. See [example plan](../tools/example-plot-plan.json).

```text
python tools/plot_compile.py tools/example-plot-plan.json
python tools/plot_compile.py tools/example-plot-plan.json --output new-world.json
```

Without output, it reports dependency order, roots, structurally reachable nodes and shared Scenarios. With output, it also validates and writes a new world; existing files are refused. Full schema checks need `jsonschema`; otherwise the report explicitly identifies reduced coverage.

Generation puts prerequisite triggers before their dependents. A single script guards both completion and award and commits them together, allowing retry when a script has not completed. The resulting world uses literal Scenarios and a script-owned Plot progress tracker. Two eligible nodes sharing a Scenario may both complete in one turn; no hidden priority or fairness rule is implied. Later narration sees committed state according to platform timing; the compiler does not rewrite narration retrospectively.

Unknown prerequisites, cycles, duplicate identifiers, dynamic Scenario templates and unsupported plan fields are rejected. This compiler supports prerequisite DAGs, not arbitrary cyclic plots, mutually exclusive branches or all possible IW worlds. Independent nodes retain author order. It does not infer events from prose or prove that the AI will recognize a Scenario, that a scene is achievable, or that every player's route is possible. Connectivity is not narrative satisfiability. The generated composition is structurally checked, not live-certified.

---

END OF DOCUMENT: reference/Engineering-Tools.md
