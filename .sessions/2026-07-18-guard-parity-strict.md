# Session · 2026-07-18 · guard-parity-strict

> **Status:** `complete`

Intent: pin the `bootstrap check --strict` sub-check surface by adding a `STRICT_SUBCHECKS` manifest to `engine/guards.py` and a set-equality parity test, so a strict sub-check (check_ledger, check_no_false_walls, etc.) can't be dropped or renamed silently.

- **📊 Model:** Opus 4.8 · high · test writing
- ⚑ Self-initiated: yes — extended guard-parity to the 3rd surface (bootstrap check --strict sub-checks) — rung-b baton candidate from PR #465's heartbeat, decide-and-flag.

## What I did

Pinned the third enforcing guard surface — the `bootstrap check --strict` sub-checks — so it can no longer drift silently, closing the gap the first two surfaces (ci.yml `kit-quality` steps and the generated adopter `substrate-gate` job) already had covered.

- `src/engine/guards.py` — added `STRICT_SUBCHECKS`, a 7-entry registry (`check_ledger`, `check_stamp_discipline`, `check_namespace`, `check_seam_authority`, `check_no_false_walls`, `check_orientation_budget`, `check_engagement`), each classified `ADOPTER_ALWAYS` or `ADOPTER_WHEN_CONFIGURED` with a one-line reason, plus name/reason accessors mirroring the existing `REGISTRY` shape.
- `tests/test_guard_parity.py` — added 3 tests that parse the live `cli._extra_check_findings` source and assert bidirectional set-equality against the registry (a hand edit to EITHER side — dropping/renaming a `check_*()` call, or the registry entry — goes red), plus a reason-quality test and a count floor (`EXPECTED_STRICT_SUBCHECKS = 7`).
- Rebuilt `dist/bootstrap.py` (byte-pin green).

Evidence: 7/7 guard-parity tests pass, byte-pin green, full suite **1768 passed / 1 skipped**, `dist/bootstrap.py check --strict` exit 0. Commits 485d922 (born-red) + 4791749 (impl).

## 💡 Session idea

**Guard-surface census — a meta-test/doc that enumerates ALL enforcing guard surfaces in the kit and asserts each carries a parity pin.** Three enforcing surfaces are now each guarded independently — ci.yml `kit-quality` steps, the generated adopter `substrate-gate` job, and (this PR) the `check --strict` sub-checks — but nothing prevents a FOURTH enforcing surface (a new git-hook, a new workflow job) from shipping with NO parity assertion at all. A single census that lists every enforcing surface and fails until each has a registry + parity test would make "add an enforcing surface without pinning it" structurally impossible, rather than relying on the author to remember. Small, test-only, reversible. Deduped `docs/ideas/` + `docs/roadmap.md` for "census"/"guard.surface"/"parity" — the nearest neighbours (`guard-parity-kit-vs-adopter-2026-07-18.md`, the 2-surface origin idea; `t5-headless-guard-surface-2026-07-09.md`, a different headless-hook hole) are not this; the census is a genuinely new meta-level over them. Idea used: the census (deduped, not a dup).

## ⟲ Previous-session review

Of PR #465 (the guard-kit-side wake): genuine credit — it retired the ci.yml⇄manifest codegen baton as a *verification-covered null* rather than building a 388-line generated workflow that would have added brittleness for zero safety, and left a durable in-code trace so the null is not re-chased. Choosing the honest null over busywork was the right call. One concrete system improvement it surfaces: all three guard surfaces now each re-implement a bespoke source-slicing parser inside `tests/test_guard_parity.py` (each greps a different live source region to recover its guard set), and a future 4th surface would re-implement the parser a fourth time — extracting a shared source-set-extractor helper would let that parser logic be written and tested once, then reused per surface.
