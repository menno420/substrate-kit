# 2026-07-20 · check_no_false_walls P2+P3 detector hardenings

> **Status:** `complete`

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

- **📊 Model:** Opus 4.8 · high · runtime bugfix

Run type: owner-directed (fm ORDER 048 standing resume + coordinator dispatch).

## What shipped

- **`src/engine/checks/check_no_false_walls.py`** — two hardenings:
  - **P2:** added `_CAP_FAMILY_PATTERNS` / `_capability_families`, and gated the
    wrapped-lookback branch of `is_cleared` so it bridges only when the prev-line
    trailing clause names the SAME capability family as the current wall (or names
    none — a genuine continuation). A `different_capability` (disjoint families)
    prev clause no longer clears the wall.
  - **P3:** added `match_blocklist_all` (all matches + spans); `scan_text` now
    grades each match independently and reports the first UNCLEARED one (≤1
    finding/line preserved). Clearing is position-aware: `_clause_at(line, idx)`
    grades the match's OWN clause, and `_false_quote_covers(line, start, end)`
    clears a match only when a `false "…"` quote SPANS it — so a genuine wall
    outside the quote on the same line is no longer masked. `match_blocklist`
    retained (delegates to `match_blocklist_all[0]`) for `explain_wall`.
- **`dist/bootstrap.py`** — rebuilt from engine source via `src/build_bootstrap.py`
  (1332987 bytes); currency test green (47 passed).
- **`tests/test_check_no_false_walls_leg.py`** — mutation-pinned BOTH directions:
  `_MUST_STAY_RED["p2_prev_line_repudiates_different_capability"]` +
  `_FP_CLEAR["p2_same_capability_wrap_clears"]`;
  `_MUST_STAY_RED["p3_genuine_wall_shares_line_with_false_quote"]` +
  `_FP_CLEAR["p3_lone_false_quote_wall_clears"]`; plus a ≤1-finding-per-line
  count-contract test. Verified by real mutation: neutering the P2 gate or
  reverting P3 to line-wide clearing each breaks a pinned test.
- **Verification:** full suite **2060 passed, 1 skipped**; `check --strict` clean
  except this card's by-design born-red HOLD; cold-adopt tree shows zero
  `false-wall:` findings from the change. Every existing
  `_MUST_FAIL`/`_MUST_PASS`/`_MUST_STAY_RED`/`_FP_CLEAR` invariant preserved.
- **CI diagnosis (coordinator flag):** the `Kit test suite` +
  `Cold-adoption smoke (adopt + check --strict)` check runs are TEMPORARY
  legacy-context ALIAS jobs (ci.yml §362-399: `needs: kit-quality`, conclude
  failure whenever kit-quality ≠ success). The real suite + cold-adopt smoke are
  STEPS inside kit-quality. On build SHA f050182 kit-quality reached its final
  session-gate step ("HOLD (by design)") — all prior steps green — so all three
  reds trace to the single born-red hold and clear at this flip.

- **💡 Session idea:** **`check_wall_families` advisory — surface the capability
  family a red wall names, and (when a nearby line repudiates a DIFFERENT family)
  print "did you mean to clear <family-B> but the wall is <family-A>?".** This
  session's P2 fix silently keeps a cross-capability repudiation from bridging;
  an adopter who *intended* the repudiation to clear the wall gets a bare red with
  no hint that the mismatch is capability-family, not phrasing. A never-exit
  advisory that names both families turns a confusing red into a one-glance fix —
  the same friction→guard instinct as the dateless-wall / inline-date advisories,
  aimed at the family-mismatch gap this fix deliberately enforces. Deduped against
  the inline-date advisory idea in #549's card (that flags section-vs-inline-date;
  this flags capability-family mismatch on a wrap).

- **⟲ Previous-session review:** #549 (card `fix-false-wall-clearing-vocab`) was
  an exemplary close — it not only shipped the attachment-based rewrite but ran an
  ADVERSARIAL self-review that caught its own gate-blinding first cut AND recorded
  the two residual hardenings (P2, P3) precisely enough that this session could
  build them straight from the card with no re-derivation. That is the session
  chain working as designed. The one thing it left implicit: it labelled P2/P3
  "non-blocking" but did not say WHY they were safe to defer — both are
  *tighten-only* (they can only ADD reds, never clear a genuine wall), so shipping
  #549 without them could never blind the gate, only occasionally over-clear a
  contrived FP. Stating that safety rationale on the deferral would have saved this
  session re-deriving it. **System improvement:** a deferred-hardening note should
  carry a one-line "safe-to-defer because: <tightens only / advisory only / …>"
  tag, so the next session inherits the risk assessment, not just the task.

- **Doc audit:** no durable doc home is left stale — the change is engine source +
  dist + tests only; `control/status.md` heartbeat updated this session with the
  live wave table; CHANGELOG `[Unreleased]` carries the detector fix into the next
  cut. The residual adopter reds are resident-lane (captured in the heartbeat wave
  table + each PR body), not substrate-kit doc drift.

- **📊 Model:** Opus 4.8 · high · runtime bugfix
