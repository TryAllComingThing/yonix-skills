# Acceptance matrix
| Dimension | Example assertion | Evidence |
|---|---|---|
| Product | required field and action correct | page/interaction contract |
| Layout | component bounds, alignment, overflow | browser bounding rect |
| Typography | computed font sizes and hierarchy | computed style |
| Theme | affected controls use semantic colors | multi-theme screenshots/computed styles |
| Language | all labels localized and layout intact | language permutations |
| Interaction | click, copy, close, submit, navigate | Playwright assertions |
| Visual | screenshot difference within reviewed tolerance | baseline/current/diff PNG |
| Accessibility | focus, keyboard, labels, contrast | axe/manual report |
| Delivery | canonical baseline and hashes | manifest |

Set scope by risk: modified shared components require broad matrix; local text change needs targeted route/languages. Always distinguish total combinations, executed combinations, failures and skips.
