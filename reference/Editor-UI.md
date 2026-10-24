# Editor and UI reference

Current through 2026-10-23. This covers observed authoring, play and troubleshooting surfaces, not every menu. [DOCUMENTED] means editor guidance; [RUNTIME] means observed behavior. Unlisted fields are not necessarily unsupported.

## Terminology for users

Use tracker and trigger **Names**, not IDs, unless the user requests IDs. Distinguish duplicate Names by purpose/editor location. Keep IDs for internal wiring and preserve them during edits. Use variable handles when explaining code. Say **Scenarios**, never ambiguous Conditions, for reusable narrative situations. Call a character's Brief Summary **Summary**.

| User/editor term | JSON mapping or distinction |
| --- | --- |
| Tracker Name | `trackedItems[].name`; not `id` or `variableName` |
| Trigger Name | `triggerEvents[].name`; not `id` |
| Scenarios; Triggering situation / Manage Situations in the selector | Root `conditions`; referenced by `triggerOnEvent` |
| Trigger conditions | `triggerConditions`; gates within a trigger |
| Summary; Brief summary in Other Characters | `one_liner` in current exports; do not invent a `oneLiner` alias |
| Character detail | `detail` |
| Extra instruction blocks | `instructionBlocks`; explain before abbreviating EIB |
| Give information to AI | `effectGiveInfo` |
| Tell the AI what should happen next turn | `effectTellAIWhatToDo`; distinct from Give information |
| Change other characters / Change other character data | `effectChangeOtherCharacters`; picker/panel labels differ |
| Trigger at start of game / Or mid-game | `triggerOnStartOfGame` / `triggerMidGame` |
| Allow triggering multiple times | `canTriggerMoreThanOnce` |
| Hide this item even in Storyteller Mode / Extra-hidden | `hidden_boring` or `ai_only_boring`; display filtering |
| Change starting values of Tracked Items (if applicable) | `allowChangeCharacterItemValues`; character-selection permission |
| Custom Evaluation / Description / Summarisation | `evaluationRequest` / `descriptionRequest` / `summaryRequest` |

## Import, export and preserving work

1. Open **Show optional features > Misc advanced features > Show raw JSON**.
2. To export editor changes, **Refresh raw JSON** then copy/export the whole value. The box does not track native field edits automatically.
3. To import, replace the whole raw value and select **Import JSON to world**. Accept the intended overwrite, acknowledge success, and wait for the editor to rebuild itself.
4. After rebuilding, reopen optional/raw sections and refresh/export if needed. Do not refresh the old editor immediately after import or refresh a pasted source you intend to import.

[RUNTIME] Import can persist independently of a later Discard changes action. Keep a backup. Check target dropdowns and Scenario bindings after import; preserved text is not proof of valid references. Tracker IDs can be regenerated without remapping their references.

[RUNTIME] Narration can stream before background work finishes. Following interruption, inspect retained state and controls before submitting again; a temporary turn number is not a saved-turn guarantee.

## Triggers and Scenarios

An ordinary trigger with no conditions says it will never fire. This is not unconditional execution; Start-gated triggers and explicit random dispatch differ. Empty effects do no work but eligible triggers can still record firing.

Start mode changes the picker and compatibility warnings. Start-only disables Repeat in the editor; Or mid-game enables it. Stored unsupported combinations may survive import while effects are ignored. Read the [trigger capability catalog](Trigger-Catalog.md) before declaring an operation unavailable.

A mismatched Scenario shows **Select a situation** while the JSON keeps its string. The Situations manager's Add control stops at ten entries. Binding rules and limits are in [Triggers.md](Triggers.md#scenarios).

## Trackers, visibility and customization

**Menu > Settings > Storyteller mode** toggles the mode, rather than opening a status dialog; enabling asks for confirmation. **Menu > Settings > World debug tools** contains Include Extra-hidden. Reopen panels after changing this setting if they still show old content.

| Surface | Observed behavior |
| --- | --- |
| Hidden Tracked Items, Storyteller on, Include Extra-hidden on | Extra-hidden values displayed |
| Hidden Tracked Items, Storyteller on, override off | Extra-hidden omitted; ordinary hidden values remain |
| Tracker editing dialog, Storyteller on, override off | Extra-hidden still visible/editable |
| Storyteller off | Player-visible values remain; live tracker editing control unavailable in the observed UI |

Neither hidden nor extra-hidden protects information from Storyteller inspection. Visibility and automatic-update rules are in [Trackers.md](Trackers.md).

For per-character values, select **Initial value depends on which character the player chooses** under Tracked items, then edit under **Player character options > [Name]**. Player-selected preferences can appear on the character card and in Customize Character. Opening the customizer can reset card selections; check final values there. Starting-value permission is not general in-play edit permission.

Rename warnings offer **Update** and **Ignore** for a variable-name mismatch; Ignore preserves the handle and ID. When acknowledgement is needed is covered in [Trackers.md](Trackers.md). Initial-value changes do not migrate running state; edit current tracker values for that.

## Play, debug and live design

The database icon opens trackers; the nearby edit control edits their values. The pencil opens action/outcome editing and **View/edit world design**. Regenerate turn opens modification of an existing turn. These operations have different purposes.

The bug icon opens debug. **Active instructions** is live rendered state, including post-narration trigger updates and live edits, not the full historical prompt. A trigger badge/list is not always exhaustive; inspect detailed history and actual state.

**PawScript > Open in Sandbox** uses the historical data that script ran against. It can differ from current manually edited values. A run displays a result/diff; **Update Game** is separate. A collapsed summary can misrepresent nested structure; inspect actual values or supported reads.

The live-design notice warns that Player/Other Character changes do not affect the current playthrough; live copies are covered in [Import-Integrity.md](Import-Integrity.md). Runtime block replacements and tracker changes can leave original content/initial values in design exports; those exports are not complete live-state snapshots.

Story exports offer a turn range and optional background, character, secrets, trackers and hidden trackers, with text/PDF/image options. Select the relevant options. Secret Info is generated narrative data, not an authoritative character database. No live character-database or complete prompt viewer is available through these surfaces.

An unchecked **Hide skill system** option may omit `hideSkillSystem` from the editor export. This is normal visible-skills state, not a missing setting to repair. Generated JSON may explicitly use `false`.

## Characters, images and models

Other Characters separates Summary, Character detail, narrative appearance and image appearance/clothing. Help says Summary is available before full detail, with detail available from the turn after name/location mention. Repeat essential Summary facts in detail. Location guidance asks for no more than two words; Full list of names accepts comma-separated variants. Unchosen player options are not automatically NPCs: add Other Characters when they should exist in the story.

The illustration wrench opens **Illustration details**. Character fields: Appearance, Clothing, Expression/position, Setting. Scenery fields: Appearance, Setting. **Edit details > Save changes** immediately generates an image; it is not a text-only save. **Settings > Illustration options** supports one, two or three alternatives; automatic generation is separate.

Image style has Character/Scenery start/end prompts, mapped to `imageStyleCharacterPre/Post` and `imageStyleNonCharacterPre/Post`. Retained `illustrationStyle*` fields are not current controls. Full image prompts and cache identities are hidden.

**Misc advanced features > Enable AI-specific instruction blocks** exposes block model choices mapped to `selectedAIProfiles`. All-model blocks remain active during model switches; filtered blocks follow the selected model. Availability changes; imported unfamiliar IDs are not automatically invalid.

## Specialist instructions, forms and PawScript cues

[DOCUMENTED] Description includes length guidance, but exact length control remains unreliable. Video help describes `$videoDuration` and `$videoStyle` in video context (see below).

Misc advanced features can show PawScript Expression Editor buttons. Missing icons do not prove lack of support: YAML Set a value supports template expressions according to help despite having no icon. This is not an exhaustive icon inventory.

Present choice enforces required selection and configured multiple-selection bounds. Required Request Input can leave Confirm enabled while empty, then reject submission with **Please enter a response**. Optional blank input clears its target. Single/multiline fields show counters of 600/3000 respectively, not universal tracker limits. Newline-delimited multiple selections remain text, not automatically a YAML list.

Trigger-provided next-turn guidance can disable the Storyteller guidance box while leaving ordinary action input usable. Ends game can offer **Continue game**, depending on its flag. Without continuation, history and regeneration can remain available.

## Permissions and specialist destinations

These mappings describe the observed editor controls, not an exhaustive account-role entitlement matrix.

| Editor control | JSON field | Scope |
| --- | --- | --- |
| Change character name | allowChangeCharacterName | Starting-character customization |
| Change character description | allowChangeCharacterDescription | Starting-character customization |
| Change character skills | allowChangeCharacterSkills | Starting-character customization |
| Select other portraits from that character's gallery | allowChangeCharacterPortrait | Existing portrait choices |
| Create a new portrait | allowChangeCharacterNewPortrait | New portrait creation permission |
| Change starting values of Tracked Items | allowChangeCharacterItemValues | Applicable character-scoped starting values |

[DOCUMENTED] These switches belong to character customization. They are distinct from `permissionsOnceShared.sharing` and `.editing`, and from Storyteller mode. Cross-account author/recipient permission enforcement has not been verified; do not infer that sharing or editing grants live-state access. Keep these settings separate when diagnosing a missing control.

[DOCUMENTED] Custom Evaluation guides the AI's interpretation of the attempted action. The default includes skill/difficulty reasoning and labels such as SUCCESS and PARTIAL_SUCCESS; those labels are generated evaluation content, not direct state-changing commands. Custom Description guides narrated results. Custom Summarisation guides what the memory summary retains; it is not a viewer of the actual summary. Native specialist placeholders are context-specific and are not all PawScript tracker handles.

[DOCUMENTED] Video prompt instructions are under the optional specialist settings. From an illustration's Generate video dialog, prompt preparation has three destinations: scene plan, first/last-frame decision and video-AI prompt. Editor help says each can be overridden independently, a blank field retains its default, and expressions are evaluated before sending. `$videoDuration` and `$videoStyle` are documented in this destination. No current JSON key mapping or runtime precedence is certified for these controls; inspect a native export before editing them programmatically. Video creation and cross-role access remain unverified.

## Troubleshooting by visible symptom

| Symptom | First check |
| --- | --- |
| JSON does not reflect a field edit | Refresh raw JSON after completing the edit. Do not refresh over a pasted import. |
| Imported trigger target is unassigned | Compare the target tracker by Name and inspect source/import ID references; normalization can leave dangling targets. |
| Scenario selector is empty while JSON retains text | Match the declared Scenario exactly, including case, punctuation and whitespace. |
| Character choice changes on entering customization | Check the choice again inside Customize Character; card selections have been observed to reset. |
| Extra-hidden item appears unexpectedly | Distinguish the display panel override from the tracker editing dialog, which still exposes it in Storyteller mode. |
| Form answer exists but later values are blank | Check trigger order and the answer's stored type/domain; consuming triggers must follow the form. |
| Trigger history shows firing but accepted state is unchanged | Inspect script failure/rollback and an explicit completion flag; firing is not successful commit. |
| Reload shows an earlier turn | Inspect retained history/export and controls before retrying; streamed output does not prove persistence. |

Input counters, the Scenario creation cap and retained text sizes are observations, not platform maxima. Additional roles, full prompts, live character records and video runtime remain reference gaps.

---

END OF DOCUMENT: reference/Editor-UI.md
