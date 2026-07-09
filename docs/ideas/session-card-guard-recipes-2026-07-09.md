---
state: promoted
origin: lab
shipped_pr: 19
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-09
outcome: shipped
---

# Guard recipes in session cards (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (⟲ workflow improvement,
> `.sessions/2026-07-09-kl1-ci-delta.md`) → promoted → **shipped** same day
> (kit PR #19). **Origin:** lab — KL-1 had to re-derive `_vendor_bootstrap` /
> `_ref_mine_log` by grep because KL-0's friction entries named symptoms only.

## The idea

When a session card records friction→guard material for a *later* session (a
"friction → guard candidates" entry, a deferred ⚑ flag), it should carry a
one-line **guard recipe** — the code anchors the fix needs: function + file +
the test target — not just the symptom. A recipe turns the follow-up from a
re-derivation grep pass into a minutes-long landing.

## What shipped (PR #19)

Convention text (deliberately a convention, not a checker — the entry shape is
prose and a needle-check would be ceremony): the kit's own
`.sessions/README.md` and the planted adopt README
(`_adopt_sessions_readme`, `src/engine/adopt.py`) both carry a **Guard
recipes** paragraph, so the convention travels to every consumer. Test:
`tests/test_adopt.py::test_sessions_readme_carries_the_guard_recipe_convention`.

## Survive window

Merged 2026-07-09 → the D-15 revert-scan may flip `outcome: survived` from
2026-08-08.
