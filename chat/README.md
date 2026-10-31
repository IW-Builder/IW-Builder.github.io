# Bring the kit into your chat

These text files let you use IW Builder with an AI that accepts attachments, even if it cannot browse the website or open a ZIP.

For web retrieval, an AI can open the [authoring guide page](https://iw-builder.github.io/chat/) directly, or start from the [homepage](https://iw-builder.github.io/) and fetch individual files listed in [llms.txt](https://iw-builder.github.io/llms.txt).

There are two kinds of file here. The **reference** is what the AI reads to do the work; attach it once. The **content to pick from** is examples, library modules and tools; attach a piece only when the AI asks for it.

## Reference: attach one file, or four

| File | What's inside |
| --- | --- |
| [Complete Reference](IW-Complete-Reference.txt) | Everything in the four files below in one attachment: about 290 KB, around 75k tokens. The simplest choice when your AI's chat accepts a file that size. |
| [Authoring Guide](IW-Authoring-Guide.txt) | The main prompt, starting template, core guides to creating worlds, and how to choose library modules. Start here if you attach the four files separately. |
| [Technical Reference](IW-Technical-Reference.txt) | Exact world-file structure, PawScript, turn lifecycle, characters, images and models, and feature recipes. |
| [IW Behavior](IW-Behavior.txt) | Notable findings and what is still unknown, editor and UI workflows with import checks, cost estimating and tested platform behavior. Useful for debugging. |
| [Payloads](IW-Payloads.txt) | The exact building block for every trigger condition and effect, plus an index of all example worlds. Small; useful for any world with mechanics. |

The four-file split exists for tools that cap attachment or fetch size around 100 KB: each file is under 90 KB. A model fetching by URL should use those or the individual files in [llms.txt](https://iw-builder.github.io/llms.txt), since most fetchers truncate the complete file.

## Content to pick from: attach only what is asked for

| File | What's inside |
| --- | --- |
| [Mechanics Examples](IW-Mechanics-Examples.txt) | Complete worlds showing purchases, unlocks, choices, timers, optional settings, layered openings, on-demand generation and other mechanics. |
| [Narrative Examples](IW-Narrative-Examples.txt) | Complete story worlds: ensemble romance, a platonic fantasy expedition, contained horror, a fantasy relationship story and high-heat erotica. Large; use the one closest to your idea. |
| [Sample Blocks](IW-Sample-Blocks.txt) | Ready-made building blocks for storytelling, continuity and other optional features. |
| [Storymaster](IW-Storymaster.txt) | The Storymaster narrative-direction framework. Only needed if you choose it. |
| [Tools](IW-Tools.txt) | Code the AI can use to check worlds and handle reusable content, if it can run Python. |

Start by attaching the reference and telling the AI what you want to make. You can describe an idea, attach a world you want changed, or ask how something works. If your AI cannot run the checks, you can use the [web checker](https://iw-builder.github.io/checker/) yourself and paste the results back into the conversation.

`sources.json` records which files went into each package; you can ignore it during normal use.

[Back to the main guide](https://iw-builder.github.io/guide/)
