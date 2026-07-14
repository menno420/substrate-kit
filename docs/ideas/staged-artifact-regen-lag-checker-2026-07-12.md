---
state: captured
origin: consumer:menno420/websites
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Regeneration-lag checker for staged `.substrate/` artifacts (2026-07-12)

> **Status:** `ideas`
>
> **State:** captured → route: quick-win engine checker leg → **built:
> kit PR #345** (2026-07-13, ORDER 019 item 6 — `check_staged_regen`,
> advisory-first; parked green for review-merge. Frontmatter ship fields
> flip when the PR merges, per the idea-index outcome rules).
> **Origin:** consumer:menno420/websites — friction issue
> [#39](https://github.com/menno420/substrate-kit/issues/39), filed by the
> 2026-07-09 fleet adoption review; triaged and closed by the 2026-07-12
> lab-loop run (this file is the backlog home).

## The gap

Staged `.substrate/` artifacts (agents, skills, staged CLAUDE.md) can carry
unfilled `${...}` slots even though `state.json` `slot_values` are ALL
filled — the artifacts were staged pre-slot-fill and nothing re-renders
them outside an `upgrade` (whose staged-regen step DOES fix the state).
The engagement gate never sees it: `_unrendered_findings` scans **planted
docs** (`scan_relpaths`), not the staged tree. A "looks staged, isn't
rendered" class — proven live on websites at main `992c045`
(`.substrate/agents/architect.md`, `reviewer.md`, `claude/CLAUDE.md`, two
skills templated while every slot was answered).

Re-verified at triage (2026-07-12, kit v1.12.1): no such checker exists
(grep `regeneration-lag|staged-regen|stale-staged` over `src/engine/` =
0 checker hits). The websites *instance* was fixed by its rollout +
subsequent upgrades; the kit-side guard so the class can't recur in any
adopter is still the open item.

## The fix

A `check` finding (engagement-gate leg or standalone) that fires when
`slot_values` are filled but staged `.substrate/` artifacts still contain
live `${...}` placeholders — reusing `find_placeholders_outside_code` (the
code-span-aware scan already used for planted docs, so backticked mentions
never false-positive). Message names the recovering command (re-render /
upgrade). Advisory vs strict: decide at build time; advisory-first per the
adopt-freely posture.

## Guard recipe

`src/engine/checks/check_engagement.py` — `_unrendered_findings` is the
pattern to mirror; the staged-tree root comes from `config.state_dir`.
Fixture: a repo with all slots answered + one staged artifact carrying
`${project_name}` must fire; the same artifact with the slot inside a
code span must not. Engine change → dist byte-pin.
