# Bring the kit into your chat

These text files let you use IW Builder with an AI that accepts attachments, even if it cannot browse the website or open a ZIP.

For web retrieval, an AI can open the [authoring guide page](https://iw-builder.github.io/chat/) directly, or start from the [homepage](https://iw-builder.github.io/) and fetch individual files listed in [llms.txt](https://iw-builder.github.io/llms.txt).

There are two kinds of file here. The **reference** is what the AI reads to do the work; attach it once. The **content to pick from** is examples, library modules and tools; attach a piece only when the AI asks for it.

## Reference: attach one file, or the numbered parts

| File | What's inside |
| --- | --- |
| [Complete Reference](IW-Complete-Reference.txt) | The whole reference in one attachment: over 300 KB, around 80k tokens. The simplest choice when your AI's chat accepts a file that size. |
| [Reference part 1](IW-Reference-1.txt) | Start here: the main prompt, starting template and the core guides to creating worlds. |
| Reference parts 2, 3 and up | The rest of the reference in reading order: exact world-file structure, PawScript, runtime, characters, recipes, notable findings, editor and UI workflows, cost, tested platform behavior, payload snippets and model IDs. The [file index](https://iw-builder.github.io/llms.txt) lists each part with what it holds. |

The parts exist for tools that cap attachment or fetch size around 100 KB: each is under 90 KB. They split the reference by size, not by topic, and the build adds a part when the reference grows, so attach all of them. Each part begins with a list of which documents are in which part. A model fetching by URL should use the parts or the individual files in [llms.txt](https://iw-builder.github.io/llms.txt), since most fetchers truncate the complete file.

The older editions (IW-Authoring-Guide.txt, IW-Technical-Reference.txt, IW-Behavior.txt and IW-Payloads.txt) were replaced by the parts on 2026-11-15; their links now hold a short pointer.

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
