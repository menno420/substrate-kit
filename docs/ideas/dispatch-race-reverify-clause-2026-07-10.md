---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Dispatch race: every maintenance/dispatch brief needs an explicit re-verify-then-stand-down clause (2026-07-10)

> **Status:** `ideas`
>
> **State:** captured (origin: the lab's own coordinator lane — source:
> coordinator chat 2026-07-10; the event itself was previously documented
> nowhere in the repo; this file is the record. Frontmatter `origin: lab`
> because the checker's vocabulary is lab/owner/consumer — the coordinator
> lane is the lab).

## The finding

During the 2026-07-10 overnight window, the #106 green-but-behind stall (the
auto-merge stall class — recipe in `docs/CAPABILITIES.md`, "auto-merge STALL
CLASS" entry) produced a live dispatch race between parallel lanes:

- At ~06:10Z a scout flagged PR #106 as green-but-behind (armed auto-merge,
  stale head).
- The coordinator dispatched an unstall session at **06:11:23Z**.
- A sibling lane pushed the same branch-update at **06:11:17Z** — **6 seconds
  before the dispatch went out**.
- The dispatched unstall session re-verified at origin/main HEAD first, found
  the work already taken, and **stood down with zero writes**.
- #106 merged at 2026-07-10T06:12:33Z as `266807e8` (repo-verified merge
  commit; the intra-minute scout/dispatch/push timestamps above are
  **reported-by-coordinator** from the coordinator chat, not
  repo-verifiable — the stand-down session wrote nothing, so the race left no
  git trace).

## The lesson

With parallel lanes running, **any scout finding can be claimed within a
minute of being flagged** — the fix window and the dispatch latency are the
same order of magnitude. So every maintenance/dispatch brief must carry an
explicit clause: **"re-verify at origin/main HEAD first; stand down if
already taken."** It worked here: the clause is why the race cost zero
duplicate writes instead of a conflicting push or a twin PR (#50/#51 class).

The same clause proved itself again the same day, twice, in this very lane's
close-out session: sibling close-out PR #122 opened 39 seconds before this
lane's recon completed, and the re-verify step is what narrowed this lane's
scope instead of producing a colliding heartbeat.

## What IS already documented (this file adds only the race event)

- The #106 stall **class** and its cure (branch update + still-armed
  auto-merge) — `docs/CAPABILITIES.md`, the 2026-07-10 "auto-merge STALL
  CLASS, root cause" append-log entry, including the PARTIAL FIX
  (`synchronize` re-arm, PR #111).
- The **stand-down-on-re-verify pattern** for a whole-session scope —
  `.sessions/2026-07-10-coordinator-dispatch-inbox-check.md` (an unrelated
  inbox-check dispatch that stood down after its bus re-read; same instinct,
  different trigger).
- The race event itself — the 6-second scout-vs-sibling window and the
  zero-write stand-down — lived only in the coordinator chat until this file.

## Done-when

The re-verify-then-stand-down clause is standing doctrine in whatever template
generates dispatch/maintenance briefs (the coordinator's dispatch prompts
and/or `docs/operations/` runbooks), so no future brief can omit it; the
clause text names both halves: verify at origin/main HEAD, stand down with
zero writes if taken.
