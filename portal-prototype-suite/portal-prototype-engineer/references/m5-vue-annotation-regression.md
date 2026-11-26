# M5 Vue tracing, red-box extraction, and regression matrix

## Security and evidence boundaries
1. Use red annotation detection only on screenshots with a red rectangular outline; multiple or missing boxes block unattended selection. Screenshot resolution and scroll offsets must match browser.
2. Vue DOM source tracing uses runtime `__vueParentComponent` and development `__file`; production builds may omit both. A file match is **component-level** evidence, not exact source line mapping. Dynamic expressions, slots, Teleport, Suspense, and compiled templates require further tracing. Never patch on a guessed match.
3. Runtime regression matrix executes page × theme cases. All configured pages/themes/selectors must pass; optional pixel baseline files are mandatory for visual-regression claims. Stable fonts, animations, data and viewport are the caller's responsibility.
4. Read-only diagnostics by default. Any proposed source change must be reviewed and tested before merge. Preserve the V1.3 guarded repair rules.

## Commands
```bash
python scripts/detect_red_annotations.py --image annotated.png --output region.json
python scripts/trace_vue_dom.py --url http://localhost:5173 --selector '[data-testid="save"]' --project . --output trace.json
python scripts/run_regression_matrix.py --contract tests/scenarios/m5-matrix.example.json --output-dir evidence/matrix
```

## Acceptance
- M5-A red outline: exactly one region, positive and ambiguous negative tests.
- M5-B Vue trace: dev component owner path verified; production metadata absence blocks source assertion.
- M5-C matrix: page/theme cross-product, browser errors and selector assertions, screenshots; visual baselines separately required.
- M5-D independent Vue 3 project: not covered by HTML fixture. Requires a real Vue runtime and a distinct project supplied for blind acceptance.
