# 2026-07-11 — pull-visible handoff pointer (run-6 delivery-gap fix)

> **Status:** `complete`

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

## Close-out (PR #203)

Shipped the declared scope exactly. New `src/engine/loop/handoff_pointer.py`:
one shared handoff-lines composer feeding BOTH delivery surfaces (the #165
orientation push section 2 — refactored in `session_start.py` to delegate —
and the new marker-guarded repo-root `HANDOFF.md` writer), so pushed and
pulled text can never drift. Wiring: `_hook_sessionstart` + `session-start`
CLI regenerate the pointer at boot; `ensure_draft` (Stop hook /
`session-close` / `draft`) refreshes it silently after drafting (advisory
contract unchanged — pinned by test). Untracked-not-gitignored decided (a
gitignored file is invisible in `git status`, the one surface with observed
worker acknowledgment in run-6); host-owned `HANDOFF.md` never
written/overwritten/deleted (marker guard, 2 tests); stale kit pointer
removed when no card exists; fail-open everywhere. Lean rider:
`CLAUDE.md.tmpl` read-first list names `HANDOFF.md` at slot 2 (claudeMd
injection = the one channel run-6 proved reaches and directs workers;
ON-T4 obeyed its verify instructions verbatim). Leanness pinned by test:
pointer file ≤ 113 words (the push's orchestrator-side size). Honest
negative carried in the record: both T5 workers touched zero orientation
surfaces — no working-tree artifact reaches a worker that reads nothing.
Verify: `python3.10 -m pytest tests/ -q` → **1008 passed** (995 → 1008);
`python3.10 src/build_bootstrap.py` → 673937 B, `git diff dist/` empty
(byte-pin clean; `loop/handoff_pointer.py` added to the module order);
`ruff check src/engine/` clean; `check --strict` red only by this card's
pre-flip hold; `check_program_law` OK; `check_idea_index` OK. CHANGELOG
[Unreleased] Added ×2 with the run-7 re-validate-AFTER-distribution note.
Claim `control/claims/handoff-pointer-file.md` (#202 @ 43a1ef6) deleted;
status heartbeat overwritten as the deliberate last content step (1b3a214).

## 💡 Session idea

**Handoff-pointer delivery probe as a scripted bench fact.** Run-7 should
not re-litigate "did the signal arrive" from transcript vibes: add one
scripted collect-time fact per measured session — did the worker's stream
touch `HANDOFF.md` (open/cat/cite) and did its first `git status`/`ls`
output contain it — mirroring run-6's signal-visibility grep that made the
delivery gap undeniable. Cheap (one grep pair in the collect script),
and it converts the new mechanism's acknowledge/ignore/decline split into
scripted ground truth the judge takes as given. Dedup-checked: the #165
card's handoff-read probe idea covers the CARD path, not the pointer file;
no existing idea covers pointer-delivery scripting.

## ⟲ Previous-session review

The B1 run-6 session (#200/#201) is the reason this slice exists at all —
its scripted signal-visibility probe (grep the push text in worker-native
streams, 0/3) turned two runs of "continuity NULL, unclear why" into a
named, buildable mechanism (orchestrator→worker seam), and its 💡 idea
sketched this very fix, evidence attached. That is the bench doing its job:
honest-negative headline plus a mechanism the next session can build
against. One improvement it surfaces: the run-6 card's idea proposed the
Stop hook as the pointer's (re)write seam but not SessionStart — yet boot
is the only seam guaranteed to have fired before a delegated worker looks
at the tree (the Stop hook fires after the work). Bench ideas that name a
mechanism should also name WHEN in the session lifecycle it must fire;
this slice added the boot seam on its own judgment (decide-and-flag).

## Docs audit

Fix + rationale → this card + PR #203 body + CHANGELOG [Unreleased];
slice record + next-slice queue → control/status.md (1b3a214); run-7
measurement note → CHANGELOG + the slice record; the shared-composer
contract → module docstrings (`handoff_pointer.py`, `session_start.py`);
session idea recorded above. Nothing captured only in chat.
