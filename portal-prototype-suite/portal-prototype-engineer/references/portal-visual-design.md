# Senior Portal UI/UX — decision framework
## Visual decision sequence
Understand brand and user intent → choose IA and navigation (top nav, side nav, contextual tabs) → define page hierarchy → select layout primitives → map to existing tokens → review component states → check responsiveness and accessibility.
## Decision heuristics
- Hero is appropriate for first-visit discovery and service value; avoid oversized hero on frequent-use workspaces.
- Use cards for comparable services and discovery; use lists/tables for high-density comparison. Preserve a clear CTA and predictable metadata.
- Use persistent sidebar only when depth and task switching justify it. Do not add two parallel nav systems without distinct roles.
- Establish heading scale, reading width, spacing rhythm and consistent card heights; prefer semantic tokens over hardcoded colors.
- Empty, loading, error, disabled, success and confirmation states are part of high fidelity, not optional polish.
- At narrow viewports, preserve action reachability, text legibility and keyboard focus. Check actual computed styles for each theme.
## Design review rubric (0–4 each)
Information hierarchy, navigation clarity, typography, spacing/layout, component consistency, responsive adaptation, state feedback, accessibility. Report scores with observable evidence and prioritized changes; no unsupported numeric score.
## Negative cases
Large headline with weak content hierarchy; duplicate icons on actions; CSS `!important` layering; low-contrast code blocks; inconsistent modal close buttons; deleted labels leaving dead click areas.
