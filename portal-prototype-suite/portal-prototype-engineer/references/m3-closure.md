# M3 capability closure contract (V1.2)

## Theme runtime checks
Input: theme identifiers, actual switch callback, selectors, computed-style properties, expected semantic values, viewport/state. Pass only when each contracted element is visible, computed values meet expectations, and browser reports no errors. Invariance is only a failure when the contract explicitly requires variation; white card backgrounds may legitimately remain white in seven light themes. Record CSS tokens and expected palette from the project's design authority. Pixel screenshot review and interaction state coverage are separate gates.

## Screenshot → DOM
User provides screenshot and target region. Align screenshot dimensions, browser zoom, viewport, device scale, scroll and page state. Browser tool ranks DOM candidate boxes; review text and bounding boxes, then map to actual source code with repo search. If ambiguity remains, ask for selection or obtain better evidence. Never delete code from a candidate list without confirming the component and usages. Red-box extraction is not currently implemented.

## Three-way merge
Require an actual common ancestor. Compare base, ours and theirs hashes. Run true merge and refuse to write output if conflict markers exist. Clean textual merge is a candidate, not a functional acceptance; run build, interaction, themes, screenshots, and user review. No direct modification of either branch.

## Cross-project generalization
Keep MaaS cases as training/replay; test on unrelated industry, framework and layout. An author-created warehouse fixture is a controlled cross-domain test, not a blind evaluation. Blind test requires independently supplied unseen project and independently scored acceptance criteria. Negative controls must fail when a fixed brand color is introduced or a merge conflict exists.
