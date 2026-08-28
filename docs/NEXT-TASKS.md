# substrate-kit — next tasks (superseded: the worklist lives in fleet-manager)

> **Status:** `reference` · superseded as a plan 2026-08-28 (kit #587, the
> OD-24 review round's session 2)
>
> **The kit's live worklist is fleet-manager's
> [`docs/findings/2026-08-13-substrate-kit-v1210-followups.md`](https://github.com/menno420/fleet-manager/blob/main/docs/findings/2026-08-13-substrate-kit-v1210-followups.md)**
> — 34 rows of dist/template defects found by Codex across the v1.21.0
> adoption wave, with the fix order restated at its tail (the false
> negatives lead). The round's running thread is fleet-manager's
> [`docs/repos/substrate-kit/README.md`](https://github.com/menno420/fleet-manager/blob/main/docs/repos/substrate-kit/README.md).
> Start any kit session from those two; this file exists so the kit's own
> tree routes there (it routed nowhere until 2026-08-28 — fm genesis dig,
> gap #5).
>
> Releases are cut only via `release.yml` `workflow_dispatch`, and the
> adopter rollout is **owner-paced** — fixes land on `main`; a cut is its
> own owner-said-go session.

## What the 2026-07-17 plan this file used to carry became

The previous body (preserved in git history at
[`8ae4199`](https://github.com/menno420/substrate-kit/blob/8ae419971eddec1b401a54c18daa19aecce38a1d/docs/NEXT-TASKS.md))
was written for a Project-seat relaunch that never happened and had gone
actively false — its top priority was distributing **v1.18.0**, while
v1.21.0 has been cut, published and distributed since 2026-08-13. Its six
tasks, terminally:

| task | state |
|---|---|
| 1 — distribute v1.18.0 | spent — superseded by the v1.21.0 wave (fm #853–#858, 2026-08-13/14) |
| 2 — merge-doctrine template fix | shipped — `src/engine/templates/CONSTITUTION.md.tmpl:113-116` carries the corrected doctrine and repudiates the old wall (verified against the tree, 2026-08-28) |
| 3 — self-pin drift | done per the old body's own record (kit #438) |
| 4 — reconcile or retire `current-state.md` | **still open** — `docs/current-state.md:31` still says v1.20.2 (verified 2026-08-28); belongs to the review round |
| 5 — overnight veto menu | stale, owner-gated then and now; the menu is `planning/2026-07-16-overnight-veto-menu.md` |
| 6 — grounded-skills measurement | ran 2026-07-19 — the fleet-grounding self-measurement returned a negative (12%→10%, fm genesis dig §4); the program did not continue |
