# R8 — fast-lane prefix symmetry as a runtime advisory (enabler⇄guard)

> **Status:** `complete`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R8 (fast-lane prefix symmetry runtime advisory) from docs/planning/2026-07-19-night-run-idea-groom.md

- **📊 Model:** Opus 4.8 · high · feature build
- **⚑ Self-initiated:** R8 is baton work (backlog rung from the night-run groom
  R8 entry). Self-initiated decide-and-flag route-arounds within it: (1) **posture
  flip** — the R8 recipe body named `_extra_check_findings` + `guards.STRICT_SUBCHECKS`
  (exit-affecting), but building it that way reds the SAME enabler-branch drift the
  tested `check_automerge_preflight` advisory deliberately keeps warn-only
  (`test_drift_never_reds_strict_check`: "a required-check red here would be a fleet
  bomb during version skew" — reproduced live: the strict test went red until I moved
  R8 to the advisory seam). So R8 ships on the `posture="advisory"` seam like its R5/R7
  siblings — flagged. (2) **scope narrowing** — since `check_automerge_preflight` already
  owns the enabler⇄config surface, R8 covers only the complementary, otherwise-uncovered
  **enabler⇄guard** leg (a pure two-file cross-check, so it can never false-wall a
  custom-prefix host). (3) Registered the R7-surfaced PL-004 gate gap as groom idea R13
  (not built this slice).

## What shipped (PR #500)

Added `src/engine/checks/check_fastlane_symmetry.py` — an ADVISORY-only
(warn-only, never exit-affecting) `check` finding that fires when a host's
`.github/workflows/ci.yml` claims-only fast-lane guard cards a prefix its
`auto-merge-enabler.yml` never arms (`carded − armed`) — i.e. the guard cards a
branch the fast lane never touches. This is the runtime promotion of the
enabler⇄guard leg of the B-3 kit-only meta-test
(`tests/test_fastlane_prefix_symmetry.py`), so ADOPTERS catch their own drift,
not just substrate-kit's CI. It is a pure two-file cross-check (no baked-registry
pivot → false-wall-proof for hosts that customized their fast-lane prefixes) and
self-gates on BOTH surface files existing.

Wired on the `posture="advisory"` seam in `src/engine/cli.py` (compute beside
R5/R7 + a `fastlane_symmetry_advisories` emit block, mirroring `check_stale_walls`);
added to `src/build_bootstrap.py` `MODULE_ORDER`; `dist/bootstrap.py` rebuilt
byte-pin clean.

Files: `src/engine/checks/check_fastlane_symmetry.py` (new), `src/engine/cli.py`,
`src/build_bootstrap.py`, `dist/bootstrap.py` (rebuilt),
`tests/test_check_fastlane_symmetry.py` (12 tests, incl. `test_not_a_strict_subcheck`
and `test_real_kit_surfaces_are_symmetric`), `docs/planning/2026-07-19-night-run-idea-groom.md`
(R13 idea registered), `control/status.md` (heartbeat + baton→R9),
`.substrate/guard-fires.jsonl` (telemetry delta).

Evidence: full suite **1868 passed / 1 skipped** (`python3 -m pytest tests/ -q`);
`dist/bootstrap.py check --strict` exit 0 (born-red HOLD is the designed session
gate, not a defect); byte-pin `tests/test_bootstrap.py` green; `ruff check
src/engine/` + `check_changelog_structure.py` + `check_no_false_walls.py` all OK.
The advisory does NOT fire on the real kit repo (enabler arms {claude/, claim/},
guard cards {claude/} → `carded ⊆ armed`). Not a STRICT_SUBCHECK — nothing added
to `guards.py`/`_extra_check_findings`; `test_not_a_strict_subcheck` pins it
advisory. CHANGELOG untouched (R-series pattern: the release-cut session documents
R5–R8 together; `[Unreleased]` is empty at HEAD after #495–#498).

## 💡 Session idea

**Make the ci.yml claims-only guard self-declare its cardless prefixes so
`check_fastlane_symmetry` can verify the REVERSE direction too.** R8 only checks
`guard-carded ⊆ enabler-armed` because the guard's *cardless* prefixes (e.g.
`claim/`) ride the bare `*)` fallback and name no prefix — so an enabler that arms
a prefix the guard silently treats as cardless-by-default is indistinguishable from
a genuine hole, and the reverse leg (`enabler-armed ⊆ guard-known`) can't be
computed. A one-line machine-readable marker in the guard block — e.g.
`# fastlane-cardless: claim/` beside the `*)` arm — would let the check enumerate
the guard's FULL fast-lane intent (carded ∪ cardless) and flag an enabler-armed
prefix that appears in NEITHER guard set (a prefix arming the fast lane that the
guard never deliberately classified). Purely additive: the marker is a comment the
existing bash ignores; only the runtime check reads it. Deduped: grepped `docs/`
for `cardless` / `fastlane symmetry` / `reverse direction` — the only `cardless`
hits are about session-card gates, not fast-lane prefixes; nothing covers this.

## ⟲ Previous-session review

Previous session — **R7 append-log ⇄ Walls-correction disagreement lint (PR #498)**.
Did well: a clean structural sibling of R5 that correctly stayed on the advisory
seam and pinned itself off STRICT_SUBCHECKS with a `test_not_in_strict_subchecks`
negative — and its ⟲ review *surfaced the exact PL-004/`kit-feature` gate gap* this
session was asked to register (good forward-carrying of a system flaw). What it
could have done better: it asserted the gap as "either doesn't validate the
task-class or doesn't scan cards at all" — but a two-minute read of
`check_model_line.py` shows it does BOTH (validates against the 9 classes at L181,
scans cards at L214); the real gap is that it's *advisory-only + windowed to 10
cards*, so a drifted card merges green and ages out unfixed. Concrete system
improvement (now acted on): I registered the gap as groom idea **R13** with the
*accurate, cited* framing (fold the task-class check into the born-red session-gate
that already grades the PR's own added card — enforce-don't-exhort, scoped to one
card, leaving the fleet-wide window advisory). The lesson for the loop: a ⟲ review
that names a gap should *cite the source line* before hypothesizing the cause — the
guess and the ground truth here pointed at different fixes.
