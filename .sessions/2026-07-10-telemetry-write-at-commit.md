# 2026-07-10 — gen-2: telemetry write-at-card-commit + backfill

> **Status:** `complete`

- **📊 Model:** claude-opus-4-8 · high · gen-2 kit-side telemetry fix (single
  scoped PR: emit the model-usage row at card-commit + backfill the historical
  undercount)

## Scope

Gen-2 queue item 6 (the #50-lane idea): the PL-004 model-usage feed
(`telemetry/model-usage.jsonl`) **undercounts** — 10 recorded rows against 42
eligible session cards (a card is *eligible* when it carries a valid,
non-`[[fill:]]` `📊 Model:` line). The cause is a *lossy, single-latest*
harvest: `harvest_model_usage` runs only at `session-close`, and only over
`latest_session_log` (the newest `.sessions/*.md` by mtime). Any card committed
while a newer card already existed — or a session that never ran its own
`session-close` — never reached the feed. So the dataset silently dropped ~3 of
every 4 sessions.

Fix (write-at-card-commit): a new `reconcile_model_usage(root, sessions_dir)`
in `src/engine/loop/telemetry.py` sweeps **every complete card** carrying a
valid `📊 Model:` line and appends the ones not already recorded — so the
moment a card commits complete its row exists and no later card can shadow it
out of the harvest. Completeness is gated on the exact session-log machinery
(`status_in_progress` + `unresolved_fill_count`): a born-red / in-progress /
drafted card has no finished session to report and is picked up only once it
flips complete. Idempotent (dedupe by session slug, in-batch too), append-only,
fail-open — the founding telemetry contract. Wired into `cmd_session_close`
right after the existing single-latest harvest (which keeps its per-card
missing-line / off-taxonomy advisory); the record shape is shared with harvest
via `_build_model_usage_record`, so both feeds emit the identical PL-004 object.

Backfill: run the reconcile once over the live tree to append the 32 missing
rows for the already-complete eligible cards — the DATA file only; historical
`.sessions/*.md` content is never rewritten. The 3 cards with no `📊` line
(`kl0-dogfood-seed`, `kl1-ci-delta`, `kl1-release-train`) are not eligible and
stay uncounted (no data to harvest, and rewriting their cards is out of scope).

Touches only `src/engine/loop/telemetry.py`, `src/engine/cli.py` (the
session-close wiring + import), `dist/bootstrap.py` (regenerated),
`tests/test_telemetry.py`, `telemetry/model-usage.jsonl` (backfill data), and
this card. NEVER touched: `control/inbox.md`, `control/status.md`, or anything
under `bench/`.

## 💡 Session idea

The model-usage feed and the guard-fires feed are both "append one row at a
mechanized choke point," but they diverged on *how many* rows a run may write:
guard-fires is one-per-finding (naturally complete), model-usage was
one-per-latest (lossy). Reconcile makes model-usage self-healing — every
session-close closes the whole gap, not just its own row. The same
"reconcile-the-whole-tree at the ritual, don't trust the incremental write"
pattern would harden any other per-card feed the loop grows.

## ⟲ Previous-session review

The prior card (2026-07-10 gen-2: claim-aware checker) closed `complete` with
`check --strict` green and shipped as #90. No defect inherited; this session
picks up queue item 6, the telemetry undercount the gen-2 queue explicitly
lists as "10 harvested rows vs 21+ eligible cards."
