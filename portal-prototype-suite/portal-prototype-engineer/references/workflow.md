# Workflow and decision gates
G0: locate repo/HTML, identify authority and hash; enumerate unresolved branches. G1: scope page/component/state and acceptance. G2: review design tokens and reuse options. G3: implement minimal patch. G4: verify functionality, visual, accessibility and relevant permutations. G5: review risks. G6: package evidence and report.

## Decision table
| Request | Required inspection | Minimum validation |
|---|---|---|
| Screenshot deletion | image region, DOM source, all render paths | target absent, neighbors preserved, no broken interactions |
| Text/translation | localization dictionary and fallback | all supported languages, no stale duplicates |
| Theme | token source, hard-coded colors, computed CSS | affected components in every supported theme |
| Dialog | dialog state, focus, close and save handlers | open, close, escape, focus, submit, responsive |
| API docs | protocol contract, layout, code snippets | section routing, code validity, dark/light contrast |
| Cross-version merge | base/current/desired hashes and diffs | conflicts resolved, tests for both change sets |

Do not treat an absent feature as a failure unless required by contract. Unavailable test infrastructure is `NOT_RUN`, never `PASS`.

## M3 verification escalation
For any theme defect, run computed-style theme contracts; for annotated screenshots, obtain DOM candidates and source mapping before modification; for divergent branches, run three-way merge with explicit ancestor; for generalized Skill claims, test on an independently supplied unseen application. See `m3-closure.md`.
