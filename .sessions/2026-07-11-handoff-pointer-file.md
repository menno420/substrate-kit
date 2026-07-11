# 2026-07-11 — pull-visible handoff pointer (run-6 delivery-gap fix)

> **Status:** `in-progress`

- **📊 Model:** fable-5 · high · feature build

## Scope (what is about to happen)

One bounded slice, claim `control/claims/handoff-pointer-file.md`
(#202 @ 43a1ef6, on main before build). Fix the bench run-6 headline
(PR #201, report §5): the #165 SessionStart handoff-push fires at boot but
lands only in the ORCHESTRATOR's context — it reached the measured delegated
WORKER in 0/3 (precondition-NULL; the orchestrator→worker seam does not
forward SessionStart context and SessionStart does not re-fire for
subagents). The signal never reaches the session that acts.

**Design (decide-and-flag): shape #1 primary + a lean #2 rider, both chosen
from transcript evidence.** (1) A kit-regenerated, working-tree-visible
`HANDOFF.md` at repo root — same lean content as the push's handoff section
(newest card path + status + unresolved slots + resolved "next session
should know" pointer), written by the SessionStart hook / `session-start`
and refreshed by the Stop-hook/`session-close`/`draft` seam (`ensure_draft`),
UNTRACKED BY DESIGN (not gitignored — a gitignored file is invisible in
`git status`, and run-6's one acknowledgment-adjacent event was the ON-T2
worker noticing untracked paths in its own `git status`; `git status`/`ls`/
`find` ran early in 4 of 6 measured workers, and the two T5 workers touched
no orientation surface at all). Never clobbers a host-owned HANDOFF.md
(marker-guarded), removed when no session card exists. (2) One orientation
line in the planted `CLAUDE.md.tmpl` pointing at `HANDOFF.md` — the
harness's claudeMd injection is the ONE channel run-6 proves reaches AND
directs delegated workers (ON-T4 verbatim: "Ran `python3 -m pytest tests/
-q` per `.claude/CLAUDE.md`'s verification instructions").

Files: new `src/engine/loop/handoff_pointer.py` (shared composer + writer),
`src/engine/hooks/session_start.py` (section 2 delegates to the shared
composer), `src/engine/loop/handoff.py` (`ensure_draft` refreshes the
pointer), `src/engine/cli.py` (sessionstart seams),
`src/engine/templates/CLAUDE.md.tmpl`, tests (new
`tests/test_handoff_pointer.py` + wiring assertions), `CHANGELOG.md`
[Unreleased], dist regen. Close-out: status.md overwrite (preserving ALL
standing content — orders through 013, ⚑ OWNER-ACTION 2–13, Self-review,
ROUTINE STATE/Q-0265, release/wave/P4/run-6 records) + claim delete before
this card's flip. NEVER: control/inbox.md, PR #181, sibling session cards,
bench pin paths, bench/results rows.
