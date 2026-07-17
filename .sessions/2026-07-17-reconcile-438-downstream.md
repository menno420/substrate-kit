# Session card — reconcile #438 downstream drift

> **Status:** `in-progress`
> **📊 Model:** opus-4.8 · high · mechanical refactor

## Scope
Routine failsafe-wake ladder run (rungs 2/3/5) reconciling the three drift items left
downstream of merged PR #438 (kit self-pin version-truth).

## What I'm about to do
Reconcile the three drift items left by #438: (a) regenerate `docs/adopters.md` so the
resolved substrate-kit self-DRIFT row clears, (b) conform the prior session card's
malformed `📊 Model:` line to the PL-004 taxonomy, (c) mark the completed NEXT-TASKS §3
self-pin drift task done.

## Shipped (PR #440)
All three items are downstream reconciliation of merged PR #438 (commit 828de60):
- `docs/adopters.md` — self-DRIFT row cleared via a clean 12-repo `dist/bootstrap.py currency`
  regen: substrate-kit's own pin `v1.0.0 → v1.18.0`, verdict `⚠️ DRIFT · current → current`,
  and the DRIFT bullet removed (the pin fix #438 landed now shows current on a live origin/main
  scan).
- `.sessions/2026-07-17-kit-self-pin-version-truth.md` — prior card's `📊 Model:` line conformed
  to the PL-004 taxonomy.
- `docs/NEXT-TASKS.md` §3 — the self-pin drift task #438 completed marked done.

## Verification
- `python3 -m pytest tests/ -q` → **1721 passed, 1 skipped**.
- `python3 dist/bootstrap.py check --strict` → green except the intended born-red HOLD
  (now flipped as the final step of this session).

## 💡 Session idea (Q-0089)
**Version-home change → downstream-regen guard.** This session's entire drift tail existed
because merged #438 changed a *version-home* (`substrate.config.json` + `scripts/cut_release.py`)
at the SOURCE, but nothing flagged that the downstream discovery-generated `docs/adopters.md`
(and the NEXT-TASKS §3 task it completed) were now stale — they sat stale for a day until this
wake caught them on sight. Idea: an advisory `check --strict` warning that fires when
`docs/adopters.md`'s "Generated:" timestamp predates the latest commit touching a version-home
(`substrate.config.json` / `cut_release.py` / the version constant) — i.e. "adopters.md is
stale-by-N-commits vs a version-home change, run `currency`." Turns a recurring on-sight catch
into a guard (friction → guard). Not built this session.

## ⟲ Previous-session review (Q-0102)
Of the afternoon #438 session (card `.sessions/2026-07-17-kit-self-pin-version-truth.md`):
genuine remark — it did the RIGHT thing fixing the pin **at the source** (`substrate.config.json`
as a third synced write target in `cut_release.py`) and adding a drift-brake test, a
source-of-truth fix rather than a local patch. But it left a **downstream drift tail**: it did
not regenerate `docs/adopters.md` (which still reported the now-resolved self-DRIFT), nor strike
the NEXT-TASKS §3 task its own merge completed — so this next session had to reconcile it. The
concrete system improvement it surfaces is exactly the Session-idea guard above (couple
version-home changes to a downstream-regen advisory), so "fix-at-source" sessions don't leave a
drift tail for the next wake.

## Doc audit (Q-0104)
The merged-PR ledger / current-state note the three fixes land cleanly under PR #440; nothing
from this session is captured only in chat. Nothing else outstanding.
