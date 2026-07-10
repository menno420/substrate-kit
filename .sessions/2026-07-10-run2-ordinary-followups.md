# 2026-07-10 — gen-2: run-2 ordinary-lane follow-ups (queue item 3)

> **Status:** `complete`

- **📊 Model:** claude-fable-5 · high · engine+bench fix (one scoped PR: the three
  run-2 ordinary-lane follow-up idea files)

## Scope (as declared)

Implement the three run-2 follow-up fixes the B1 record sessions filed as idea files
(queue item 3, claimed on `control/status.md` by kit-lab-gen2 via PR #94 — the status
close is the orchestrator's, not this PR's). No pin paths, no `control/` writes.

## What shipped (PR #95)

1. **`run_ab.py prepare` engagement arc** (`run-ab-prepare-engagement-arc-2026-07-09`):
   `cmd_prepare` walks the ON-arm RED→ENGAGED→GREEN arc itself — deterministic
   seed-derived interview answers (the CI cold-adopt smoke's 13 slots; truthful values
   where the seed project has one), `render --live`, staged-gate install, first
   (complete) session card, seed heartbeat, commit — then asserts `check --strict`
   exit 0. `manifest.json` is written on the failure path too (`smoke_failed: true`).
   Tests: e2e green-arc pin + failure-path manifest + deterministic-answers unit
   (`tests/test_bench.py`).
2. **`render --live` covers `.claude/CLAUDE.md`** (`render-live-claude-md-gap-2026-07-09`,
   fix shape (a) per the idea file): `_render_live` iterates
   `check_engagement.scan_relpaths()` (made public) — the SAME scope the gate scans —
   so the two surfaces can never disagree; `project.index.json` joins the render set
   harmlessly (no slots). Test: include-claude adopt → answer → `render --live` →
   zero `unrendered-*` findings across ALL gate-scoped files → full gate GREEN
   (`tests/test_check_engagement.py`).
3. **Model-line marker byte-forms** (`model-line-checker-false-red-2026-07-09`, the
   two halves left open after PR #40): `_adopt_sessions_readme()` plants
   ``label (`needle`)`` pairs, and `missing_markers` misses report as
   ``label (expected `needle`)`` (e.g. ``Model line (expected `📊 Model:`)``).
   Ripple fixed at the root: `loop/handoff.py`'s draft path matched drafted stand-ins
   by bare label against `check_log` output — it now maps misses back through the
   same `_marker_miss` formatter, so checker message format and draft composer can't
   drift apart again. Tests: planted-needle assertion (`tests/test_adopt.py`),
   miss-message pins (`tests/test_checks.py`).

Interpretation notes (idea files win over paraphrase, source over idea files): fix 2
took the idea file's preferred option (a) — no contract reason found for a `.claude/`
render exemption; fix 1 pins the slot list to the CI smoke's 13 on purpose
(byte-reproducible arms; bank drift is caught loudly by the arc's own strict assert).

## Gates (final head, run in the worktree)

- `python3 -m pytest tests/ -q` → **776 passed**
- `python3 dist/bootstrap.py check --strict` → exit 0 (after this card flip)
- `python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py` →
  byte-pin green (build verified deterministic)

## Run report

### ⚑ Flags

1. **⚑ Ripple beyond the three named files:** `src/engine/loop/handoff.py` needed the
   `_marker_miss` mapping fix (its draft path consumed `check_log` output as bare
   labels — caught by `test_ensure_draft_appends_close_out_to_in_progress_card`).
   Root-cause fix, not a test patch.
2. **⚑ Docs drift fixed on sight:** `docs/current-state.md` agent-queue item 2 still
   described B1 run-3 as blocked/pending (it fired 2026-07-10, PR #85); refreshed to
   the post-run-3 truth (remaining: T5 shape choice + the now-HOT F-5 ruling).

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**`check_log`/`missing_markers` should return structured misses, not formatted
strings.** This session's one ripple was exactly a string-shaped seam: `handoff.py`
parsed the checker's human-readable miss list to decide which stand-ins to draft, so
changing the message format silently emptied the draft set. Returning
`(marker, reason)` records with formatting applied only at the emit edges (cli
message, guard-fire finding) makes every future message improvement ripple-free.
Small ordinary-lane refactor; no existing idea file covers it.

### ⟲ Previous-session review (B1 run-3, `.sessions/2026-07-10-b1-run-3.md`)

Genuinely strong session: recorder≠judge discipline held under a FAIL verdict, the
judge=arm deviation was self-caught from the native transcripts, and its precise
"follow-up still open on v1.6.0" notes are what made this session's three fixes
land-in-one-pass (the conveyor working). What it could have done better: its 💡 idea
(bench rows should carry measured arm/judge model identity + a judge==arm warning) is
genuinely buildable but lives only in the card — it never became a `docs/ideas/` file,
so it is invisible to the B4 index/backlog conveyor. **Workflow improvement:** the
session-close ritual should either promote the card's 💡 into `docs/ideas/` when it is
actionable (one file, frontmatter, README line) or state why not — a card-only idea is
exactly the orphaning the ideas README exists to prevent.

### Docs audit

Everything in a durable home: fixes → engine/bench + dist (byte-pinned), idea files →
`shipped` frontmatter + README Shipped section (window closes 2026-08-09), release
note → CHANGELOG `[Unreleased]` ### Fixed, ledger → `current-state.md` Recently
shipped + queue-item-2 refresh, telemetry → `.substrate/guard-fires.jsonl` (this
session's own born-red gate fire — committed per the #54 write-back convention).
**`docs/gen2/queue-state.md` deliberately untouched:** it is the gen-1 wind-down
snapshot ("the living ledger and live GitHub win over it as time passes" — its own
header) and no gen-2 session has updated it (items 2/5/6/7 were closed on
status.md/current-state.md only); item 3's closure lands the same way — this PR plus
the orchestrator's status overwrite.
