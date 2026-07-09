---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Label-added disarm guard — the enabler race's residual half (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (enabler-race-hotfix session, from the #22 incident's
> residual gap analysis).

## The gap the hotfix does NOT close

The deployed fresh-label re-read guard (hotfix PR, from #17's diff) defeats
labels applied *before the enabler's arm step executes* — the stale-payload
race and arbitrary runner-queue lag. But it is still a **point-in-time**
check: a `do-not-automerge` label applied *after* the enabler has armed
(e.g. the owner labels a PR five minutes — or a day — after open, wanting to
hold it) silently does nothing. Auto-merge stays armed; the PR merges on
green. The #22 incident proved manual disarm cannot be relied on to win a
timing window.

## The guard (enforce, don't verify — PL-002)

A tiny workflow on `pull_request: types: [labeled]`: if the added label is
`do-not-automerge`, call `gh pr merge --disable-auto "$PR"`. Symmetric,
event-driven, and idempotent — the label *itself* becomes the disarm switch
at any moment in the PR's life, not only in the enabler's arming window.
Optional symmetric half: `types: [unlabeled]` re-arms via the same enabler
conditions (probably NOT worth it — re-arming has judgment in it; removing
the label and letting a human/agent re-arm is the safer default).

## Done-when

Label added at ANY time after open → auto-merge verifiably disarmed within
one workflow run; a test-shaped verification note on the shipping PR (label
a scratch PR post-arm, watch it disarm).
