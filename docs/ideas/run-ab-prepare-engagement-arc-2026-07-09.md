---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# run_ab prepare vs the P0 engagement gate: prepare should drive (or knowingly script) the RED→ENGAGED→GREEN arc (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (B1 record session, run `2026-07-09-run02`).
> `bench/run_ab.py` is **NOT** a pin path — this is an **ordinary-lane
> fix** (no `do-not-automerge` needed).

## The gap (found live, run-2 prepare)

Kit v1.3.0's post-adopt ENGAGEMENT gate (KL-7, shipped after run-1)
holds a bare `adopt` **born red** under `check --strict` by design — so
`run_ab.py prepare`'s smoke step (`check --strict` exit 0) now **fails
by design on every ON arm**. The run-2 runner had to complete the
documented RED→ENGAGED→GREEN arc manually: answer all 13 interview
slots with truthful seed-project values, `render --live`, re-plant
`.claude/CLAUDE.md` (separate engine gap — see
`render-live-claude-md-gap-2026-07-09.md`), write the adoption session
card, write the first `control/status.md` heartbeat, commit. It also
had to write `manifest.json` by hand because `cmd_prepare` aborts
before writing it when smoke fails (`runner_notes` items 2–3,
`bench/results/cold-start/2026-07-09-run02/manifest.json`).

The harness predates the gate; nobody taught prepare that "adopted" no
longer implies "green".

## Fix shape (ordinary lane)

Teach `cmd_prepare` the engagement arc for the ON arm: after `adopt`,
script the documented checklist (deterministic seed-derived interview
answers, `render --live`, first session card, seed heartbeat — the same
steps the CI cold-adopt smoke already walks), then assert
`check --strict` exit 0 and write the manifest. Also: write
`manifest.json` (with a `smoke_failed` marker) even when smoke fails,
so an aborted prepare leaves evidence instead of nothing. A scripted
arc keeps arms reproducible across runs — better than each runner
hand-engaging with ad-hoc answers (a cross-run comparability variable;
the judge already flags ON-surface drift between runs 1 and 2).

## Done-when

`run_ab.py prepare` on the current kit produces an ON arm that passes
its own smoke (`check --strict` exit 0) with zero manual runner steps,
manifest written on both success and failure paths; a test pins the
arc.
