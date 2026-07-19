# R9 — measure_grounded_skills --commit-results PATH

> **Status:** `complete`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R9 (harness `--commit-results PATH`) from docs/planning/2026-07-19-night-run-idea-groom.md — redirected here after a sibling claimed R8 (PR #500).

**About to do:** add a `--commit-results PATH` flag to `scripts/measure_grounded_skills.py` that persists the raw results.json as a durable artifact surviving ephemeral-container splits.

- **📊 Model:** Opus 4.8 · medium · feature build (measure_grounded_skills --commit-results PATH flag + tests)
- **⚑ Self-initiated:** R9 is baton work (#2 baton, taken after a sibling session claimed R8 / PR #500 first — avoided the duplicate). Decide-and-flag calls within it: (1) "commits" = write the JSON file to PATH, NOT a git-commit side-effect from the script (the surrounding chain does the `git add`); (2) shared `--json`'s shallow-clone REFUSE gate so a committed-but-zeroed artifact off a shallow clone can't ship. Also fixed on sight (flagged): reconciled the R7→R8→R9 heartbeat narrative drift the sibling's mid-flight R8 heartbeat left in `control/status.md` (and added the missing #500 to Recently-shipped).

## What shipped (PR #501)

Added a `--commit-results PATH` flag to `scripts/measure_grounded_skills.py`: it writes the same machine-readable payload `--json` emits to a caller-named PATH, creating the parent directory, so a GSW-style measure→verify→publish chain persists its raw results.json as a durable artifact that survives ephemeral-container splits. Both flags now share one payload build (byte-identical when both are passed) and one shallow-clone REFUSE gate — a committed-but-zeroed artifact off a shallow clone would be worse than an ephemeral one. `--json` behavior is unchanged; the flag is default-off and backward-compatible.

Files: `scripts/measure_grounded_skills.py` (argparse flag + shared write/refuse block + docstring), `tests/test_measure_grounded_skills.py` (5 new tests: durable write, parent-dir creation, byte-identical-with-`--json`, shallow-clone refuse, default-off backward-compat). Standalone `scripts/` file — NOT in `MODULE_ORDER`; `dist/bootstrap.py` untouched (confirmed).

Evidence: full suite **1863 passed / 1 skipped**; `dist/bootstrap.py check --strict` exit 0 (aside from the by-design born-red hold, now cleared by this flip); `--help` shows `--commit-results PATH`; a live run on a non-shallow tree wrote a valid results.json (top keys `generated` / `window` / `repos`) to a freshly-created parent dir, and correctly REFUSED (exit 2, no file) on a shallow clone.

## 💡 Session idea

**Stamp committed results.json with clone-depth provenance.** The `--commit-results` artifact exists precisely to survive a multi-container chain — the container that *measures* (full clone) is often not the one that later *publishes*. The shallow-clone REFUSE gate protects the measuring step, but once a good full-clone artifact is committed, the publishing step (which may itself be shallow) has no way to tell a trustworthy artifact from a REFUSE stub. Add a `clone_depth: full|shallow` (and `git_sha`) provenance field to the results payload so the publish step trusts-or-refuses on the *artifact's own* provenance, not the publishing container's clone state — the natural completion of "surviving ephemeral-container splits." Deduped: grepped the groom doc + docs/ideas for `results` / `provenance` / `clone` — R10 is harness --freeze self-cite, R11 recipes applies-when, R12 folded-gate; none touch artifact provenance. Distinct.

## ⟲ Previous-session review

Previous session — **R8 fast-lane prefix symmetry runtime sub-check (PR #500, sibling)**. Did well: it made the false-wall-safety call the kit-only B-3 meta-test couldn't — pivoting the *adopter-runtime* check on the adopter's own `config.automerge.branch_patterns` rather than the kit's baked `FASTLANE_PREFIX_REGISTRY`, so a host with custom branch patterns isn't false-walled — and it carried the atomic strict-subcheck triple (the `_extra_check_findings` call + the `STRICT_SUBCHECKS` entry + `EXPECTED_STRICT_SUBCHECKS` 7→8) cleanly past the parity meta-test. What it missed: its heartbeat was written mid-flight (`updated:` stamped 11:20:04Z, three minutes *before* #500 auto-merged at 11:23:21Z) and only advanced the *pointer* sections — `phase:` / baton / Backlog went to R9, but `## This wake`, `## Recently shipped`, and `## PR state` were left describing R7, and #500 itself never got added to Recently-shipped. This session reconciled that drift on sight. Concrete system/workflow improvement it surfaces: the heartbeat is overwritten wholesale each session, and the born-red flip gates on the *card* badge, not on heartbeat internal consistency — so a rushed/partial rewrite merges with cross-section drift the next session must clean up. A lightweight `check` advisory that asserts status.md self-consistency (the PR number in `phase:`, `## This wake`, `## PR state`, and the top `## Recently shipped` entry all agree) would catch a partial heartbeat before it merges — the enforce-don't-exhort closure for exactly this drift class, and a good future R-rung.
