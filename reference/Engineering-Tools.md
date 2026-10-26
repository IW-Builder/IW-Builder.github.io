# Plot compiler

A local authoring tool, not a platform API. It never submits a turn or publishes a world. See [Story tools](Story-Tools.md) for export parsing and import comparison.

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
