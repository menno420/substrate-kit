# 2026-07-10 — gen-2: reconcile queue-state + auto-merge stall class + enabler synchronize

> **Status:** `complete`

- **📊 Model:** claude-opus-4-8 · high · gen-2 kit-side docs reconcile +
  low-risk enabler-trigger fix

## Scope

Three parts, one PR — touching ONLY `docs/gen2/queue-state.md`,
`docs/CAPABILITIES.md`, `.github/workflows/auto-merge-enabler.yml`, and this
card. NEVER `control/inbox.md`, `control/status.md`, or anything under
`bench/`.

- **PART A — reconcile `docs/gen2/queue-state.md` against reality.** The #109
  night-cap pass reconciled the file at HEAD `704a537`, but **PR #106** (the
  full upgrade-apply-docs post-hoc mechanism) landed AFTER that pass — it sat
  ~1h green-behind and landed via branch-update `855a8e4`. So agent-queue
  item 10's "full post-hoc-apply mechanism idea stays `open`" was stale.
  Corrected item 10 to record #106 shipped it (`outcome: shipped`), and added
  a follow-on reconcile note to the header (HEAD now `266807e`; #107/#109/#110
  also landed after #109 as control-lane housekeeping). All other ✅/PR
  numbers were already accurate — not re-touched. The three genuinely
  remaining, owner-gated items (T5 guard-probe, legacy-alias delete,
  P6/loop sweeps) kept as-is.
- **PART B — record the auto-merge STALL CLASS.** Appended a newest-first
  entry to `docs/CAPABILITIES.md`: the enabler fires only on
  `[opened, reopened, ready_for_review]` (not `synchronize`) so it arms once
  at PR birth; `main` requires up-to-date branches; a PR that goes behind
  stalls green-but-unmerged with a stale-head arm. RECIPE: `git merge
  origin/main` + push re-runs CI on the up-to-date head and the still-armed
  native auto-merge completes. Evidence: PR #106 → `855a8e4`.
- **PART C — fix the enabler trigger (low-risk).** Added `synchronize` to
  `auto-merge-enabler.yml`'s `pull_request` types so it RE-ARMS on every push.
  Arming is idempotent (`gh pr merge --auto` no-ops if armed, re-arms if a
  behind-push disarmed it, NEVER self-merges — merge stays gated by
  `kit-quality`). No guard misbehaves on `synchronize` (rules-count and
  fresh-label re-read are stateless; concurrency is per-PR,
  cancel-in-progress:false). This narrows but does not fully close the stall
  class.

## 💡 Session idea

The stall has two independent causes and this PR fixes the cheaper one. Cause
1 (fixed): the enabler armed only at birth, so a legitimate branch-update
never re-armed. Cause 2 (owner-gated, ⚑): the `main` "require up-to-date"
constraint means even a re-armed PR can't merge while behind — the only full
cure is the repo setting "automatically update branches", which keeps every
green PR at the front of main without a human round-trip. The generalizable
shape: when an automation stalls on a "freshness" invariant, separate the
*re-trigger* gap (a workflow-trigger fix, agent-ownable) from the *staleness*
gap (a platform auto-update setting, owner-ownable) — shipping the first
shrinks the manual toil immediately while the second waits on the owner.

## ⟲ Previous-session review

The prior card (`2026-07-10-upgrade-apply-docs-posthoc.md`, shipped #106)
closed `complete`, `check --strict` green, suite 803. It landed the full
post-hoc-apply mechanism but — because it itself sat ~1h green-behind and
landed only after the #109 reconcile — left `queue-state.md` item 10 pointing
at the now-obsolete "interim slice / idea stays open" state. No defect
inherited in code; this session closes the documentation lag that #106's own
behind-stall created, and pins the stall class + trigger fix so the next PR
that goes behind self-heals on a push instead of waiting an hour.

## Outcome

Shipped all three parts in one PR. **PART A:** `queue-state.md` item 10 now
records #106 shipped the full post-hoc-apply mechanism (`outcome: shipped`),
plus a header follow-on reconcile note (HEAD `266807e`; #107/#109/#110 landed
after the #109 pass). No other item re-touched — the rest were already
accurate; the three remaining owner-gated items kept. **PART B:** appended the
auto-merge stall-class entry + `git merge origin/main` branch-update recipe to
`docs/CAPABILITIES.md` (evidence PR #106 → `855a8e4`). **PART C:** added
`synchronize` to `auto-merge-enabler.yml` — LOW-RISK (arming idempotent, never
self-merges, no guard misbehaves on synchronize); this narrows the stall by
re-arming on fix-pushes. ⚑ RESIDUAL owner item flagged in both the workflow
comment and CAPABILITIES: fully closing the behind-stall needs the repo setting
"automatically update branches".

Verification: `python3 dist/bootstrap.py check --strict` green; full suite
819 passing; `tests/test_ci_control_lane.py` 6/6 (no pin broken). No src/
change → no dist regen. No pin test needed updating (no test references the
enabler trigger).
