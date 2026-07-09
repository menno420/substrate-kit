---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# `--apply-docs` is a single-shot window — the "re-run with --apply-docs" hint is misleading (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (v1.6.0 fleet rollout — observed live on both consumer
> upgrade runs, superbot-next#96 and websites#45).

## The finding

When an upgrade run finds template-improved docs and was NOT invoked with
`--apply-docs`, the report says (src/engine/upgrade.py:390–394):

> `note: N doc(s) have template improvements you never edited — re-run with
> --apply-docs to take them.`

That hint is wrong **after the run completes**. The improved classification
only exists *during* the version transition: step (5) replaces the vendored
dist with the new one, and step (9) self-cleans `bootstrap.py.new` + its
adjacent `release.json`. A re-run of `upgrade` now parses "old" templates out
of the (already-new) vendored dist — old == new, so `classify_planted_docs`
can never yield a `CLASS_IMPROVED` row again. The window was single-shot; the
hint sends the operator on a no-op.

The only recovery today is `upgrade --rollback` and a full re-run with
`--apply-docs` — heavyweight, and it has its own data-loss side effect (the
adopt-pass hash records; see the companion idea
[`upgrade-rollback-loses-doc-hash-records-2026-07-09.md`](upgrade-rollback-loses-doc-hash-records-2026-07-09.md)).

## The fix to build

Post-hoc apply against the **banked archived dist**: both `adopt` and
`upgrade` archive the pre-upgrade dist under
`<state_dir>/backup/bootstrap-<old-version>.py` (archive-first covenant,
`archive_dist`, src/engine/adopt.py:122), so the old templates are still on
disk after the window closes. A same-version `upgrade --apply-docs` (or a
dedicated `apply-docs` subcommand) should detect vendored == running version
and load `old_templates` from the newest archived pre-upgrade dist instead of
the vendored file — turning the single-shot window into a durable one without
rollback. The report hint then becomes true again; until the mechanism
exists, the hint text should name the real recovery path.

**Guard recipe:** `upgrade()` step (3)/(4) + the `improved and not
apply_docs` note branch in `src/engine/upgrade.py`; `load_old_templates` /
`archive_dist` seams; test target `tests/` `test_upgrade.py` — a fixture that
upgrades without `--apply-docs`, then applies post-hoc and asserts the
improved doc actually updates.

## Done-when

An operator who skipped `--apply-docs` on the upgrade run can still take the
template improvements afterwards without a rollback, and no report line
recommends a command that cannot work.
