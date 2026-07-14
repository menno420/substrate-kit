# docs/operations — runbooks & standing operational contracts

> **Status:** `reference`
>
> Index of the kit's operational docs (a reachability root — link new
> operations docs here, not from the K0-metered boot docs).

- [lab-loop.md](lab-loop.md) — the daily kit-lab routine definition + its
  paste-ready prompt (binding).
- [auto-merge-guards.md](auto-merge-guards.md) — the auto-merge guard
  stack: enabler, disarm, label carve-out.
- [release-runbook.md](release-runbook.md) — the proven release recipe
  (version homes, CHANGELOG cut, dist byte-pin, release.yml dispatch,
  three-way hash verification, adopters regen).
- [../reports/2026-07-11-t5-rescope-analysis.md](../reports/2026-07-11-t5-rescope-analysis.md)
  — T5 guard-probe re-scope (dated analysis): why v1's fire/obey items
  stopped discriminating after runs 4-5, the v2 response-to-visible-signal
  design (pin PR #181, parked for owner ratification), run-6 design.
- [../reports/2026-07-11-adopter-outcomes-measurement.md](../reports/2026-07-11-adopter-outcomes-measurement.md)
  — adopter outcomes measurement (dated audit): before/after kit-adoption
  effect unmeasurable today (9/10 adopters born-with-kit; superbot pin-only),
  false-claim audit near-clean, post-adoption time-to-ship baselines.
- [../reports/2026-07-12-prompt-template-hardening-input.md](../reports/2026-07-12-prompt-template-hardening-input.md)
  — prompt-template hardening input (dated audit, inbox ORDER 014): the
  must-carry seat-prompt doctrine list per regression class, the kit-template
  graduation map, and corrections to stale kit facts in the fleet prompts.
- [../reports/2026-07-12-trigger-forensics.md](../reports/2026-07-12-trigger-forensics.md)
  — overnight trigger forensics (dated audit, owner-requested): timeline of
  every scheduling mechanism the seat armed, ranked root-cause hypotheses for
  the missed fresh-session cron fires, other overnight anomalies, and
  recommendations (read-only pass; none executed).
- [../reports/2026-07-12-grounded-skills-wrap.md](../reports/2026-07-12-grounded-skills-wrap.md)
  — grounded-skills program wrap (dated audit): the full verified receipts
  chain (plan #263 → 8 slices → releases v1.13.0–v1.15.0 → distribution waves
  → close-out #298), what the owner's five ideas became, honest gaps
  (lane-owed · owner asks · backlog candidates · the unmeasured-effect gap +
  a #247-methodology measurement proposal), and the ORDER 015 rider
  disposition.
- [../reports/2026-07-09-cfgdiff-differential-testing-method.md](../reports/2026-07-09-cfgdiff-differential-testing-method.md)
  — differential-oracle testing method (bench-practice reference, ported from
  `menno420/codetool-lab-sonnet5` per fm ORDER 025 / inbox ORDER 019 item 5):
  a corpus vs a reference parser (python-dotenv) found 3 real bugs behind
  114 green self-written tests; the corpus design and the fleet-wide rule it
  proposed.
- [../reports/2026-07-09-cfgdiff-v0.1.1-release-decision.md](../reports/2026-07-09-cfgdiff-v0.1.1-release-decision.md)
  — cfgdiff v0.1.1 release-decision writeup (dated audit, ported from
  `menno420/codetool-lab-sonnet5` per the same order): the decide-and-flag
  release reasoning, the tag-push/MCP/api walls with exact errors, and the
  paste-ready owner release path.
- [../reports/2026-07-13-night-run-adopter-outcomes.md](../reports/2026-07-13-night-run-adopter-outcomes.md)
  — night-run adopter outcomes (dated audit, ORDER 016 item 5): 13-seat
  sweep of the 2026-07-12→13 night run (11 SHIPPED · 2 IDLE-CLEAN ·
  0 STALLED), which kit mechanisms the shipping seats exercised (enabler
  landings, three failsafe-bridged wake drops, born-red gate + one
  flip-race bug, control fast lane, ORDER fan-out), and the honest null on
  shipped-vs-stalled discrimination.
- [../eap-closeout-walkthrough-2026-07-14.md](../eap-closeout-walkthrough-2026-07-14.md)
  — EAP closeout walkthrough (owner-facing, ORDER 021): what the seat
  shipped (audit-cited), exact verify commands, the OWNER ACTIONS
  checklist (leads with the #317 click → release wave), a 5-minute
  verify-it-yourself tour, and handoff notes for the next phase.
- [../audits/eap-project-audit-2026-07-14.md](../audits/eap-project-audit-2026-07-14.md)
  — EAP project audit, definitive close-out (dated audit, owner-directed):
  measured program totals (191 sessions · 361 PRs · 350 merged · 2.9-min
  median landing · 19 releases), tooling verdicts, all 20 verified walls
  with verbatim denials and FLEET-FIX/ANTHROPIC/ACCEPTED dispositions,
  scheduling/environment/ceremony findings, the fixed-ourselves ledger,
  ranked remaining pains + paste-ready Anthropic asks, and honest gaps.
- [../reports/2026-07-13-fleet-cleanup-audit.md](../reports/2026-07-13-fleet-cleanup-audit.md)
  — EAP final-night fleet-cleanup audit (dated audit, external read-only
  pass, complementary to owner fm ORDER 045): live-vs-heartbeat activity
  finding (repo was ACTIVE mid-session despite a stale `updated:` line),
  local CI-mirror verification (1284 tests, ruff, idea-index, program-law,
  `check --strict` all clean), disposition of the 3 open PRs at audit time
  (#317/#340/#345, all correctly left untouched), and fleet-wide
  suggestions (mechanical heartbeat writer, the P10 required-check swap,
  a liveness-signal convention for outside audits).
