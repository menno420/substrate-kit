---
state: promoted
origin: lab
shipped_pr: 19
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-09
outcome: shipped
---

# Reflection miner: line-start markers only (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (KL-5-era observation on the band's real cards) →
> promoted → **shipped** same day (kit PR #19). **Origin:** lab — the miner
> run over the kit's own `.sessions/` cards.

## The problem

`mine_reflections` passes 1–2 tagged any non-heading line *containing* 💡/⚑.
Real session cards mention the markers mid-prose as cross-references — "see 💡
below for the durable fix", "its friction-index 💡 (…) was left floating",
"under a ⚑ Self-initiated line" — and each became a junk lesson candidate,
polluting the B2 buffer's input.

## What shipped (PR #19)

`_ref_marker_tags` (`src/engine/loop/reflections.py`) now requires the marker
to **lead** the line — after list bullets, ordered-list numbers, blockquote
marks, and emphasis characters (`_REF_LEAD_PREFIX_RE`). `1. ⚑ Decide-and-flag:
…`, `- 💡 Session idea: …`, and `> ⚑ …` still mine; mid-prose mentions never
do. `_ref_clean_line` shares the prefix regex (numbered-list prefixes no
longer leak into lesson text). Regression test:
`tests/test_reflections.py::test_mine_skips_mid_prose_marker_fragments`.

## Survive window

Merged 2026-07-09 → the D-15 revert-scan may flip `outcome: survived` from
2026-08-08.
