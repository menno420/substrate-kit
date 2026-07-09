# Session 2026-07-09 — Control protocol adoption: land #27 + first status heartbeat

> **Status:** `in-progress`

**Scope (about to do):** land the manager's control-plant PR #27 (it sat
open behind main with no CI runs — the fleet bus was dark on main): merge
origin/main into `manager/control-plant` (trivial, no overlapping files),
push forward-only to the manager's branch (⚑ flagged below), wait for CI
green on the new head, squash-merge. Then run the `control/README.md`
per-session ritual for the first time: read `control/inbox.md` (ORDER 001
P1, ORDER 002 P2), execute by priority, and — as the deliberate LAST step —
overwrite `control/status.md` with the real picture. One-line protocol
notes in `docs/current-state.md` + `.session-journal.md`. No engine code,
no `bench/` pin paths, no release files (a parallel session is cutting
v1.1.0 in PR #29 — its files are avoided entirely).

## What shipped

- **PR #27 LANDED (squash → `11744d8` on main)**: the manager's control-plant
  PR sat open behind main (base 22fe538) with zero CI runs. This session
  merged `origin/main` into `manager/control-plant` (clean — the plant is
  new-files-only: `control/README.md` + `inbox.md` + `status.md`), pushed
  forward-only (no force), waited for all three checks green on the new head
  `4f4a07f` (kit-quality · Kit test suite · Cold-adoption smoke), then
  squash-merged via MCP. `control/` verified on main by fetch.
- **First ritual run per `control/README.md`** — inbox read FIRST, orders
  executed by priority, `control/status.md` overwritten LAST (this PR):
  - **ORDER 001 (P1) — acked**: B1 firing already DONE (#28 — run
    `2026-07-09-run01`, VERDICT PASS, row appended); the CHANGELOG
    heading-order fix already landed. The remaining leg — the v1.1.0 cut —
    is IN FLIGHT via the parallel release session (PR #29 open at
    status-writing time; tag list still v1.0.0-only), so 001 is acked, NOT
    done — it flips to done when the release is live.
  - **ORDER 002 (P2) — acked, queued**: the coordination-protocol kit band
    (superbot `docs/planning/fleet-coordination-protocol-2026-07-09.md` §2:
    control/ scaffold in ADOPT_PLAN · README tmpl · `check_status_current.py`
    · CI paths-ignore `control/**` · fresh release) is substantial —
    deliberately queued as its own next band session, not built here.
  - `inbox.md` untouched (manager-owned — one writer per file).
- **One-line protocol notes**: `docs/current-state.md` (In flight — protocol
  ADOPTED bullet) + `.session-journal.md` (⚡ Quick reference — the
  FIRST-inbox / LAST-status ritual line).

- **📊 Model:** fable-5 · high · docs-only

### ⚑ Self-initiated / decide-and-flag (PL-001)

1. **⚑ Pushed to a manager-owned branch** (`manager/control-plant`) — a
   forward-only `origin/main` merge + push so #27 could get CI runs and land;
   no manager-authored content changed (their three commits are intact in the
   branch history; the squash lands the same 74-line plant). Flagged because
   branch ownership crossed a writer boundary, even though file ownership
   did not.
2. **⚑ Landed #27 without the manager session** — decide-and-flag: the plant
   is new-files-only (zero existing files touched), owner-directed protocol,
   and the fleet bus stays dark on main until it lands. Veto = revert of
   `11744d8`.
3. **⚑ ORDER 001 reported acked-not-done** while its last leg rides a
   parallel session's PR #29 — the honest reading of `done-when` (release
   live), stated precisely in status.md rather than optimistically.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**Manager-PR staleness guard in the control protocol**: #27 shows the
failure mode — a manager-planted PR opens behind main with no CI runs and
no session owning its landing, so the bus sits dark until someone notices.
The ORDER 002 kit band should include (or the protocol spec §2 should gain)
a one-line rule: *a control-plant/inbox-append PR names its lander* — the
receiving Project's next session treats an open `manager/*` PR touching
`control/**` as an implicit P0 order (update branch → CI → merge), so the
plant can never strand. Cheap: one paragraph in the README tmpl +
`check_status_current.py` could warn when an open `manager/*` PR exists.
Not filed as a `docs/ideas/` file — it folds directly into the already-acked
ORDER 002 band, where it belongs.

### ⟲ Previous-session review — b1-record (PR #28)

Strong session: the honest-shapes call (per-task `m1_on`/`m1_off` objects
instead of a fake scalar) and committing the raw run dir whole made the
first bench row genuinely auditable, and the three follow-ups were filed as
ideas with evidence pointers instead of being silently fixed on pin paths.
What it missed: it left `docs/current-state.md`'s "In flight" naming PR #28
itself as in-flight in the very PR that shipped it — a self-staleness the
ledger convention ("a DONE item moves on the next touch") tolerates but a
one-word "(this PR)" marker would have avoided. **Workflow improvement:**
the session-close checker could flag a card/ledger that lists its *own* PR
number as in-flight — a zero-cost lint that catches self-staleness at the
source. (Noted for the ORDER 002 / check_status_current.py band, same home
as the session idea above.)
