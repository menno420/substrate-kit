# 2026-07-12 — Grounded skills program: survey + design plan

> **Status:** `complete`

- **📊 Model:** fable-5 · high · planning

## Scope (what is about to happen)

Survey + design plan for the kit-owned grounded skills / capability
self-knowledge / playbook program (owner directive via coordinator,
2026-07-12). Supersedes the 2026-07-11 feature-growth freeze for this
program only — owner-directed live.

Deliverable this session: `docs/planning/2026-07-12-grounded-skills-program.md`
(survey + design plan) added in a follow-up commit on this branch, then this
card flips `complete`. Lane claim:
`control/claims/claude-grounded-skills-program.md`.

## Close-out (what shipped — PR #263)

- **The plan**: `docs/planning/2026-07-12-grounded-skills-program.md` —
  consolidated owner directive + provenance; architecture built on the
  EXISTING `src/engine/skills/skills.py` layer + ADOPT_PLAN/upgrade
  hash-classification + `ENGINE_CONTEXT_KEYS` plug points (extend, don't
  duplicate); owner-assist output standard (Q-0263.2 extended, worked
  example, control-plane `/journal/{repo}/file` link pattern verified live
  for 4 repos); capability self-knowledge mechanism — **venue-scoped
  (venue × operation) entries + posture rule (owner-live vs autonomous;
  designed to replace superbot Q-0270 local prose at next upgrade) and
  per-entry freshness + a staleness clause as discovery-rule step 5**
  (night-review 2026-07-12 evidence, verified at superbot origin/main);
  Q-0254 intake playbook drafted as a kit skill body; honest gap map
  (12 rows, "partly done" honestly marked); 8 one-PR slices; 4 structured
  owner questions (§8). **Plan only — no slice implemented; slices are
  follow-up sessions.**
- **Ledger link + drift fix**: plan linked from `docs/current-state.md`
  § In flight (reachability); the three stale In-flight bullets
  (#69/#63/#46 — all merged 2026-07-09, releases verified) condensed to a
  dated drift note, restoring the 7000-word orientation budget.
- **CI diagnosis (task 0)**: the three reds on head 521929b (run
  29188676570) are ONE designed red — kit-quality's Session gate holds the
  born-red card (all other steps green, incl. the real "Kit test suite" and
  "Cold-adoption smoke" steps); the standalone `Kit test suite` +
  `Cold-adoption smoke` FAILURES are the ci.yml legacy-context alias jobs
  that deliberately fail whenever kit-quality is not success (the KL-1 #7
  skipped-check hole). Main's latest CI run is green (1295d73); the two
  newest main merges have no push runs (workflow-token merges don't trigger
  workflows), not red ones. No real failure; nothing fixed because nothing
  was broken — the W-9 false-alarm class, third sighting.

## Session enders

💡 **Session idea:** a skill-grounding rot linter — once slice 2 ships
playbook-grade skill bodies with exact commands, add an advisory check that
extracts every command/path a kit-shipped skill body names and verifies it
against the tree (script exists, referenced doc exists, flag accepted per
`--help`). Playbooks with exact groundings are the program's core bet, and
exact groundings rot silently when a script is renamed; the emit pipeline
already owns both sides (writer = `skills.py`, enforcer = a sibling check),
matching the grammar.py writer/enforcer-share pattern. Deduped against
`docs/ideas/` (no skill-related entries exist).

⟲ **Previous-session review:** the ORDER 015 session (#261) set the bar
this plan leans on — its fixture-evidence pattern (pristine main + synthetic
card + verbatim command/exit transcripts) settled a census claim in ~5
commands, and its `agreement_home` fix created the exact ENGINE_CONTEXT_KEYS
precedent §2 of the plan builds on. One workflow improvement it surfaces:
the designed born-red red still arrives amplified ×3 (kit-quality + the two
legacy alias jobs), and for the third recorded time (W-9, #244, this
session's task 0) a coordinator/reviewer spent a diagnosis cycle on it. The
cheapest enforcing fix is the owner's queued P10 repo-settings switch
(require `kit-quality`, delete the aliases) — worth surfacing as the
structured one-liner it is rather than leaving it parked in the gates list.

**Documentation audit:** `check --strict` green at flip (only the designed
hold before it); durable homes: the plan doc (program design),
current-state.md (In-flight link + drift note), this card (CI diagnosis +
enders). Claim file `control/claims/claude-grounded-skills-program.md`
deleted this commit (claims README step 4). No new owner decisions taken —
the four §8 questions are routed to the owner via the plan + run report.
