# Six-role evidence-based review V1.1

This is a simulated expert-panel review, not signatures from external experts.

| Lens | Finding | Priority | Remediation |
|---|---|---|---|
| Product/prototype | Page contracts are minimal and do not enforce negative scope | P1 | Explicit acceptance and non-goals |
| UI/UX | Theme audit checks only variable existence, not computed styles | P0 | Runtime theme matrix with computed-style assertions |
| Frontend | Regex CSS inventory cannot safely remove overrides | P0 | Diagnostic-only; source-located changes and A/B validation |
| Screenshot diagnostics | No visual-to-DOM localization algorithm | P1 | Human-confirmed selector and screenshot evidence |
| QA | Sample fixture smoke tests are not historical replay | P0 | Historical version comparison, browser probes, failure injection |
| Codex/configuration | No automated merge-guard against divergent baselines | P0 | Fingerprint comparison, conflict BLOCKED, explicit merge plan |

## Decision
Keep one orchestrator and five capability references. Do not create additional agents. Scripts must distinguish DETECTED, REPAIRED, VERIFIED, BLOCKED and NOT_TESTED. Never equate reproducing a historical patch with autonomous repair. Do not modify historical originals. Test only with explicit copies and reproducible evidence.
