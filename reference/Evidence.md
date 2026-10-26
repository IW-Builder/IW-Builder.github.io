# Compatibility and evidence

This is an independent, unaffiliated kit. Platform baseline: Infinite Worlds' October 8, 2026 "Save/load system, Image style system and Pawscript update," with editor/runtime information consolidated through October 26, 2026. Export schemaVersion is 2.4. Kit version is 1.6.0; the structural profile is 1.2.0. Neither is an IW application version. The unaffiliated Script Library source snapshot is version 3.16, October 16, 2026; source details and updating advice are in ../library/Integration.md.

Use four evidence labels when a distinction matters. Ordinary reference sentences do not need a repeated tag.

| Label | Meaning |
| --- | --- |
| [DOCUMENTED] | Supported by editor help, a native export shape or cited language documentation. Does not alone establish runtime behavior. |
| [RUNTIME] | The stated behavior was exercised in IW within the described scope. |
| [PATTERN] | An optional authoring design assembled from supported features; not a platform requirement. |
| [UNKNOWN] | A concrete behavior remains unresolved; avoid depending on it without a focused check. |

These rules apply throughout the kit and are not repeated in each entry:

- Observed sizes, counts and caps (text lengths, Scenario counts, input counters) are working examples, not platform maxima.
- A tested feature does not certify every composition built from it; test new combinations in play.
- Rendered panels (Active instructions, debug, Secret Info, narration) show what IW displays, not the complete prompt or hidden engine state.
- Credits are not token counts.

Structural validation is a separate status, not a fifth evidence label. It checks export structure and explicit references. Static lint reports likely mistakes; neither executes PawScript or certifies a story. The example index records structural and runtime scope separately. Do not present generated prose as evidence of tracker state.

## Current result hierarchy

[Notable-Findings](Notable-Findings.md) is the plain-language summary. [Verified-Behavior](Verified-Behavior.md) consolidates detailed conclusions, [Editor-UI](Editor-UI.md) separates editor guidance from observed behavior, and [Known-Limits](Known-Limits.md) records unresolved boundaries. User-confirmed behavior is identified where it is the basis. Do not promote an unknown mechanism to fact or repeat superseded open questions from older examples as current conclusions.

---

END OF DOCUMENT: reference/Evidence.md
