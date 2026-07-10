# 2026-07-10 — gen-2: full upgrade-apply-docs post-hoc-apply mechanism

> **Status:** `complete`

- **📊 Model:** claude-opus-4-8 · high · gen-2 kit-side upgrade-UX (the 4th
  idea's full mechanism, deferred to interim in #92)

## Scope

Ship the **full** post-hoc-apply mechanism for
`docs/ideas/upgrade-apply-docs-single-shot-window-2026-07-09.md` — the fourth
upgrade-UX idea whose full shape was deferred in #92 (only an interim hint
correction shipped there).

The finding: after an upgrade run, `--apply-docs` template improvements are
only takeable during a single-shot window — once the vendored dist is replaced
by the new one, a bare re-run parses new==new templates and can never yield a
`template-improved` row again. An operator who skipped `--apply-docs` had to
`upgrade --rollback` + re-run to take them.

The mechanism: a same-version `upgrade --apply-docs` (vendored version ==
running `KIT_VERSION`) now works POST-HOC — it loads `old_templates` from the
newest banked archived pre-upgrade dist (named by `last-upgrade.json`, the
archive-first covenant) and runs the SAME classify/apply the in-run path uses.
No rollback needed. The skipped-apply report note now names that working path
(the interim `--rollback` recovery from #92 is removed). The covenant is
unchanged: only consumer-untouched kit-form docs are written, consumer-edited
docs stay diverged, hashes re-record (composes with the #92 self-heal), and a
re-run is idempotent. No banked archive → a clean, actionable message (no
crash, no impossible command).

Touches ONLY `src/engine/upgrade.py`, `tests/test_upgrade.py`,
`dist/bootstrap.py` (regenerated), the idea file's lifecycle marks +
`docs/ideas/README.md`, and this card. NEVER touched: `control/inbox.md`,
`control/status.md`, or anything under `bench/`. In-run `--apply-docs` behavior
is UNCHANGED (the post-hoc branch is guarded by `apply_docs` AND
vendored-version == KIT_VERSION, which the in-run OLD-dist case never hits).

## 💡 Session idea

The archive-first covenant already banked everything post-hoc apply needed —
the pre-upgrade dist survives on disk under `<state_dir>/backup/`, named
precisely by `last-upgrade.json`. So the "single-shot window" was never a
data-availability limit; it was a *code-path* limit: `run_upgrade` only ever
sourced `old_templates` from the vendored file, which the transition had
already overwritten. The fix cost almost no new logic — it reuses
`classify_planted_docs`/`apply_doc_improvements` verbatim and only changes
*where* `old_templates` come from (archive instead of vendored). The pattern
worth generalizing: when a covenant (archive-first) durably preserves state,
audit whether the consuming code path is needlessly reading a *transient*
source of the same truth — the durable one may already make a "single-shot"
operation repeatable for free.

## ⟲ Previous-session review

The prior card (`2026-07-10-upgrade-ux-fixes-batch.md`, shipped #92) closed
`complete`, `check --strict` green. It explicitly deferred this idea's full
mechanism: it shipped only the interim hint slice (the note named the
`--rollback` + re-run recovery) and left the idea `open` for "a groomed-ideas
increment [that] still owes the full post-hoc apply against the banked archived
dist". This session picks up exactly that owed increment — no defect inherited;
the interim note is now replaced by the working post-hoc path.

## Outcome

Shipped the full post-hoc-apply mechanism as kit PR #106. `run_upgrade` gains a
guarded branch (`apply_docs` AND vendored version == `KIT_VERSION`) routing to
`run_apply_docs_posthoc`, which loads `old_templates` via
`newest_banked_archive` (read from `last-upgrade.json`) and runs the same
classify/apply the in-run path uses — recovery without rollback. The
skipped-apply report note now names that working path; the interim `--rollback`
recovery is removed, so no report line recommends an impossible command. In-run
`--apply-docs` behavior is UNCHANGED. Idea file marked `promoted` /
`outcome: shipped` (#106), README moved Backlog → Shipped.

Verification: `python3 dist/bootstrap.py check --strict` green; full suite
798 → 803 passing (5 new guard tests); `ruff check src/engine/` clean;
`dist/bootstrap.py` regenerated from the engine change. No pin path touched;
`bench/` and the `control/` heartbeat/inbox left alone.
