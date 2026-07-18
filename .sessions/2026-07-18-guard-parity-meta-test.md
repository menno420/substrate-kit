# Guard-parity meta-test — kit-vs-adopter guard drift detector

> **Status:** `complete`

Added `tests/test_guard_parity.py` — a meta-test that fails CI when an enforcing
`kit-quality` guard in `.github/workflows/ci.yml` has no mirrored counterpart in
the generated adopter CI (`src/engine/adopt.py` `live_ci_workflow()`), unless it
is allowlisted as legitimately kit-only with a one-line reason. Closes the drift
class PR #457 had to close by hand (the #455/#457 gap).

- **📊 Model:** opus-4.8 · high · test writing (kit self-improvement / CI meta-guard)

Run type: coordinator-assigned worker lane under fm control/inbox.md ORDER 048
standing grant (decide, build, land on green; green CI + cross-agent review ARE
the review).

## What shipped (PR #459)

- `tests/test_guard_parity.py` — a stdlib-only meta-test (no YAML parser, no
  subprocess, same string-splitting convention as `test_ci_control_lane.py` /
  `test_adopt.py`). It carries a maintained `REGISTRY` with exactly one entry
  per NAMED `kit-quality` step, three-way classified as `SETUP` (non-enforcing
  setup/detect/echo), `MIRRORS(<adopter step>)` (enforcing, with a live
  counterpart in the generated `substrate-gate`), or `KIT_ONLY(<why>)`
  (enforcing but legitimately kit-only, with a reason).
- Four assertions: (1) every kit-quality step is classified and REGISTRY has no
  phantom keys — the primary drift-catch, so a new kit guard cannot be added
  silently; (2) every `MIRRORS` target names a step that actually exists in
  `live_ci_workflow()` — catches the reverse of #457-class drift; (3) every
  `KIT_ONLY` reason is non-empty/descriptive — the allowlist can never be a bare
  escape hatch; (4) an anchor floor (5 MIRRORS + 10 KIT_ONLY) so the registry
  cannot be gutted to a vacuously-green empty pass.
- The parser isolates ONLY the `kit-quality` job block (stops at the next
  2-space-indented job key), so `legacy-alias-test` / `legacy-alias-smoke` never
  bleed in.

## Verification

- `python3 -m pytest tests/test_guard_parity.py -q` → 4 passed.
- `python3 -m pytest tests/ -q` → 1765 passed, 1 skipped (Python 3.10 floor).
- Independent cross-check: 18 named kit-quality steps ⇄ 18 REGISTRY keys, exact
  set match (no unclassified, no stale); 3 SETUP / 5 MIRRORS / 10 KIT_ONLY; all
  5 MIRRORS targets present verbatim as named steps in the generated adopter
  `substrate-gate` job.
- `dist/bootstrap.py` unmodified — this is a test-only change, no `src/engine/`
  edit, no rebuild.

## ⚑ Self-initiated

Guard-parity meta-test (`tests/test_guard_parity.py`), rung-4 per the logged idea
`docs/ideas/guard-parity-kit-vs-adopter-2026-07-18.md`. Rationale: makes a new
`kit-quality` guard without an adopter counterpart or a justified kit-only
allowlist entry fail CI, so the #457 drift class cannot recur silently.

## 💡 Session idea

A canonical declarative **"guard manifest"** — one file listing every enforcing
guard, its surface (a CI workflow step vs. a `bootstrap check --strict`
sub-check, since guards like "No false merge-walls" live in check-strict per
PR #450, not as a CI step), and its adopter-propagation status — that BOTH the
CI-workflow generation and this parity test read from, so the kit↔adopter guard
mapping stops being hand-maintained in two places. Why: this test mitigates the
two-places-by-hand risk but does not eliminate it; a single declarative source
would remove it at the root. (Kept as a one-liner here, distinct from the
existing `guard-parity-kit-vs-adopter-2026-07-18.md` idea file — no new idea file
so the idea index is untouched.)

## ⟲ Previous-session review

PR #457 propagated the claims-only guard to the adopter CI by hand and — to its
credit — logged the guard-parity meta-test as a durable idea rather than fixing
only the one instance, which is exactly what let this session close the whole
drift class. What it could have done better: it added the adopter guard and its
`test_adopt` pin but not a parity assertion in the same PR, leaving a one-PR
window for renewed drift. System improvement: the guard-manifest idea above —
the mapping being hand-maintained across `ci.yml` and `live_ci_workflow()` is the
residual risk this test mitigates but does not eliminate.
