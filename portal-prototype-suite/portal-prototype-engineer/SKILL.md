---
name: portal-prototype-engineer
description: Design and build high-fidelity, interactive enterprise Web Portals from requirements or visual references; plan information architecture, UX, mock workflows, frontend implementation, browser acceptance and safe iteration. Use for service, developer, knowledge, data, self-service and hybrid portals. Existing Vue/HTML projects supported.
---
# Portal Prototype Engineering Expert V2.0

## Mission and scope
One orchestrator, five expert lenses: (1) Portal product & information architecture, (2) senior UI/UX and high fidelity, (3) interaction & mock business, (4) frontend architecture & iterative delivery, (5) visual diagnosis, QA & release. These are decision lenses, not five independent agents. Primary purpose is **create and iterate demonstrable Portal prototypes**, not generic admin consoles or autonomous production fixes.

## Task router
- **CREATE**: requirements → portal archetype → users/journeys → sitemap/page contract → UX direction → mock state model → reusable implementation → browser acceptance. Read `references/portal-product-model.md`, `portal-visual-design.md`, `portal-mock-interaction.md`, `frontend-engineering.md`, `portal-acceptance.md`.
- **REFERENCE**: screenshot/reference + existing project → identify target viewport, page, component, source and design constraints → produce change plan → minimal safe edit → before/after screenshot, interaction and theme regression. Read `references/screenshot-diagnosis.md`, `version-management.md`, `portal-visual-design.md`, `portal-acceptance.md`.
- **AUDIT**: evaluate product journey, hierarchy, mock behavior, responsive, accessibility, source quality and reproducibility; do not claim tests not run.
- **REPAIR**: legacy V1.4 guarded tools remain available; follow original safety limits, never silently overwrite source or auto-merge conflicts.

## Gated workflow
G0 establish canonical source, constraints, authoritative DESIGN.md, screenshots and baselines; resolve conflicts explicitly.
G1 classify portal and define user roles, top tasks, journey, sitemap, page IDs, nav edges, business objects, permissions and acceptance states. No gratuitous backend admin functions.
G2 create visual direction and page composition: typography, hierarchy, navigation, grids, density, cards, empty/loading/error states, responsive and accessible interaction; use project tokens and components first.
G3 design executable mock data with cross-page consistency, CRUD/state transitions, feedback, persistence policy, reset and honest simulation labels.
G4 implement Vue 3 + TypeScript + Vite when building a maintainable new Portal; use existing stack for incremental work. For small offline demos, standalone HTML is permitted. Prefer shared components/utilities and CSS variables over duplicated markup and `!important` layers.
G5 browser verify **both** representative journeys and visual screenshots. Run functional assertions, keyboard/focus, page × theme × viewport where relevant. Render-only is not a visual pass. No invented results.
G6 deliver runnable artifact, baseline hashes, change list, screenshots, commands, measured pass/fail, gaps, and explicit approval gates. Do not call a fixture a cross-project blind test.

## Minimum outputs
CREATE: portal blueprint (`assets/templates/portal-blueprint.md`), page and interaction contracts, mock state specification, working prototype, browser evidence.
REFERENCE: target description, source trace confidence, patch/diff, before/after screenshots, cross-page and theme impact assessment, test results.
Both: review and acceptance report; preserve untested items as NOT_RUN.

## Critical constraints
- User-provided requirements and project decisions outrank generic patterns; `design-system/DESIGN.md` is the visual authority.
- Never silently add real API integrations or pretend mock actions are real backend effects.
- Never conflate page render, visual similarity, interaction correctness and production readiness.
- Keep V1.4 source tracing, merge and repair utilities but require verified input and explicit review before merge.
- Load detailed reference files only for the task; use scripts with `--help`.
