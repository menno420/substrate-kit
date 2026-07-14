# substrate-kit — fleet cleanup audit (2026-07-13, EAP final night)

> **Status:** `audit`
>
> External, read-only audit pass by a fleet-cleanup subagent — complementary
> to the owner's live "ORDER 045" fleet dispatch happening the same night in
> a separate coordinator chat. This is **not** a self-review from the
> resident coordinator seat; it is an outside verification pass. Scope:
> repo health, doc/CI quality, open-PR disposition. No control-bus files
> (`control/inbox.md`, `control/status.md`) were touched by this audit.

## Headline finding: this repo is live right now, not stale

The audit brief this pass started from described a "STALE heartbeat ~5h27m
old" and "only 1 open PR (#317)". Both were true of `control/status.md`'s
self-reported `updated:` field (`2026-07-13T16:03Z`) but **not of the live
repository state** at audit time (~2026-07-13T23:10–23:25Z):

- `git log` on `main` shows a commit at `2026-07-13T23:14:21Z` (PR #344,
  "ORDER 019 item 4"), roughly 5–10 minutes before this audit began, with a
  continuous chain of merges through the evening: #334 (14:49Z) → #335
  (15:22Z) → #336 (15:55Z) → #337 (16:04Z, the heartbeat's own last refresh)
  → #338 (22:16:57Z) → #339 (22:38:10Z) → #341 (22:44:53Z) → #342
  (23:00:25Z) → #343 (22:55:03Z) → #344 (23:14:21Z).
- Three PRs were open at audit time, not one: **#317** (as briefed),
  **#340** ("Port fm ORDER 025 writeups", opened 22:37:13Z, **still being
  pushed to at 23:23:28Z** — `mergeable_state: dirty`, 5 commits), and
  **#345** ("Add staged-artifact regen-lag checker", opened 23:11:00Z — 8–14
  minutes before this audit's PR check, `mergeable_state: blocked`,
  `kit-quality`/`Kit test suite`/`Cold-adoption smoke` all **failing** as of
  23:11:39–44Z).

This is a live coordinator seat mid-way through the owner's ORDER 019
EAP-final-night worklist (`control/inbox.md` lines 164–219), working the
7-item list top-down inside the same ~1-hour window this audit ran in.
**Conclusion: ACTIVE, hands-off.** Per the audit's own safety rules (never
touch a PR created/updated in the last 2–3 hours), all three open PRs were
left completely untouched — including the two that are not the
explicitly-named #317. #345 being red is very likely a normal
in-progress state for a born-red session card that the resident seat will
fix forward in the same session, not a signal requiring outside
intervention.

**Actionable note for the fleet manager:** the heartbeat's staleness (7+
hours since its own `updated:` line, despite ~10 fresh commits since) is
itself evidence for `docs/ideas/heartbeat-verb-2026-07-09.md` — a
"`bootstrap heartbeat` mechanical status writer" — which ORDER 019 item 7
already lists as this seat's own backlog item. No new idea filed; this
audit corroborates the existing one with a fresh data point.

## What the repo is

`substrate-kit` (placeholder name; the published name is an owner call at
extraction time, `pyproject.toml`) is a portable, stdlib-only "agent-memory
substrate": a bootstrap script (`dist/bootstrap.py`) that plants and
maintains the binding docs, session-log discipline, idea lifecycle,
question router, doc-hygiene checkers, and Claude Code hook/skill scaffolding
that let AI coding agents work correctly across a repo with minimal human
steering. It was extracted from the `menno420/superbot` project's own agent
workflow and is now the fleet's **substrate coordinator** — the source of
the doctrine templates (`CONSTITUTION.md.tmpl`, `collaboration-model.md.tmpl`,
`question-router.md.tmpl`, etc.) that other fleet repos (superbot included,
per its own `CLAUDE.md` §"Understand-and-reflect", provenance Q-0254) adopt
and graduate from. It is also "consumer #0" of its own kit (dogfooding).

## Structure

```
dist/bootstrap.py       THE distribution — one stdlib-only self-contained file
src/build_bootstrap.py  manifest -> artifact builder (regenerate after edits)
src/engine/             source of truth: lib, interview, loop, economy,
                         checks (17 checkers), hooks, stances, skills,
                         agents, ledger, adopt, contextpack, render, cli
src/engine/templates/   16 content templates the ADOPT_PLAN plants
tests/                  1284 tests (in-repo; substrate_kit/ path historical)
bench/                  benchmark rubric + append-only results (KF-5/B1 program)
control/                inbox.md (manager-written orders) / status.md
                         (coordinator heartbeat) / outbox.md (lane→manager) /
                         claims/ (per-session lane claims)
docs/                   architecture.md, ownership.md, runtime_contracts.md,
                         collaboration-model.md, current-state.md,
                         decisions.md, question-router.md, ideas/ (40 files),
                         program/rulings.md (PL-register), reports/, retro/,
                         planning/, succession/, gen2/
telemetry/               guard-fire + model-usage JSONL
.substrate/              staged .claude/ material, hook templates, CI example
```

## CI setup and health

Single required check `kit-quality` (`.github/workflows/ci.yml`) on Python
3.10, plus a "control-only fast lane" that short-circuits heartbeat/inbox
commits to green without running the heavy suite (so coordination traffic
never burns Actions minutes or blocks on an unrelated build), gated by its
own control-status + inbox-append-only sub-checks. Two `legacy-alias-*` jobs
exist purely because the branch ruleset still names the pre-consolidation
job names (`docs/current-state.md` 👤 P10 — still an open owner action as of
this audit; verified live via `pull_request_read` that #317's checks report
under the modern `kit-quality` name, so the alias jobs are dead weight
pending that one owner click). Two more workflows: `auto-merge-enabler.yml`
(arms native auto-merge on non-draft, non-`do-not-automerge` PRs) and
`auto-merge-disarm.yml`.

Local verification run during this audit (Python 3.11.15 — no 3.10
interpreter available in this sandbox; CI itself pins 3.10, so this is a
best-effort local mirror, not a byte-identical CI replay):

| Check | Result |
|---|---|
| `python3 -m pytest tests/ -q` | **1284 passed**, 26.4s |
| `python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py` | clean, no diff |
| `python3 -m ruff check src/engine/` | all checks passed |
| `python3 scripts/check_idea_index.py` | OK |
| `python3 scripts/check_program_law.py` | OK |
| `python3 dist/bootstrap.py check --strict` | all checks passed (one advisory NOTE, see below) |

The one NOTE: `check --strict` reports `preflight script scripts/preflight.py
not found — skipped (config preflight_scripts; plant one to converge the
local ritual and the CI gate on one check list)`. This is the kit's own
`substrate.config.json` not setting `preflight_scripts` — by design here,
since this repo's CI runs `check_idea_index.py` / `check_program_law.py` /
`check_bench_integrity.py` as discrete workflow steps rather than through
the generic preflight hook the kit ships for adopters. It is advisory-only
(never exit-affecting) and does not indicate a real gap; ORDER 019 item 3
(`control/inbox.md` "ASK 002") already closed the adopter-facing half of
this convergence question as a no-op in PR #343 ("already satisfied by
#332"), evidenced live in this same audit's commit-log read.

Actions run history returned by the MCP `list_workflow_runs` tool during
this audit was truncated/stale at `2026-07-12T20:38:00Z` regardless of the
`per_page`/`branch`/`event` filters passed (`total_count: 187`, but only 30
runs returned, none newer than 07-12) — this looks like an MCP-side
listing/caching quirk, not a real CI gap: the git history's continuous
chain of auto-merged PRs through 23:14Z on 07-13 is only possible if
`kit-quality` was green on each of those heads (auto-merge requires it).
Flagging for whoever next debugs Actions-API tooling in this fleet, not
treating it as a finding about the repo itself.

## Doc quality

Documentation is unusually disciplined for a fast-moving repo, enforced
by its own tooling rather than convention alone: `check_docs.py`
(badges/links/reachability), `check_idea_index.py` (idea-lifecycle
frontmatter + backlog completeness — 40 idea files under `docs/ideas/`,
39 indexed in `README.md`, consistent with the checker's own passing
verdict), `check_program_law.py` (the `[PL-NNN]` register + owner-gate label
enforcement), `check_skill_grounds.py` / `test_template_pointer_guard.py` /
`test_skill_pointer_guard.py` (dead-pointer guards added tonight, PRs
#334/#335/#336 — verified in `check --strict` NOTE-free), and
`check_status_current.py` (heartbeat staleness — evidently not wired to
fail loudly enough to have caught the 7-hour-stale `updated:` line noted
above, since `check --strict` passed clean with that same stale timestamp
present; worth a look by the resident lane, see suggestions).

`docs/current-state.md` self-labels as a "dated snapshot" (2026-07-09
baseline, later sections dated through 2026-07-13) and explicitly instructs
readers to verify against source/merged-PRs — an honest, low-risk pattern
that avoids the more common failure mode of a status doc silently going
stale and being trusted anyway.

## Open PRs — disposition

| PR | Title | State at audit | Action taken |
|---|---|---|---|
| #317 | Graduate autonomy rider (Q-0271) + reading-path (Q-0272) into templates | `do-not-automerge` label, all checks green, opened 2026-07-13T01:31Z, last updated 20:15Z | **Left untouched** — explicitly named program-law ratification gate; never arm/close/rebase per repo's own doctrine and this audit's brief. |
| #340 | Port fm ORDER 025 writeups into bench docs | opened 22:37:13Z, **still being pushed at 23:23:28Z** (5 commits), `mergeable_state: dirty` | **Left untouched** — updated inside the audit's own run window; unambiguously live work. |
| #345 | Add staged-artifact regen-lag checker | opened 23:11:00Z (8–14 min before audit check), all 3 substantive checks **failing**, `mergeable_state: blocked` | **Left untouched** — opened inside the audit's own run window; red state is consistent with a born-red card mid-fix, not a stale abandoned failure. |

No PR was merged, closed, or modified by this audit. Nothing met the "not
active + genuinely superseded/red" bar this audit's rules require before
even considering action — every open PR was disqualified by the recency
rule alone.

## Inconsistencies / errors noticed

1. **Heartbeat staleness vs. real activity** (see headline finding above):
   `control/status.md` `updated: 2026-07-13T16:03Z` is ~7 hours stale
   against a repo that has merged 6 PRs and pushed to 2 more since. This is
   the exact class the resident seat's own ORDER 019 item 7
   ("`bootstrap heartbeat` mechanical status writer",
   `docs/ideas/heartbeat-verb-2026-07-09.md`) is meant to fix — this audit
   is independent corroborating evidence, not a new finding.
2. **`substrate.config.json` `kit_version: "1.0.0"`** vs. the shipping
   `KIT_VERSION = "1.15.0"` in `src/engine/lib/config.py` / `pyproject.toml`
   `version = "1.15.0"`. This is already known and documented as the
   deliberate owner-held pin ("kit-self DRIFT row … the designed
   owner-held pin path — do-not-automerge territory", `control/outbox.md`
   "2026-07-13 · DRIFT-row classification" entry) — confirmed still
   present and still intentional at audit time, not a new drift.
3. **Two dead `legacy-alias-*` CI jobs** (`ci.yml` lines 274–312) remain
   because `docs/current-state.md` 👤 P10 (swap the branch ruleset's
   required-check names from the two legacy job names to `kit-quality`) is
   still an open owner-only action — verified live: #317's check runs
   report as `kit-quality` (modern name), confirming the ruleset itself,
   not the workflow, is what's out of sync. Every PR in this fleet pays a
   small tax running two no-op alias jobs until that one settings click
   happens; this is a portal action only the owner can take (`docs/
   current-state.md` names the exact click path already).
4. **`list_workflow_runs` (GitHub MCP tool) returned stale/truncated data**
   during this audit regardless of `per_page`/`branch`/`event` filters (see
   CI section) — a tooling observation, not a repo defect, but worth a note
   for whoever relies on that tool for Actions history elsewhere in the
   fleet tonight.

No other structural, doc-link, or config inconsistency was found; `check
--strict`, the full pytest suite, ruff, the idea-index checker, and the
program-law checker all passed clean locally at audit time (SHA `6de4494`
on `main`).

## Suggestions

1. **Ship the mechanical heartbeat writer** (`docs/ideas/
   heartbeat-verb-2026-07-09.md`, already an ORDER 019 item on this seat's
   own list) — this audit is a second, independent data point that
   heartbeat staleness is a recurring, self-inflicted false signal across
   the fleet (the same pattern is visible in the outbox's DRIFT-row
   classification entry for `fleet-manager` and `superbot-games`). A
   `bootstrap heartbeat` command that stamps `updated:` mechanically at
   session close, rather than relying on hand-maintained prose, would be
   worth graduating into the kit template set specifically because this
   *is* the kit repo — fixing it here is the highest-leverage place to fix
   it fleet-wide.
2. **Land 👤 P10 (required-check ruleset swap)** — a single owner portal
   click (`docs/current-state.md` § "Pending owner action — 👤 P10") that
   deletes the two dead alias jobs and removes a small but permanent CI tax
   from every PR in this repo. Cited three separate times across the
   repo's own docs as still-open; this audit adds one more independent
   confirmation it is still open at `main@6de4494`.
3. **Consider a lightweight "live session" signal on `control/status.md`**
   readable by outside audits/agents without needing to cross-reference git
   log timestamps — e.g. a `last_commit_at:` field auto-stamped alongside
   `updated:`, or explicit `session: live | idle` state. This audit had to
   reconstruct liveness from `git log` + PR `updated_at` + check-run
   timestamps because the heartbeat file itself (the doc built for exactly
   this purpose) was silently wrong. This generalizes suggestion 1: the fix
   is the same mechanism, but framed as a fleet-wide interoperability
   contract (any outside agent auditing any fleet repo should be able to
   trust `control/status.md`'s own `updated:` field as ground truth for
   "is someone in here right now").
4. **Centralize-across-fleet candidate: the born-red / recency-aware PR
   safety rule this audit itself was given.** The rule "never touch a PR
   created or updated in the last 2–3 hours" is exactly the shape of
   protection this repo's own `check_session_gate` / born-red-card
   convention (`docs/current-state.md` § "Review rhythm") already encodes
   server-side for *this* repo's own agents. An outside-agent-facing
   version of the same signal (e.g., a `fleet-audit-safe: true|false` label
   or a documented "PR age < N hours" convention referenced from
   `control/README.md`) would let future cross-repo audits verify liveness
   from PR metadata alone, without needing bespoke git-log archaeology per
   repo — worth raising with the fleet manager as a `control/README.md`
   protocol addition, applicable to all ~20 fleet repos, not just this one.

## Evidence index

- Commits cited: `6de4494` (HEAD at audit start), `4e09862`, `5354786`,
  `08de140`, `c90494b`, `fdeb439`, `736e114`.
- PRs cited: #317, #334, #335, #336, #337, #338, #339, #340, #341, #342,
  #343, #344, #345.
- Files read: `README.md`, `CONSTITUTION.md`, `control/status.md`,
  `control/inbox.md`, `control/outbox.md`, `docs/current-state.md`,
  `docs/AGENT_ORIENTATION.md`, `.session-journal.md`, `substrate.config.json`,
  `pyproject.toml`, `.github/workflows/ci.yml`, `docs/adopters.md`,
  `.sessions/2026-07-13-si-coordinator-close.md`.
- Local checks run at SHA `6de4494`: `pytest tests/ -q`,
  `src/build_bootstrap.py` + `git diff --exit-code dist/bootstrap.py`,
  `ruff check src/engine/`, `scripts/check_idea_index.py`,
  `scripts/check_program_law.py`, `dist/bootstrap.py check --strict`.
