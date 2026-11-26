# Portal acceptance — two equal-weight gates
## A: Requirement → new Portal
Verify (1) archetype, IA, complete journey, (2) design system and hierarchy, (3) functioning navigation and mock state, (4) empty/error/validation, (5) responsive + theme + keyboard, (6) runnable build, repeatable test and evidence.
## B: Screenshot → existing Portal revision
Verify (1) reference screenshot and viewport aligned, (2) intended region/source mapped, (3) scope-limited diff, (4) screenshot before/after and visual comparison, (5) affected actions remain working, (6) cross-page/theme regression, (7) baseline and rollback.
## Status taxonomy
PASS: asserted and observed. FAIL: asserted and violated. BLOCKED: cannot safely proceed (ambiguity/conflict). NOT_RUN: no execution evidence. PARTIAL: only specified subcoverage. Do not mark A or B PASS from a fixture alone when real-project blind testing is required.
## Severity
P0 broken core journey, unsafe destructive action, lost baseline or misleading real/mock claim. P1 major visual inconsistency, failed cross-page state, missing accessibility path. P2 polish.
