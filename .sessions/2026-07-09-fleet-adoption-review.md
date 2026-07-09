# Session 2026-07-09 — fleet adoption review (owner-directed) + control-lane status gate

> **Status:** `in-progress`

**Scope (about to do):** the owner-directed fleet adoption review, consolidated
from five completed read-only assessments (kit / superbot / superbot-next /
websites / context self-sufficiency). One coherent PR: (1) the durable review
report at `docs/reports/2026-07-09-fleet-adoption-review.md` (per-repo
verdicts, findings tables, the kit's-own-promises proofs, the owner-directed
context-self-sufficiency lens, rollout coordination notes, fixed/filed/⚑
needs-owner close); (2) **ship the med fast-lane fix** — the CI control fast
lane (kit `ci.yml` + the planted `substrate-gate.yml` template) skips
`check_status_current` on exactly the PRs that write control files, so a
heartbeat-deleting control-only PR rides the lane GREEN while `check --strict`
would exit 1 — add a status-scoped check step to the lane itself (`check
--strict --status-only`), dist rebuilt, tests pinned; (3) file the non-shipped
gaps as `friction` issues per the kit's protocol. Hard rails honored: no
bench/ writes, no version bump / release cut, PR #26 untouched (PL-011 +
cite-never-copy tension routed to the owner, not resolved).
