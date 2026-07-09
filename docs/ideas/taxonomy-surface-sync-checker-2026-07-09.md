---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Taxonomy-surface sync checker — TASK_CLASSES ⇄ ladder ⇄ telemetry README (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (PL-010 ruling session, PR #22).
> **Origin:** lab — friction felt while shipping the PL-010 amendment.

## The gap

The task-class taxonomy lives on **three surfaces that must agree** (the
feature-build idea's own done-when said so): `TASK_CLASSES` in
`src/engine/loop/telemetry.py`, the `telemetry/allocation-ladder.md` table
rows, and the class list in `telemetry/README.md`. Nothing enforces the
agreement — the PL-010 session updated all three by hand and also found the
class **count** hardcoded in prose/messages/test-names in four places
(fixed: the advisory now derives from `len(TASK_CLASSES)`). The next
amendment (or a ladder edit that drops/typos a row) can silently desync
them, and the ladder is the surface agents actually read when picking a
model.

## Guard recipe (friction → guard, PL-007)

A `scripts/check_taxonomy_sync.py` (stdlib, kit-quality step, PL-008
header): parse the ladder's first table column (strip emphasis) and the
README's class list; assert set-equality with `TASK_CLASSES` imported from
`src/engine/loop/telemetry.py` (or regex-parsed, keeping the script
import-free); test anchors in a new `tests/test_check_taxonomy_sync.py`
(clean fixture · missing-ladder-row · extra-row · README drift). ~60 lines
+ tests; ships with its convention per §5.4.

## Done-when

A deliberately-desynced fixture fails in CI; the real repo passes; the
checker carries the PL-008 provenance/kill-switch header.
