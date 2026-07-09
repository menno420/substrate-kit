# Session 2026-07-09 — P0: close the render/engage adoption gap (band KL-7)

> **Status:** `complete` *(PR #25 — band PR, auto-merge armed at open; the
> companion PL-register note rides its own `do-not-automerge` PR, left OPEN
> for the owner beside #17.)*

**Scope (owner directive, routed from the independent fleet review — superbot
`docs/eap/fleet-review-2026-07-09.md` §4):** both fresh adopters (superbot-next
AND websites) stranded identically — planted docs still under UNRENDERED
banners, `${...}` slots unfilled, `session_count` 0, `.claude/` inert, no CI.
Root cause is upstream in the kit: `adopt` plants-and-banners, but rendering
and enforcement are separate opt-in steps nothing forces. This band ships the
**born-red post-adopt engagement gate** — "enforce, don't exhort" (PL-007)
applied to onboarding itself.

## What shipped (PR #25, band KL-7, D-0005)

- **`src/engine/checks/check_engagement.py`** — the ENGAGEMENT gate riding
  the ordinary `check` finding loop (strict-only exit impact, guard-fire
  telemetry + reasons-required allowlist apply unchanged). Four finding
  kinds, each message an actionable checklist line:
  `unrendered-banner` (planted doc still opens with the adopt banner —
  fires even without version evidence: a banner IS kit output),
  `unrendered-slot` (leftover `${...}` in a planted doc;
  adoption-evidence-gated so host `${name}` prose in a never-adopted repo
  never false-positives), `enforcement-unwired` (no workflow under
  `.github/workflows/` runs `check --strict` — substring match, so a
  hand-rolled gate like the kit's own `ci.yml` counts), and
  `session-loop-idle` (`session_count` 0 AND no real session card). Scope =
  the ADOPT_PLAN destinations + `project.index.json` + a live
  `.claude/CLAUDE.md` — never template sources, so the kit repo's own
  `src/engine/templates/` can never red its own gate (verified: consumer #0
  is engaged-green; only this card's born-red badge held CI).
- **`adopt` stages the door + tells the adopter** — the live
  `substrate-gate.yml` is now staged at `<state_dir>/ci/substrate-gate.yml`
  on EVERY adopt (kit stages, host installs — doctrine unchanged;
  `--wire-enforcement` still installs it live), and `cmd_adopt` ends by
  running the engagement scan and printing `NOT ENGAGED — check --strict
  holds RED until these N item(s) are done:` with the findings as the
  checklist (or `ENGAGED` when green).
- **Cold-adopt smoke rewritten to the RED→ENGAGED→GREEN arc** (`ci.yml` §3.2
  item 4): bare adopt must print the checklist, stage the gate file, and be
  RED under `check --strict`; the smoke then walks the checklist (answer all
  13 slots → `render --live` → install the staged workflow → first complete
  session card) and asserts GREEN, including the `--require-session-log`
  gate mode; the `--wire-enforcement` leg asserts wired-but-unrendered is
  STILL red. Verified end-to-end locally against the regenerated dist.
- **Tests** — `tests/test_check_engagement.py` (12 tests: all four kinds,
  evidence gating, template-source immunity, hand-rolled-CI acceptance,
  card-or-count loop engagement, the born-red→green arc, adopt UX +
  staging); `tests/test_cli_gate.py` fixture upgraded to an ENGAGED scratch
  (all slots answered pre-adopt, enforcement wired, `session_count` 1) so
  the session-log gate stays tested in isolation. Suite **626 → 637**.
- **Governance** — `docs/decisions.md` [D-0005]; CHANGELOG `[Unreleased]`
  Added (bottom of section, away from #17's pending hunk);
  `docs/current-state.md` KL-7 band entry + #25 rows (owner-actions list
  untouched — stays the one live list). Dist regenerated + byte-pinned
  (`src/build_bootstrap.py` MODULE_ORDER gains the module after `adopt.py`).

## Run report

- **📊 Model:** fable-5 · high · feature build

### ⚑ Self-initiated / decide-and-flag (PL-001)

1. **Band named KL-7** — the founding plan defines KL-0…KL-6 only; this
   owner-directed band takes the next free id per the §10 numbering.
2. **Strict-only hard-fail** — default `check` prints engagement findings
   but still exits 0. Every CI path (planted `substrate-gate.yml`, the
   kit's `ci.yml`) runs `--strict`, so the gate holds where it enforces;
   default check stays the mid-session advisory surface ("a host may run
   check mid-session" — same split as the session-log gate).
3. **Engagement findings ARE allowlist-suppressible** (reasons-required,
   verdict-recorded) — unlike the never-allowlistable session-log gate. A
   host with a deliberately unrendered doc gets an audited escape valve
   instead of a fork.
4. **Kept "kit stages, host installs"** rather than making adopt
   render-and-wire by default (the review offered both shapes; the owner
   recommended the reversible one) — the gate + staged workflow + printed
   checklist force the last mile without the kit ever writing live CI
   silently.
5. **Adoption evidence = recorded kit_version; a banner counts alone** —
   bare `${name}` prose in a never-adopted repo is host content, never a
   finding (superbot-shaped repos with shell/JS `${...}` in docs stay
   clean).
6. **A born-red card counts as "session loop engaged"** — engagement
   measures that the loop RUNS; card completeness is the session-log
   gate's own job (no double-gating).
7. **Drift-on-sight**: replaced the stale In-flight #24 row in
   `docs/current-state.md` (merged) with the #25 row.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**`status` shows the engagement headline** — `bootstrap status` prints
project_id/stage/mode/stance/sessions but not the one thing KL-7 makes
first-class: a final `engaged : yes | NO (N blocker(s))` line (one
`check_engagement` call) would put the gap on the cheapest surface every
agent already checks, before CI ever runs. Small, self-contained, rides any
next increment.

### ⟲ Previous-session review — audit follow-ups (PR #24)

Genuinely strong: it converted both label-gate holes into *enforcing*
guards (the labeled-event disarm workflow + `check_program_law
--label-gate` as a red required check, not advice) and corrected the run's
incident count upward — the honest direction. One concrete system
improvement it surfaces: its guard sweep audited **merge-time** surfaces
only (labels, arming, required checks) while the *adoption-time* surface —
today's fleet-review finding, live in two consumer repos during that same
session — sat unguarded one lifecycle stage earlier. When auditing a guard
stack, sweep every lifecycle stage the kit owns (adopt-time, session-time,
merge-time, release-time), not just the stage that most recently bit; this
band retro-fills the adopt-time cell.

## KPIs / verification (this worktree)

- `python3 -m pytest tests/ -q` → **637 passed** (626 + 12 new, 1 reworked
  fixture file).
- Dist byte-pin: `python3 src/build_bootstrap.py` → regenerated; committed
  in the same commit (CI re-verifies byte equality).
- `python3 -m ruff check src/engine/` → clean (stdlib-only, no
  print/assert/subprocess in the new module; fail-open reads).
- `python3 scripts/check_program_law.py` → OK; `--label-gate` self-test →
  correctly skips outside PR context (this PR touches no law surface).
- `python3 scripts/check_idea_index.py` → OK.
- `python3 dist/bootstrap.py check --strict --require-session-log
  --session-log .sessions/2026-07-09-p0-adopt-engage-gate.md` → held red on
  the born-red card exactly as designed; green at this flip. Engagement
  findings on consumer #0: **none** (the kit repo is engaged).
- Full dist-driven RED→ENGAGED→GREEN arc exercised in a scratch repo
  (adopt → checklist printed → red → 13 answers → `render --live` → staged
  gate installed → first card → green, both strict and gate mode).
