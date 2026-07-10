# Session 2026-07-10 — EAP §6.1: substrate-gate.yml declared kit-owned (regenerated on adopt/upgrade)

> **Status:** `complete`

- **📊 Model:** claude-fable-5 · medium · engine+tests

**Scope (as declared, born-red):** the coordinator's program-review §6.1 slice
(spec: menno420/superbot `docs/eap/eap-program-review-2026-07-10.md` §6.1;
claim `claimed-by: eap-review-6.1 kit-eap61-lane 2026-07-10T16:42Z`, fast-lane
PR #129, landed before this build work per the ORDER 007 ritual).

§6.1 has two halves. The first — port gba-homebrew's ADDED-advisory /
MODIFIED-locked born-red gate fix into the kit's generated gate template —
**already shipped on main via PR #108** (claim `gate-template-sentinel-fixes`;
verified this session: the `live_ci_workflow()` output is functionally
identical to gba-homebrew's shipped `.github/workflows/substrate-gate.yml` at
their HEAD — comment wording only differs). So this slice ships the second
half plus alignment:

1. **Declare `.github/workflows/substrate-gate.yml` kit-owned** — once the
   live gate EXISTS, every adopt/upgrade pass regenerates it in place (the
   existing staged-artifacts-always-regenerate mechanism, extended to the one
   live workflow the kit installs), so upstream gate fixes reach installed
   gates instead of stranding as hand-forked patches. A default adopt still
   never CREATES live CI (safety doctrine unchanged — only
   `--wire-enforcement` installs it; existence is the opt-in signal after
   that). The generated header now declares the ownership out loud.
2. Update the commented `ci_snippet()` example + refresh the kit's own stale
   `.substrate/ci/quality.yml.example` to the current snippet.
3. Tests for the new kit-owned semantics; CHANGELOG [Unreleased]; dist regen
   (byte-pin).

NOT in this slice: distributing the regenerated gate to adopter repos — that
is the next release's distribution wave (noted as follow-on in status.md).

## Close-out

**Shipped (session PR #130; claim fast-lane PR #129 → d3352f1):**

- `src/engine/adopt.py` — step (6b) kit-owned regeneration: an EXISTING
  live gate is regenerated in place on every adopt/upgrade pass
  (byte-compare → `regenerated:` / `kept: (kit-owned, already current)`
  report lines); `--wire-enforcement` still the only path that CREATES it.
  Generated header + `live_ci_workflow()` / `adopt()` docstrings +
  `ci_snippet()` declare the ownership; host carve-outs routed to a
  separate workflow file.
- `tests/test_adopt.py` — the old never-clobber test deliberately INVERTED
  to kit-owned semantics (regenerate under wire-enforcement; regenerate on
  default adopt when the gate exists; idempotent second pass; header
  declaration). `tests/test_upgrade.py` — upgrade regenerates a stale gate;
  upgrade never creates an uninstalled one.
- `.substrate/ci/quality.yml.example` refreshed (was stale, pre-KL-8
  wording); `CHANGELOG.md` [Unreleased] Changed entry (with the adopter
  overwrite warning); dist rebuilt, byte-pin verified clean locally.

**Verified:** `python3 -m pytest tests/ -q` → **823 passed** (819 on main →
823: +5 new, −1 inverted); `python3 -m ruff check src/engine/` clean;
`python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py`
clean; `check --strict` green except this card's own born-red hold
(by design — this flip clears it).

**Mid-flight note:** the coordinator flagged PR #130's first CI run
(29108440904) red as a possible breakage — diagnosis: kit-quality failed
ONLY on `session log … badge still says in-progress` (the born-red hold
working as designed), and the other two reds are the legacy-alias jobs
mirroring kit-quality's result by design. No breakage; no fix needed.

**⚑ Follow-on (next release's distribution wave, NOT this slice):** adopter
repos with installed gates (gba-homebrew's hand-fixed copy included) receive
the kit-owned regeneration on their next `bootstrap upgrade` — their next
upgrade OVERWRITES hand edits to the gate by design; host carve-outs belong
in a separate workflow file from now on.

**💡 Session idea:** the kit-owned overwrite is silent about WHAT changed in
the gate — a one-line unified-diff summary in the adopt/upgrade report
(`regenerated: … (+N/−M lines)`) would let an adopter's upgrade-PR reviewer
see gate deltas without opening the file; cheap (difflib is already
imported in upgrade.py) and it generalizes to any future kit-owned file.

**⟲ Previous-session review:** the ORDER 011 lane (#127/#128) was clean —
claim-first, born-red, CI-immutable results respected, and the ROUTINE STATE
cutover record is exemplary provenance. One improvement it surfaces: its
status heartbeat announced this §6.1 slice as "in flight" before any claim
existed for it — an announced-but-unclaimed slice is exactly the twin-work
window the claim ritual closes; next time, either claim it in the same
overwrite or mark it "queued (unclaimed)". This session closed that gap via
claim PR #129.
