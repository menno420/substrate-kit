# 2026-08-14 — Regenerate docs/adopters.md: gba-homebrew adopted

> **Status:** `complete` — branch `claude/adopters-regen-gba`, one generated
> file, complete at push (the #584 pattern; a card rides along because
> `--require-session-log` holds card-less PRs, measured on #584's first round).

- **📊 Model:** fable-5 · high · docs-only

## previous-session review

Kit #584 (same session, earlier turn) regenerated after the phase-3 four; its
row for gba-homebrew said honestly stale, parked on the toolchain fork. The
fork resolved: owner-authorized one-time bypass merged gba #215 (record on
that PR); the 1.22.3 toolchain migration stays open on gba #216.

## Shipped

- `docs/adopters.md` regenerated: gba-homebrew now reads current
  (tree v1.21.0 · pin v1.21.0 · self-report v1.21.0). Remaining stale rows:
  superbot-games (+self-report DRIFT), trading-strategy (owner-skipped
  pending archive decision), pokemon-mod-lab — each honestly stale.

## Verify

- `currency` exit 0, 0 unreadable rows; DRIFT only superbot-games' true
  self-report rows.

💡 gba's row went stale → current in under a day only because the bypass was
recorded ON the PR with timestamps and the restored ruleset verified — the
registry regen could cite it instead of explaining it.
