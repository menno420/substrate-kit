# Archive-ready close-out — checklist doctrine

> **Status:** `binding`
>
> S1 of the archive-ready close-out plan
> ([`../planning/2026-07-15-archive-ready-close-out-plan.md`](../planning/2026-07-15-archive-ready-close-out-plan.md)),
> generalizing the hand-written evidence note
> [`../retro/archive-ready-2026-07-11.md`](../retro/archive-ready-2026-07-11.md).
> This doc is the checklist doctrine; the note template is
> `src/engine/templates/archive-ready.md.tmpl`; the drafting verb is
> `bootstrap.py archive-prep` (S2, `src/engine/loop/archive.py`).
> S3 (REQUIRES-PROBE resolve semantics) is shipped in the engine.
> S4 (the `check --strict` advisory) is shipped:
> `src/engine/checks/check_archive_ready.py` surfaces an incomplete note —
> unresolved slots or guarded-slot residue — on every `check` run,
> advisory-only (PL-008 unverified posture; graduation to a preflight/gate
> leg is a later, separate decision). Follow-up slice: S5 distribution
> (plan §5).

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

1. **Instantiate the note.** Run `python3 bootstrap.py archive-prep` in the
   archiving repo (S2, shipped): it drafts
   `docs/retro/archive-ready-<date>.md` from the template with evidence
   pre-fills (claims scan · heartbeat ⚑ extraction · CHANGELOG
   `[Unreleased]` park), reports unresolved slots on re-run, and never
   touches a completed note. Fallback when the verb is unavailable: copy
   `src/engine/templates/archive-ready.md.tmpl` by hand — the checklist is
   the template's section list.
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
  § "Routine state at archive"). S3 (shipped) enforces this at resolve
  time: `archive-prep` fingerprints the guarded slot bodies from the
  shipped template (whitespace-normalized word runs), and a zero-slot note
  where the templated instruction text survives marker-stripping is
  reported NOT complete — stripping the `[[fill:]]` markers around the
  default text is not a resolution, and a sham note is never silently
  superseded by a fresh draft. S4 (shipped) surfaces the same verdict —
  plus the plain unresolved-slot count — as a `check --strict` advisory on
  every run, so an incomplete note is visible without re-running the verb.
  **Generalized (2026-07-16, KL-5 residue generalization):** the fingerprint
  core now lives in `src/engine/lib/residue.py`, shared by every KL-5
  drafted surface — the same wholesale-replacement verdict covers **session
  cards** (`check_card_residue`, the `session-card-slot-residue` advisory,
  plus the same report at the Stop-hook/`session-close` seam): a card whose
  drafted `[[fill:]]` hints were marker-stripped but kept passes the
  token-counting session gate, and the advisory is what names it a sham.
  **Surface sweep completed (2026-07-16, baton 2b):** the archive note's
  S2 *evidence-judgment* hints (claims disposition · ⚑ verification ·
  payload park — the judgment slots the drafter itself injects into
  evidence replacements, invisible to the template-body extraction) are
  now guarded too, via canonical constants (`ARCHIVE_EVIDENCE_HINTS` in
  `src/engine/loop/archive.py`, the `CARD_GUARDED_HINTS` one-source
  pattern). The last surface named by the sweep — adopt-planted doc
  `[[fill:]]` slots — was investigated and is **empty**: no `ADOPT_PLAN`
  template carries `[[fill:]]` (grep-verified; the archive template is
  verb-instantiated into `docs/retro/`, already covered above), and
  planted docs carry `${slot}` interview placeholders, a different token
  owned by the engagement gate + `check_staged_regen` — building a
  `[[fill:]]` guard there would double-report that lane or watch nothing.
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
