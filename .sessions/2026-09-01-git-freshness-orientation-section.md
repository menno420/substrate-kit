# 2026-09-01 — a git-freshness section for SessionStart orientation

> **Status:** `complete` — pushed, PR open, not auto-merged (owner review
> requested before this lands — see "Why this PR is not on auto-merge" below).

- **📊 Model:** sonnet-5 · high · feature build
- **📍 Venue:** Claude Code, local (Menno's laptop, not this fleet's own
  scheduled/routine session flow — an outside ad-hoc session working at the
  owner's direct request)

💡 Session idea: a laptop-side research pass into `fleet-manager` today read a
resident local clone instead of fetching fresh, and produced findings that
were about 5 hours stale — it missed nine already-merged PRs entirely. The
owner separately described cloud sessions reporting a stale clone moments
after supposedly cloning it fresh, with no clear explanation for how that's
possible. Both point at the same gap: nothing checks clone-vs-remote drift at
session start, so staleness is discovered by accident (or not at all) rather
than surfaced up front.

## Previous-session review

No directly preceding session in this repo on this exact topic — this is new
ground, not a continuation. The section it adds sits in `compose_orientation`
alongside the existing handoff-push section (2026-07-11, the B1 run-4/run-5
continuity-null fix), which solved an adjacent problem: cold sessions not
knowing the previous session's trail. This solves the sibling problem: cold
sessions not knowing whether the trail they're about to read is even current.

## Mission

Add a new SessionStart orientation section that fetches the tracked remote
for the current branch and reports ahead/behind drift, so an agent knows
before reading anything else whether its working tree matches origin.

## Shipped

- `src/engine/hooks/session_start.py` — new `_ori_git_freshness(root)`
  section, inserted as section 3 (right after the handoff push, before the
  stance briefing); all later sections renumbered 4→11 in their docstrings
  and the `compose_orientation` builders tuple. Included in
  `_ORI_MINIMAL_SECTIONS` — staleness is not optional information at any
  orientation depth.
- Behavior: fetches only the current branch (`git fetch <remote> <branch>`,
  not the whole repo — matters for the estate's larger repos), then compares
  `HEAD...<remote>/<branch>` with `git rev-list --left-right --count`.
  Reports commits behind, commits ahead (unpushed), or both. Renders nothing
  when: not a git repo, no remote configured, fetch fails (offline/no
  auth/unreachable), HEAD is detached, no upstream counterpart, or already
  in sync. Every subprocess call is timeout-bounded (3s for local git-metadata
  reads, 8s for the one network call) so an unreachable remote degrades to a
  silently-dropped section, never a slow session start. Only fetches — never
  pulls, merges, or rebases; a stale-but-clean clone is reported, not
  silently rewritten out from under uncommitted work the agent hasn't seen.
- `tests/test_hook_session_start.py` — 6 new tests, each building a real
  bare-remote + clone via `subprocess` (no mocking of git itself): silent
  outside a repo, silent when in sync, reports N behind, reports N ahead,
  silent with no remote configured, and present even at `observe`/minimal
  depth.

## Why this PR is not on auto-merge

Unlike a same-repo consolidation PR the owner scoped directly, this changes
a section every adopter's SessionStart orientation will eventually run, and
substrate-kit's own convention is "consumers pull upgrades, the lab never
writes to consumer repos" — the wider blast radius (a version bump, a
CHANGELOG entry, then a per-adopter `/upgrade-distribution` pass) is a
separate decision from "does this source change look right," so it's left
for the owner's explicit word rather than assumed.

## Verification

- `python3 -m pytest tests/test_hook_session_start.py -q` → 31 passed, 1
  failed (pre-existing on an unmodified checkout — confirmed via `git stash`
  before touching anything; `test_handoff_pushes_newest_card_with_status_and_slots`
  fails identically on `main`, almost certainly a Windows path-separator
  artifact unrelated to this change — not investigated further, out of scope).
- `python3 -m pytest -q -k "session_start or orientation"` → 60 passed, 1
  pre-existing failure (same one), 2135 deselected.
- Section renumbering double-checked by grep: every docstring number and the
  `builders` tuple agree, no `section 4`/`section 5` duplicates remain.

## What this does NOT establish

Whether the estate's other adopter repos would benefit from this immediately
is not evaluated here — that's a per-repo `/upgrade-distribution` decision
after a release exists, not implied by merging this. `KIT_VERSION` is
untouched; no release was cut.

Capability delta: SessionStart orientation now includes an eleventh section.
Owner ask: none blocking — full design + rollout path reported directly to
the owner in the same conversation that requested this.
