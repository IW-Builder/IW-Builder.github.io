# Unresolved boundaries

Current through 2026-10-26. This is the kit's single list of platform behavior that remains unverified; other files state only what is established. Verified conclusions are in [Consolidated behavior](Verified-Behavior.md); workflows are in [Editor and UI](Editor-UI.md).

| Area | Established | Still unknown | What to do meanwhile |
| --- | --- | --- | --- |
| Prompt construction | Active instructions shows live rendered templates and updates | Full historical storyteller/specialist prompts, hidden wrappers, exact inclusion and timing | Put essential facts in fields known to reach the storyteller (background, firstInput, instructions, always-on blocks); treat UI visibility as display, not proof of what the AI receives |
| Scenarios | Exact literal binding works; imported registries larger than ten persist and execute | Why dynamic multi-slot, cyclic and parallel arrangements fail; any runtime maximum | Use literal Scenarios with explicit state gates ([Triggers.md](Triggers.md#scenarios)) |
| NPCs and knowledge | Same-name player retrieval of authored facts; dedicated image fields have observable effects | Live character records, identity merging, mutation and retrieval routing; why name-only mentions often fail to surface Character detail; Secret Info is not a database | Put facts that must surface in the Summary or always-on text; author relationships and knowledge explicitly; correct an invented detail early by editing the turn |
| Import normalization | ID reminting, field omission, scope normalization and registry population observed; missing tracker description breaks the rebuild | Internal failure stages; ID rules for every entity type; why an omitted replaceWith broke the opening | Use ASCII alphanumeric tracker IDs; always serialize description and replaceWith; re-export after import and compare with tools/import_audit.py |
| Visibility | Extra-hidden values remain inspectable; AI-only automatic updates work | Whether visibility changes what the AI receives | Do not rely on visibility to keep information from the storyteller |
| Interpolation | Direct templates, installed snapshots and deferred `<<=...=>>` references behave differently | Timing in other destination fields; full specialist inputs | Use the template probe example before relying on a new field ([Capabilities.md](Capabilities.md)) |
| Randomness and selectors | Independent evaluations can differ; cached choices agree | Exact evaluation counts; whether unselected library text is excluded | Store a shared roll in a tracker when several consumers must agree |
| AI tracker dependencies | Same-turn dependent values can be available | How generation is staged internally | Stage prior-turn values explicitly when a rule depends on them |
| Format and YAML | Manual and script writes can bypass expectations; coercions occur | Complete grammar, XML mutation, strict typing, hidden AI repair | Validate shape and meaning in scripts before accepting state |
| Legacy list context | current() is rejected in Run Script | A supported List Update target/value context in the current editor | Use for-each loops and collection methods instead |
| Memory | Summary compression every six turns from turn eight (user-confirmed); later recall occurs | Summary contents and how they weigh against persistent context | Use summaryRequest and trackers for facts that must persist |
| Length | Strong override wording does not reliably lengthen narration | A reliable length recipe or hidden maximum | Describe the desired length in authorStyle; do not promise exact length |
| Images and video | Current wrappers and dedicated image fields affect results | Full image prompt and cache, precedence, internal macros, video runtime | Author with current style controls and preserve imported legacy fields; avoid depending on video until checked |
| Limits and permissions | Large text retention and separate startup customization established | Maximum field, loop or trigger sizes; account-role permission matrix | Treat observed sizes as working examples |
| Recovery and forms | Interrupted generation can leave a turn unretained but charged; a turn with two input forms once failed to persist | Server-side cause and automated recovery | After an interruption, inspect retained history and the export's turn count before resubmitting; prefer one input form per turn |

The schema and validator are a partial compatibility profile.

---

END OF DOCUMENT: reference/Known-Limits.md
