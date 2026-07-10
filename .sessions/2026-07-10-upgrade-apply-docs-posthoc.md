# 2026-07-10 — gen-2: full upgrade-apply-docs post-hoc-apply mechanism

> **Status:** `in-progress`

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

## Outcome

(filled at close)
