# 2026-07-18 · guard-parity kit-side — verification closes the codegen baton

> **Status:** `complete`

## Scope
Resolve the rung-2 baton from PR #463's heartbeat: "drive ci.yml's kit-quality
step NAMES from the `src/engine/guards.py` manifest via codegen (`--emit-kit-ci`),
closing the last hand-kept guard copy." Determine whether that last hand-kept
copy (ci.yml `kit-quality` step names ⇄ manifest `REGISTRY` keys) actually needs
codegen, or is already closed by the verification landed in #463.

## What I did
- Established what `tests/test_guard_parity.py` already enforces between ci.yml's
  `kit-quality` step names and the `guards.py` `REGISTRY` keys.
- Proved by mutation that a hand edit to EITHER side already goes red.
- Honest null on the codegen baton + a durable in-code trace so it is not
  re-chased; folded in two drift fixes.

## Outcome — shipped (honest null on the codegen baton, evidenced)
The rung-2 codegen baton is already closed by verification.
`tests/test_guard_parity.py::test_every_kit_quality_step_is_classified` asserts
exact set-equality in BOTH directions between the `guards.py` `REGISTRY` keys and
the live ci.yml `kit-quality` step names (`unclassified = ci − REGISTRY`,
`stale = REGISTRY − ci`, both empty), so a hand edit to either side goes red.
Proven by mutation both ways (2026-07-18):
- ci.yml step rename `Install dev tools`→`…XXX`: FAIL — `unclassified={'Install dev tools XXX'}`, `stale={'Install dev tools'}`.
- `REGISTRY` key rename `Install dev tools`→`…YYY`: FAIL — mirror image (`stale={'…YYY'}`, `unclassified={'Install dev tools'}`).
Baseline and post-revert suites both 4/4 green; tree clean after each experiment.

`--emit-kit-ci` codegen would generate a 388-line static, mixed-shell-logic
workflow to save re-typing ~18 names a test already guards — brittleness for zero
added safety. ci.yml is a static file GitHub reads directly; drift-DETECTION is
the terminal design, not generation-verification. Recorded as a durable in-code
trace (`tests/test_guard_parity.py` module docstring) and retired in the
status.md next-2 baton so it is not re-chased.

Drift-fixed on sight (same PR): removed the stale
`control/claims/release-v1-19-0.md` claim (v1.19.0 released+verified, PR #461
merged, its card flipped complete — never cleaned up); corrected the status.md
Backlog line (v1.18.0 → v1.19.0 adopter wave, matching the live ⚑ block).

Verify: `python3 -m pytest tests/ -q` → 1765 passed, 1 skipped; guard-parity 4/4;
`python3 dist/bootstrap.py check --strict` → the only exit-affecting red was this
card's born-red hold (cleared at this flip). Tests-only docstring + control-only
diff → `dist/bootstrap.py` unmodified (byte-pin gate untouched). Commits d723282
(born-red) · 1017a30 (deliverable + heartbeat) · this flip.

- **📊 Model:** opus-4.8 · medium · review/verify (guard-parity kit-side coverage + drift cleanup)

💡 Session idea: **Guard-parity for the THIRD surface — `bootstrap check --strict`
sub-checks.** `tests/test_guard_parity.py` pins parity between ci.yml's
`kit-quality` steps and the generated adopter `substrate-gate` job, but several
enforcing guards run in `bootstrap check --strict` rather than as a ci.yml step —
e.g. "No false merge-walls" (PR #450), which the `guards.py` REGISTRY classifies
KIT_ONLY *because* it propagates via check --strict, not a CI step. Nothing
asserts the check-strict guard set stays in agreement with what adopters actually
enforce. A manifest entry + a parity assertion for that surface would close it.
Small, test-only, reversible; not built this wake. (Dedup-checked against
docs/ideas/ — distinct from the kit-vs-adopter guard-parity idea, which is the
ci.yml↔substrate-gate surface, not check --strict.)

⟲ Previous-session review — PR #463 (guard-manifest single-source): genuine
credit — it single-sourced the kit↔adopter mapping into `src/engine/guards.py` so
the ADOPTER side can no longer drift by construction (the generator imports the
step-name constants), verified byte-identical + dist reproducible. Small miss:
its 💡 idea queued the ci.yml codegen baton framing it as still-owed
("generation-verified rather than drift-detected"), but the parity meta-test it
built on already gives bidirectional drift-DETECTION that fully satisfies "a hand
edit goes red" for a static file — so the queued baton was, on inspection, already
closed, and this wake spent a cycle confirming it (evidenced null). System
improvement: when queuing a "close the last hand-copy via codegen" baton, first
check whether verification already gives the same guarantee — codegen is warranted
only when the artifact is fully generatable (like dist/bootstrap.py), not for a
static file GitHub reads directly.

⚑ Self-initiated: the durable-trace docstring note, retiring the codegen baton,
and removing the stale `release-v1-19-0` claim were my decide-and-flag calls under
the ORDER 048 standing grant; flagged here for review. No irreversible / external
actions taken.
