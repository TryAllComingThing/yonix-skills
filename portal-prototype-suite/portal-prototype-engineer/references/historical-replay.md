# M2 historical replay protocol

1. Read the actual historical bad and known-good files, fingerprint both.
2. Assert the bad-state signature; if missing, report NOT_REPRODUCED, never PASS.
3. Apply a **diagnostic candidate** to a temporary copy or replay the historical change with explicit provenance.
4. Execute browser/computed-style/interaction checks on bad and candidate where feasible.
5. Report DETECTED, REPAIRED_VERIFIED, PATCH_REPLAY_VERIFIED, BLOCKED, NOT_TESTED separately.
6. Store screenshots, JSON results, command and environment. Never alter original versions.
7. Use unknown project blind tests before claiming generalized autonomy.

Historical patch replay demonstrates reproducibility of an existing fix, **not** that the Skill autonomously discovered the fix. Source detection alone demonstrates neither functional repair nor visual equivalence.
