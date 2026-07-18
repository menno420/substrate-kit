# Claims-only fast-lane guard — close the #451 race

> **Status:** `complete`

Closed the #451 claims-only fast-lane race: a `claude/*` work PR whose ENTIRE
diff is only `control/claims/**` used to ride the CI `control_only` fast lane,
skip the born-red session gate, and auto-merge card-less. A new red
`kit-quality` step now rejects exactly that shape while leaving `claim/*`
standalone-claim PRs green.

## What this session did

- `.github/workflows/ci.yml`: new `kit-quality` step "Claims-only fast-lane
  guard", placed beside the Inbox append-only gate — fast-lane only
  (`control_only == 'true'`), `claude/*` heads only (a non-`claude/*` head
  exits 0), red (`::error::` + `exit 1`) when every changed path is under
  `control/claims/`. Mirrors the inbox gate's merge-base/range bash idiom;
  git does the diff, the engine never shells out (§3.2 subprocess ban).
- `tests/test_ci_control_lane.py`: textual pin asserting the step exists, is
  lane-conditioned, references `github.head_ref` / `claude/*`, uses the
  `grep -v '^control/claims/'` detection, and lives in `kit-quality`.
- `docs/operations/auto-merge-guards.md`: guard-stack row 7 (enforcing).

## Before / after

**Before:** a `claude/*` PR that committed only a claim file (`control/claims/
<slug>.md`) was a `control/**`-only diff → `control_only=true` → the whole
heavy suite (including the born-red session gate) was skipped → `kit-quality`
reported green with no session card → auto-merge landed card-less "work"
(the #451 race artifact). **After:** that exact diff hits the new fast-lane
guard, which sees a `claude/*` head whose changed paths are entirely under
`control/claims/`, prints an `::error::` telling the author a `claude/*` work
PR must carry real work plus its `.sessions/` card (which moves it to the full
lane), and `exit 1` holds `kit-quality` red so it cannot auto-merge.
`claim/*` standalone-claim PRs are untouched — a non-`claude/*` head exits 0,
so the intended card-less fast lane for real claims (control/claims/README.md)
still works.

## 📊 Model

📊 Model: Opus 4.8 · medium · feature build

## 💡 Session idea (Q-0089)

**Fast-lane head-prefix ⇄ enabler branch_patterns symmetry lint.** This guard
hardcodes the `claude/*`-vs-`claim/*` distinction and the `control/claims/`
prefix; the SAME branch-prefix knowledge also lives in the enabler's
`automerge.branch_patterns` (default `["claude/*", "claim/*"]`) and in
`control/claims/README.md`. Nothing keeps the three in agreement, and a NEW
seat branch prefix is exactly the kit#293 stall class (a head matching no
pattern sits green+unarmed forever). Idea: a stdlib advisory that reads the
enabler's `branch_patterns`, the guard's head-prefix cases, and the claims
doctrine, and flags when a fast-lane-eligible prefix is not covered by the
card-less guard (or vice-versa) — so a new prefix can't silently reopen a
card-less-merge hole. Distinct from the guard itself (which enforces one
prefix pair); this asserts the prefix SET stays consistent across surfaces.
Low-priority, one-file advisory; not built this session.

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18T15:42Z SESSION-ENDER v3.7 wake: genuine credit — it did the
disciplined thing and left a *precise, buildable* baton, teeing up this exact
slice as next-2 task 2 ("Enabler guard candidate: decline a claude/* PR whose
ENTIRE diff is a control/claims/** addition"), so the baton worked as designed
— a later session picked up exactly the queued rung with zero re-derivation.
It also verified triggers to exhaustion rather than trusting carried state.
Small miss + workflow improvement: that buildable candidate lived ONLY as a
prose bullet in `status.md` (which is overwritten every heartbeat) — had a
sibling session not read this heartbeat, the rung would have evaporated.
Improvement: a baton item that is a genuinely buildable slice should ALSO be
dropped as a one-line `docs/ideas/*.md` file (indexed by `check_idea_index`),
so it survives heartbeat rewrites and is visible to the durable idea backlog,
not just to the next reader of the transient status page.
