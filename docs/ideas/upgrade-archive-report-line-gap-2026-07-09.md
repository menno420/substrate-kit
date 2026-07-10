---
state: promoted
origin: lab
shipped_pr: 92
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-10
outcome: shipped
---

# Upgrade report shows only the NEW dist's `archived:` line — third report, priority bumped (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (v1.6.0 fleet rollout — **third field report** of the
> same confusion, seen again on both consumer runs superbot-next#96 +
> websites#45; cosmetic, but three reports in one day earn a priority bump
> over other cosmetic items).

## The finding

`archive_dist` (src/engine/adopt.py:122) is idempotent: when an identical
archive already exists it returns the path **without appending the
`archived:` report line** (the early return at "an identical existing archive
is left alone"). In an upgrade run where the old dist was already banked
(a prior `adopt`/`check` pass, or a re-run), the upgrade's step-(2) archive
of the OLD dist is therefore silent, while the embedded adopt pass (step 6 →
adopt.py:501) later archives the NEW dist and *does* print its line. The
operator reads a report whose only `archived:` line names the new version and
reasonably concludes the old dist was never banked — exactly the doubt the
archive-first covenant exists to remove.

Cosmetic — the old archive IS on disk and `--rollback` works — but it has now
misled readers three times.

## The fix to build

Never silent: on the idempotent path, append
`archived: <rel> (already banked)` instead of nothing. One line in
`archive_dist`, dist regen, one test.

**Guard recipe:** the `dest.exists() and dest.read_text(...) == text` early
return in `archive_dist`, `src/engine/adopt.py:122`; test target
`test_adopt.py`/`test_upgrade.py` — run archive twice, assert the second
report still carries an `archived:` line naming the old version (with the
already-banked qualifier).

## Done-when

Every upgrade report accounts for the old dist's archive explicitly, whether
it was written this run or found already banked.
