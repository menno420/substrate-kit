---
state: captured
origin: consumer:menno420/websites
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Kit-version / readiness cell on the control-plane board (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (surfaced during the websites v1.2.0 upgrade,
> menno420/websites#31 — the consumer-rollout session that also found the
> model-line shadowing bug fixed in kit PR #40).

## The idea

The fleet's control-plane board (the websites-rendered view over each
repo's `control/status.md`) has no cell answering the two questions the
substrate coordinator actually asks per adopter: **which kit version is it
running** and **is it ready** (check --strict green + engagement green).
Add a kit-version/readiness cell per repo row, fed from the status
heartbeat rather than any new access path.

## Fit with ORDER 003 (the adopter-visibility band)

This is the **board-side rendering** of exactly the data ORDER 003 makes
adopters self-report: the order's item (1) adds a `kit:` line to the kit's
status template (`kit: v<X.Y.Z> · check: green|red · engaged: yes|no`) and
item (2) creates `docs/adopters.md` in the kit repo. Once adopters carry
the `kit:` line, the websites board can parse it per repo with zero new
access (KF-2-clean — the board already reads status files). So the routing
is: kit side ships with ORDER 003; this idea then travels to
menno420/websites as "parse + render the `kit:` heartbeat line as a board
cell (version + readiness badge)".

## Guard recipe

Websites side: the status-card parser that already splits heartbeat
`key: value` lines — add `kit:` extraction + a three-state badge
(green/red/absent = pre-ORDER-003 adopter); test target: a fixture
status.md with and without the `kit:` line. Kit side: nothing beyond
ORDER 003's own items.

## Done-when

The board shows, per adopted repo, the kit version it last self-reported
and a readiness badge — with "absent" rendering honestly for repos that
have not yet upgraded to a kit release carrying the `kit:` template line.
