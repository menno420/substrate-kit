# 2026-08-14 — Regenerate docs/adopters.md: trading-strategy at v1.20.2

> **Status:** `complete` — branch `claude/registry-regen-post-160`, one
> generated file plus this card, complete at push (the #584/#585 pattern; a
> card rides along because `--require-session-log` holds card-less PRs —
> measured again on this PR's first round).

- **📊 Model:** fable-5 · high · docs-only

## previous-session review

Kit #585 (previous regen) recorded trading-strategy honestly stale at
v1.17.0, owner-skipped pending its archive decision. The skip stands; what
changed is the tree: the owner answered the fleet-manager review session's
fork live (2026-08-14) with "land the July parks", so trading-strategy #160
merged (v1.20.2 vendored, three resident overclaims narrowed in place first)
and #163 reconciled the heartbeat at source.

## Shipped

- `docs/adopters.md` regenerated: trading-strategy now reads v1.20.2 three
  ways (tree · pin · self-report) — no DRIFT, still honestly stale vs
  v1.21.0, still owner-skipped for the v1.21.0 wave. pokemon-mod-lab reads
  v1.15.0 over the direct-egress authed path. superbot-games' 3-file DRIFT
  unchanged — its own upgrade session reconciles it. 9 current · 3 stale.

## Verify

- `currency` exit 0, 0 unreadable rows; DRIFT only superbot-games' true
  self-report rows. First run's 403s were the proxied-API path quirk (direct
  egress cleared them); its stale raw read of the just-restamped heartbeat
  is the cached-vs-current defect already filed on kit #583.

💡 A parked upgrade PR that finally lands leaves TWO trails to reconcile —
the tree the registry reads and the heartbeat the adopter self-reports —
and the second is invisible until currency runs. Landing and restamping in
the same hour kept the DRIFT row's lifetime to minutes.
