# 2026-07-11 — gate fixes: grade modified siblings + red on card deletions (disposition of #226)

> **Status:** `complete`

- **📊 Model:** fable-5 · high · engine gate fix (one scoped PR)

## Scope (what is about to happen)

Coordinator-dispatched worker slice (claim
`control/claims/claude-gate-sibling-deletion-fix.md`, main @ b441b22).
Disposition of the external gate-generation review, PR #226: two verified-real
findings fixed, one refuted.

1. **G-1 (real)** — in the generated adopter gate (`live_ci_workflow()`,
   `src/engine/adopt.py`), sibling cards MODIFIED by a diff that also adds
   card(s) are advisory-only, so a PR adding one good card can silently break
   a sibling (flip it in-progress, strip markers) and still merge. Fix: grade
   modified siblings through the SAME `--require-session-log` locked door the
   modified-only branch uses — strictly tighter, cannot reintroduce the
   tail-1 shadowing #187 fixed. Supersedes #187's advisory-sibling design
   (decide-and-flag).
2. **G-2 (real)** — both the generated gate and the kit's own dogfood gate
   (`.github/workflows/ci.yml`) build the card list with `--diff-filter=d`
   (excludes deletions), so a deletion-only PR falls to the no-card path and
   can merge while erasing session memory. Fix: capture `--diff-filter=D`
   deletions and hard-red the gate on both surfaces.
3. **B-1 (refuted)** — dist MODULE_ORDER completeness is already proven by
   `tests/test_bootstrap.py::test_module_order_covers_every_engine_module`
   (PR #147, 6f87900), in CI. No change.

Tests for both fixes (static + behavioral via the #187 scratch-git harness),
CHANGELOG `[Unreleased]` entries, dist regenerated (byte-pin). After merge:
comment per-finding on #226 and close it, then status heartbeat.

## Close-out

Shipped the declared scope exactly — build commit f75460c, flip-complete is
this commit. Tests **1029 → 1034** (+5: one static deletion pin, three
generated-gate scratch-repo shapes — added-good + broken-sibling red,
healthy-sibling green, deletion-only red — and the ci.yml deletion-only
mirror); the two existing sibling pins re-pinned from the advisory text to
the locked-door text; interpreter thread count 4 → 5. Ruff clean; dist
byte-pin clean (**691876 B**, deterministic rebuild); idea-index /
program-law / bench-integrity OK.

Design decisions (decided-and-flagged, evidence on each):
- **D1 — sibling grading supersedes #187's advisory design** (the veto-window
  item in control/status.md ORDER-013 self-review (c)): grading modified
  siblings through the modified-only branch's exact locked door is strictly
  tighter — the added card still gates via its own `--added-card` lane, so a
  sibling verdict can only ADD red, never substitute; the #33 tail-1
  shadowing cannot be reintroduced. Prompted by external review #226 G-1.
- **D2 — deletion red is unconditional** (no carve-out lane): session memory
  is append-only by convention; a legitimate card rename would ship as
  add+delete and needs a human-visible red to justify itself. Both surfaces
  get the identical guard so kit dogfood and adopter gates can't drift.
- **D3 — B-1 refuted, not "fixed":** the review's recommended checker already
  exists (`test_module_order_covers_every_engine_module`, PR #147 commit
  6f87900, in CI via kit-quality pytest) — no code shipped for it.

## 💡 Session idea

The gate's deletion guard now distinguishes D from d — but a RENAME
(`--diff-filter=R`) of a session card currently surfaces as a plain modify
with the new path graded and the old path silently gone from history's
expected location. Cheap follow-up: capture `--diff-filter=R` with
`--name-status` in the generated gate and log an advisory naming
old → new, so card renames are visible in the gate log (and a later slice
can decide whether renames deserve the deletion-tier red or stay legal).

## ⟲ Previous-session review

The v1.12.0 release slice (#224/#225/#227) ran the claim → bump → verify →
close-out chain cleanly, and its three-way sha256 verification (asset =
release.json = committed dist) is exactly the paranoia a release lane needs.
One improvement it surfaces: its status RECORD is enormous (status.md is
~127KB) — the heartbeat file is drifting from "current state" toward "full
history", which slows every session's orientation read. Workflow
improvement: cap status.md at the current phase + last N records and move
older records to an archive file (mirrors the .session-journal archive
convention this program already uses elsewhere).
