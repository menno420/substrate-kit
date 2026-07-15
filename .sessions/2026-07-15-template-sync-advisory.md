# 2026-07-15 · template-sync-advisory

> **Status:** `in-progress`

- **📊 Model:** [[fill: model line at flip]]
- Scope: baton item 2 — build the template↔local-copy sync-advisory checker
  (docs/ideas/template-local-copy-sync-advisory-2026-07-15.md): a new
  advisory-only `check` leg comparing `## ` heading SETS between each
  `ADOPT_PLAN` template and the kit's own rendered local copy, firing
  `template-local-heading-drift` when a doctrine section exists on only one
  side. Engine change → dist byte-pin regen. One PR.

About to: write `src/engine/checks/check_template_sync.py` (fence-aware
heading scan, `${slot}`-pattern matching so rendered headings never
false-positive, `[[fill:]]` skip, live-traffic destinations excluded), wire
it into `cmd_check`'s full lane next to the staged-regen advisory, add
fixture tests (template-only section fires; identical heading sets with
divergent prose stay silent), regenerate dist, flip the idea's lifecycle.
