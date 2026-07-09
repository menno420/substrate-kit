# Fleet coordination protocol — `control/`

> Local copy for this repo. Canonical spec: `menno420/superbot` →
> `docs/planning/fleet-coordination-protocol-2026-07-09.md` (§1). Projects cannot talk to each
> other directly — committed git files are the only shared medium; this directory is the bus.

## The two files
- `control/inbox.md` — ORDERS to this Project. **One writer: the manager** (appends via the
  GitHub Contents API). Never edit this file.
- `control/status.md` — STATE from this Project. **One writer: this Project** (overwrite it each
  session).

## The one rule that keeps it conflict-free
**One writer per file.** The manager is the sole writer of `inbox.md`; this Project is the sole
writer of its own `status.md`. Two writers never touch the same file, so there are no merge
conflicts. Everything is append-only / overwrite-own — forward-only git.

## Multi-Project repos — per-lane heartbeats (optional extension)
A SHARED repo can host several Projects ("lanes") — the live example is superbot-games with a
mining lane and an exploration lane. The one-writer rule scales by **splitting the heartbeat,
never by sharing it**:
- **One status file per lane** — `control/status-<lane>.md` (e.g. `control/status-mining.md` +
  `control/status-exploration.md`); each lane is the sole writer of its own file and overwrites
  it as its session's deliberate LAST step.
- **`control/inbox.md` stays single** — the manager remains its one writer; a lane-specific
  order names its lane in `do:`.
- **Declare every lane heartbeat to the kit** — `substrate.config.json` →
  `"heartbeat_files": ["control/status-mining.md", "control/status-exploration.md"]` (default
  when unset: `["control/status.md"]`); the status checker gates each listed file independently,
  and the Stop hook's overwrite reminder clears when any lane's heartbeat is fresh. An empty
  list falls back to the default — misconfiguration never silently disables the gate.
(This repo is single-lane; the extension is documented here because this file is the local copy
of the planted contract. Shipped v1.4.0, inbox ORDER 004.)

## Per-session ritual (every session, and every routine wake)
- **FIRST:** git pull (a stale clone reads stale orders); read `control/inbox.md`; execute any
  order whose status is `new`, in priority order (P0 before P1). An order's `do:` is a pointer to
  a committed doc — read it. If an order is ambiguous or you disagree, do NOT guess: write it in
  your status under `⚑ needs-owner` and proceed with the rest.
- **LAST (deliberate final step):** overwrite `control/status.md` — updated timestamp, current
  phase, health (green / red-by-design+why / broken+what), last-shipped PR, blockers, orders
  acked/done, `⚑ needs-owner`. You report order progress ONLY here; never edit `inbox.md`
  (the manager owns it — one writer per file).

## `status.md` format (what you write every session — your heartbeat)
```markdown
# <project> · status
updated: <ISO8601>            # heartbeat — stale = the manager treats the Project as dark
phase: <what I'm doing right now, one line>
health: green | red-by-design (<why>) | broken (<what>)
kit: v<X.Y.Z> · check: green|red · engaged: yes|no   # kit self-report (adopter-visibility band, ORDER 003)
last-shipped: #<PR> — <one line>
blockers: <what's stopping me, or `none`>
orders: acked=<ids> done=<ids>
⚑ needs-owner: <a decision/action only the owner can give, or `none`>
notes: <anything the manager should know>
```

## `inbox.md` order format (manager-written, append-only)
```markdown
## ORDER <nnn> · <ISO8601> · status: new     # manager flips new→done after seeing status done=
priority: P0 | P1 | P2
do: <pointer to a committed doc/section + the ask, kept short>
why: <one line>
done-when: <acceptance test>
```
