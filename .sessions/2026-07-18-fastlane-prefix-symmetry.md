# Session · 2026-07-18 · fastlane-prefix-symmetry

> **Status:** `complete`

Intent: B-3 — pin the fast-lane branch-prefix set so the auto-merge-enabler,
the claims-only fast-lane guard, and the engine defaults can't silently drift
out of sync. A new seat prefix added to one surface but not another reopens a
card-less merge hole (enabler arms a prefix the guard doesn't card) or the
kit#293 green-and-unarmed stall (guard cards a prefix the enabler never arms).

- **📊 Model:** Opus 4.8 · high · kit-engine meta-test + guard registry
- ⚑ Self-initiated: none — B-3 is a groomed-baton slice (docs/planning/2026-07-19-grounded-skills-window-run.md) under the ORDER 048 standing grant. The lint DESIGN is decide-and-flag: registry-in-guards.py + test-only meta-test (no check --strict wiring, matching test_guard_surface_census.py); surfaces asserted = enabler workflow, ci.yml guard carded-case, adopt.DEFAULT_AUTOMERGE_BRANCH_PATTERNS, claim.BRANCH_PREFIX, adopter-enabler generator; deliberately OUT of scope = the label-keyed disarm workflow and the prose control/claims/README.md (neither holds a machine-checkable prefix set). Flagged for review.

About to: add `FASTLANE_PREFIX_REGISTRY` (+ kinds, floor, accessors) to
`src/engine/guards.py` and a stdlib-only meta-test
`tests/test_fastlane_prefix_symmetry.py` asserting all live surfaces agree
with the registry both directions; rebuild `dist/bootstrap.py`.

## What shipped

Pinned the fast-lane branch-prefix set so the three surfaces that duplicate it
can no longer drift out of sync. Before, `claude/` and `claim/` lived
independently in the auto-merge-enabler workflow, the claims-only fast-lane
guard in `ci.yml`, and the engine defaults, with nothing asserting agreement — a
new seat prefix added to one surface but not another silently reopened a
card-less merge hole (enabler arms a prefix the guard never cards) or the
kit#293 green-and-unarmed stall (guard cards a prefix the enabler never arms).

- `src/engine/guards.py` — new `FASTLANE_PREFIX_REGISTRY` (`claude/`→carded,
  `claim/`→card-less) + `FASTLANE_KINDS`, `EXPECTED_FASTLANE_PREFIXES` floor,
  and three accessors, mirroring the `WORKFLOW_JOB_CENSUS` house style.
- `tests/test_fastlane_prefix_symmetry.py` — 10 stdlib-only tests (no
  subprocess, §3.2) parsing the live enabler `startsWith` terms, the `ci.yml`
  guard's carded `case` arm, `adopt.DEFAULT_AUTOMERGE_BRANCH_PATTERNS`,
  `claim.BRANCH_PREFIX`, and the adopter-enabler generator — bidirectional
  set-equality against the registry, so prefix drift in EITHER direction reds CI.
- `dist/bootstrap.py` — rebuilt via `src/build_bootstrap.py` (byte-pin clean on
  fresh rebuild).

Out of scope by design: the label-keyed disarm workflow (keys on the
`do-not-automerge` label, not a prefix) and the prose `control/claims/README.md`
(no machine-checkable prefix set).

Verify: `python3 -m pytest tests/ -q` → 1796 passed, 1 skipped (new file 10/10);
`python3 -m ruff check src/engine/` clean; `python3 dist/bootstrap.py check
--strict` green after the flip; dist byte-clean on fresh rebuild.

## 💡 Session idea (Q-0089)

**Promote the fast-lane prefix symmetry from a kit-only pytest meta-test to a
runtime `check --strict` advisory (`check_fastlane_symmetry`) so ADOPTERS catch
their own enabler↔guard prefix drift.** B-3 pins the set for the kit, but the
meta-test only runs in the kit's own `tests/` suite — adopters fork the enabler
and the claims guard yet never run the kit's pytest, so an adopter that adds a
seat prefix to their enabler but not their guard gets no signal today. A
`src/engine/checks/check_fastlane_symmetry.py` that reads the adopter's OWN live
`.github/workflows/` + config, wired into `_extra_check_findings` +
`guards.STRICT_SUBCHECKS` (bump `EXPECTED_STRICT_SUBCHECKS`), would travel in
`dist/bootstrap.py` and red every adopter's `bootstrap check --strict` on the
same drift — turning a kit-local test into fleet-wide enforcement. Worth having:
it closes the exact hole B-3 closes, but for the ~19 adopters instead of only
the kit. [DEDUP: grep docs/ideas/ for fastlane / prefix / symmetry / check_fastlane
returned only unrelated hits — the control-fast-lane short-circuit idea
(adopt-plants-pytest-gate-step-2026-07-10.md) and the claims-only fast-lane
guard-parity idea (guard-parity-kit-vs-adopter-2026-07-18.md, README.md L62/L148);
no prior idea for a prefix-symmetry check or `check_fastlane_symmetry`. New.]

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18 B-2 self-row-registry-stamp wake (PR #472): **genuine
credit** — it wired the self-restamp **network-free** (`local_self_scan` /
`restamp_self_row` off the local version home) into `cut_release.py`, so the
version-bump PR carries the correct self-row inline with no network dependency
and no manual aftermath hop — a clean removal of a recurring drift class. **What
it could improve:** its own 💡 flagged that `restamp_self_row` bumps the
config-pin cell but leaves the tree cell lagging until the aftermath dist
rebuild, so the bump PR momentarily commits a self-drifting `adopters.md` — the
session *identified* a window it had just created but *deferred* the close to a
follow-up rather than reordering the flow inline, where "bugs-first, durably /
fix drift you can SEE" would have closed it in the same PR. **System improvement
it surfaces:** when a session's own Q-0089 idea names a contained window the
session itself introduced, the ender flow should ask "fixable inline now?"
before filing it as a follow-up — a self-created window deferred to a future
wake is exactly the see-it-fix-it class the working agreement says not to leave
behind.
