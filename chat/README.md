# Bring the kit into your chat

These text files let you use IW Builder with an AI that accepts attachments, even if it cannot browse the website or open a ZIP.

For web retrieval, an AI can open the [authoring guide page](https://iw-builder.github.io/chat/) directly, or start from the [homepage](https://iw-builder.github.io/) and fetch individual files listed in [llms.txt](https://iw-builder.github.io/llms.txt).

For attachments, start by uploading [IW-Authoring-Guide.txt](IW-Authoring-Guide.txt) and telling the AI what you want to make. You can describe an idea, attach a world you want changed, or ask how something works. Let it ask for the other files when it needs them.

| File | What's inside |
| --- | --- |
| [Authoring Guide](IW-Authoring-Guide.txt) | The main prompt, starting template, core guides to creating worlds, and how to choose library modules. Start here. |
| [Technical Reference](IW-Technical-Reference.txt) | Exact world-file structure, PawScript, platform capabilities and feature recipes. |
| [IW Behavior](IW-Behavior.txt) | Editor and UI workflows, cost estimating, tested platform behavior, known limits and import checks. Useful for debugging. |
| [Payloads](IW-Payloads.txt) | The exact building block for every trigger condition and effect, plus an index of all example worlds. Small; useful for any world with mechanics. |
| [Mechanics Examples](IW-Mechanics-Examples.txt) | Complete worlds showing purchases, unlocks, choices, timers, optional settings and other mechanics. |
| [Narrative Examples](IW-Narrative-Examples.txt) | Complete story worlds: ensemble romance, a platonic fantasy expedition and contained horror. Large; use the one closest to your idea. |
| [Sample Blocks](IW-Sample-Blocks.txt) | Ready-made building blocks for storytelling, continuity and other optional features. |
| [Storymaster](IW-Storymaster.txt) | The Storymaster narrative-direction framework. Only needed if you choose it. |
| [Tools](IW-Tools.txt) | Code the AI can use to check worlds and handle reusable content, if it can run Python. |

You do not need to upload everything at once. If your AI cannot run the checks, you can use the [web checker](https://iw-builder.github.io/checker/) yourself and paste the results back into the conversation.

`sources.json` records which files went into each package; you can ignore it during normal use.

[Back to the main guide](https://iw-builder.github.io/guide/)
