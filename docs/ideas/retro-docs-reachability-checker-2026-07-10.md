---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Retro/docs reachability checker — no unindexed retro file (2026-07-10)

> **Status:** `ideas`
>
> **State:** captured (gen-2 night-prep seed by the grand-review session).
> **Origin:** lab — the wind-down addendum (PR #76) merged unindexed and stayed
> invisible until a gen-2-boot reconcile pass (#78) added its README line; the
> addendum had even self-flagged the follow-up, and no session executed it.

**One line:** a small kit-quality check asserting every `docs/retro/*.md` (and
optionally `docs/ideas/*.md`, which already has `check_idea_index.py` as the pattern) is
linked from its directory README — an unindexed retro doc is invisible to every
orientation route that starts at the index.

**Why the kit:** parallel wind-down lanes collide on the shared index file and defer the
line "until after X merges" — exactly the deferral that got lost. The checker converts
the convention into enforcement, fleet-wide via the next release.

**Size:** small (mirror `check_idea_index.py`; wire into kit-quality).
