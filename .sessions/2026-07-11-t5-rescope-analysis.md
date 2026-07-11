# 2026-07-11 — T5 re-scope analysis doc (support lane, merges on green)

> **Status:** `complete`

## What happened

Shipped the supporting analysis for the T5 guard-probe re-scope (pin PR #181,
parked `do-not-automerge` for owner ratification):
`docs/reports/2026-07-11-t5-rescope-analysis.md` — the full rationale (v1's
fire/obey items stopped discriminating: firing proven in runs 4–5, obedience
confounded by the advisory layer's invisibility), the v2
response-to-visible-signal design, and the run-6 measurement plan. Indexed
via `docs/operations/README.md` (reachability root — chosen over
`docs/current-state.md` because a boot-doc pointer pushed the K0 set to
7040/7000 words, tripping the orientation-budget finding; the near-ceiling
K0 budget is already QUEUED KIT FIXES item 1) plus a `bench/README.md`
spec-provenance pointer. No pin-path files in this diff.

## Session enders

- 💡 **Session idea:** carried on the sibling pin-PR card
  (`.sessions/2026-07-11-t5-guard-probe-rescope.md`): a signal-visibility
  lint so no bench row can ever again score guard obedience against a
  signal the session could not see. This card's own smaller find: the
  [reachable] checker's roots are `readpath_docs` + READMEs **under
  docs/ only** (`check_reachable`, `src/engine/checks/check_docs.py`) — a
  README outside docs_root (bench/README.md) silently doesn't count;
  worth one clarifying line in the orphan message so the next session
  doesn't test the wrong root empirically like this one did.
- ⟲ **Previous-session review:** the v1.10.0 close-out review is on the
  sibling pin-PR card; reviewing THIS session's first leg (pin PR #181):
  labeling after MCP-open left an ~8 s window where the `opened` CI
  payload had no label, so the first CI round red-ed on the §5.0 pin gate
  by design-but-avoidably — the improvement is to make the FIRST push
  after labeling immediate (or label before any CI-triggering event when
  the API allows), which this session did via the card-flip push.
- **📊 Model:** fable-5 · medium · docs-only
