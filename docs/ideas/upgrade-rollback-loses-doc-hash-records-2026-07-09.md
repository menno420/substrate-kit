---
state: promoted
origin: lab
shipped_pr: 92
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-10
outcome: shipped
---

# `upgrade --rollback` + re-run loses the adopt-pass doc-hash records (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (v1.6.0 fleet rollout — the recovery path the
> misleading `--apply-docs` hint points at was walked mentally on both
> consumer runs, superbot-next#96 + websites#45, and it costs provenance)
> → **shipped** (kit PR #92, merged 2026-07-10, gen-2 upgrade-UX batch:
> self-heal in `classify_planted_docs` — a doc that byte-matches the new
> template render provably stayed kit-form, so its hash is recorded from
> ground truth; a rollback + re-run round-trip regains the coverage).

## The finding

`upgrade --rollback` restores the banked `state.json`
(`<state_dir>/backup/state.json`, banked at upgrade step (2)). That snapshot
predates the upgrade's adopt pass — so every `planted_doc_hashes` entry the
pass recorded (`record_doc_hash`, src/engine/adopt.py:96/517) is discarded.
On the re-run, docs the kit itself wrote moments earlier carry no hash record
and are honestly classified **consumer-diverged**
("docs planted before hashes existed have no hashes and are honestly treated
as consumer-diverged", adopt.py:83–87) — which means `--apply-docs` will no
longer touch them. The recovery path for the single-shot `--apply-docs`
window (companion idea
[`upgrade-apply-docs-single-shot-window-2026-07-09.md`](upgrade-apply-docs-single-shot-window-2026-07-09.md))
therefore degrades the very state that makes doc improvements applicable.

## The fix to build

**Self-healing hash records on byte-match**: during the upgrade's classify
pass (or adopt's skip-if-exists path), when a kept doc's current text
byte-matches the NEW template's render for this install's context, record its
hash. A byte-match *proves* the content is kit-form — recording it is not a
provenance lie, it is recovering a lost record from ground truth. Docs a
consumer actually edited never byte-match and stay honestly diverged.

**Guard recipe:** `classify_planted_docs` + `record_doc_hash` /
`doc_hash_matches` (`DOC_HASHES_STATE_KEY`) in `src/engine/adopt.py`, the
classify call site in `src/engine/upgrade.py` step (3); test target
`test_upgrade.py` — fixture: upgrade → rollback → re-run, assert the kept
kit-form docs regain hash records and classify as kept/improved, not
diverged.

## Done-when

A rollback + re-run round-trip ends with the same `planted_doc_hashes`
coverage the first run achieved; no kit-written, unedited doc reads
consumer-diverged after the trip.
