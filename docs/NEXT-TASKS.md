# substrate-kit — Next tasks (fresh-start, 2026-07-17)

> **Status:** `living-ledger`
>
> The clean next-task set after the 2026-07-17 fresh-start cleanup, ordered
> by leverage. Written so a freshly-recreated Project seat boots straight
> onto real work. Live truth wins: `control/status.md` +
> [`adopters.md`](adopters.md) are the heartbeat; this file is the plan.
> Context: the EAP goes read-only **2026-07-21**, the auto-mode classifier
> froze agent self-merge/arm/ready-flip ~**2026-07-15**, and the owner is
> **recreating the Projects** — so these tasks assume an owner-live or
> post-relaunch seat, not the retired autonomous-routine apparatus.

## 1 — Distribute v1.18.0 to the ~15 adopter repos (TOP PRIORITY)

**The headline undelivered artifact.** v1.18.0 is released + verified (tag
`v1.18.0`, sha256 three-way PASS) and the registry [`adopters.md`](adopters.md)
already reads v1.18.0 — but **no adopter tree has actually been upgraded**.
Every adopter is still on v1.17.0-or-older (9 repos at v1.17.0:
`superbot-next`, `websites`, `superbot-games`, `trading-strategy`,
`gba-homebrew`, `venture-lab`, `fleet-manager`, `idea-engine`,
`superbot-mineverse`; `pokemon-mod-lab` at v1.15.0; `superbot` pin-only at
v1.0.0). The registry-vs-tree gap is exactly what made the old
"distribution COMPLETE" reading false.

**Mechanism — one upgrade PR per adopter, run IN that adopter's own session**
(kit-lab has zero write access to adopters, KF-2 — the upgrade must run in a
session scoped to each adopter repo):

1. In the adopter repo, run the kit's upgrade verb:
   `python3 dist/bootstrap.py upgrade` (or `bootstrap.py.new upgrade`) — it
   archive-firsts to `.substrate/backup/`, re-vendors the new
   `dist/bootstrap.py`, and writes `.substrate/upgrade-report.md`.
2. Bump that repo's `substrate.config.json` pin `kit_version`
   1.17.0 → 1.18.0 (or its current pin → 1.18.0).
3. Open ONE **ready** PR per adopter and land it on green — via a merge call
   (MCP/REST), by arming native auto-merge, or by letting the server-side
   merge-on-green workflow land it (see the merge doctrine note in
   `CONSTITUTION.md` / current-state § Review rhythm).

This is an **upgrade** (re-vendor + pin bump), NOT a `bootstrap render`
(that only fills interview slots) and NOT a single kit-side version-bump PR.
Distribution is complete only when every adopter **tree** — not just the
registry — is at v1.18.0.

## 2 — Propagate the merge-doctrine template fix

The fleet-wide merge doctrine lives in
`src/engine/templates/CONSTITUTION.md.tmpl`. The correct doctrine (automode
OFF): **agents open PRs READY and merge their own green PRs directly** — via a
merge call (MCP/REST), by arming native auto-merge, or by letting the
server-side merge-on-green workflow land them; a mergeable green PR is never
routed to the owner, and a one-off merge refusal is venue-specific, not a
standing wall. That template is vendored into `dist/bootstrap.py`, so **every
adopter picks up the doctrine automatically on its v1.18.0 upgrade (task #1)** —
verify the clause is present and accurate in each adopter's regenerated
`CONSTITUTION.md` after upgrade. The paired scaffolding
(`auto-merge-enabler.yml` / `auto-merge-disarm.yml`) is intentionally NOT
deleted here — arming on green is one sanctioned landing path; retire it only if
a recreated project drops auto-merge entirely (owner call).

> **Flag (2026-07-18):** the template on `main` still carries the earlier
> FALSE "agents do NOT ready-flip / arm / REST-merge — classifier-denied"
> wording (lines ~78–83). It is out of scope for this docs-only PR; the
> `.tmpl` correction ships in its own PR.

## 3 — Fix the kit's own self-pin drift — ✅ DONE (PR #438, 2026-07-17)

Resolved by merged PR #438: `substrate.config.json` `kit_version` now tracks
the release (bumped `1.0.0` → `1.18.0`), and `scripts/cut_release.py` writes it
as a third synced version-home so it advances at every cut. `currency` no longer
emits a self-`⚠️ DRIFT` row — [`adopters.md`](adopters.md) reads substrate-kit as
`current`. Downstream reconciliation (registry regen) landed in PR #440.

## 4 — Reconcile or retire `current-state.md`

The 2026-07-17 fresh-start block at the top of
[`current-state.md`](current-state.md) now carries the true state, but the
dated sections below it (EAP-console gate stack P4/P5/P10/P11/P13, the
2026-07-12 snapshot) are historical. Either finish reconciling them to
reality or formally retire `current-state.md` in favour of
`control/status.md` + [`adopters.md`](adopters.md) as the live ledgers, so a
recreated seat boots on true state.

## 5 — Curate the overnight veto menu into the backlog

[`planning/2026-07-16-overnight-veto-menu.md`](planning/2026-07-16-overnight-veto-menu.md)
is a 23-proposal owner veto menu drafted to become the next clean task set.
Get owner vetoes, then promote the buildable-S survivors (dogfood
branch-sweep of spent `claude/*` refs, adopters-staleness self-signal
advisory, landing-protocol doctrine consolidation, planning-doc index,
prune the four ~530B 2026-07-06/07 rebuild briefs).

## 6 — Advance the grounded-skills measurement program

[`planning/2026-07-12-grounded-skills-program.md`](planning/2026-07-12-grounded-skills-program.md)
— harness merged (#386), protocol pre-registered, measurement window
~2026-07-19..26. The kit's next genuine capability bet, independent of the
retired autonomy apparatus.
