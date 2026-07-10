---
state: promoted
origin: lab
shipped_pr: 95
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-10
outcome: shipped
---

# Engine gap: `render --live` cannot fill `.claude/CLAUDE.md` while `check_engagement` flags it (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (B1 record session, run `2026-07-09-run02`) →
> promoted → **shipped** (kit PR #95, 2026-07-10, fix shape (a):
> `render --live` iterates the engagement gate's own `scan_relpaths()`
> scope, `.claude/CLAUDE.md` included). Engine fix — dist regenerated.

## The gap (found live, run-2 prepare)

During the run-2 ON-arm engagement arc, `render --live` filled the
planted docs — but **not `.claude/CLAUDE.md`**, while
`check_engagement` still flags that file's unrendered banner/slots as
strict-RED findings. The two engine surfaces disagree about whose job
`.claude/CLAUDE.md` is: the render path skips it, the gate counts it.
The runner had to re-plant/fill it by hand to get to GREEN
(`runner_notes` item 2,
`bench/results/cold-start/2026-07-09-run02/manifest.json`).

Every fresh adopter walking the KL-7 checklist hits the same wall: the
checklist says "render, then check goes green", and it doesn't — a
checklist that cannot be completed by its own named commands is exactly
the stranding class KL-7 exists to prevent.

## Fix shape

Either (a) `render --live` includes `.claude/CLAUDE.md` in its render
set (preferred — one render verb finishes the arc), or (b)
`check_engagement` excludes it from planted-docs scope with a named
reason. (a) unless there is a deliberate contract reason `.claude/` is
render-exempt; if so, (b) must document it. Add the cold-adopt smoke
leg: after `render --live`, zero `unrendered-banner`/`unrendered-slot`
findings remain across ALL scoped files — that assertion is what would
have caught this gap in CI.

## Done-when

A bare adopt → answer slots → `render --live` reaches
`check --strict` GREEN (engagement findings zero) with no manual file
surgery; smoke/test pins it; dist regenerated + byte-pin green.
