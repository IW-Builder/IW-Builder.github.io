---
title: "Infinite Worlds Authoring Kit"
permalink: /guide/
---
# Infinite Worlds Authoring Kit

Create an IW story or game from an idea. The authoring AI selects suitable features; you do not need to understand IW mechanics first. Experienced authors can also edit, review, debug or discuss mechanics.

This is an independent, unaffiliated resource by a single user. [Compatibility and evidence note](reference/Evidence.md). The kit describes supported authoring workflows and makes remaining boundaries explicit; it is not an official exhaustive engine specification.

## Start here

**Web-capable model:** just give it this URL: `https://IW-Builder.github.io/`. If it doesn't have Python, a [client side validator](https://IW-Builder.github.io/checker/) is available; validation is not required, it's just for troubleshooting.

**[Full-kit workflow](full-package.zip):** upload this ZIP to an AI that can extract files. Ask it to read Authoring-Prompt.md and select the references it needs. Archive access and code execution are separate capabilities; the AI should state which it has.

**Two-step workflow:** attach Authoring-Prompt.md and World-Template.json (or your world) and describe the task. The AI outlines the features and names additional files it needs. Attach those files, then it builds. You do not have to decide which technical references apply.

**[Text-only workflow](chat/):** start with [IW-Authoring-Guide.txt](chat/IW-Authoring-Guide.txt): the prompt, template and core references. Add [IW-Examples.txt](chat/IW-Examples.txt) for native payloads and complete recipes and [IW-Sample-Library.txt](chat/IW-Sample-Library.txt) for library modules. Only provide if the model asks for them. [IW-Tools.txt](chat/IW-Tools.txt) supplies the tool sources for an AI that can reconstruct files and run Python.

## Ready-to-use requests

**Build**

> Use this IW kit to build a complete world. Premise: [idea]. Player role: [role]. Tone and content boundaries: [preferences]. Important activities/features: [features]. Ending or ongoing: [choice]. Read the core prompt, outline the features, and name any missing reference files you need before generating unfamiliar mechanics.

**Edit**

> Use this kit to edit the attached current world. Change [specific behavior]. Preserve everything else, including existing IDs. If you can execute code, apply changes programmatically and compare the exports. Return the full JSON, relevant changed IDs/paths and a short verification plan.

**Review**

> Review this world using the kit. Prioritize import problems, broken references, timing/state errors, unused or conflicting instructions and unnecessary complexity. Give findings with IDs/paths, impact and suggested fixes. Do not modify it yet.

**Debug**

> Expected: [behavior]. Actual: [behavior and turn]. Attached: current world and [tracker values / Evaluation / active blocks / script logs]. Trace the likely cause, distinguish evidence from inference, and ask only for missing data that would distinguish the causes. Propose the smallest appropriate fix.

**Consult**

> Using the kit, explain how to implement [feature] and compare suitable approaches. I am comfortable with [plain-language design / IW mechanics / PawScript]. Do not generate a full world unless needed. Identify any uncertain platform behavior the design would rely on.

**Data / personal bank**

> Extract [characters or mechanics] from this world into my character/data bank. Preserve existing entries and all original fields. Suggest useful bundles and identify external dependencies. Tags: [none / my specified tags / suggest tags following my existing vocabulary].

> Apply [entries or bundle] from this bank to my world, adapting [requested details]. Convert characters to PC or NPC form where requested; preserve the bank source and report integration changes.

**Repository link**

> Read [release-tagged prompt URL] and retrieve the required template and relevant references from the same release. If access fails, name the files I should upload rather than guessing. My task is: [task].

## Personal libraries and build reports

Ask for Data mode to maintain reusable characters, trackers, triggers, scripts, instruction blocks or complete bundles. Tags such as [fantasy] or [shop] are optional; use your own or request suggestions. The AI can also offer extraction during other tasks and a complete portable build report when delivering a world. See [reference/Portable-Banks.md](reference/Portable-Banks.md).

You can add to or edit your personal sample library, or request removal of entries you will not use. Omitting a module from one world does not remove it from the library. Keep the latest returned file: an uploaded attachment is not necessarily writable or remembered in another session. Changes to your personal copy do not update the public repository.

## Suggested reference bundles

These are reading selections, not mandatory extra downloads. The AI can request individual files instead.

| Bundle | Files |
| --- | --- |
| Narrative | Prompt + template/current world; Craft, Trackers, Capabilities; narrative example as needed |
| Mechanics | Narrative selection plus Schema, Triggers, PawScript, Recipes, Payloads and relevant full examples; tools when execution is available |
| Library | Relevant selection plus library/Integration.md and chosen Sample-Blocks modules |

## Package map

| Location | Purpose |
| --- | --- |
| Authoring-Prompt.md | Core workflow and file-routing table |
| World-Template.json | Neutral import envelope; sharing/editing default to true |
| reference/ | Selective guidance, shared evidence legend and known limits |
| examples/ | Compact payload cookbook, complete worlds and scope index |
| library/ | Adaptable narrative modules and dependencies |
| tools/ | Validator, portable data-bank tools, maintainer checks and chat-edition generator |
| chat/ | Generated text edition for upload-oriented interfaces |
| samples/ | Design conversations, resulting worlds. Human analysis; not required for authoring |

Use [examples/README.md](examples/README.md) to find a feature. See [reference/Import-Integrity.md](reference/Import-Integrity.md) for identifiers, path checks and live-world limitations.

## Sample-module source

The unaffiliated [Script Library world](https://infiniteworlds.app/shared/Dxb2ko), code Dxb2ko, contains additional image-style, content and character blocks and is frequently updated; check whether desired blocks are current. The snapshot version is recorded in the compatibility note. The packaged collection is a menu of adaptable modules, not a complete configuration to enable wholesale. Read [library/Integration.md](library/Integration.md) before using Storymaster and its dependencies.

## Import and export

Create or open a world in the IW editor. Enable Show optional feature, expand Misc advanced features (optional), and enable Show raw JSON. Copy the full box to export. Importing replaces the whole world definition: keep an export of content you want to retain, replace the entire box, remove any blank line after the final closing brace, click Import JSON to world, and save. Do not paste Markdown fences.

Starting play creates a separate live copy. Editing the base does not update existing playthroughs. Save as new world preserves live-world edits for future games. Player/Other Character edits do not affect an existing playthrough, and fired effects are not rewritten retroactively. Image changes can need save/reload before export reflects them.

## Validate your world

No Python needed: use the [public checker](https://uhhwheresdre.github.io/), including its numbered-chunk assembler. Copy its report back to your AI for corrections. A model may use the site directly if it has suitable interaction tools; simply reading the site does not run a check.

From the package root:

```sh
python tools/validate_iw_export.py WORLD.json --json
```

Install jsonschema for full schema checks (`python -m pip install jsonschema`). Without it, the validator reports reduced coverage and still performs guarded reference/static checks. To review an edit, add `--diff ORIGINAL.json`. The tool never executes IW or PawScript; consult [tools/README.md](tools/README.md) for diagnostics and limitations. Maintainer package checks are separate from the normal user workflow.
