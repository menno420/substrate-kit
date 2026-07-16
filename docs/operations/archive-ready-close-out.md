# Archive-ready close-out — checklist doctrine

> **Status:** `binding`
>
> S1 of the archive-ready close-out plan
> ([`../planning/2026-07-15-archive-ready-close-out-plan.md`](../planning/2026-07-15-archive-ready-close-out-plan.md)),
> generalizing the hand-written evidence note
> [`../retro/archive-ready-2026-07-11.md`](../retro/archive-ready-2026-07-11.md).
> This doc is the checklist doctrine; the note template is
> `src/engine/templates/archive-ready.md.tmpl`. Follow-up slices: S2 ships
> the `archive-prep` draft verb, S3 the REQUIRES-PROBE slot semantics, S4
> the `check --strict` advisory, S5 distribution (plan §5).

## When this runs

When a long-running coordinator/session chat is about to be **archived** —
the owner announces an archive, a program phase ends, or a coordinator seat
winds down. Chat archival is a routine program event (three archives in
three days at plan capture time), and everything not in the repo is lost
when the chat closes. The wrap-up work has a *fixed shape*; hand-deriving it
under time pressure is exactly where chat-only knowledge leaks (a lessons
file one archive order pointed at did not exist; a "disarmed" failsafe was
found still armed by the live probe — plan §1).

## The ritual

1. **Instantiate the note.** Copy the template
   (`src/engine/templates/archive-ready.md.tmpl`) to
   `docs/retro/archive-ready-<date>.md` in the archiving repo. (S2's
   `archive-prep` verb automates this with evidence pre-fills; until it
   ships, copy by hand — the checklist is the template's section list.)
2. **Resolve every `[[fill:]]` slot with live facts**, section by section:
   - **True state** — re-verify health *from scratch this session* (run the
     repo's verify command + kit check) and paste the real output numbers.
     Never copy a prior heartbeat's numbers.
   - **Open PR / claims / branch disposition** — enumerate from the live
     API and the claims directory at HEAD; every open item gets a
     disposition (merge on green / parked with label + reason / closed).
   - **Routine state** — **REQUIRES-PROBE** (rule below).
   - **Unreleased payload park** — what survives where (CHANGELOG
     `[Unreleased]` contents when the repo keeps one, unshipped slices,
     pinned PRs) and what the next session cuts from it.
   - **⚑ owner-actions** — extract the open set from the heartbeat
     (`control/status.md`); full paste-ready blocks stay there.
   - **Fresh-session resume path** — concrete next actions in priority
     order, each with its pointer.
   - **Chat-only confirmation** — written LAST (rule below).
3. **Land the note on main before the chat closes** — the program-level
   done is the note reaching main with zero `[[fill:]]` remnants (plan §6).

## Slot rules (the doctrine half)

- **`[[fill: hint]]` marks what only the archiving session can know.**
  Resolve with live facts; a slot resolved from memory is worse than an
  unresolved slot, because it *looks* done.
- **REQUIRES-PROBE slots resolve only by wholesale replacement** with
  freshly probed output (routine/trigger state is the canonical case).
  Never a record-shaped default, never a prior session's record: the one
  realized failure this surface exists to prevent is a stale routine record
  trusted at archive time — the 2026-07-11 archive order recorded a
  failsafe as already deleted; the live probe found it still armed
  ([`../retro/archive-ready-2026-07-11.md`](../retro/archive-ready-2026-07-11.md)
  § "Routine state at archive"). S3 formalizes these semantics in the
  engine; the rule binds now.
- **The confirmation slot is never drafted as complete.** "Nothing remains
  chat-only" is an explicit attestation written after everything above is
  resolved — writing it IS the final check.

## Division of labor (why slots exist at all)

The engine (S2+) fills what the tree can prove — heartbeat ⚑ blocks, claims
entries, newest session cards, CHANGELOG `[Unreleased]`, network-free git
facts. It cannot reach GitHub or the trigger API (the kit's stdlib-only
standing constraint), so live PR/check state and routine state are *always*
session-resolved slots. The engine guarantees the checklist is complete; the
session guarantees the facts are live (plan §3).
