# Session · 2026-07-19 · r4-hook-census

> **Status:** `complete`

Intent: task R4 (HOOK_CENSUS) — the second fourth-surface guard vector.
Building HOOK_CENSUS — pinning the kit's four Claude Code lifecycle hooks so a
new hook can't ship unregistered/unclassified.

- **📊 Model:** Opus 4.8 · high · feature build
- ⚑ Self-initiated: none — R4 is baton-directed work (dispatched from the R4
  HOOK_CENSUS baton in `docs/planning/2026-07-19-night-run-idea-groom.md`), not
  self-initiated. One decide-and-flag call: the recipe said "git-hooks" but the
  kit ships zero git-hooks, so I censused the four real Claude Code **lifecycle
  hooks** instead (flagged in the PR #493 body, gate flag 1).

## What shipped (PR #493)

- **`HOOK_CENSUS` in `src/engine/guards.py`** — one entry per real lifecycle hook,
  keyed by its `cli._HOOK_EVENTS` dispatch event, each classified by kind. New kind
  constants `HOOK_ENFORCING` / `HOOK_ADVISORY` / `HOOK_ORIENTATION` (+ `HOOK_KINDS`)
  and copy-returning accessors, mirroring the shape of `WORKFLOW_JOB_CENSUS` (#470).
  The census pins **all four** planted hooks: 3 fail-open `ADVISORY` guards (exactly
  `cli._HOOK_GUARD_KINDS`) + 1 `ORIENTATION` injector (SessionStart, absent from the
  guard-kinds set).
- **8 meta-tests** in `tests/test_guard_surface_census.py`: bidirectional
  set-equality of the census keys vs `cli._HOOK_EVENTS`, the `ADVISORY` subset vs
  `cli._HOOK_GUARD_KINDS`, kind-validity, expected-advisory-count, and an
  `ENFORCING`-references-a-pin guard for the (currently empty) enforcing set — so
  adding/removing a hook without censusing it reds the kit's own suite.
- **Dist rebuilt** via `python3 src/build_bootstrap.py` (byte-pin clean).

## Verification

- `python3 -m pytest tests/ -q` → **1832 passed** (full suite green, +8 over R3's 1824).
- `python3 dist/bootstrap.py check --strict` → red ONLY by the born-red HOLD
  (in-progress card + 4 `[[fill:]]` slots); clears to green once this card flips
  `complete`.
- PR #493 born-red by design; auto-merges (armed, squash) on green CI after this flip.

## 💡 Session idea

**A `check_surface_census` advisory (kit-quality / `check`) that surfaces the whole
census family in `bootstrap check` output** — one advisory line per pinned surface
(guard manifest, `WORKFLOW_JOB_CENSUS`, and now `HOOK_CENSUS`) reporting its entry
count and kind breakdown, e.g. `census: 4 hooks pinned (3 advisory · 1 orientation ·
0 enforcing) · N jobs · N guards`. Worth having because gate flag 3 of *this very PR*
names the gap: all three censuses are **kit-only pytest meta-tests** that redden the
kit's suite on drift but are **invisible to adopters**, who only ever run `check`
(pytest is not part of an adopter's loop). An advisory readout — same fail-open posture
as `check_status_current` / `check_model_line`, so it never pre-reddens adopters — turns
the census family from "silently pinned in the kit" into "visible everywhere `check`
runs", which is the surface where an agent actually reads it. Deduped: grepped
`docs/ideas/` for `census` — zero matches; this is a net-new candidate, not a restatement.

## ⟲ Previous-session review

Previous session — **R3 shallow-clone REFUSE marker (PR #492)**. Did well: it turned a
prose trap into an *enforced* refuse-to-publish (REFUSE marker + exit 2) and scoped the
guard tightly — only the `--json` publish path refuses, the markdown/stdout path keeps
its existing soft-null, so no false failure on the common case — and it added both a
negative (shallow-refuses) and a positive (full-clone-writes-JSON) test, which is the
right pair for a guard. What it could improve: its own 💡 already spotted that
`measure_pr_latency.py` carries the *same* unguarded shallow trap, yet R3 hardened only
one of the two scripts — the fix and the follow-up gap were named in the same breath but
the follow-up wasn't seeded as a `docs/ideas/` file, so it risks the orphaning the groom
doc exists to prevent. System improvement it surfaces: the **census pattern this session
built is the durable answer to R3's one-off** — instead of each measurement script
re-implementing (or forgetting) `is_shallow()`, a *measurement-script census* (mirroring
`HOOK_CENSUS`/`WORKFLOW_JOB_CENSUS`) enumerating every git-history-reading script and
asserting each routes through the shared `require_full_history()` seam R3's 💡 proposed
would make "forgot to guard the new script" a kit-red condition, not a latent trap — the
same enforce-don't-exhort move, applied to the surface R3 left half-covered.
