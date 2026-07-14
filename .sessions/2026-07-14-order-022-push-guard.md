# 2026-07-14 — ORDER 022: stop-hook merged-head final-push guard

> **Status:** `complete`

About to (opening declaration): execute inbox ORDER 022 — guard the kit
stop-hook session-close final-push path so a session whose branch head is
already merged to origin/main (after a fetch) is loudly told to SKIP the
final push instead of silently re-creating the branch GitHub just deleted
(PROPOSAL 003 + ADDENDUM: primary cause is GitHub-side auto-delete not
firing for bot-merged PRs; this closes the proven secondary re-creation
path). Fail-open on unprovable ancestry (shallow clone / failed fetch):
push proceeds with a NOTE. Engine-shipped port of the scripts/_git_truth.py
ancestry primitive (parity-pinned), new `_stop_push_guard` advisory in
`evaluate_stop`, tests for all three decision branches + mutation-tested,
dist regenerated.

- **📊 Model:** Claude Fable 5 · high · feature build

Run type: worker session (coordinator-dispatched, ORDER 022).

## What shipped (PR #371)

- `src/engine/lib/git_truth.py` (new) — dist-shipped port of the
  `scripts/_git_truth.py` ancestry primitive (PR #358): `provable_ancestry`
  with the shallow-clone degradation rule, behind the injectable
  `GitCommand` seam. Parity-pinned source-identical against the scripts
  original by `tests/test_git_truth.py::TestEngineParity`. Second
  documented §3.2 TID251 subprocess carve-out (noqa at the import site;
  `pyproject.toml` ban message names both carve-outs).
- `src/engine/hooks/stop_check.py` — `_stop_push_guard`, the sixth
  `evaluate_stop` advisory: after `git fetch origin main`, merged head →
  one loud SKIP line; provable-unmerged on a fresh fetch → silent;
  unprovable (shallow / failed fetch / git error) → push proceeds with a
  NOTE (fail-open: a wrongly-skipped push loses work; a wrong push only
  re-creates a branch). Default branch / detached HEAD / not-a-repo exempt.
- `src/build_bootstrap.py` module-order entry + regenerated
  `dist/bootstrap.py` (byte-stable ×2, sha256 identical across regens).
- Tests: 8 new stop-check tests + 1 parity test (suite 1550 → 1559 passed,
  1 skipped unchanged). Mutation proof: inverting merged→SKIP failed
  `test_push_guard_merged_head_advises_skip` (+2 others); deleting the
  unmerged→silent early return failed
  `test_push_guard_unmerged_head_is_silent`; silencing the unprovable NOTE
  failed `test_push_guard_shallow_clone_notes_and_proceeds` +
  `test_push_guard_failed_fetch_notes_and_proceeds`.
- CHANGELOG [Unreleased] Added entry; `scripts/_git_truth.py` docstring
  now names its engine port + the parity pin.

Verify: `python3 scripts/preflight.py` → 7/7 green (pytest, dist-byte-pin,
ruff, idea-index, changelog-structure, program-law, bench-integrity);
`python3 dist/bootstrap.py check --strict` → all checks passed.

⚑ Decide-and-flag: engine needed its own copy of the ancestry primitive
because scripts/ never rides dist into adopters — resolved as a
source-identical port + parity test pinning the two copies together,
rather than relaxing the scripts module's "never ships" contract.

💡 Session idea: when `_stop_push_guard` fires its SKIP on a DIRTY tree,
extend the advisory with the paste-ready rescue-ref commands verbatim
(e.g. `git checkout --detach && git push origin HEAD:refs/heads/rescue/<slug>`)
— the Q-0263.2 paste-ready bar applied to the one moment an agent holds
unmerged leftovers on a deleted branch; today the line names the concept
but the agent still has to derive the commands.

⟲ Previous-session review: ORDER 021 (PR #368, EAP closeout walkthrough)
re-verified every premise live per Q-0120 and honestly retracted the #345
"green" heartbeat claim with evidence (zero check runs, merge-tree proof)
— exactly the right instinct. Improvement it surfaces: heartbeat facts
lines have grown into multi-hundred-word paragraphs (done=021 is ~180
words), which fights the machine-scan purpose; a soft length budget or a
facts/pointer split in the heartbeat grammar would keep them parseable.
