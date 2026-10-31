# PawScript working reference

PawScript reads game data, computes values and updates trackers. It is its own language, not JavaScript or Python. Start with sections 1-3 when learning; use the later tables for lookup. Examples use declared tracker variable names, not display names or IDs.

## 1. Where PawScript runs

| Context | Example | Purpose |
| --- | --- | --- |
| Template in supported text field | `Coins: <<$coins>>` | Insert result into text; no mutation |
| Deferred template in text installed by a block-modification effect | `Coins: <=$coins=>` | Stays live after installation instead of freezing; no mutation |
| PawScript trigger condition | `$coins >= 5` | Return true/false; no mutation |
| Run Script trigger effect | `$coins -= 5` | Execute statements, save changes |

An **expression** returns a value. A **statement** performs work, such as assignment or a loop. Script conditions are still expressions: the test after `if` decides whether its indented statements run. Use bare code in trigger conditions and Run Script, without `<<...>>` or Markdown fences. Text that a block-modification effect installs is a snapshot of its `<<...>>` values; a deferred `<=...=>` reference stays live in that destination. See [Capabilities.md](Capabilities.md) for template timing.

Example, in the content of a Modify instruction block effect:

```text
Win path: <=choose($win_path, "escape", "Find the hidden exit before dawn.", "expose", "Gather proof and reveal the warden.", "Survive until the relief ship arrives.")=>
```

When the effect installs this text, the deferred reference is kept rather than resolved, so the block describes the current `win_path` each time it is prepared. Written as `<<choose(...)>>`, it would freeze when the effect ran. In the JSON export the inner quotation marks are escaped as `\"`.

`<<=...=>>` stays literal despite the editor's highlighting ([Editor-UI.md](Editor-UI.md)); what happens when a tracker is set to a deferred reference is in [Verified-Behavior.md](Verified-Behavior.md).

PawScript cannot write arbitrary world fields, including background or instruction-block content, or invoke native trigger effects. Calculate or assemble content in trackers, then use native effects to install it or display messages. Templates do not expand write permissions. `$player` and `$game` are read-only; do not infer writability from a field being readable.

A script changes state only when it executes. It does not automatically enforce what the storyteller narrates. Trigger timing and template installation timing are described in [Triggers.md](Triggers.md) and [Capabilities.md](Capabilities.md).

## 2. Values, trackers and scope

Create a tracker before referencing it. Its `variableName` supplies the root: a tracker named Party with variable name `party` is `$party`. A script assignment does not create a missing tracker.

| Value shape | Example | Access |
| --- | --- | --- |
| Number | `12` | `$coins` |
| Text | `"Open"` | `$status` |
| Boolean | `true` or `false` | `$state.ready` |
| List | `list("red", "blue")` | `$colors.item(1)` |
| Record (named fields) | YAML below | `$hero.name` |

List positions are **1-based**. A record uses keys, not positions. A list of records represents several objects; a record containing lists represents one object with collections.

For example, this YAML initializes one record:

```yaml
name: Mira
hp: 4
tags:
  - scout
  - injured
```

Stored in tracker `hero`, it provides `$hero.name`, `$hero.hp` and `$hero.tags`. YAML indentation defines nesting; `[]` initializes an empty list and `{}` an empty record. Quote numeric-looking identifiers such as `"001"` to preserve leading zeros in storage; comparisons and arithmetic still treat them as numbers (quoted or unquoted `007` plus 1 gave 8). YAML `yes`, `no`, `on` and `off` are text, not Booleans. `true`/`false` compare equal to both the Boolean and the same-spelled text. A `null` value's `.exists()` is false. Use YAML `|` for multiline text. In an export, `initialValue` is a JSON string containing this YAML, not a JSON object. `formatSchema` is a separate shape description; see [Trackers.md](Trackers.md).

Persistent roots use direct assignments: `$coins = 12`. Temporary locals use `set $price = 5` and last only for that script run. Locals do not cross Run Script effect boundaries; executed branch locals and the last nonempty-loop binding remain available later in the same script. Do not give a local the name of an existing tracker. Inside collection predicates, bare field names refer to the current member; `$...` refers to a tracker/system root or script local. For a list of plain values, `value()` denotes the current value.

## 3. A complete small example

Create a YAML tracker named Party with variable name `party`, initial value below, and automatic AI updates disabled for this mechanically managed example:

```yaml
- name: Mira
  hp: 4
  max_hp: 8
- name: Oren
  hp: 8
  max_hp: 8
```

**Read:** put `Injured members: <<$party.where(hp < max_hp).count()>>` in a supported template field.

The chain reads left to right:

1. `$party` is the whole list.
2. `.where(hp < max_hp)` selects injured members. Each comparison uses that member's fields.
3. `.count()` returns the selection size. This reads data; it does not heal anyone.

**Test:** a PawScript trigger condition can use `$party.any(hp < max_hp)` to decide whether healing is needed.

**Change:** a Run Script effect can restore every member:

```text
for each $member in $party
  $member.hp = $member.max_hp
```

The loop variable refers to each original member, so assignments persist in the tracker. After execution, both members have full health and the injury condition is false. Inspect tracker data to verify this; no visible story output is required. Add a native message effect if the player should receive confirmation.

Use the expression/script Sandbox to try the read and change separately. For an in-game trigger, also configure timing and repeat behavior; see [Triggers.md](Triggers.md). To practice, change the condition to detect a member at zero health, then predict the result before running it.

## 4. Expressions and decisions

| Operation | Syntax / meaning |
| --- | --- |
| Arithmetic | `+ - * / % ^`; `%` is remainder, `^` is exponentiation |
| Comparison | `= != < <= > >=` |
| Logic | `and`, `or`, `not`; parenthesize mixed tests |
| Text concatenation | `"Coins: " & $coins`; numbers become text |
| Conditional value | `if($coins >= 5, "Affordable", "Too expensive")` |
| Value mapping | `choose($status, "open", "Enter", "locked", "Find a key", "Inspect")` |
| Missing/blank fallback | `first_available($hero.nickname, $hero.name, "Stranger")` |
| Error fallback | `try($total / $count, 0)`; catches missing paths, type mismatches, division by zero, reads through a scalar and out-of-range `item(99)`. Do not use it to conceal broken essential state |
| Existence | `$hero.nickname.exists()`; distinct from being nonempty or nonzero |
| Numeric bounds | `$hp.constrain(0, $max_hp)` |
| Rounding and bounds | `round_down($cost)`, `round_up($cost)`, `$cost.round()`; standalone `round(1.6)`, `min(2, 3)`, `max(2, 3)` also work |
| Text normalization | `$label.replace("_", " ")` |

`=` compares within an expression and assigns in an assignment statement. In the following script, the first `=` tests; the second writes:

```text
if $status = "locked"
  $status = "open"
```

`and` and `or` short-circuit, as do native And/Or condition groups. A left-hand guard can prevent an unsafe right-hand read; this skips evaluation but has no measured speed benefit. Fallback and `try` operations handle missing values but do not make expressions valid in unsupported contexts. `current()` is rejected in Run Script; it belongs to a legacy List Update context the current editor does not expose. Functions require parentheses: `.count()` calls a function; `.count` reads a field named count.

A statement-level branch changes data, unlike expression-level `if(...)`, which returns a selected value:

```text
if $coins >= 5
  $coins -= 5
  $purchases.total += 1
else
  $message = "Not enough coins."
```

Declare `coins`, `purchases` (including `total`) and `message` first. Use `else if` for additional branches, at the same indentation as `if`. `#` starts a script comment; instruction-text comments use `<#...#>` instead.

## 5. Collections: select, calculate, change

### Read and select

| Need | Expression |
| --- | --- |
| Construct a list / empty record | `list("red", "blue")`, `list()`, `record()` |
| First item / first few | `$party.first()`, `$party.first(3)` |
| Last item / recent subset | `$history.last()`, `$history.last(3)` |
| Dynamic record lookup | `$catalog.item($selection)` |
| Lookup with read fallback | `$reputation.item($faction, 0)` |
| Record keys / values | `$catalog.keys()`, `$catalog.values()` |
| Key or value membership | `$catalog.contains($selection)` tests a record key; `$tags.contains("scout")` tests a list value |
| Matching records | `$party.where(hp < max_hp)` |
| Matching plain values | `$tags.where(value() != "retired")` |
| Any / every / none | `$party.any(hp > 0)`, `$party.every(hp > 0)`, `$party.none(hp > 0)` |
| Project fields | `$party.all().name`, `$party.where(hp > 0).name` |
| Total a field | `$party.sum(hp)` |
| Largest field value | `$party.max(hp)` |
| Member with largest value | `$party.max_by(hp)`; append `.name` to read its name |
| Sort by a field | `$party.sort_by(hp, desc).all().name` |
| Remove duplicate values | `$tags.unique()` |

A selection can contain several members even when you expect one. Use stable unique keys when identifying an object. Guard empty selections before requesting a member. `every(...)` is true for an empty list; add a count check when your rule requires at least one member.

Within filters, `name contains "fire"` tests the current member's field; `id in $unlocked` checks membership in an outer list. Bare `in` is filter syntax, not a general replacement for `.contains(...)`. For example:

```text
$abilities.where(id in $unlocked).all().name
```

An advanced predicate can check named requirements:

```text
$requirements.every($flags.item(value(), 0) = 1)
```

Initialize `requirements` as a list and `flags` as a record. An empty requirement list passes; a missing flag uses zero and fails. Missing structure and empty structure are different cases.

### Write and mutate (scripts only)

| Need | Statement |
| --- | --- |
| Assign a field | `$hero.hp = $hero.max_hp` |
| Update a dynamic key | `$reputation.item($faction) = $reputation.item($faction, 0) + 1` |
| Append an entry | `$entries.append($new_entry)` |
| Remove a record key | `$catalog.remove($selection)` |
| Remove every equal list value | `$tags.remove("retired")` |
| Remove selected members | `$party.where(hp <= 0).remove()` |
| Replace matched records | `$entries.where(id = $update.id) = $update` |
| Persist a transformed list | `$tags = $tags.unique()` |

Assigning a record copies it: `$archive = $current` keeps an independent copy that later edits to `$current` do not change. A read such as `$tags.unique()` does not change stored tags by itself. Assignment persists its result. Appending a list appends its members; it does not wrap them as a nested list. Replacement of matched records is not a field-preserving merge: include every field to retain. Plain nested assignment can create missing paths, but a scalar parent rejects child writes and rolls back the script; compound arithmetic on a missing path can fail where plain assignment succeeds. Boolean-expression results can be stored as quoted text, so rendered output is not strict type introspection. Native text add/remove effects are not substitutes for structured list mutation.

To construct an entry, create a local record, fill its fields and append it:

```text
set $entry = record()
$entry.id = "supply-cache"
$entry.name = "Supply Cache"
$entries.append($entry)
```

Initialize `entries` to `[]`. Repeating this script adds another entry; add an identity check if duplicates are unwanted.

Loops can iterate lists or records; `range(n)` supplies a bounded repetition list. Keep mutations straightforward. Library buffer examples remove processed entries while iterating; do not assume every different mutation loop is equally safe. For new update-buffer designs, iterating updates and clearing the buffer afterward is easier to reason about. Test new complex selection/mutation chains in Sandbox.

## 6. Randomness and formatted output

| Need | Expression |
| --- | --- |
| Numeric random value | `random()` |
| Inclusive integer range | `random_between(1, 6)` |
| Dice sum | `dice_roll(6, 3)` or `3d6` |
| One random list member | `$encounters.random()` |
| Several without repeats | `$encounters.random(3)` |
| Shuffle | `$encounters.shuffle()` |
| Text with expressions | `format_text("Coins: {$coins}")` |
| Join list values | `$names.join(", ")` |
| Format each record | `$party.format_each("{name}: {hp}/{max_hp}").join("\n")` |
| Numbered / bulleted output | `$names.numbered_list()`, `$names.bulleted_list()` |

`dice_roll(sides, count)` defaults to six sides and one die. Every random evaluation can produce a new result. Store a shared roll once when several checks or outputs must agree:

```text
$roll = dice_roll(6)
if $roll >= 4
  $result = "Success"
else
  $result = "Failure"
```

Declare `roll` and `result` first. An inline block can instead say `Encounter roll: <<dice_roll(6)>>`, but that only supplies a number; instructions or deterministic effects must define its consequences. Permanent block templates and templates installed through block effects can evaluate at different times; see [Capabilities.md](Capabilities.md).

Inside `format_each`, `{name}` reads the current member's field, `{$coins}` reads an outer tracker, and `{value()}` reads a plain list member. `index()` supplies a 1-based position. These braces belong to formatting functions; they are not a replacement for outer `<<...>>` template delimiters.

Additional presentation helpers include `.bold()`, `.italic()`, `.code()` and `.format_date(...)`. Formatting produces display content, not styling guarantees in every UI field. `now_utc()` and `now_local()` report real-world time, not the story's clock. Consult the official reference for date tokens and less common numeric/string functions.

## 7. Execution and debugging

1. Declare trackers and initialize every required structure. Give mechanically managed values one update owner or an explicit AI/script handoff.
2. Test a read-only expression first. Confirm the selected records and values before mutating them.
3. Run the script against known starting data in Sandbox; inspect the resulting trackers.
4. Test it in its trigger. Confirm timing, condition eligibility and order, not only script syntax.
5. Check repeat execution and boundary cases: no matches, insufficient resources, missing optional fields and already-completed work.

Statements in one script execute sequentially. Later triggers see earlier committed writes. Multiple native numeric effects in one trigger can overwrite rather than accumulate; they do not share script statement semantics. A script failure rolls back that script's changes, not preceding effects or the entire turn.

Use `log("Coins: {$coins}")` for diagnostics in the PawScript Log. Logs are not player narration; messages logged before a failure remain useful for locating the problem. "Ran successfully, with no output" is normal for assignments. Writing a key that does not yet exist in a record succeeds but logs `created a new entry 'x' in $tracker - did you mean 'y'?`; treat it as a typo check. A model saying PASS is not runtime verification.

Enable Menu > Settings > Storyteller Mode, then open the bug icon beside tracked items. Inspect tracker state, evaluated conditions and script errors; use Open in Sandbox to isolate a script. See [Capabilities.md](Capabilities.md) for wider debug coverage.

The validator's lint is heuristic, not a PawScript interpreter. It checks likely mistakes, roots and locals with limited static analysis; passing it does not prove runtime behavior. When teaching or reporting tests, distinguish documented syntax from compositions actually run in IW. [Verified-Behavior](Verified-Behavior.md) lists the runtime-tested PawScript results.

## 8. System roots, escaping and common mistakes

Read Skills with `$player.skills.<slug>` and display them with `$player.skills_and_levels`. `$game.skill_map` maps slugs to display names. Other roots include `$player.name`, `$game.turn_number` (opening turn is 1), `$game.ai_model`, `$game.skill_list` and `$game.difficulty_list`. Native skill effects change levels; scripts do not write `$player`. Runtime narration fields and video placeholders are separate concepts, not automatically script roots.

| Mistake | Use instead |
| --- | --- |
| `$coins == 5` | `$coins = 5` in a condition |
| `a && b` / `a || b` | `a and b` / `a or b` |
| `if $coins > 0:` | No colon; indent the following statements |
| `"Coins: " + $coins` | `"Coins: " & $coins` |
| `$new_tracker = 1` without declaration | Declare the tracker; `set $local = 1` is temporary only |
| `<<$coins -= 1>>` | Mutation belongs in Run Script |
| `.count` to count members | `.count()` |
| Host-language object literals or arrow functions | `record()`, field assignments and supported collection methods |
| Writing background, blocks or system roots | Use the supported native effect |

Escaping has three layers: JSON serialization, PawScript string literals, and rendered text/YAML. Use a JSON serializer. A physical newline separates script statements; the two-character `\n` inside a script string represents an intended text newline. For example, the decoded script:

```text
$message = "Ready\nProceed"
```

has this JSON string representation:

```json
"$message = \"Ready\\nProceed\""
```

Inspect decoded code when debugging escapes. Include spaces explicitly when composing text with numbers. Do not add host-language semicolons, statement braces, arbitrary libraries or external IO.

## Official references

This guide covers common authoring and teaching needs, not every function. Use the official pages for advanced signatures and additional behavior; do not invent syntax when a reference is unavailable.

- [Expression and function reference](https://infiniteworlds.app/pawscript-reference)
- [Writing scripts](https://infiniteworlds.app/pawscript-script-guide)
- [YAML guide](https://infiniteworlds.app/yaml-guide)

The language tables include officially documented operations beyond the kit's runtime-tested examples. A new composition still needs appropriate testing; what remains unresolved is listed in [Notable-Findings.md](Notable-Findings.md#still-unknown).

---

END OF DOCUMENT: reference/PawScript.md
