# t5 doc/status reconcile — ⚑ → PR #552 + correct false cross-tree premise

> **Status:** `complete`

**Session:** 2026-07-20 · Self Improvement work-loop · substrate-kit
**Baton:** coordinator-authorized docs/control reconcile — correct factual drift about
the t5-headless-guard work now that it landed as owner-review PR #552. Owner provenance:
fm ORDER 048 + coordinator go-ahead. Docs + control only (NOT a pin path) — self-merges
on green; not labeled do-not-automerge.

**About to do:** (A) update the `⚑ t5-headless-guard` block in `control/status.md` from
"owner-gated, not yet built" framing to "PR #552 opened, awaiting owner review", correcting
the false "not landable from substrate-kit / kit-lab repo" phrasing (bench/ IS in
substrate-kit); (B) add a dated `[Corrected 2026-07-20]` note to
`docs/planning/2026-07-19-needs-planning-recipes.md` §4 refuting the "bench/ is not in this
repo / not landable from here" premise, pointing at PR #552; (C) claim + this card.

- **📊 Model:** opus-4.8 · low · docs-only (factual reconcile of status ⚑ + planning §4)
- **⚑ Self-initiated:** NOT self-initiated — coordinator-directed docs/control reconcile
  under fm ORDER 048 + coordinator go-ahead. No unprompted promotions.

## What shipped (PR #TBD)

Factual reconcile of the t5-headless-guard drift, verified against GitHub ground truth
before editing:

- **PR #480 (STEP 0 verification):** confirmed — #480 IS the merged "planning: turnkey
  recipes for the 4 needs-planning backlog items" PR (merged 2026-07-19 by menno420, head
  `claude/backlog-recipes`), and it added
  `docs/planning/2026-07-19-needs-planning-recipes.md`. Earlier session records were
  accurate. Neither the planning doc nor `control/status.md` contains any literal `#480` /
  `480` citation, so there was nothing to reconcile or delete on that front (STEP 0's
  "no change needed" branch).
- **PR #552 (the subject):** open, `do-not-automerge`, awaiting owner merge; head
  `claude/t5-headless-guard`; touches only `bench/tasks/T5.md` (+ its session card). NOT
  touched by this session.
- **False cross-tree premise, refuted against the tree:** `bench/tasks/T5.md`,
  `bench/run_ab.py`, `bench/README.md`, and `scripts/check_bench_integrity.py` all live in
  the substrate-kit checkout. The planning doc's / status ⚑'s claim that bench/ is "the
  kit-lab harness … not even in this repo" and "not landable from substrate-kit" was false;
  #552 landed from substrate-kit itself.

Edits: `control/status.md` (t5 ⚑ → STATUS line + PR #552 link, WHERE `kit-lab repo` →
`substrate-kit`, RISK "not landable" → "landed as owner-review pin PR #552 in substrate-kit
… awaits owner merge"); `docs/planning/2026-07-19-needs-planning-recipes.md` §4 (dated
`[Corrected 2026-07-20]` note + classification line fix, six-field ⚑ and recommendations
left intact); `control/claims/t5-doc-reconcile.md`; this card.

**Verify.** `python3 bootstrap.py check --strict` green. Docs/control only — no runtime,
template, or bench/ pin-path change.

## 💡 Session idea

**A tiny `control/status.md` ⚑-lifecycle lint that flags an owner-gated ⚑ whose PR is
already open.** The whole reason this reconcile was needed is that the ⚑ block kept saying
"owner-gated, not yet built" after the work had shipped as an open PR — the ⚑ and the PR
drifted with nothing catching it. A cheap advisory check could scan ⚑ blocks for a
`STATUS:`/PR-link line and warn when an owner-gated ⚑ has no pointer to its PR once one
exists, so the heartbeat never silently lags the tree. Deduped: grepped `docs/ideas/` and
`docs/recipes/` — the closest is the pinned-feed-contract doctrine (feed staleness, not ⚑
lifecycle); no idea names ⚑→PR drift detection. Advisory-only, disposable.

## ⟲ Previous-session review

Previous session — **the t5-headless-guard build (PR #552 + claim #551)**. Did well: it
correctly routed a pin-path `bench/tasks/T5.md` change through a `do-not-automerge`
owner-review PR (respecting `check_bench_integrity.py` rule 1) and kept the edit strictly
additive with the pinned prompt fence byte-unchanged — exactly the right discipline for an
oracle change. What it missed: it opened #552 but left the `control/status.md` ⚑ and the
planning doc §4 still asserting the old "not landable from substrate-kit / kit-lab repo"
premise — a factual drift the same session could have swept, since building the PR *proved*
bench/ lives here. Concrete system/workflow improvement: **when a session ships a PR that
falsifies a premise written in a status ⚑ or planning doc, reconcile that doc in the same
session** — the born-red card's own "durable-home" audit should include "does any ⚑/plan I
just contradicted still assert the old framing?". This session is the after-the-fact
cleanup that the ⚑-lifecycle lint idea above would make automatic.
