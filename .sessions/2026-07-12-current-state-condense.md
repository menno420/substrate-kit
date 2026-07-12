# Session 2026-07-12 — current-state.md condensation

> **Status:** `complete`

Condensed `docs/current-state.md` after the K0 headroom gauge (PR #308) fired
live at 6913/7000 boot words (87 words headroom, current-state.md 6564 the
dominant term).

## What happened

- History/superseded detail relocated **verbatim** to
  `docs/reports/2026-07-12-current-state-archive.md` (badge `archive`, linked
  from the ledger's header pointer block; relative link targets re-based for
  the new location — sole mechanical change). Full band narratives (KL-0…KL-8,
  release cuts), B1 per-run prose, incident timelines, P10 incident narrative,
  and the full per-PR "Recently shipped" rows all live there now.
- The ledger keeps condensed rows and **every durable link/pointer it
  carried** (script-verified against the pre-change pointer set — 45 path
  tokens + 7 relative link targets, zero dropped).
- Boot set: **6913/7000 → 2862/7000 words** (current-state.md 6564 → 2513;
  headroom 87 → 4138). The headroom advisory is now silent by design
  (below the 0.95 warn ratio).
- Decision-id stamps D-0005/6/7/10 de-duplicated (kept at one home, the
  archive) after the stamp checker flagged the two-doc citation — a checker
  interaction the relocation recipe should name (see ⟲ below).
- Claim file re-formatted to the parseable `- ` bullet grammar after the
  `claims-format` advisory flagged the initial one-liner.
- Verify: `python3 -m pytest tests/ -q` → 1214 passed; `check --strict` red
  only on this card's designed born-red hold pre-flip.

💡 Session idea: **declare a `substrate-budget:` self-cap in
`docs/current-state.md`** (e.g. `substrate-budget: 4000 words` in its head
block). The per-doc self-cap mechanism shipped with the budget gate
(`check_orientation_budget.py`) but NOTHING uses it — the living ledger is
the one doc with measured runaway growth (6564 words in 3 days), and a
self-cap catches regrowth per-doc long before the boot-total gauge nears the
cliff again. Dedup-checked: no existing `docs/ideas/` entry covers
budget/orientation/headroom.

📊 Model: Claude 5 family

⟲ Previous-session review (the K0 headroom advisory session, PR #308): the
gauge did exactly what it promised on its first live firing — one advisory
naming total/budget/headroom **with the per-doc split**, which made this
session's trim targeted (straight to current-state.md, no guess-and-recheck
loop; the split line is the whole reason the BEFORE number was actionable).
Concrete workflow improvement: the advisory names the pressure but not the
relief valve — the responding session had to re-derive the relocation recipe
(verbatim archive + pointer + link re-basing) and discovered the stamp-checker
interaction (decision ids cited from 2 docs after a verbatim archive copy) by
tripping it. Either extend the advisory message with a one-line pointer to a
condensation recipe, or add that recipe (incl. the de-dup-the-D-ids step) to
the doc the advisory's spec cites.
