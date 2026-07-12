# 2026-07-12 — gate multi-card shadowing: ground-truth verify + idea-file reconciliation

> **Status:** `complete`

- **📊 Model:** Claude (Fable family) · gate-integrity verification lane

## Scope (what is about to happen)

Verify against ground truth that the HIGH gate-integrity bug in
docs/ideas/gate-tail1-multi-card-shadowing-2026-07-11.md (the `tail -1`
card picker, venture-lab #33) is actually closed on main, prove the
before/after with a local reconstruction of the shadowing scenario, and
reconcile the idea file's stale body (captured → shipped).

## What happened

- **The dispatched "fix the bug" task found the fix already landed** —
  v1.10.1 (PR #187) grades EVERY card in the diff on both surfaces
  (generated gate template + kit ci.yml, in lockstep), tightened further
  by the external review #226 findings G-1/G-2 (locked-door siblings,
  deletion hard-red); full regression coverage already in
  tests/test_adopt.py ("Gate multi-card grading" block). No engine change
  → no dist rebuild, no new CHANGELOG entry, no version bump (any of
  those would duplicate v1.10.1).
- **Ground-truth proof delivered** (PR #311 body, verbatim): scratch repo
  via the CI cold-adopt smoke recipe with the real dist/bootstrap.py; the
  venture-lab #33 shape (ADDed in-progress card + MODIFIED later-sorting
  sibling). Reconstructed v1.10.0 `tail -1` gate → exit 0 GREEN (the
  bug); current planted substrate-gate.yml → exit 1 HOLD-by-design on the
  added card; all-complete multi-card diff → exit 0 (no over-holding).
  Pre-#187 history is grafted out of the clone (root c83b23e), so the OLD
  picker was reconstructed verbatim from the line the idea file quotes.
- **Idea file reconciled**: body State captured → shipped with pointers
  (#187, #226 tightening, PR #311); "Interim wave doctrine" marked
  obsolete; "Proposed fix direction" annotated as implemented. The
  frontmatter already said shipped — the stale BODY is what
  mis-dispatched this task.
- **Claim bullet** rewritten to the check_claims grammar (the free-text
  line drew a claims-format advisory).
- Verify: `python3 -m pytest tests/ -q` → 1214 passed;
  `python3 dist/bootstrap.py check --strict` → only this card's designed
  born-red hold.

## 💡 Session idea

`check_idea_index.py` validates the frontmatter `state:` against the
allowed set but never cross-checks the body's prose `> **State:**` line —
this file sat with frontmatter `shipped` and body `captured` for a day
and the stale body dispatched an entire redundant fix task. An
advisory-tier frontmatter-vs-body state agreement check (only when the
body carries a `**State:**` line) closes that mis-dispatch class.
Dedup-checked docs/ideas/ — no existing idea covers it.

## ⟲ Previous-session review

PR #310 (current-state.md condensation for K0 headroom) did exactly what
the gauge asked and left the boot doc materially lighter — good, gauge-
driven scope discipline. What it could not catch: condensation guards the
BOOT docs, while this session's failure mode was a stale IDEA file body
steering a dispatcher. Improvement: state-bearing docs outside the boot
set need their own cheap drift guards (the 💡 above is the concrete
first one).
