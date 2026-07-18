# 2026-07-18 · guard-parity kit-side — verification closes the codegen baton

> **Status:** `in-progress`

## Scope
Resolve the rung-2 baton from PR #463's heartbeat: "drive ci.yml's kit-quality
step NAMES from the `src/engine/guards.py` manifest via codegen (`--emit-kit-ci`),
closing the last hand-kept guard copy." Determine whether that last hand-kept
copy (ci.yml `kit-quality` step names ⇄ manifest `REGISTRY` keys) actually needs
codegen, or is already closed by the verification landed in #463.

## What I'm about to do
- Establish what `tests/test_guard_parity.py` already enforces between ci.yml's
  `kit-quality` step names and the `guards.py` `REGISTRY` keys.
- Prove by mutation whether a hand edit to EITHER side already goes red.
- If already covered: honest null on the codegen baton + a durable in-code trace
  so the baton is not re-chased, then the next-highest-value slice.
- Drift-fix-on-sight (same PR): remove the stale
  `control/claims/release-v1-19-0.md` claim (v1.19.0 released+verified, PR #461
  merged, card flipped — the claim was never cleaned up); correct the status.md
  Backlog line ("v1.18.0 adopter wave" → "v1.19.0 adopter wave", matching the
  live ⚑ block).
