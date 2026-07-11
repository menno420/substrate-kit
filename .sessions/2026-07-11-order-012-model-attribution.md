# 2026-07-11 — ORDER 012: model-attribution ground truth

> **Status:** `complete`

## What is about to happen

Inbox ORDER 012 (P3, fm relay #166 @ b58e740; claimed on the heartbeat orders
line via #169 @ 4d96ae5, on main before this build). Check-first execution:

1. **Item 1 (template carries `📊 Model:`)** — verified ALREADY SATISFIED;
   citations in the close-out. No re-implementation.
2. **Item 2 (family-level self-report doctrine)** — the one genuinely-missing
   sliver: nothing in the planted convention says the model segment is the
   FAMILY-LEVEL name the session's own harness reports, nor that external
   surfaces (schedule/Routines screens) are unreliable attribution. Add that
   doctrine sentence to the planted `.sessions/README.md` composer
   (`_adopt_sessions_readme`) + the kit's own copy, with a test and a
   CHANGELOG `[Unreleased]` entry. NO release cut.
3. **Item 3** — n/a per the order; the standing rule is kept.

This card itself is the order's behavioral done-when: it commits with a real
family-level `📊 Model:` line (see the close-out).

## What happened (close-out)

**Check-first verdicts, per done-when item:**

- **Item 1 — ALREADY SATISFIED** (nothing re-implemented). The session-card
  "template" is the convention machinery, and every surface already carried
  the line: `session_markers` default (`src/engine/lib/config.py`
  `_default_session_markers`, needle `📊 Model:`); the planted
  `.sessions/README.md` composer (`src/engine/adopt.py`
  `_adopt_sessions_readme` — exact needle byte-forms since the run-1
  false-red fix); the auto-draft stand-in (`src/engine/loop/handoff.py`
  `_marker_line` drafts `- **📊 Model:** [[fill…]] · …`); the checker
  (`check_session_log` marker scan); the KL-3 telemetry harvest + reconcile
  (`src/engine/loop/telemetry.py`, `telemetry/model-usage.jsonl`); and the
  upgrade join (`src/engine/upgrade.py` step 6b adds the needle to existing
  installs).
- **Item 2 — built the genuinely-missing sliver: doctrine text.** Grep found
  NO "family-level" / self-report-source doctrine anywhere in src/ or docs/.
  Build (commit 5032590): `_adopt_sessions_readme` renders one
  attribution-ground-truth sentence when the host's markers require the
  Model line (keyed to the `MODEL_LINE_NEEDLE`; hosts without the marker get
  nothing) — family-level name the session's own harness reports (`fable-5`,
  `opus-4.8`, `sonnet-5`), committed-card self-report is the ground truth,
  never copy from schedule/Routines surfaces (websites #59 evidence), never
  a dated full model ID. Kit's own `.sessions/README.md` carries the same
  sentence. Tests: `test_sessions_readme_teaches_family_level_model_attribution`
  + `test_sessions_readme_model_doctrine_only_with_model_marker`
  (971 → 973). CHANGELOG `[Unreleased]` Added entry. Dist regenerated
  (645448 bytes real). Scratch-adopt live verify: planted README carries the
  doctrine. Behavioral half: this card's own Model line below is the order's
  done-when instance.
- **Item 3 — n/a; standing rule kept** (family-level names only in recorded
  attribution; no model IDs in commits/PRs/code).

**Adjacent queued idea — ABSORBED:** "model-identity capture automation"
(docs/gen2/next-boot.md §0 item 3, already flagged partially superseded) is
absorbed by ORDER 012: the fm model matrix's finding is that per-session
SELF-REPORT in the committed card is the only reliable attribution — an
automated capture from an external surface is exactly what the order rules
out, and the harness-visible model name is readable only by the session
itself (auto-draft already stands in the fill slot; session-close already
nags). Nothing left to build; removed from the next-queue in
control/status.md by this close-out.

**Verification:** `python3 -m pytest tests/ -q` → **973 passed** ·
`python3 -m ruff check src/engine/` clean · dist byte-pin clean
(`python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py`)
· `check_idea_index` / `check_program_law` / `check_bench_integrity` OK ·
`check --strict --status-only` exit 0 · full
`check --strict --require-session-log` red ONLY with the designed born-red
hold (this card in-progress), which this flip clears.

**CI note (for the observer red-ping on head d14d8fc):** the kit-quality
FAIL on the born-red head was the DESIGNED session-gate hold — the job log
itself printed `HOLD (by design) … not a defect; nothing to investigate`
plus the `::notice` annotation (the #168 banner firing on its first
successor PR, working as intended). No defect; this flip-complete commit is
the fix-by-design.

**Off-taxonomy drift observed (flagged, not fixed here):** recent complete
cards carry `📊 Model:` payloads whose segment 2/3 are off the PL-004
grammar (e.g. `claude-fable-5 · kit-dev lane · queued-fixes batch slice`,
`… · high · bench-run`, `… · medium · release-prep — MINOR bump` — none of
segment-3 values are PL-004 task classes), so their harvested telemetry
rows carry junk-ish class fields. This card's line conforms. See the 💡
below for the enforcing fix.

## 💡 Session idea

A `check` advisory (never exit-affecting, like the claims nags) that lints
the newest complete card's `📊 Model:` payload: warn when the model segment
looks like a dated full model ID (e.g. a `-2026…` suffix) or when the
task-class segment is off the PL-004 taxonomy — mechanizing both the ORDER
012 family-level rule and the taxonomy the telemetry harvest already
advises on at session-close (where it's routinely missed: 4 of the last 5
cards are off-taxonomy). "Enforce, don't exhort" applied to attribution.

## ⟲ Previous-session review

The kit-fixes-batch-2 session (#167/#168) shipped five fixes whole with 24
regression tests and — the standout — routed ORDER 012 correctly per its
`executor:` field instead of grabbing it mid-slice, leaving a check-first
note that saved this session real derivation time. Improvement it surfaces:
its own card's Model line (`claude-fable-5 · kit-dev lane · queued-fixes
batch slice`) is off the PL-004 grammar in both trailing segments, so the
telemetry row it fed is unclassifiable — evidence for the model-line lint
idea above; the workflow half is that close-out reviews should glance at
the 📊 payload against the taxonomy, not just the needle's presence.

- **📊 Model:** fable-5 · medium · feature build
