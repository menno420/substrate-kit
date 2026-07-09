# Session 2026-07-09 — run-2 harness prep: score_m1 artifacts + telemetry last-line shadowing

> **Status:** `in-progress`

**Scope (about to do):** the run-2 harness-fix increment (ordinary auto-merge
lane — `bench/score_m1.py` and `src/engine/` are not bench pin paths).
(1) `score_m1.py`: stop the mutation regex matching read-only fd redirects
(the `2>/dev/null` artifact that tainted ON-T2 / OFF-T4 M1), and skip
tool_use events whose paired tool_result is an error (the OFF-T5
failed-Edit-counted-as-first-mutation artifact) — regression tests for all
three run-1 artifact cases; run-1's recorded results stay untouched
(append-only law; the row already says M1 unmeasurable).
(2) `src/engine/loop/telemetry.py`: fix the model-line harvest taking the
LAST needle-bearing line even when it is prose that merely mentions the
marker (found live in websites#31) — prefer the last line that parses
validly; regression test; dist regenerated (byte-pin).
(3) B4 ledger: flip the score-m1 idea to shipped, file the websites-surfaced
control-board kit-readiness-cell idea, record the arm-card investigation
disposition on the checker-false-red idea.
(4) `control/status.md` heartbeat as the closing act of the same PR.
