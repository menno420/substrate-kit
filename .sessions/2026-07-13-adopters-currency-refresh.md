# 2026-07-13 — adopters registry currency refresh

> **Status:** `complete`

Intent: re-verify docs/adopters.md against actual adopter trees (registry
generated 2026-07-12T18:31:47Z was stale — dry-run at HEAD 96bece9 showed
superbot-next / websites / trading-strategy / venture-lab had reconciled
their DRIFT rows since) and regenerate it via the kit's own tooling
(`python3 dist/bootstrap.py currency`), never by hand.

## What happened

- Boot slice on main @ 96bece9 (hard-sync clean; all inbox ORDERS 001–017
  `done=` per control/status.md; verification green: `check --strict` exit 0,
  `check_idea_index` OK, 1245 pytest passed).
- Lane scan: only open PR was #317 (`do-not-automerge` owner park — untouched);
  no live claims. Chose baton rung (b): adopters.md re-verification.
- Regenerated `docs/adopters.md` via `python3 dist/bootstrap.py currency`
  (scan stamp 2026-07-13T12:42:36Z). Four DRIFT rows reconciled at their
  source since 2026-07-12: superbot-next, websites, trading-strategy
  self-reports now v1.15.0; venture-lab's stale `kit:` line gone. Remaining
  DRIFT (reconcile at source, not here): kit-self config pin v1.0.0,
  superbot-games two-lane v1.7.1 self-reports, fleet-manager v1.7.0
  self-report.
- PR #325, born-red per the session gate; this flip is the last commit.

## Enders

- **📊 Model:** fable-5 · high · docs-currency

💡 **Session idea:** `bootstrap currency` should emit a machine-readable
sidecar (`docs/adopters.json` or `.substrate/currency-drift.json`) alongside
the markdown registry — repo · tree · pin · self-report · verdict · drift
list — so the fleet-manager sweep and the websites control board consume
rows without parsing a markdown table. Dedup'd vs `docs/ideas/`: distinct
from `control-board-kit-readiness-cell` (that is the display cell on the
websites board; this is the kit-side data feed it would read).

⟲ **Previous-session review (2026-07-13 SI coordinator close, #324):** the
close-out left an exceptionally clean successor surface — verified routine
disposition with explicit LEFT-ARMED/NEVER-REBIND lines and a next-2 baton
that made this session's rung choice a one-read decision; repeat that. Its
gap: the baton's rung-b phrasing ("Owner sweeps #317 → cut release wave")
fuses an owner-gated step with agent-doable follow-ons, so a successor must
re-derive which half is actionable — batons should split owner-gated and
agent-doable items onto separate lines.
