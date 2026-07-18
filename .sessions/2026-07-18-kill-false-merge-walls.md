# 2026-07-18 · kill the false "agents cannot merge" wall in the root templates

> **Status:** `complete`

About to happen (opening declaration): the kit's `CONSTITUTION.md.tmpl` and
`CAPABILITIES.md.tmpl` seed every adopted repo with a standing
"classifier-denied since 2026-07-15" merge wall — agents must not
ready-flip / arm auto-merge / REST-MCP-merge; the owner or a server-side
workflow is framed as the only merge authority. This is false and
self-propagating: agents CAN merge their own green PRs (verified this
session by a direct MCP merge). Remove the false doctrine from the two
templates, keep every genuinely-true wall (ref/branch DELETION 403,
tag-push/release 403, raw api.github.com blocked, repo settings/secrets/
external = owner), regenerate the baked `dist/bootstrap.py`, and preserve
the exact PL-012 rider phrases `test_rider_graduation` guards.

- **📊 Model:** opus-4.8 · high · docs-only

Run type: owner-directed fleet cleanup (the owner is tired of sessions
writing false restrictions that each later session copies and amplifies).

## What shipped (PR #444)

- `src/engine/templates/CONSTITUTION.md.tmpl` — the "An open PR is never a
  reason to stop" rail no longer says agents must not merge / must leave it
  to the owner or a server-side workflow. It now says: open READY, land
  your own green PR directly (MCP/REST, or let a merge-on-green workflow
  land it — either is fine), merging is a normal agent action, never route
  a mergeable green PR to the owner; a specific verbatim refusal is
  attempt-once and never a standing wall. The PL-012 rider phrases the test
  suite pins (`An open PR is never a reason to stop.`, `Open READY (never
  draft)`, `queue ONE owner item for the systemic cause`) are preserved.
- `src/engine/templates/CAPABILITIES.md.tmpl` — replaced the
  "Self-merge classifier … owner-gated PRs" wall with "Merging works
  agent-side — NOT a wall", and corrected the false "branch-push … remain
  owner-only" clause (branch creation and commit-pushes work agent-side;
  only ref DELETION is walled). The branch-deletion / tag-push / raw-REST
  walls stay, re-verified 2026-07-18.
- `dist/bootstrap.py` — regenerated (`python3 src/build_bootstrap.py`) so
  the committed single-file artifact matches the edited templates
  (`test_committed_bootstrap_is_current`).

## Verification

- `python3 -m pytest` — full suite green locally (1726 passed, 1 skipped),
  including `test_rider_graduation` and `test_committed_bootstrap_is_current`.
- Direct MCP merge of an unrelated PR this session is the live proof the
  removed wall was false.

## Follow-on (same session, separate PRs)

The already-materialized repos carried rendered / hand-copied versions of
the same false doctrine; a fleet-wide sweep removed it from their
forward-binding docs in parallel (one PR per repo), keeping every true
wall. This PR is the root that stops it recurring in newly-adopted repos.

## 💡 Session idea

The kit's own tests hard-coded pieces of the false doctrine
(`test_rider_graduation` pins guarded the *good* rider phrases, but nothing
stopped a wall row from being asserted-present in a future test). Add a
kit-side lint that scans templates AND their guard-tests for
standing-prohibition phrasings ("classifier-denied", "agents do NOT merge",
"owner is the merge authority") and fails unless the phrase sits inside a
dated `## Append log` evidence entry — so a false wall can never be
re-seeded into the templates or frozen into a test again.

## ⟲ Previous-session review

The prior sessions that wrote the "2026-07-15 classifier-denied merge wall"
generalized a single dated, venue-specific refusal into a permanent,
fleet-wide prohibition and baked it into binding templates — the exact
over-generalization the capabilities discovery rule ("attempt once; one
refusal ≠ a permanent wall") exists to prevent. The systemic improvement:
the discovery rule needs teeth — walls in the kit-owned capability-seed
should carry a machine-checkable `venue` + `LAST-VERIFIED` and auto-expire
past the staleness window into "re-verify", so a stale refusal degrades to
a claim instead of hardening into doctrine.

