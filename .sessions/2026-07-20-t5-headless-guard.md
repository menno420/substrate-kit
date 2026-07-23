# T5 headless guard-observability — shape-2 additive protocol step (owner-review)

> **Status:** `complete`

**Session:** 2026-07-20 · owner-review PR · substrate-kit
**Baton:** t5-headless-guard — additive shape-2 (check-driven) guard-observability
step on `bench/tasks/T5.md` — fm ORDER 048 standing grant.

**About to do:** insert one additive block into `bench/tasks/T5.md`'s ON-arm
protocol — a "Guard-observability step (shape 2)" that has the runner invoke
`python3 bootstrap.py check --strict` pre-session (guard fires red against the
seeded drafted card) and post-session (obey/repair: exit 0 = repaired, red =
left broken), recorded as scripted facts — so the headless guard's
fire/obey/repair arc becomes scoreable instead of n/a. Pinned oracle path
(`bench/tasks/`): the PR rides `do-not-automerge` for owner review and is NOT
merged by the session.

- **📊 Model:** opus-4.8 · high · docs-only (additive bench-task protocol block on T5.md; no engine/runtime code)
- **⚑ Self-initiated:** none — this is ordered baton work (fm ORDER 048 standing
  grant). Decide-and-flag calls within it: (1) landed the standalone claim on a
  `claim/*` branch (not the suggested `claude/*`) because the CI "claims-only
  fast-lane guard" reds a `claude/*` PR whose entire diff is only
  `control/claims/**` (the #451 race) — `claim/*` is the blessed card-less
  fast-lane prefix; (2) created the `do-not-automerge` label (it did not exist
  in the repo) and refreshed the CI payload with an empty commit so the
  bench-integrity pin-path gate reads the label; (3) added this session card
  because the v1.20.1 engine's diff-derived card selection HOLDS a non-control
  PR red with no card in the merge-base diff (it does not fall back to mtime
  when git context exists) — a bench/tasks-only PR still needs a card.

## What shipped (PR #552)

`bench/tasks/T5.md` gains one purely additive block — the "Guard-observability
step (shape 2 — the headless guard surface; ON arm only)" — inserted between the
Seed-state precondition's Probe-validity gate and the pinned session prompt. The
block documents two runner scripted facts: pre-session `check --strict` (expected
≠ 0 against the seeded drafted card = the guard firing observed headless; exit 0
folds into the Probe-validity gate as null/protocol-deviation) and post-session
`check --strict` (exit 0 = repaired the announced state, red = left the guard
red — the outcome judge items 2 and 4 already key on). Implements the shape-2
recommendation from `docs/planning/2026-07-19-needs-planning-recipes.md` §4;
shape 1 (a hook-honoring harness) is explicitly not chosen.

The pinned prompt fence and judge items 1–4 (rubric PR #220) are byte-unchanged;
the diff is zero-deletion additive (26 inserted lines). Scope is `bench/tasks/T5.md`
only (plus this required session card).

**Evidence.** PR #552, branch `claude/t5-headless-guard`, labeled
`do-not-automerge`. Claim PR #551 (`claim/t5-pin-claim`) merged green on the
control fast lane (squash `5cd4b70`). `git diff origin/main -- bench/tasks/T5.md`
shows zero `-` lines. NOT merged and auto-merge NOT armed — held for owner review
per the `bench/tasks/` pin (scripts/check_bench_integrity.py rule 1).

## 💡 Session idea

**Machine-enforce the T5 pre/post `check --strict` exit codes as run artifacts.**
This PR documents the shape-2 step as *runner protocol* only — `run_ab.py` records
the prompt-file path, not T5.md's body, so a human runner performs the pre/post
capture by hand (same as the existing Seed-state steps). A small `run_ab.py`
companion could run `check --strict` on the ON arm before and after the T5 session
automatically and write both exit codes into the run's `s-row-facts`/manifest, so
the fire/obey/repair rows are captured deterministically instead of by-hand. It is
itself a `bench/` pin-path `do-not-automerge` change, so it stays a separate PR
out of this T5.md-only scope. Deduped against
`docs/planning/2026-07-19-needs-planning-recipes.md` §4 (which recommends the
shape, not the harness wiring) — distinct.

## ⟲ Previous-session review

Previous session — **R14 exact-model-ID gate on the born-red added card**. Did
well: it completed the advisory→born-red-gate promotion pattern R13 named,
exit-affecting segment-1 (exact model-ID) on the PR's own added card with the same
no-retroactive-redden scoping, and carried the dist rebuild cleanly. What this
session surfaces about the *system*: the ci.yml "Session gate" step comment still
claims a no-card diff falls to a "mtime fallback (fail-open; on main every merged
card is complete)", but the v1.20.1 engine actually HOLDS red via diff-derived
selection whenever git context exists (log line: "diff-derived selection never
falls back to the mtime guess when git context exists"). That stale comment cost a
red CI cycle this session (a bench/tasks-only PR was assumed card-optional). Worth
a one-line ci.yml comment fix so the next author knows a non-control PR always
needs a card — a cheap enforce-don't-exhort doc/comment guard.
