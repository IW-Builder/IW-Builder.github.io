# Check worlds and manage your files

Most people can start with the [web checker](https://iw-builder.github.io/checker/). Paste your world there, check the results, and copy the report back to your AI if something needs fixing. It can also join numbered output chunks into one file.

The files here provide the same kinds of checks locally, along with tools for saving reusable content and maintaining the kit. You only need them if you or your AI can run Python.

| Tool | What it helps you do |
| --- | --- |
| `validate_iw_export.py` | Check a world for formatting problems, broken references and likely mistakes; compare an edited world with the original. |
| `data_bank.py` | Save characters or other world content in a portable text bank, or create a full-content report. |
| `build_distribution.py` | Rebuild the homepage, combined text packages, checker tools and file-integrity manifest in one step. |
| `check_package.py` | Check the kit's example files and links. Primarily for maintaining the kit itself. |
| `test_validator.py`, `test_data_bank.py` and `test_distribution.py` | Run checks on the tools themselves. |

For commands, setup and detailed explanations of the results, see [Usage.md](Usage.md). For character banks and reusable bundles, see the [data-bank guide](../reference/Portable-Banks.md).

The remaining support files are `iw-export.schema.json` (the expected world structure), `static_checks.py` (additional checks), and `Validation-Report.json` (results from a package check). You do not need to edit them to check your world.

A clean report is useful, but it cannot guarantee how a world will play. Try the important features in IW too.

[Back to the main guide](https://iw-builder.github.io/guide/)

## Additional diagnostics

- `import_audit.py` compares source and imported worlds without repairing them.
- `story_export.py` proposes reviewable boundaries, extracts raw tracker text and merges only nonconflicting declared histories.

See [Story tools](../reference/Story-Tools.md) for commands and limits.

- [iw_browser.py](iw_browser.py): optional standalone browser capture, refresh-verified export and offline integrity/recovery inspection.
- [plot_compile.py](plot_compile.py): literal-Scenario prerequisite-DAG analysis and fresh-world generation; [example plan](example-plot-plan.json).
- [Engineering tools](../reference/Engineering-Tools.md): contracts, setup and remaining live-integration boundary.
