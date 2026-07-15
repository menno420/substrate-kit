# Archive-ready close-out as a kit surface — structured plan (2026-07-15)

> **Status:** `plan`
>
> **Provenance:** baton item 1 (`control/status.md` § Next-2 at HEAD `0984d95`)
> promoting `docs/ideas/archive-ready-close-out-surface-2026-07-11.md` through
> its own route line ("Structured-plan lane (touches loop + templates +
> checker); not a quick win"). This PR ships the **PLAN ONLY** — every slice in
> §5 is a follow-up session with its own PR.
>
> Evidence base: the hand-written archive note the idea generalizes
> (`docs/retro/archive-ready-2026-07-11.md`) · the KL-5 evidence-draft seam it
> reuses (`src/engine/loop/handoff.py::ensure_draft`, wired at
> `src/engine/cli.py::cmd_session_close`) · the live failure that motivates the
> probe rule (the "disarmed" failsafe found still armed at archive-prep,
> retro note § "Routine state at archive").
>
> Grep route: §1 problem · §2 surface contract · §3 evidence sources ·
> §4 design decisions (decide-and-flag) · §5 slices · §6 verification ·
> §7 non-goals.

---

## 1. Problem — the wrap-up ritual is hand-derived under time pressure

When a long-running coordinator/session chat is archived, everything not in
the repo is lost, and the wrap-up work has a *fixed shape*: verify health from
scratch, enumerate + disposition open PRs/claims/branches, record live routine
state, park the unreleased payload, list open owner-actions, and write a
fresh-session resume path ending in an explicit "nothing remains chat-only"
confirmation. Chat archival is a routine program event (three archives in
three days at capture time; the EAP reboot added more), and each one re-derives
that checklist by hand — which is exactly where chat-only knowledge leaks:

- the lessons file one archive order pointed at **did not exist**;
- the routine-state record was **stale** — the archive order recorded the
  Q-0265 failsafe as already deleted, but the live probe found it still armed
  (`docs/retro/archive-ready-2026-07-11.md` § "Routine state at archive").

Today the shape lives in one owner order and one hand-written note
(`docs/retro/archive-ready-2026-07-11.md`). The kit already owns the matching
mechanism for cards: KL-5 evidence-drafting (`ensure_draft` — a missing card
gets a drafted skeleton with `[[fill:]]` slots; evidence fills what evidence
can; the session resolves the rest). This plan points that same pattern at the
archive seam.

## 2. Surface contract — what "archive-ready" means, checkable

A new engine verb `bootstrap.py archive-prep` (naming decided in §4.1) that:

1. **Drafts** `docs/retro/archive-ready-YYYY-MM-DD.md` from evidence when it
   does not exist — same fail-open posture as `ensure_draft`: evidence fills
   what evidence can; everything else becomes a named `[[fill:]]` slot.
2. **Reports** unresolved slots on re-run (the `cmd_draft` idiom: drafted
   surface reports its `[[fill:]]` slots; a completed note is never touched).
3. **Advises red** through `check --strict` while an archive-ready draft with
   unresolved slots exists (advisory first, PL-008 unverified-tool posture;
   graduation to a hard leg only after it proves itself — §5 S4).

The drafted note carries the fixed sections of the 2026-07-11 note, each
backed by a slot or an evidence-fill:

| Section | Fill source |
|---|---|
| True state (health numbers) | `[[fill:]]` — session pastes real check-run output (never synthesized) |
| Open PR / claims / branch disposition | `control/claims/` scan (evidence) + `[[fill:]]` for the live-API PR table (engine cannot reach GitHub — §3) |
| Routine state | **REQUIRES-PROBE slot** — never auto-filled (§4.2) |
| Unreleased payload park | `CHANGELOG.md [Unreleased]` scan (evidence) |
| ⚑ owner-actions open at archive | heartbeat ⚑ block extraction from `control/status.md` (evidence) |
| Fresh-session resume path | drafted skeleton from the boot-reading list + `[[fill:]]` |
| "Nothing remains chat-only" confirmation | `[[fill:]]` — an explicit human/agent attestation, never drafted as complete |

## 3. Evidence sources — what the engine can and cannot fill

Can fill (tree-local, stdlib-only — the kit's standing constraint):
`control/status.md` ⚑ blocks and heartbeat facts · `control/claims/` entries ·
`.sessions/` newest cards · `CHANGELOG.md [Unreleased]` · git facts available
without network. Cannot fill: live PR/check states and routine/trigger state —
the engine cannot reach GitHub (the same wall `cmd_session_close` handles by
advising the session instead of filing issues itself, `src/engine/cli.py`
~2570). Those become slots the *session* resolves with its own tools, which is
the correct division of labor: the engine guarantees the checklist is
complete; the session guarantees the facts are live.

## 4. Design decisions (decide-and-flag — reversible until a slice builds)

1. **Separate `archive-prep` verb, not `session-close --archive`.** Rationale:
   `session-close` runs every session and ends in the KPI footer; the archive
   ritual is rare, produces a different artifact (a `docs/retro/` note, not a
   card close-out), and a mode flag would fork that function's contract.
   Reversible — the verb is one `add_parser` + one dispatch line. ⚑ flagged.
2. **Routine state is a REQUIRES-PROBE slot, never auto-filled.** The one
   realized failure this surface exists to prevent is a *stale routine
   record trusted at archive time*. The draft writes the slot pre-populated
   with the probe instruction (list triggers live, paste ids + enabled state),
   and slot-resolution requires replacing it wholesale — a record-shaped
   default would defeat the purpose. ⚑ flagged.
3. **Advisory-red first, hard gate later.** The idea text says "holds
   `check --strict` advisory-red until every slot is resolved"; shipping it as
   an advisory matches the kit's PL-008 pattern (new checks are unverified
   until proven over sessions) and cannot brick an adopter's gate on a false
   positive. ⚑ flagged.

## 5. Slices — each a follow-up PR, in order

- **S1 — checklist doctrine + note template.** The archive-ready checklist as
  a template (`src/engine/templates/`, planted like the other doctrine
  surfaces) with the §2 section table and slot grammar; link it from the
  operations index. Docs-only; no engine code. *Smallest shippable.*
- **S2 — `archive-prep` draft verb.** The evidence-draft half: new loop module
  function (sibling of `ensure_draft` in `src/engine/loop/handoff.py` or a new
  `archive.py`), `add_parser` + dispatch in `src/engine/cli.py`, fail-open,
  tests for draft/re-run/never-touch-complete. Depends on S1's template.
- **S3 — REQUIRES-PROBE slot semantics.** Slot type that resolves only by
  wholesale replacement (no default survives), covering routine state and the
  chat-only confirmation; tests prove a templated default cannot pass.
- **S4 — `check --strict` advisory.** Unresolved-slot advisory when an
  archive-ready draft exists; PL-008 header (unverified → graduate/delete);
  one deliberate red fixture. Graduation to a preflight leg is a later,
  separate decision after it proves itself.
- **S5 — distribution.** Ride the next release wave; upgrade plants the
  template + verb for adopters; release-notes line in the adopter upgrade
  checklist. No adopter-repo writes from this lane (KF-2).

## 6. Verification

Per slice: `python3 scripts/preflight.py` (all legs) + `python3 bootstrap.py
check --strict` + the slice's own red fixture where one is named. Program-level
done: the *next real archive event* runs `archive-prep` instead of hand-writing
the note, and the resulting note reaches "no unresolved slots" before the chat
closes — measured by the note landing on main with zero `[[fill:]]` remnants
(the existing no-placeholder discipline already polices cards; S4 extends it
here).

## 7. Non-goals

- No live GitHub/trigger API calls from the engine (stdlib-only stands).
- No auto-archival or chat-side action — the surface prepares the repo, the
  owner archives the chat.
- No retroactive regeneration of past archive notes; the 2026-07-11 note stays
  as-written (it is the evidence base).
