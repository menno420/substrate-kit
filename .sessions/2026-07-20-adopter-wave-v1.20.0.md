# 2026-07-20 · adopter-wave v1.20.0 → v1.20.1 — distribute kit to reachable adopters

> **Status:** `complete`

Wave-lane PR #548 (branch `claude/adopter-wave-v1.20.0`). Distributed the
substrate-kit v1.20.1 dist to the reachable fleet adopters and recorded the
wave outcome here. During the wave a detector fix + patch release landed, so
the wave target advanced v1.20.0 → **v1.20.1** mid-flight; the sweep ran
against v1.20.1.

- **📊 Model:** opus-4.8 · medium · docs-only

Run type: owner-directed (fm ORDER 048 + Q-0261.3 — adopter-wave; adopter
writes = kit distribution only, standing-authorized).

## Kit fix + release shipped this wave (kit-side, cited)

- **Detector fix — PR #549 (squash `662be7d`):** `check_no_false_walls`
  clearing vocab rewritten to **attachment-based** matching, fixing false
  positives on repudiation / dated-record lines (the 5 idea-engine
  false positives) while keeping genuine bare walls red. Two non-blocking
  detector follow-ups recorded in #549's card: (P2) wrapped-lookback
  punctuation-gated bleed; (P3) `match_blocklist` one-hit-per-line masking.
- **Patch release — v1.20.1:** bump PR #550 (squash `40eb0fe`); `release.yml`
  run `29720142913` success; tag **`v1.20.1` → `40eb0fe`**; dist sha256
  `d6c4f81565f8877f38e2b4315968fc5f22a378c9c4dfdd89f8ed02827e7f6b39`
  (verified three ways). Local tree confirmed at v1.20.1
  (`substrate.config.json` / `pyproject.toml` / `dist/bootstrap.py` header /
  dist sha256 all agree).

## Sweep results — 10 reachable adopters (pokemon-mod-lab DARK/skipped)

All upgrades 1.17.0 → 1.20.1 unless noted; kit-distribution files only (host
workflows / control / settings / hooks untouched). Residuals are
resident-owned pre-existing false-wall / badge doc content noted in each PR
body — the resident lane's to reconcile, **not a wave defect**.

| adopter | old→new | outcome | residual (resident-owned) |
|---|---|---|---|
| idea-engine | 1.17.0→1.20.1 | PR #740 ready | CAPABILITIES.md:139,:149 (dated incident records, no inline date) |
| superbot-next | 1.17.0→1.20.1 | PR #602 ready | current-state.md:97,:114 |
| websites | 1.17.0→1.20.1 | PR #452 ready | ideas/backlog.md:924; owner/OWNER-ACTIONS.md:173,187,481; seat-digest.md:48 |
| trading-strategy | 1.17.0→1.20.1 | PR #160 ready | current-state.md:389; review-queue.md:8; CONSTITUTION.md:166 |
| superbot-games | 1.17.0→1.20.1 | PR #183 ready | current-state.md:102; gen2-custom-instructions-exploration.md:73; + resident test tests/tools/test_preflight.py pins old "designed hold" wording |
| venture-lab | 1.17.0→1.20.1 | PR #282 ready | 9 false-wall findings across docs/ (all resident-owned) |
| superbot-mineverse | 1.17.0→1.20.1 | PR #138 ready | NEXT-TASKS.md:26; decisions.md:39 |
| fleet-manager | 1.17.0→1.20.1 | PR #390 ready | 39 false-wall findings, all hub-owned docs |
| gba-homebrew | 1.17.0→1.20.1 | PR #211 **merged** | PLATFORM-LIMITS.md:45; + 2 missing-Status-badge (arcs/TILTSTONE.md, arcs/UNDERROOT.md) |
| superbot | pin 1.0.0 | skip-not-applicable | pin-only nominal adoption; no vendored bootstrap.py, no .substrate/ state — dist-vendoring upgrade N/A. Pin still 1.0.0 (flagged for a possible separate pin-only bump). |

## Wave verdict

9/9 vendoring adopters swept — each upgrade PR opened ready, kit-distribution
files only, host workflows/control/settings/hooks untouched. gba-homebrew's
PR #211 has since **merged** (github-actions bot, 2026-07-20T06:16:35Z →
main tree now v1.20.1); the other 8 sit ready, ⚑ awaiting resident merge.
Each open PR reds its adopter's gate ONLY on pre-existing, resident-owned
false-wall / badge doc content, which is the resident lane's to reconcile —
not a wave defect. superbot is pin-only (skip-not-applicable); pokemon-mod-lab
is DARK (private, skipped, adoption UNKNOWN).

**2 transient auto-mode-classifier denials** occurred on worker-SPAWN
(superbot special-framing + gba-homebrew) — both cleared on a neutral retry.
These are transient venue/classifier states, **NOT** adopter-side walls and
**NOT** standing walls; recorded here as transient only, deliberately not
appended to `docs/CAPABILITIES.md` as capability walls.

## Kit-side close-out

- `docs/adopters.md` regenerated via `python3 dist/bootstrap.py currency`
  (12-repo scan; `currency --check` exit 0 — current). The registry reflects
  each adopter's main-branch tree (still pre-upgrade for the 8 open PRs — the
  correct truth, an open PR is not yet in the tree). A hand-added
  `## v1.20.1 distribution wave (2026-07-20)` bullet section records the
  pending upgrade PRs the rows-only scan cannot see (bulleted so the lines
  stay invisible to the currency row parser).
- `control/status.md` heartbeat overwritten: `kit: v1.20.1`, wave-results
  table, adopter-wave ⚑ resolved with evidence. Standing ⚑ items (kit-lab
  daily cron A/B, visibility A/B, t5-headless-guard) carried forward
  unchanged. Failsafe trigger `trig_01194PdaWChtHGNKASURxdLx` untouched.
- Wave claim `control/claims/adopter-wave-v1.20.0.md` removed at close.

## 💡 Session idea

A **wave-tracker checker** (`check_wave_pending`, advisory): when
`docs/adopters.md` carries a `## v<X.Y.Z> distribution wave` section listing
open upgrade PRs, cross-check each named repo's `Registry` tree cell — a repo
whose tree now equals the wave target while the wave section still lists its
PR as `open` is stale (the PR merged; flip it to `merged` or re-run
`currency`). This closes the one manual gap this wave exposed: the bulleted
pending-PR list is hand-maintained and can silently drift from the generated
rows (exactly what happened to gba-homebrew #211 mid-session). Advisory-only,
off STRICT_SUBCHECKS, reuses `_registry_rows` as the single source of truth.

## ⟲ Previous-session review

The prior leg (release v1.20.1, PR #550 / card `2026-07-20-release-v1.20.1.md`)
cut the patch cleanly and verified the dist sha256 three ways — solid,
evidence-first. What it left for this session to catch: its own card's
`📊 Model:` task-class reads `release cut`, which is off-taxonomy (advisory
warning still firing in `check --strict`); the 9 PL-004 classes don't include
a release class, so `docs-only` is the honest fit for a release-cut card.
**System improvement:** the born-red card templater plants a task-class slot
but nothing steers the author to the 9-value taxonomy at author time — the
off-taxonomy classes (`docs-ops`, `engine-bugfix`, `release cut`) recur across
cards. A one-line taxonomy hint in the card template (or a Stop-hook nudge
listing the 9 classes when it detects an off-taxonomy segment) would convert
these recurring advisory warnings into an at-write fix. Captured as the
adjacent shape of this session's 💡 idea.

## Doc audit

- `currency --check` exit 0 (adopters registry current, 12 repos).
- `check --strict` green apart from the by-design born-red HOLD (cleared by
  this card's flip to `complete`); no exit-affecting FAIL.
- Kit release facts cross-checked against git: #549→`662be7d`, #550→`40eb0fe`,
  tag `v1.20.1`→`40eb0fe`, dist sha256 matches the release row.
- Wave state (open PRs + gba #211 merged + superbot skip + pokemon DARK)
  recorded in both `docs/adopters.md` and this card — no wave fact lives only
  in chat.
