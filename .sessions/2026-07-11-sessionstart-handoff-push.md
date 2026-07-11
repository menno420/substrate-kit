# Session 2026-07-11 — SessionStart handoff-push (cold-session continuity, evidence-backed)

> **Status:** `complete`

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

## Close-out (PR #165)

- **Shipped:** the SessionStart handoff push — `compose_orientation`
  (`src/engine/hooks/session_start.py`) gains section 2 (right after the
  status header, EVERY depth incl. observe/minimal): newest session card
  path + status (`complete` / `in-progress/drafted`) + unresolved `[[fill:]]`
  slot count + the previous card's resolved "Next session should know"
  pointer (last resolved match wins; unresolved slots never pushed) + one
  read-this-first line. Excerpt capped at 300 chars (M1 footprint lesson).
  Live-verified end-to-end in a scratch adopter via the rebuilt dist:
  `bootstrap.py hook sessionstart` prints the pushed handoff at slot 2.
- **Mechanism decision (decide-and-flag), grounded in transcripts:** hook
  push, NOT a check/CLI boot banner — run-5 manifest runner_notes prove
  SessionStart fires in cold sessions ("Hooks LIVE on the ON arm …
  SessionStart … fired") while no cold session in run-4 or run-5 ever ran a
  bootstrap CLI command (transcripts: T4 went find → git log → git show), so
  a banner would never be encountered. Flagged design choices: (1) rendered
  at minimal/observe depth too — a pointer informs, imposes nothing; (2) the
  next-boot idea's "current-state top" component was deliberately DROPPED —
  both T4 runs show sessions already pull current-state.md unprompted (and
  found an empty template); the card is what pull missed, and duplicating
  current-state would inflate the M1 regression.
- **Grep-pollution disposition (run-5 judge limitation 5):** cheap half
  folded in — search-hygiene note in the planted `CLAUDE.md.tmpl` naming the
  exclusion flags; mechanical fix (planted ignore/attributes) queued in
  `control/status.md` QUEUED KIT FIXES with the citation.
- **Tests:** 938 → 947 (9 new in `tests/test_hook_session_start.py`);
  `ruff check src/engine/` clean; dist rebuilt (`625817` bytes) and byte-pin
  green; `check --strict` red only on this card's designed born-red hold.
- **NOT this slice:** no release cut; bench re-validation (run-6) needs the
  P4 daily loop per queue-state.
- Claim `control/claims/sessionstart-handoff-push.md` (PR #164) deleted by
  this commit.

## 💡 Session idea

Make the continuity measure mechanical: a scripted **handoff-read probe** in
the bench runner — record whether the ON T4 arm opens the pushed card path
(now named verbatim in its opening context) within its first N tool calls,
written into s-row-facts like the M1 counts. Today "handoff used" is
judge-inferred from transcripts (run-4 item 5 / run-5 item E); with the push
shipped, the exact pushed path is known at prepare time, so run-6 can measure
uptake as a boolean instead of a judgment — and a FAIL/PASS on the fix
becomes indisputable either way.

## ⟲ Previous-session review

The B1 run-5 session (PR #162/#163) was exemplary evidence work: second
clean scripted prepare, an honest 0-of-3 FAIL row recorded verbatim, and —
decisive for this session — its status `next:` queue named this exact slice
with the evidence pointers attached, making orientation near-instant. One
improvement it surfaced and this session re-confirms: it recorded the K0
orientation budget at ceiling (6998/7000) and paid for its bullet by
condensing older ones — the headroom-advisory idea (from #128) is still
unshipped and should graduate to a queued kit fix before the ceiling forces
a lossy condense.
