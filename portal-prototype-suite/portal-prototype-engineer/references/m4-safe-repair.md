# M4 guarded autonomous diagnosis and repair

## Scope and safety contract

M4 implements a narrow, **source-aware candidate repair** workflow. The skill may propose a patch and run browser acceptance but **must not auto-merge to a production branch**. `CANDIDATE_VERIFIED_REVIEW_REQUIRED` is not a release status.

1. Capture a screenshot with fixed viewport, page state, scroll and theme; user-provided red rectangles require explicit ROI coordinates, not inferred red-pixel detection.
2. Locate DOM target by ROI center and geometry; record computed CSS and text.
3. Trace to **unique static source**. For static text, require exactly one leaf node, exclude controls and script/style. For CSS, require one source rule and one property declaration. Reject ambiguous matches.
4. Create a separate candidate file. Never overwrite source; preserve source SHA256.
5. Run before/after Chromium with identical setup and capture screenshots, computed styles, JS errors, and overflow.
6. Report before/after/diff and structured evidence. Require human review and full project regression before release.

### Explicit limitations

- No OCR/red-box segmentation, source maps for dynamically generated DOM, Vue SFC source tracing, or general-purpose CSS causality analysis.
- Source edit for HTML supports only exact static leaf elements. Generated JS/templated text is **blocked**.
- Shared CSS selector changes require `--allow-shared`, and all affected component instances need further acceptance in the host project.
- Theme-color changes are only accepted if computed color actually changes in the supplied theme; the token's correctness across eight themes must be checked separately.
- A pixel diff proves an observable difference, not the semantic correctness of a fix. The tool does not check unrelated user journeys.
- Input `--setup-js` executes trusted local code. Do not pass untrusted user-provided JavaScript.

### Example

```bash
python scripts/diagnose_repair_verify.py \
  --input tests/fixtures/warehouse-operations.html \
  --intent remove-text --target-text '仅供演示' \
  --region '{"x":270,"y":210,"width":90,"height":20}' \
  --output /tmp/warehouse-candidate.html --evidence-dir /tmp/m4-evidence
```

ROI must be measured against the actual rendered target, not guessed from this illustrative command. For other tasks, use `--intent theme-color --selector .action --property background-color --replacement 'var(--brand)'` with a matching theme state.

### Gates

- `BLOCKED`: no candidate or unsafe source match.
- `CANDIDATE_FAILED`: candidate created but browser acceptance failed; never merge.
- `CANDIDATE_VERIFIED_REVIEW_REQUIRED`: limited browser check passed; reviewer must approve and run full regression.
