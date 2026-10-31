# Images, video and model-specific blocks

The export fields and editor controls for image style, portraits and video, and how instruction blocks are limited to particular storyteller models.

## Image style

The image-style editor is a reusable style with Name, Model and prompt wrappers. With separate character/scenery prompts enabled, Characters start/end and Scenery start/end add text before and after the respective image prompts; with it disabled, Start/End apply to every image. The export fields are imageStyleCharacterPre/Post and imageStyleNonCharacterPre/Post; a shared Start/End is exported by duplicating the values into both pairs, so no extra switch is needed. The imageStyle value is a generated identifier; preserve it rather than deriving it from the prompt text. A world export carries the style's values, not the reusable style itself.

The older illustrationStyle*LowPriority/HighPriority fields still occur in exports but have no current controls; preserve them in existing worlds and author with the current Pre/Post wrappers, which took precedence over them in testing. Manticore is the model that editor help recommends; its preset text includes IWBeautiful/IWUpscaleFace macros whose mechanism is undocumented. The player can override the selected style. The cover prompt is separate from these wrappers. Exact prompt assembly is hidden.

Dedicated Other Character image appearance/clothing populate Illustration details independently of narrative appearance. Edits change generated images and can be reversed; alias-related clothing drift can occur. Saving Illustration details generates a new image (about 4 credits).

PC portraitPromptDetails holds four strings: illustrAppearance, illustrClothes, illustrExpressionPosition and illustrSetting ([Payloads.md](../examples/Payloads.md) has an example). Image generation and upload produce asset references, which belong in portrait and preview fields. The library's Cover Image script produces a prompt, not an asset: use it in the image workflow, select or upload the result as the world preview, and export the resulting metadata. previewImage holds the asset reference, not prose.

When adapting library image-style text, resolve bracketed slots as deliberate choices: remove unselected alternatives and incidental sexualized defaults unless they match the requested audience and style, keep the neutral medium, composition, lighting and identity guidance, and pick one medium rather than a contradictory list.

## Video

videoPromptInstructions has videoPlan, videoImagePosition and videoPrompt strings: the library uses videoPlan to choose a beat, videoImagePosition to choose start/end anchoring, and videoPrompt to describe the clip. Its `$videoDuration` and `$videoStyle` references are video-context values, not declared trackers or general PawScript roots; confirm their availability in the video editor or debug context before adopting the sample. The kit has no video-enabled runnable example. Editor-side video controls are in [Editor-UI.md](Editor-UI.md#permissions-and-specialist-destinations).

## Model-specific blocks

Enable model selection per world under Show optional features > Misc advanced features > Enable AI-specific instruction blocks. Selected block models serialize in selectedAIProfiles. All-model blocks stay active while selected-model blocks follow the active model, including when the player switches model mid-game. Current-AI-Profiles.json lists each storyteller model's ID, underlying real-world model, isCurrent flag and typical credits per turn, including retired models, as of the date it records; models retire every few months. It is an authoring convenience, not a validator enum: accept historical IDs and preserve imported selections.

Disabling the option removes selectedAIProfiles from exported blocks and hides their controls; the still-open editor remembers the choices if re-enabled, but not after it is closed. A block name alone does not select models.

Per-model text inside one block, and per-model tracker update instructions, use `$game.ai_model` ([Recipes.md](Recipes.md#turn-state-patterns)). Per-model cost is in [Cost.md](Cost.md).

---

END OF DOCUMENT: reference/Images-and-Models.md
