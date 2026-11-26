# Portal interaction and Mock expert
## Mock contract
Define object schema and IDs; seed deterministic data; model transitions (idle/loading/success/error/empty/disabled); connect state across cards, detail and user center; specify persistence (memory/localStorage) and reset path; label simulated actions and never claim backend success.
## Behavioral acceptance
Every visible actionable control must have an observable outcome: route, dialog, copy, filter, validation, update, notification or disabled rationale. Form actions require validation and cancellation semantics. Modal must close by explicit control and Escape when appropriate, with focus restored. Filters and pagination must update visible results. Show loading/error feedback when workflow warrants.
## Demonstration protocol
Provide reset-to-seed, a 3–5 minute scripted journey, negative case, state snapshots and an offline fallback. Avoid secrets and real keys in fixtures.
## Anti-patterns
Fake clickable buttons, unlinked detail data, arbitrary counters, mock quota presented as actual, successful save without state update, localStorage leakage between tests.
