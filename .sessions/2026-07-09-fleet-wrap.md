# Session 2026-07-09 — fleet rollout v1.6.0 wrap-up (kit-side increment)

> **Status:** `complete` *(PR #75 — auto-merge armed at open via MCP, per convention)*

**Scope (about to do):** record the completed v1.6.0 fleet rollout on the
kit side, docs-only. (1) `docs/adopters.md`: superbot-next + websites rows
→ v1.6.0 / engaged yes / last-seen 2026-07-09, evidence superbot-next#96 +
websites#45 (both merged today). (2) File four B4-frontmatter ideas from
the two upgrade runs' field findings (`--apply-docs` single-shot window;
rollback-loses-hash-records; idempotent-archive report gap, third report;
release.json placement line in the upgrade checklist). (3)
`docs/current-state.md`: rollout complete, agent queue re-pointed at the
upgrade-UX fixes + B1 run-3; websites' unexecuted ORDER 005 noted as a
manager relay item. (4) STATUS LAST: `control/status.md` heartbeat (phase
line only; the six-field ⚑ OWNER-ACTION list and the gen-1 wind-down claim
stay intact). No src/ / dist/ / bench/ writes; no version bump.

## What shipped (PR #75)

- **`docs/adopters.md`** — superbot-next + websites rows → **v1.6.0 /
  engaged yes / last-seen 2026-07-09** with evidence links:
  [superbot-next#96](https://github.com/menno420/superbot-next/pull/96)
  (merged 9761db4; report 7 consumer-edited / 2 diverged / 1
  missing→planted / 3 template-improved applied / 6 unchanged;
  `from_version` honest; inputs self-cleaned; CAPABILITIES.md planted fully
  rendered + hash-recorded; six-field heartbeat live; `check --strict` exit
  0; 1124 tests green) and
  [websites#45](https://github.com/menno420/websites/pull/45) (merged
  ab0995d; 13 kept / 5 diverged hand-merged / 1 template-improved applied;
  CAPABILITIES.md replanted + seeded with 4 repo-verified entries;
  six-field ⚑ rewrite; `check --strict` exit 0; 125 tests green). **The
  v1.6.0 fleet rollout is complete — every active adopter ENGAGED on
  v1.6.0.**
- **Four B4-frontmatter ideas** (dedup-grepped; README backlog indexed;
  guard recipes with code anchors in each):
  `upgrade-apply-docs-single-shot-window-2026-07-09.md` (the "re-run with
  --apply-docs" hint is a no-op post-run; fix = post-hoc apply against the
  banked archived dist), `upgrade-rollback-loses-doc-hash-records-2026-07-09.md`
  (rollback restores pre-upgrade state.json → `planted_doc_hashes` lost;
  fix = record hash when a kept doc byte-matches the new template render),
  `upgrade-archive-report-line-gap-2026-07-09.md` (idempotent
  `archive_dist` is silent → report shows only the NEW dist's `archived:`
  line; **third field report — priority bumped**),
  `upgrade-checklist-release-json-placement-2026-07-09.md` (checklist never
  says to place `release.json` next to `bootstrap.py.new` → in-flow sha256
  verification silently skips; one checklist line closes it).
- **`docs/current-state.md`** — #75 Recently-shipped entry (rollout
  complete, both consumer runs' facts, the websites ORDER 005 manager-relay
  item); agent queue item 1 rewritten from "consumer upgrades" (DONE) to
  the four upgrade-UX fixes; B1 run-3 item now names its owner blocks (#49
  merge + rubric F-5 ruling) up front.
- **`control/status.md`** (deliberate LAST content act) — phase: fleet
  rollout v1.6.0 COMPLETE · inbox drained (001–009 done) · agent queue =
  upgrade-UX fixes then B1 run-3 · owner queue unchanged; `updated:`
  refreshed; the 11-item six-field ⚑ OWNER-ACTION list carried byte-intact;
  the **gen-1 wind-down claim (#72, kitlab-winddown-phase1) carried
  untouched and named as standing**; ORDER 005 relay item added to notes.
  Advisory verified pre-flip: `python3 dist/bootstrap.py check` exit 0 (its
  only findings were this card's own not-yet-flipped markers, by design).

## Verification

- `python3 scripts/check_idea_index.py` → OK (frontmatter + README index).
- `python3 dist/bootstrap.py check` → exit 0 (status heartbeat valid).
- Docs-only diff (docs/ + control/ + .sessions/) — no src/, dist/, bench/,
  or workflow writes; the full kit-quality suite runs on the PR (not the
  control fast lane, since the diff exceeds control/**).

## Flags

- **⚑ Self-initiated:** preserved + explicitly carried the sibling
  session's gen-1 wind-down claim inside the rewritten phase line (the
  fleet-wrap heartbeat postdates the #72 claim; clobbering it would have
  un-claimed the wind-down — decide-and-flag, no owner input needed).
  Added the websites ORDER 005 relay note to status `notes:` (manager-read
  surface) beyond the ledger mention the task named.
- **⚑ Origin call on the idea files:** `origin: lab` (the kit-lab
  coordinator observed the findings while driving the consumer upgrades;
  the consumer PRs are cited as evidence in each file) — `consumer:*` would
  have implied the adopter repos raised them.

## Session enders

- 💡 **Session idea:** *adopter drift-window advisory* — a scripts-level
  check (advisory, PL-008 unverified header) that parses
  `docs/adopters.md` rows and flags any ENGAGED adopter whose
  `kit_version` lags `KIT_VERSION` by ≥2 MINOR releases, plus `last-seen`
  older than N days ("staleness reads as dark"). Today that judgment is
  hand-made (OWNER-ACTION 10 cites superbot's 6-release drift manually);
  after this rollout the fleet is synchronized, and the advisory would
  catch the *next* drift window opening instead of waiting for a fleet
  review to notice. Dedup-grepped: no existing drift-window/registry-check
  idea. Guard recipe: registry table parser over `docs/adopters.md` +
  `KIT_VERSION` from `src/engine/lib/config.py`; test target a fixture
  table in `tests/`.
- ⟲ **Previous-session review (the owner-list dogfood session, #71):**
  strong pass — it converted all 11 ⚑ carries into the six-field
  OWNER-ACTION form it had just made doctrine (dogfooding ORDER 008 on the
  kit's own status within hours), and it *expired 4 stale carries with
  cited reasons* rather than letting the list accrete — exactly the
  self-auditing behavior the form exists for. The VERIFIED-NEEDED fields
  citing concrete attempt evidence (audit rows, quoted API errors) set the
  quality bar. One concrete workflow improvement it surfaces: the status
  file is now ~9KB dominated by 66 owner-item fields — the six-field form
  has no *index*; a one-line numbered title list at the top of the ⚑ block
  (or a compact summary emitted by `check_owner_actions.py`) would let the
  owner scan 11 items before committing to read any — worth folding into
  the checker's next increment rather than a new convention.
- **📊 Model:** fable-5 · high · docs-only
