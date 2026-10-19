# PawScript working reference

## PawScript practical guide

PawScript is not JavaScript, Python, SQL or the unrelated languages with the same name online. Use the supported subset below and the official references for anything additional. The examples use a small working subset.

Three contexts:

```text
Template text:  You hold <<$coins>> coins.
Condition data: $coins >= 5 and $state.ticket = 0
Script data:
$coins -= 5
$state.ticket = 1
```

Template expressions read values. triggerOnPawScript and effectRunScript contain bare code, not template delimiters or Markdown fences. Native `$game.turn_number` starts at 1 in opening-turn documentation/tests. `$player` and `$game` are read-only system roots; custom roots must bind to declared tracker variableName values. A top-level assignment to an undeclared root is not how you create a tracker.

Core syntax:

| Operation | Syntax |
| --- | --- |
| Read a YAML field | `$state.inventory.apple` |
| Write a field | `$state.inventory.apple = 1` |
| Temporary local | `set $price = 5` (not a persistent tracker) |
| Arithmetic/update | `+ - * / %`, and assignments such as `+=`, `-=` |
| Equality/comparisons | `=`, `!=`, `<`, `<=`, `>`, `>=` |
| Logic | `and`, `or`, `not`; parenthesize mixed tests |
| Text composition | `"Cash " & $coins`; append with `$ledger &= "..."` |
| Branches | `if`, `else if`, `else`, with indented bodies and no colon |
| Bounded iteration | `for each $entry in $list`, indented statements |
| Dynamic record lookup | `$rooms.item($destination)` |
| Safe permission lookup | `$flags.item($key, 0)` |
| Missing-key guards | `$rooms.contains($destination)`, `.requires.exists()` |
| Filtering | `$characters.where(significant = true)` |
| Count / first result | `$characters.count()`, `$characters.first()`; guard empty results before field access |
| Project a field from a list | `$classes.all().name` (the PC-choice editor supplies this idiom) |
| Replace text | `$label.replace("_", " ")` |
| All permissions | `$requirements.every($flags.item(value(), 0) = 1)` |
| Field mapping | `choose($code, "A", "Alpha", "B", "Beta", "Unknown")` |
| Clamp | `$coins = $coins.constrain(0, 250)` |
| Random draw | `set $roll = dice_roll(6)`; store/reuse rather than rerolling in every condition |

Example conditional script (declare credits and purchases trackers first):

```text
if $credits >= 5
  $credits -= 5
  $purchases.total += 1
```

Example dynamic record lookup, without assuming a particular game layout:

```text
$results.found = 0
if $catalog.entries.contains($selection)
  $results.label = $catalog.entries.item($selection).label
  $results.found = 1
```

An advanced predicate checks whether every required named flag is granted:
`$requirements.every($flags.item(value(), 0) = 1)`.
Initialize requirements as a list; explicitly distinguish an empty list from a missing field. This is a language capability useful for many rule systems, not a mandatory access-control design.

Do not add semicolons/braces, `==`, `&&`, `||`, `+=` inside a read-only expression, Python dict literals, `.map(x => ...)`, or arbitrary host-language libraries. Do not assume string concatenation uses `+`. List access is not assumed zero-based. List construction and library operations are covered below. The external language reference covers optional extensions beyond this kit.

PawScript can modify declared trackers and explicitly supported writable built-in values. It cannot write arbitrary world fields, including instruction-block content, or invoke trigger effects. For those operations, calculate or assemble in a tracker, then apply using a native effect. Templates read values; they do not expand script write permissions.
Keep dependent calculations in one sequential script where appropriate. A script failure rolls back that script's changes, not preceding effects or the entire turn. Use meaningful script names and inspect tracker results in World Debug; “Ran successfully, with no output” is normal for assignments.

For a structured party, a documented script loop such as `for each $member in $party` can update `$member.hp` inside the original tracker. List mutations use script methods such as `.append(...)` and `.remove(...)`; do not silently substitute native text add/remove effects for list operations. Use a separate sandbox/probe for new complex selection/mutation compositions rather than assuming every chain is writable. Prefer 1-based documented `.item(1)` access over host-language indexing.

Escaping matters at THREE layers: JSON string, PawScript string literal, eventual rendered text/YAML. Serialize code with a JSON library instead of hand-counting escapes. The physical newline between script statements is a newline inside effectRunScript.data after JSON parsing. A newline intended INSIDE a PawScript message literal must remain an escape at that layer. Inspect decoded values and expected output. Include explicit spaces around concatenated numbers: `"Cost " & $price`, not `"Cost" & $price`.


## Inline random values

Use PawScript to supply a random value in an active instruction block instead of asking the storyteller to invent a roll:

```text
Encounter roll: <<dice_roll(6)>>.
Interpret 1-2 as quiet, 3-4 as a complication, and 5-6 as an opportunity.
```

`dice_roll(sides, count)` rolls and sums dice; `dice_roll(6)` is one six-sided die and `dice_roll(6, 3)` is three. Both arguments are optional, defaulting to six sides and one die. See the [official function reference](https://infiniteworlds.app/pawscript-reference).

Each evaluation can reroll. Store a shared result in a tracker when several checks, outputs or turns must agree. Active block templates are evaluated for context, while templates in native block-modification effects can be fixed when installed; see [Capabilities.md](Capabilities.md). A mechanically generated number does not enforce the storyteller's interpretation. Use scripts/conditions for exact consequences when required.

## Operations used by the supplied library

These snippets illustrate the existing library notation. Declare and initialize the trackers they reference before using them.

| Syntax | Meaning / use |
| --- | --- |
| `# explanation` | Script comment; distinct from instruction-text `<#...#>` comments |
| `list()` / `list("red", "blue")` | Empty list / explicit list construction |
| `$entries.any(name = "Mara")` | Whether at least one entry matches |
| `$entry.name.exists()` | Whether a path exists; existence is not the same as nonempty text |
| `$entries.where(aliases contains "Mara")` | Filter using `contains` inside a predicate |
| `$entries.where(name = $update.name) = $update` | Replace each matched entry; not a field-preserving merge |
| `$entries.append($update)` | Append an entry |
| `$updates.remove($update)` | Remove matching update entries |
| `list("rain", "fog").random()` | Select a random list member; distinct from top-level numeric random() |
| `$entries.all().name` | Project names from all entries |

If multiple entries share the match key, selection/replacement can affect multiple entries. Use stable unique identities. A replacement record must include every field to retain. Library buffer examples mutate their update collection while iterating; retain that known composition only when appropriate and test any materially different mutation loop. A clearer alternative for a new merge is to iterate updates, write the destination, then clear the buffer after the loop, rather than deleting entries during iteration.

The official script guide also documents bounded `range(n)` iteration and `log("diagnostic")` for the PawScript Log. Log output is diagnostic, not player narration. See https://infiniteworlds.app/pawscript-script-guide.

## Readable data

YAML initial values are JSON strings containing YAML. Indentation defines structure; `- ` creates list members; `[]` is an empty list. Quote numeric-looking identifiers to retain leading zeros. Use `|` when a YAML text value should retain line breaks. The library's formatSchema notation is a separate shape description, not the same thing as a starting YAML value. See https://infiniteworlds.app/yaml-guide.

## Skills and context roots

Read Skills with `$player.skills.<slug>` and display them with `$player.skills_and_levels`. `$game.skill_map` maps slugs to display names. Native skill effects change levels; scripts do not write `$player`. Other documented roots include `$player.name`, `$game.turn_number` and `$game.ai_model`. Runtime narration fields and video-only placeholders are separate concepts; do not create imaginary global variables from their names.

This quick reference covers the language used by the included recipes and sample modules. It is not a bundled copy of every PawScript function. Advanced extensions can use the official references; a no-browsing author should stay within this documented subset or request the relevant reference text.

## Common mistakes

The meaning of = depends on context: it compares in an expression/condition and assigns in an assignment statement. An if condition remains an expression even inside a script.

| Mistake | Correct form |
| --- | --- |
| `$coins == 5` | `$coins = 5` in a condition |
| `a && b` / `a || b` | `a and b` / `a or b` |
| `if $coins > 0:` | `if $coins > 0` followed by an indented body |
| `"Cash " + $coins` | `"Cash " & $coins` |
| `$new_tracker = 1` without a declaration | Declare a tracker first; use `set $local = 1` only for a temporary local |
| `<<$coins -= 1>>` | Put mutation in Run Script; templates read values |
| Writing `$player` or `$game` | Use supported native effects; system roots are read-only |

The validator's lint is heuristic, not a PawScript parser. It ignores quoted literals and comments when checking code operators; warnings identify review points, not proof of a runtime failure. Script locals are checked in a lexical approximation, not full control-flow analysis. Documented engine placeholders without a dollar sign are not custom tracker roots.
