# Session 2026-07-09 — capture: pinned-feed-contract doctrine (consumer-proven pattern)

> **Status:** `complete` *(PR #20 — B4 capture only; touches nothing PR #17 owns.)*

**What happened:** filed the **pinned feed contract** pattern as a B4 idea entry
(`docs/ideas/pinned-feed-contract-doctrine-2026-07-09.md`, frontmatter
`state: captured · origin: consumer:menno420/superbot · outcome: open`) + a
README Backlog row. The pattern shipped end-to-end estate-side today —
superbot PR #1884 (committed versioned shape contract for `console.json`,
producer parity + fail-closed CI checks, `meta.schema_version` stamped into
the artifact) and websites PR #11 (pinned contract copy + render-time
verification, honest schema-drift banner) — and its first consumer-side pass
caught a live dict-vs-list defect within minutes, which is the evidence line
the capture leads with. **No doctrine/engine code built** (capture-first; the
build rides a later groomed-ideas increment, per the dispatching task's
explicit "file it, don't build it" scope).

## ⚑ Flags

1. ⚑ Decide-and-flag: origin recorded as `consumer:menno420/superbot` (the
   producer half's home and the idea's provenance card, superbot #1883→#1884)
   even though the proof spans two consumer repos; the frontmatter grammar
   takes one repo, and superbot is where a promoted build would sync from.

## 💡 Session idea

**A ledger-parity check in the planted `bootstrap check`:** websites' session
review found its `docs/current-state.md` "Recently shipped" list silently
skipped PRs #9/#10 — the kit plants the "keep this ledger current" rhythm but
ships no enforcement, while superbot's `check_current_state_ledger.py` proves
the check is cheap (newest merged PR vs newest ledgered entry). Planting a
small parity check in the engine's `check` would make the ledger rhythm
enforcing in every consumer instead of exhortative. Dedup-checked
`docs/ideas/` — nothing covers ledger freshness.

## ⟲ Previous-session review (groomed-ideas-1, PR #19)

Strong: three ideas moved capture→shipped in one coherent PR with the B4
ledger exercised for real, and the diff-aware gate selection killed the
mtime-shim class at the *template* level so it never travels to consumers —
the right altitude. Its flag-2 call (guard recipes as convention, not
checker) shows good ceremony restraint. Miss (small): its B4 rows were
written `shipped` with a merged_date *before* the merge landed (flag 1, taken
knowingly) — the flag is honest, but the cheap alternative it rejected
(outcome `open` at write, flipped by the next session's one-line touch) would
have kept the ledger never-wrong instead of briefly-wrong; worth preferring
next time since `check_idea_index` can't see an unmerged PR number.
**Workflow improvement:** `check_idea_index` could cross-check
`shipped_pr`/`merged_date` against the repo's actual merge history once P13
read scopes exist — recorded here rather than filed; it folds into the
existing B4 sweep item, not a new idea.

## Docs audit

Idea file + README Backlog row are the change; CHANGELOG untouched (docs-only
capture, no engine/planted behavior change); current-state untouched
(deliberately — PR #17 rewrites its In-flight/Stability sections); telemetry
row appended (merge=union). Nothing left chat-only.

## KPIs / verification

- `python3.10 scripts/check_idea_index.py` → OK (frontmatter grammar, cohort
  filename, README link resolution).
- `python3.10 scripts/check_program_law.py` → OK.
- `python3.10 dist/bootstrap.py check --strict --session-log
  .sessions/2026-07-09-pinned-feed-contract-idea.md` → green on this card
  once flipped.
- Conflict check vs open PR #17: file lists disjoint (bench/CI/current-state
  vs docs/ideas/ + this card).

- **📊 Model:** fable-5 · high · idea/planning
