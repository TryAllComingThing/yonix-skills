# Quality gates
P0: broken core flow, security/privacy violation, data/permission misrepresentation, corrupt baseline, required tests failing. P1: major visual regression, nonfunctional visible action, missing required state/language. P2: minor spacing/copy defects.

Required evidence levels:
- Static: source parse, lint/types/build where available.
- Runtime: page loaded without errors, key DOM visible.
- Interaction: actual click/input/navigation/clipboard/submit and assertions.
- Visual: before/after screenshots compared by pixels and reviewed.
- Accessibility: keyboard focus, labels, contrast, axe if available.
- Integration: actual backend contracts and responses.

These levels are independent. Visual pass cannot be claimed from runtime pass. Check empty/loading/error states and reduced-motion where relevant. Record skipped tests and rationale. Fail closed for P0; do not assert real integration from mock responses.


M2 release gate: an old-version/known-good comparison is PATCH_REPLAY_VERIFIED, not AUTONOMOUS_REPAIR_VERIFIED. A source marker is a static detection only. Browser probes must record selector, computed style, page route, theme, language, viewport and screenshot. For a source diff spanning unrelated changes, mark attribution as limited. A failed prerequisite blocks release rather than being ignored.
