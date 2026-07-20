# 2026-07-20 · check_no_false_walls P2+P3 detector hardenings

> **Status:** `in-progress`

About to happen (opening declaration): land the two NON-BLOCKING follow-up
hardenings recorded in PR #549's session card
(`.sessions/2026-07-20-fix-false-wall-clearing-vocab.md`, "Known non-blocking
follow-up hardenings"):

- **P2 — wrapped-lookback punctuation-gated bleed (follow-up a).** The one-line
  wrapped-sentence lookback in `is_cleared` can bridge a repudiation from the
  previous line's trailing clause onto a wall on the current line even when the
  previous clause repudiates a **different** capability. Harden: the lookback
  confirms the prev-line clause's repudiation names the **same** capability
  family as the current wall phrase before bridging.
- **P3 — `match_blocklist` one-hit-per-line masking (follow-up b).** Clearing is
  graded on only the first hit per line, so a genuine standing wall sharing a
  physical line with a repudiated `false "…"` quote is masked. Harden: evaluate
  **all** wall matches on the line independently and position-aware (the
  `false "…"` quote clears only the match it spans), so a genuine wall on the
  same line still reds.

Preserve attachment-based clearing (#549) exactly; pin both the newly-caught and
the genuine-wall cases as test invariants; mutation-test both directions.
Kit-only: engine source + `dist/bootstrap.py` rebuild + tests.

- **📊 Model:** Opus 4.8 · high · engine-bugfix

Run type: owner-directed (fm ORDER 048 standing resume + coordinator dispatch).
