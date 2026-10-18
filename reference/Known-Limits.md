# Verification scope and platform boundaries

The kit combines native exports, editor help, runtime checks and PawScript documentation. Its schema checks structure and explicit references; it does not execute IW, PawScript, AI generation or image/video models. A structurally valid world can still contain incorrect paths, unsupported assumptions or inconsistent story instructions.

## Established behavior

- Native single-answer choice/input updates and downstream trigger reads occur in the same turn with valid targets. The single-choice fixture also preserves its binding through a fresh import.
- Keyword matching is case-insensitive and whole-word for the tested plain-word inputs. A block remains active for three additional turns after a match. Debug shows active/inactive blocks and keyword lists, but not the matching term or remaining timer.
- Numeric skill levels and capped skill effects work independently of potentially inaccurate generated labels.
- Original block templates reevaluate; native trigger-installed text snapshots template substitutions at installation.
- Native operations and script statements have distinct sequencing semantics, as documented in Triggers.md.
- NPC editor help defines brief-summary visibility until the turn after first character/location mention. NPC activation cannot be directly inspected in debug.

## Boundaries to consider when relevant

| Area | Boundary |
| --- | --- |
| Keywords | Exact punctuation/multiword matching and the complete set of scanned fields are not established by the plain-word tests. |
| Native input variants | Multiple selection, newline/comma storage, optional/multiline text and YAML paths have editor/export shapes; precise delimiter spacing, blank-submission and nested-write behavior require runtime checking before depending on them. |
| Structured append | Appending a record versus a one-element list may differ; coercion and flattening are not established. |
| Templates | Evaluation timing is not established for every string field; do not generalize block timing to all surfaces. |
| Format enforcement | The complete formatSchema grammar and XML-specific behavior are not exhaustively characterized. |
| Video | The sample video template's context variables and runtime availability are not fully characterized. |
| Endings | alreadyFired is not reliable exported firing history; native ending repeat/timing behavior should not be inferred from it. |
| Engine limits | Maximum field sizes, loop bounds, trigger counts and summary scheduling are not specified by this kit. |
| IDs | The supplied single-choice import is verified; no universal ID-format or remapping rule is claimed. |

Use a focused check only when a world depends on an uncertain behavior. A narrative response is not proof of a tracker write or block activation: inspect current values and debug. For keyword checks, an OOC marker can avoid repeating the word in narration; verify that it actually does so, because repeated mentions may refresh activation.
