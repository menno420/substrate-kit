# Session 2026-07-11 — SessionStart handoff-push (cold-session continuity, evidence-backed)

> **Status:** `in-progress`

- **📊 Model:** claude-fable-5 · high · feature-build

**Scope (as declared, born-red):** ship the SessionStart handoff-push — the
top resume priority from `docs/gen2/next-boot.md` §0. Bench runs 4 AND 5 both
failed 0-of-3 with the same mechanism: the kit's continuity surface is
PULL-only and cold sessions never pull it (run-4 report T4 item 5: the
auto-drafted card was "never opened", `docs/current-state.md` an empty
template; run-5 report T4 item E: identical — ON resumed via `git show` in
both runs). The fix: the kit PUSHES the handoff at session start — a new
section in the SessionStart orientation composition
(`src/engine/hooks/session_start.py` `compose_orientation`) carrying the
newest session card path + status + unresolved `[[fill:]]` slot count + the
previous card's resolved "Next session should know" pointer. Mechanism chosen
over a check/CLI boot banner because the transcripts show cold sessions never
run a bootstrap command, while the SessionStart hook demonstrably FIRED in
both hook-live runs (run-5 manifest runner_notes: "Hooks LIVE on the ON arm …
SessionStart/PreToolUse/PostToolUse/Stop fired"). Also folds in the cheap
half of the run-5 grep-pollution finding (judge limitation 5): a search-hygiene
note in the planted `CLAUDE.md` template. Tests + CHANGELOG [Unreleased] +
dist regen; NO release cut; bench re-validation (run-6) is NOT this slice.
Claim: `control/claims/sessionstart-handoff-push.md` (fast-lane PR #164,
squash-merged before build — deleted by this PR's close-out). Status
heartbeat overwrite is the deliberate last content step; this card flips
`complete` as the final commit.
