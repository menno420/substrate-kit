---
state: promoted
origin: lab
shipped_pr: 394
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-15
outcome: shipped
---

# 📊 Model-line `unrecorded` effort marker — sanctioned terminal value for retro-sweeps (2026-07-15)

> **Status:** `ideas`
>
> **State:** shipped — kit PR #394 (2026-07-15, anticipated in-PR date):
> `MODEL_EFFORT_UNRECORDED` carve-out in `check_model_line` (advisory-silent,
> harvest verbatim, live off-taxonomy still nags) + the `.sessions/README.md`
> teaching line + tests + dist byte-pin regen.
> (Captured 2026-07-15 from the model-line payload sweep, PR #390.)

## The idea

Teach `engine.checks.check_model_line` (and the taught form's docs in
`.sessions/README.md`) that `unrecorded` is a **sanctioned terminal effort
value for retroactive payload repairs**: recorded verbatim by the PL-004
harvest (as today), but exempt from the `model-line-effort` advisory nag.

## Why

The 2026-07-15 payload sweep (PR #390) retro-fixed 4 cards whose lines were
shape-malformed or off-taxonomy. Three of them never self-reported an effort
tier, and the repairing session was not the author — backfilling `low|medium|
high` would have been **invented telemetry** polluting the PL-004
model·effort·class→outcome dataset. The honest fix (`unrecorded`) trades the
4 original advisories for 3 `model-line-effort` nags, which (a) look like
zero mechanical progress to an auditor reading `check --strict` output, and
(b) invite a later wake to "re-fix" them by inventing a tier — the exact
corruption the sweep avoided. A recognized terminal marker closes that loop:
honest repairs go advisory-silent, fabrication stays nudged-against.

## Sketch

- `MODEL_EFFORT_VALUES` stays `(low, medium, high)` (the real taxonomy the
  dataset wants from live sessions).
- `check_model_line` adds one membership check: `effort == "unrecorded"` →
  no `model-line-effort` finding (harvest unchanged — records verbatim).
- One line in `.sessions/README.md`: live sessions self-report a real tier;
  `unrecorded` is reserved for retroactive repair of cards whose author never
  reported one.
- Tests: one fixture per branch (live off-taxonomy still nags; `unrecorded`
  silent; harvest row carries `unrecorded` verbatim).

next: build — small scoped engine+docs+tests slice; dist byte-pin regen in
the same PR.
