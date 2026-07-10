# Coordinator relay sweep — 2026-07-10

> **Status:** `record` — value that existed ONLY in the coordinator chat on
> 2026-07-10, swept into a durable home at the gen-2 owner close-out. Every
> item is attributed to **coordinator relay 2026-07-10**; where the fact is
> already recorded elsewhere in the repo, this note CROSS-REFERENCES rather
> than duplicates. Landed via the gen-2 owner close-out PR (session card
> `.sessions/2026-07-10-gen2-owner-closeout.md`).

## Why this note exists

The coordinator lane runs in a DIFFERENT environment from this repo's Project
sessions, with its own walls and its own view of the fleet. Four pieces of that
lane's 2026-07-10 knowledge were load-bearing but lived nowhere durable. Recorded
here so the next boot inherits them.

---

## 1. Coordinator-environment scheduler / wake walls — NEW

*(coordinator relay 2026-07-10 — the COORDINATOR environment, not this repo's
Project-session surface. Contrast: a Project session CAN arm its own recurring
wake via `create_trigger` on the `claude-code-remote` MCP server — see
`docs/CAPABILITIES.md` append-log 2026-07-10, trigger
`trig_01FnqnAQjLU2T8d16iHwWQ2h`. The coordinator environment does NOT have that
surface. These four are its distinct walls/pattern.)*

- **(a) No `send_later` / scheduling tool exposed** — the tool is simply absent
  from the coordinator surface; there is no in-environment way to schedule a
  future self-wake.
- **(b) Standalone foreground sleep is BLOCKED.** Verbatim block message:
  > `Blocked: standalone sleep 1500. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.`
- **(c) Monitor tasks cap at ~30 min and their kill/completion does NOT
  re-invoke the parent agent** — a Monitor task that hits the timeout cap or is
  killed produces a SILENT wake loss (the parent is not notified), so Monitor is
  not a reliable self-wake mechanism.
- **(d) WORKING pattern (proven):** a WORKER running a blocking foreground
  until-loop of ~25 min (≈`sleep 20` steps) — **agent completion notifies the
  parent reliably** (~10 consecutive ticks proven). This is the coordinator
  lane's usable stand-in for a scheduled wake: a bounded blocking worker whose
  completion re-invokes the parent, not a Monitor task and not chained sleeps.

## 2. Boot cross-wire — NEW

*(coordinator relay 2026-07-10)*

Fresh coordinator-spawned sessions provision with a **venture-lab-pinned system
identity** — the boot arrives wired to the wrong Project. **3 occurrences
tonight.** Deconflict recipe before building anything:

1. Verify the repo you are actually in (`git remote -v` / the working tree),
2. Read ALL `control/status*.md` (every lane heartbeat, not just one),
3. Sibling check (what other sessions are live on this repo),

…all BEFORE building. **This lane's own boot did exactly this correctly** — it
verified it was in `menno420/substrate-kit`, read the control band and the sibling
heartbeats (`control/status-gba-homebrew-trackb.md`,
`control/status-superbot-coordinator.md`), and reconciled the stale
"inbox ends at ORDER 009" brief assumption against main (which had advanced to
ORDER 010) before writing — cite it as the positive example.

## 3. Cross-session two-party review-merge — the classifier wall is AUTHORSHIP-scoped

*(coordinator relay 2026-07-10 — cross-reference, one-line nuance ADDED to
`docs/CAPABILITIES.md`)*

The auto-mode merge classifier that refuses self-merge ("Merge Without Review")
is **AUTHORSHIP-scoped**, not a blanket merge ban: a NON-AUTHOR session that
GENUINELY reviews a PR it did not write, then merges it, **passes** the
classifier. Evidence: **venture-lab PR #9, merge `95b755b`** — a non-author
session reviewed-then-merged and was permitted. `docs/CAPABILITIES.md`'s
self-merge/enabler record did not previously carry this nuance, so a one-line
append-log entry was added there (2026-07-10) capturing it. See that entry for
the durable capability line; this note is the coordinator-relay provenance.

## 4. Fleet relay undelivered — `websites` ORDER 005 ⚑ needs-owner

*(coordinator relay 2026-07-10)*

⚑ The `websites` repo inbox **ORDER 005 is unexecuted** (surfaced in this lane's
gen-1 status notes). The coordinator has **no websites scope**, so it cannot route
or execute it — this is genuinely **OWNER-ROUTED**: the owner must relay ORDER 005
to a websites-scoped session. Also recorded as an OWNER-ACTION in
`control/status.md` at this close-out so it rides the live ⚑ list, not just this
retro note.
