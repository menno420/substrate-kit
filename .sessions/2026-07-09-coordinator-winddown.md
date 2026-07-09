# Session 2026-07-09 — SuperBot-coordinator lane: wind-down succession pack (gen-1 → gen-2)

> **Status:** `complete` *(PR — READY at open, auto-merge armed; suffixed filenames per the owner's lane rule — this session never touches control/status.md, control/inbox.md, substrate.config.json, or unsuffixed docs/retro files)*

**Scope (planned):** execute the owner's WIND-DOWN succession deliverables
for the SuperBot-rebuild COORDINATOR lane, filed here because `docs/retro/`
holds the lane's merged review pair and `docs/succession/` (new) is the
natural home for handoff packs: (1) the gen-2 next-boot doc; (2) the Custom
Instructions rewrite proposal; (3) the environment spec with the setup
script re-verified live; (4) gen-2 blueprint feedback; (5) the wind-down
retro addendum; then the lane heartbeat overwrite as the deliberate LAST
commit.

## What shipped (this PR)

- **`docs/succession/next-boot-2026-07-09-superbot-coordinator.md`** — the
  gen-2 coordinator's first 10 minutes: 6-item read order with why-lines;
  queue state committed as truth (bands 0–4 live-tested, 20+ live bugs;
  band 5 PAUSED at the owner's stop with PR #95 open/READY and only the
  born-red report job red; bands 6–7 not started; parity gated on flag 13;
  presentation follow-ups D-0025/D-0027/hub-topology/nav-polish); the
  walking-skeleton check for BOTH repos; known walls with exact error text;
  standing facts (test-bot token naming, MineSnakeBotTest, old-SuperBot
  removal ask).
- **`docs/succession/custom-instructions-proposal-superbot-coordinator.md`**
  — keep (4) / add (6) / drop-change (2), one why-line each, plus
  blueprint alignment (gen2-blueprint.md WAS readable — read live from the
  fleet-manager clone; no disagreements, two extensions, one §2a nuance).
- **`docs/succession/environment-spec-superbot-coordinator.md`** — the
  tested setup script referenced (re-verified this session: `bash -n`
  exit 0; scratch execution no-repo exit 0 and with-repo exit 0); env var
  NAMES only (DISCORD_BOT_TOKEN_PRODUCTION → rename to
  DISCORD_BOT_TOKEN_TEST in gen-2; DATABASE_URL; HTTPS_PROXY/CA bundle);
  GitHub scopes (superbot read, superbot-next write, substrate-kit write,
  fleet-manager read; repo creation owner-only).
- **`docs/succession/gen2-feedback-superbot-coordinator.md`** — 7 items of
  blueprint feedback, each anchored in a lived incident (ORDER-005 race,
  the platform-ask list, pre-filled known-walls seeding, the #35
  required-check freeze class, heartbeats + lane registry keep, Model+time
  cards keep, born-red dashboards as default).
- **`docs/succession/README.md`** — the new directory's index.
- **`docs/retro/wind-down-review-2026-07-09-superbot-coordinator.md`** —
  the retro ADDENDUM (links the merged review pair instead of repeating):
  whole-life summary (2026-07-08 15:39Z kickoff → wind-down; 13.6h/49-PR
  build; ~95 PRs total), the exact-error friction ledger (incl. the
  zombie revival and the 5.5h "cannot determine" gap), and the
  first-person close.
- **`docs/retro/README.md`** — wind-down addendum indexed (reachability).
- **CHANGELOG `[Unreleased]`** — one `### Added` bullet.
- **`control/status-superbot-coordinator.md`** — overwritten to
  "wind-down complete — ready for archive + fresh session", deliberate
  LAST commit; ⚑ needs-owner carries the remaining clicks.

## Run report

- **📊 Model:** fable-5 · high · docs-only

### ⚑ Self-initiated / decide-and-flag (PL-001)

1. **⚑ `docs/succession/` created as a new top-level docs directory** with
   its own tiny README index (no prior succession home existed; retro/
   holds reviews, not handoffs). Suffix rule carried into the README so
   later lanes file suffixed packs beside this one.
2. **⚑ fleet-manager added to the session** (owner's task text authorized
   the add) to read `docs/gen2-blueprint.md` live rather than writing
   blueprint-alignment notes from memory; read-only use, nothing written
   there.
3. **⚑ Setup-script execution cases ran against scratch copies** with the
   `/home/user` base substituted for a scratch dir (the live container
   cannot vacate its own home); the verbatim script is what `bash -n`
   checked. Both execution exits 0; noted in the env spec.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**A `succession` checker band: wind-down packs as a first-class kit
artifact.** The kit now has retro protocol (QUESTIONS.md) and session
cards, but succession packs are convention-only — nothing validates that a
lane winding down shipped a next-boot doc, an env spec, and a final
heartbeat flip. A small `check` extension (advisory, like the owner-action
band) could gate "status says wind-down complete" on the suffixed pack
existing in `docs/succession/`. Anchors: `src/engine/checks/` (the
`check_owner_actions.py` pattern), `docs/succession/README.md` naming
convention. Recorded in-card; groom pass can file it.

### ⟲ Previous-session review — coordinator wake-up review (#52)

This lane's previous ship in this repo. Strong: the audit's honest
cannot-determine language (child models, the 5.5h gap) is exactly what
made THIS session's succession pack cheap to write — nothing had to be
re-litigated, only linked. What it missed: it recorded owner actions
click-by-click but left them only in review prose + heartbeat; a
machine-readable owner-queue entry per click (the ORDER 008 six-field form
landed later the same day) would have let the wind-down heartbeat carry
them by reference instead of restating. **Workflow improvement:** when a
review files ⚑ owner actions, file them once in the six-field form and
have every later doc point at that anchor.

## KPIs / verification (this worktree)

- `python3 dist/bootstrap.py check --strict --require-session-log
  --session-log .sessions/2026-07-09-coordinator-winddown.md` → green
  before push.
- Docs-only diff: no engine/test/dist changes; suite state inherited from
  main.
- Setup script re-verified this session: `bash -n` exit 0; no-repo
  execution exit 0; with-repo execution exit 0.
- gen2-blueprint.md read live (fleet-manager clone at c8948da, status
  `binding`); superbot-next `docs/status/testing-report-2026-07-09.md` and
  `rebuild-completion-report-2026-07-09.md` existence verified via the
  live API before being cited in the read order.
