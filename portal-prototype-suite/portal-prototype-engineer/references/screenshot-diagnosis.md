# Screenshot-driven diagnosis
1. Describe exact highlighted region, surrounding layout and intended change; ask only if ambiguous.
2. Identify route, state, viewport, language and theme from evidence.
3. Locate candidate DOM nodes using text, stable attributes, selectors and bounding boxes; do not assume first text occurrence is the rendered node.
4. Trace rendering source and CSS cascade, including media queries, overlays and duplicate renderers.
5. Determine change semantics: remove text vs block, move vs align, rename vs change action, cosmetic vs behavioral.
6. Implement minimal change and check all usages, routes, themes, languages and modal states.
7. Capture before/after images and computed styles, compare; document untested combinations.

Anti-patterns: blindly deleting all occurrences; hiding an interactive control with CSS; reporting screenshot parity from page-load checks; adding global !important overrides without tracing source.
