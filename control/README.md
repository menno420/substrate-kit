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

**Enforced vs. convention.** The append-only + ORDER-grammar half of the `inbox.md` rule is now
CI-enforced — `check_inbox_append` (shipped in #87) rejects any control-lane PR whose `inbox.md`
diff is not a pure append of well-formed ORDER blocks. Writer IDENTITY cannot be enforced in-repo
on a single-account program (every commit authenticates as the same account), so *who* appends
to `inbox.md` remains convention, not a machine-checked guarantee.

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
- **One command, not hand-edits** — a Project joining a SHARED repo runs
  `bootstrap adopt --lane <name>`: it plants `control/status-<name>.md` (skip-if-exists),
  declares it in `heartbeat_files`, and leaves `inbox.md`/`README.md` single — a second lane
  never re-plants the first Project's files (the double-adoption fix; shipped by queue item 11).
(This repo is single-lane; the extension is documented here because this file is the local copy
of the planted contract. Shipped v1.4.0, inbox ORDER 004.)

## Per-session ritual (every session, and every routine wake)
- **FIRST:** git pull (a stale clone reads stale orders); read `control/inbox.md`; execute any
  order whose status is `new`, in priority order (P0 before P1) — **claim it first** (see
  "Claiming an order" below). An order's `do:` is a pointer to
  a committed doc — read it. If an order is ambiguous or you disagree, do NOT guess: write it in
  your status under `⚑ needs-owner` and proceed with the rest.
- **LAST (deliberate final step):** overwrite `control/status.md` — updated timestamp, current
  phase, health (green / red-by-design+why / broken+what), last-shipped PR, blockers, orders
  acked/done, `⚑ needs-owner`. You report order progress ONLY here; never edit `inbox.md`
  (the manager owns it — one writer per file).

## Claiming an order — one executor per order (claim FIRST, build second)

An order's `status: new` is visible to every session that wakes, so two readers can both
believe they are its executor — a realized failure, not a theoretical one (substrate-kit
PRs #50/#51: two lanes independently executed the same ORDER 005 the same day, and a whole
session's work had to be reconciled as twins). The manager only flips `new→done` after
seeing the status report; the claim covers the gap in between.

Before executing any `new` order:

1. **Re-read the bus at origin/main HEAD** — `control/inbox.md` AND every sibling status
   file (`control/status*.md`). If another lane's status already claims the order
   (`claimed-by:` naming its id) or reports it in `done=`, stand down and pick other work.
2. **Claim FIRST, on your own status file's orders line** — append
   `claimed-by: <order-ids> <lane-or-session> <ISO8601>` — and land it on **main** BEFORE
   any build work (a control-only fast-lane PR, or a direct commit where your rules allow
   one). A claim that exists only on a branch is invisible; only main counts.
3. **Re-read once more after the claim merges** — two claims can race in flight; the
   tiebreak is the earliest claim merged to main. The loser withdraws its claim line in
   its next status overwrite and stands down.
4. **Claims expire** — a claim with no visible build activity (no open PR, no fresh
   heartbeat referencing the order) after ~24h may be treated as abandoned and re-claimed;
   note the takeover in your status `notes:`. A dead lane must never deadlock an order.

With an active claim the `orders:` line reads e.g.:
`orders: acked=001-008 done=001-006 claimed-by: 007+008 coordinator-lane 2026-07-09T18:38Z`
— the executor drops the `claimed-by:` annotation in the overwrite that moves those ids
into `done=`. One writer per file is preserved: you only ever claim on your OWN status.
(Shipped by inbox ORDER 007 — the root-cause fix for the twin-execution failure; the
ritual was live-proven manually on this repo's own orders before graduating here.)

## Claiming work (not an ORDER) — one file per claim under `control/claims/`

Order claims cover the inbox; **work claims** cover everything else two
parallel sessions could both pick up — a coordinator-assigned slice, a
self-initiated build, a shared-surface change. Before starting such work,
create **one file per claim** — `control/claims/<branch-or-scope>.md`, a
single bullet `` - `branch-or-scope` · **scope** — detail · YYYY-MM-DD `` —
land it on main FAST (claims are `control/**` traffic and ride the CI fast
lane), re-read the directory at HEAD, build, then **delete the file at
session close**. Per-file is the measured winner over any shared list (~98%
merge-conflict rate for shared-append vs 0% per-file — superbot
`tools/sim/claim_layout_sim.py`); first claim merged to main wins a
collision; ~72h with no activity = abandoned, prune on sight. Full
convention + checker contract: `control/claims/README.md`. (`check` nags —
advisory-only — on unparseable, stale, duplicate, or legacy-located claims;
legacy homes `docs/owner/claims/` and root `claims/` are auto-detected
during the migration window, and a deliberate different home is pinned via
`substrate.config.json` → `claims_dir`. Shipped by EAP program review §6.4,
2026-07-10 — supersedes this repo's earlier practice of carrying slice
claims as non-numeric ids on the heartbeat orders line.)

## `status.md` format (what you write every session — your heartbeat)
```markdown
# <project> · status
updated: <ISO8601>            # heartbeat — stale = the manager treats the Project as dark
phase: <what I'm doing right now, one line>
health: green | red-by-design (<why>) | broken (<what>)
kit: v<X.Y.Z> · check: green|red · engaged: yes|no   # kit self-report (adopter-visibility band, ORDER 003)
last-shipped: #<PR> — <one line>
blockers: <what's stopping me, or `none`>
orders: acked=<ids> done=<ids> [claimed-by: <ids> <lane-or-session> <ISO8601>]
⚑ needs-owner: <a decision/action only the owner can give, or `none`>
notes: <anything the manager should know>
```

## ⚑ needs-owner — the OWNER-ACTION item format (quality contract)

The owner is the scarcest resource in the program: every ask routed to the owner costs
attention, and an unclear or unnecessary ask stalls your own lane on top of burning his.
**Before routing ANYTHING to the owner, try it yourself or cite the exact wall** — an
assumption-based ask ("agents probably can't do X") is banned; the bar is the capability
ledger (`docs/CAPABILITIES.md`) plus one real attempt with the captured error.

Every ⚑ needs-owner item carries ALL of these REQUIRED fields — inline on the item, or as a
structured block the item links to:

```markdown
⚑ OWNER-ACTION
WHAT: <one plain sentence, zero jargon — the thing the owner does>
WHERE: <exact click path or URL>
HOW: <paste-ready text/values where applicable, or "click only">
WHY-IT-MATTERS: <one sentence, in product terms>
UNBLOCKS: <what starts moving the moment it's done>
VERIFIED-NEEDED: <the attempt you made + the exact error/wall proving only the owner can do
this — never an assumption>
```

Hygiene: **expire or withdraw stale asks every session** (an answered or obsolete ask left in
the list is drift), and **fewer, clearer asks beat complete lists**. `check` warns — advisory,
never exit-affecting — when a non-`none` ⚑ needs-owner list lacks these fields.
(Shipped by inbox ORDER 008, owner directive 2026-07-09.)

## `inbox.md` order format (manager-written, append-only)
```markdown
## ORDER <nnn> · <ISO8601> · status: new     # manager flips new→done after seeing status done=
priority: P0 | P1 | P2
do: <pointer to a committed doc/section + the ask, kept short>
why: <one line>
done-when: <acceptance test>
```
