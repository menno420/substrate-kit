# 2026-07-14 — shared git-truth helper (shallow/graft degradation, extracted once)

> **Status:** `in-progress`

About to (opening declaration): build the #357 card's 💡 ender — extract the
"negative git ancestry answers are unreliable on shallow/grafted clones —
degrade honestly, never false-FAIL" rule into ONE shared module
(`scripts/_git_truth.py`: `is_shallow()`, `provable_ancestry()`), refit its
consumers (`check_idea_index.py` merged-reality leg, `verify_release.py` tag
leg) behavior-preserving, add helper-level tests on tmp git repos, and append
the shallow-graft false-negative finding to `docs/CAPABILITIES.md`.

- **📊 Model:** fable-5 · high · refactor build

Run type: worker session (Night-16 slice, coordinator-dispatched).
