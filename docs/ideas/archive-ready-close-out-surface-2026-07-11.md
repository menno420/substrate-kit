---
state: routed
origin: lab
shipped_pr: null
shipped_repo: null
outcome: open
merged_date: null
---

# Archive-ready close-out as a kit surface (2026-07-11)

> **Status:** `ideas`
>
> **State:** routed — structured plan shipped 2026-07-15:
> `docs/planning/2026-07-15-archive-ready-close-out-plan.md` (slices S1–S5,
> each a follow-up PR; outcome stays `open` until a build slice merges).
> Captured as the archive-prep close-out session's 💡 (the session
> that wrote `docs/retro/archive-ready-2026-07-11.md` by hand when the
> coordinator chat was archived).

## The idea

When a long-running coordinator/session chat is archived, everything not in
the repo is lost — and the wrap-up work is a *ritual with a fixed shape*:
verify health from scratch, enumerate + disposition open PRs/claims/
branches, record live routine state (verified by probe, not by record —
this session found a "disarmed" failsafe still armed), park the unreleased
payload, list open owner-actions, and write a fresh-session resume path
with an explicit "nothing remains chat-only" confirmation. Today that shape
lives in one owner order and one hand-written note. Make it a kit surface:
a `bootstrap.py archive-prep` (or a `session-close --archive` mode) that
walks the checklist, auto-drafts the archive-ready note from evidence
(health numbers from the real check runs, open-PR table from the API or
committed records, ⚑ list from the heartbeat), and holds `check --strict`
advisory-red until every slot is resolved — the same evidence-draft pattern
as the KL-5 card auto-draft, aimed at the archive seam.

## Why it is worth having

Chat archival is now a routine program event (gen-1 wind-down, gen-2 close,
this gen-3 archive — three in three days), and each one re-derives the same
checklist by hand under time pressure; the checklist is exactly where
chat-only knowledge leaks (the lessons file this session was ordered to
copy did not exist; the routine-state record was stale). Dedup-checked
against `docs/ideas/` (no archive-/wind-down-surface idea exists; the
succession packs are per-generation documents, not a reusable surface).

## Route

Structured-plan lane (touches loop + templates + checker); not a quick win.
