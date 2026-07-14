# 2026-07-14 — ORDER 021: EAP closeout walkthrough + park verifications

> **Status:** `complete`

About to (opening declaration): execute ORDER 021 (EAP final day) — (a) live
Q-0120 verification of the #345 zero-check-runs anomaly and of the #317/#345
park states (read-only: no pushes, no labels, no arms, no comments on either
PR), and (b) land `docs/eap-closeout-walkthrough-2026-07-14.md` (Status badge,
linked from `docs/operations/README.md`, sections A–E with the OWNER ACTIONS
checklist leading with the #317 click), plus a surgical `control/status.md`
update to `done=021` with the (a) findings and corrected park-state text.
This PR is deliberately NOT armed and NOT merged by this session.

- **📊 Model:** Claude Fable 5 · high · docs-only (walkthrough + live park-verification)

Run type: worker session (ORDER 021 dispatch, Self Improvement seat).

## What shipped (PR #368)

- `docs/eap-closeout-walkthrough-2026-07-14.md` — owner-facing walkthrough,
  `reference` badge, linked from `docs/operations/README.md`: A. what the
  seat shipped (audit-cited: 191 sessions · 361 PRs · 452 commits ·
  19 releases · 2.9-min median land; depth deferred to
  `docs/audits/eap-project-audit-2026-07-14.md`) · B. current state + the
  exact verify commands (pytest · preflight · check --strict ·
  cut_release.py · verify_release.py · heartbeat/claim verbs, all
  path-verified at HEAD) · C. OWNER ACTIONS (7 items, #317 first, each
  with deep link + paste-ready steps + bolded recommendation + VERIFY) ·
  D. 5-minute tour · E. handoff notes (release-wave mechanics, #345 baton,
  adopters.md regen condition, grounded-skills window ~07-19).
- `control/status.md` — `done=021` facts line, ledger
  `acked=001–021 · done=001–021`, and the two Parked lines corrected to
  live reality (below). Inbox untouched.

## (a) findings — live verification, 2026-07-14T10:1xZ (Q-0120)

- **#345 anomaly — verdict: class (i), conflicted-PR-gets-zero-CI (the
  #340 lesson) + a never-was-green heartbeat line.** Verbatim evidence:
  - `pull_request_read get` #345: `"state":"open"`, `"draft":false`,
    `"labels":["do-not-automerge"]`, `"mergeable_state":"dirty"`, head
    `a5d86a3b1937f3d75f1c5b0e1b1faf91424e5d59` (committed
    2026-07-13T23:27:38Z), `updated_at 2026-07-13T23:27:41Z`.
  - `get_check_runs` on the head: `{"total_count":0,"check_runs":[]}`;
    combined status: `{"state":"pending","total_count":0}`.
  - Actions run list for `claude/regen-lag-checker` (fresher than MCP PR
    reads): 3 runs total, ALL on FIRST commit `554d732` — CI run
    29292250141 `conclusion:"failure"` (the designed born-red hold,
    23:11:03Z), auto-merge-enabler success, auto-merge-disarm success
    (23:26:30Z, the label add). **No run of any workflow ever executed on
    the final head `a5d86a3`.**
  - `git merge-tree --write-tree 4e09862 a5d86a3` (main at push time) →
    exit 1, `CONFLICT (content)` in `.substrate/guard-fires.jsonl` +
    `control/status.md` — already conflicted when pushed, so GitHub never
    built `refs/pull/345/merge` and never dispatched pull_request CI.
    Vs today's main `86d8ac7`: adds `CHANGELOG.md` to the conflict set.
  - The heartbeat's "green" (status.md @ 4a23d7c) traces to the #345
    session's local verification + its card's "parked green" line; it was
    never true on GitHub for `a5d86a3`. Not class (ii): no required-check
    "expected" contexts sit on the head — there are simply zero runs.
- **#317 park state — confirmed with one divergence.** Open, non-draft,
  `"labels":["do-not-automerge"]`, head
  `df7b32418371f780752fa31a39d1ad12356ee923`; check runs at head:
  kit-quality `success` · Kit test suite `success` · Cold-adoption smoke
  `success` · enable-auto-merge `skipped` (consistent with not-armed; the
  `auto_merge` field itself is unreadable agent-side — known B-6 MCP
  omission). **Divergence:** `"mergeable_state":"dirty"` — merge-tree vs
  `86d8ac7` conflicts in `dist/bootstrap.py` + `docs/ideas/README.md`;
  the owner-click landing now needs a freshen first. Heartbeat corrected.
- **Rails held:** zero writes to #317/#345 (no pushes, labels, arms,
  comments).

## Verify (local, pre-push)

- `python3 -m pytest` → **1523 passed, 1 skipped** (baseline unchanged —
  docs/control-only PR).
- `python3 scripts/preflight.py` → OK — 7 leg(s) green.
- `python3 dist/bootstrap.py check --strict` → green after this flip
  commit (born-red hold cleared by it).
  (Verbatim lines in the PR/final report.)

💡 Session idea: **parked-PR liveness advisory in `check` / seat-digest** —
a full-lane advisory that parses the heartbeat's `## Parked` lines for PR
numbers and cross-checks each against live git truth (`git ls-remote` +
merge-tree against origin/main, no API needed): a parked PR whose branch
has become merge-conflicted, or whose recorded "green" head no longer
matches the branch tip, gets a loud `parked-drift` advisory. Both #317 and
#345 silently rotted from "green, owner-click" to "dirty, needs freshen"
overnight while the heartbeat kept asserting click-readiness — the exact
class this session had to correct by hand. Dedup: no docs/ideas/ entry
covers parked-state liveness (engagement-wiring-strength-verification is
about doc wiring, not PR parks; order-claim-cross-branch-collision is
claim-time, not park-time).

⟲ Previous-session review: the EAP-audit session (#366,
`.sessions/2026-07-14-eap-audit.md`) set a high evidence bar — measured
totals with honest "not measured" rows, 20 walls with verbatim denials,
and it corrected a status.md drift it spotted in passing (the #365 line).
One miss with a concrete lesson: its audit recorded #317/#345 as parks and
even measured "worst-5 all owner-ratification parks", but did not re-probe
their *mergeability* — three hours later this session found both dirty and
one never-CI'd, so the owner-facing "click #317" instruction it left
standing was already stale at publication. Concrete workflow improvement:
any close-out that hands the owner a click list should live-verify
`mergeable_state` on every PR it names in the same session (cheap: one MCP
get per PR, or local merge-tree) — folded into this session's 💡 idea as a
permanent advisory so the check stops depending on session diligence.
