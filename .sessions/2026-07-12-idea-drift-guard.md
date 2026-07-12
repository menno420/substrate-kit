# Session: idea drift guard

> **Status:** `complete`

Did: shipped `check_idea_index` enforcement item 5 — the body-state drift
guard (friction→guard from PR #311's stale-body misdirection) — and
reconciled the 4 drifted idea files in the same PR (#312).

## What shipped

- `scripts/check_idea_index.py`: new `check_body_state_drift` (hard error,
  kind `body-state-drift`) — shipped frontmatter (`outcome`
  shipped/survived/reverted or non-null `shipped_pr`) vs. a body
  `> **State:**` line still opening `captured`/`routed` with no
  reconciliation marker fails, naming both disagreeing values. Recognized
  markers, designed from the full 35-file corpus: arrow-chain State
  blockquote reaching `shipped`; a `## Shipped` section; a
  RULED/preserved-as-written banner. A body with no State line predates the
  convention and is skipped (frontmatter authoritative —
  `substrate-kit-auto-drafted-handoff-2026-07-07.md`).
- Reconciled (verified vs. GitHub: kit #187 merged 2026-07-11, kit #92
  merged 2026-07-10; subject matter matches):
  `model-doctrine-emphasis-blind-phrase-2026-07-11.md` (#187) and the
  `upgrade-{archive-report-line-gap,checklist-release-json-placement,rollback-loses-doc-hash-records}-2026-07-09.md`
  trio (#92) — #311-pattern arrow-chains appended, history intact.
- 10 new tests (`TestBodyStateDrift`); full suite 1224 passed. Checker runs
  in ci.yml's kit-quality lane only — NOT in `bootstrap check --strict`,
  nothing new wired into adopter surfaces.
- Decide-and-flag: hard-fail (not advisory) — the tree is clean after
  reconciliation, and the failure mode being guarded is dispatch
  misdirection, which an advisory would not stop.

## Enders

💡 **Session idea:** README blurb drift is the same failure class one level
up — `docs/ideas/README.md` entry blurbs say `state: captured` for shipped
ideas (live: the gate-tail1 entry still sits in Backlog reading captured
after #311 reconciled its body; model-doctrine's blurb likewise until this
PR's file fix — the blurb itself still lags). Either extend the drift guard
to compare each README blurb's `state:` fragment against the linked file's
frontmatter, or drop state words from blurbs entirely (single source of
truth). Dedupe-grepped `docs/ideas/` — no existing idea covers it.

📊 Model: Claude 5 family

⟲ **Previous-session review (PR #311, gate multi-card verify):** genuinely
strong ground-truth discipline — it re-verified the v1.10.0 `tail -1` gate
against the real engine before trusting the idea file's claim, and its
body reconciliation of gate-tail1 became the canonical pattern this guard
now enforces. What it missed: it fixed the one body it touched but left
the identical drift in 4 sibling files and the README blurb, and shipped
no guard — the exact "fix the instance, skip the class" gap the
friction→guard rule exists for. System improvement: this session ships the
class fix; the README-blurb residue is routed as the 💡 above rather than
scope-crept.
