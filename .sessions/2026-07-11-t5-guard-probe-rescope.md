# 2026-07-11 — T5 guard-probe re-scope (pin path, owner-ratification PR)

> **Status:** `in-progress`

## What is about to happen

Re-scope the T5 bench task (docs/gen2/next-boot.md §0 item 2, DAYTIME-eligible
per the `control/status.md` next-queue): runs 4–5 half-closed the v1 premise —
the live advisory guard FIRES (~9–10× per T5 window) but cold sessions ignore
it — so rewrite `bench/tasks/T5.md` to measure what discriminates NOW
(response to a VISIBLE guard signal on the post-v1.9.0/v1.10.0 mechanism
surface), keeping the task prompt verbatim.

**Pin-path discipline (§5.0 / check_bench_integrity rule 1):** this PR carries
ONLY the `bench/tasks/T5.md` change + this card, is labeled `do-not-automerge`
from open, is NEVER armed for auto-merge, and PARKS for owner ratification —
its terminal state is the owner's click. If this PR sits open (even CI-green
with a complete card), that is EXPECTED and BY DESIGN for an unratified pin
change.

- **📊 Model:** fable-5 · medium · docs-only
