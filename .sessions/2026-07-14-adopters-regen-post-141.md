# 2026-07-14 — Adopters regen after superbot-games #141 (v1.16.0)

> **Status:** `complete`

Intent: superbot-games PR #141 (kit v1.16.0 upgrade) merged minutes after the
last `docs/adopters.md` regeneration, so its registry row still read
v1.15.0 · stale. Rerun `dist/bootstrap.py currency` to refresh the table
(never hand-edited) and land the fix.

- **📊 Model:** Claude Fable 5 · low · docs-only

## Did

- Confirmed upstream first: menno420/superbot-games `substrate.config.json@main`
  (main @ 688cbf1) reports `kit_version: 1.16.0` — the #141 squash is live.
- `python3 dist/bootstrap.py currency` — regenerated `docs/adopters.md` from
  discovery (runbook §6, never hand-edited). superbot-games row moved from
  `v1.15.0 (bootstrap.py) | v1.15.0 | … | ⚠️ DRIFT · stale (v1.15.0 < v1.16.0)`
  to `v1.16.0 (bootstrap.py) | v1.16.0 | … | ⚠️ DRIFT · current`. The remaining
  DRIFT tag is self-report lag inside superbot-games (control/status.md says
  v1.15.0; status-mining/status-exploration say v1.7.1) — reconcile at the
  source, out of scope here.
- `python3 dist/bootstrap.py check --strict` — only red was this card's own
  born-red hold; advisories noted (claim-format warning self-resolves when the
  claim file is deleted below; staged-regen-lag + older-card model-line
  warnings pre-exist this session).
- Committed the regen (7d53088, with the guard-fires.jsonl telemetry delta),
  then flipped this card + deleted `control/claims/adopters-regen-post-141.md`
  in the final commit.

💡 Session idea: `bootstrap.py currency` could accept a `--repo <owner/name>`
scope so a single-row refresh after one adopter merge doesn't re-fetch the
whole fleet — cheaper and less likely to pick up unrelated row churn in the
same diff.

⟲ Previous-session review: the wave-aftermath session (#372/#373) regenerated
the registry correctly but minutes too early relative to the in-flight
superbot-games #141 merge — inherent race, handled cleanly by this follow-up;
a possible improvement is having the wave coordinator re-run `currency` once
after the last adopter PR of a wave reports merged, instead of at wave-record
time.
