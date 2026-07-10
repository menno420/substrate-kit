# Next boot — first 10 minutes for the gen-2 kit-lab session (2026-07-09)

> **Status:** `owner-guidance` — the succession doc a FRESH gen-2 kit-lab
> session boots from, written at the gen-1 wind-down (kit-lab lane, phase 2,
> PR #74). Companions in this directory:
> [queue-state.md](queue-state.md) · [custom-instructions-proposal.md](custom-instructions-proposal.md)
> · [environment-setup.md](environment-setup.md) + [setup.sh](setup.sh) ·
> [feedback-for-gen2-blueprint.md](feedback-for-gen2-blueprint.md).
> Capstone retro:
> [../retro/project-review-2026-07-09-gen1-winddown.md](../retro/project-review-2026-07-09-gen1-winddown.md).
> The sibling (SuperBot coordinator) lane's pack is
> [../succession/](../succession/README.md) — same protocol, different lane.

## 0. Resume here — 2026-07-10 close-out handoff

> Added at the gen-2 close-out (kit-lab lane, session
> `.sessions/2026-07-10-gen2-close-out.md`). Source: coordinator-lane
> handoff, 2026-07-10. The companion resume-points list from the sibling
> close-out lives in [queue-state.md](queue-state.md) (PR #122); this
> section carries the build priorities and the non-derivable context.

**Resume priorities, in order:**

1. **SessionStart handoff-push idea** — top buildable. Targets run-4's
   M2/M3 loss (the auto-drafted card was never opened; OFF's plain-README
   convention beat the kit at its own continuity game — see the run-4 row
   and `.sessions/2026-07-10-b1-run-4.md`).
2. **T5 guard-probe redesign — RE-SCOPE FIRST.** Live hooks in run-4
   partially resolve its premise (the guard FIRED in run-4; the probe's
   original "zero evidence" gap is half-closed). It touches a pin path
   (`bench/tasks/T5.md`), so whatever ships must be a **daytime
   `do-not-automerge` PR for owner ratification** — never auto-merged.
3. **Model-identity capture automation** — partially superseded; check
   what already ships (telemetry model line, card 📊 Model convention)
   before building anything.

**Non-derivable context (would otherwise be lost with the chat):**

- **Adopter v1.7.0 upgrades belong to consumer lanes (KF-2)** — the lab
  never writes to consumer repos; do not "helpfully" open upgrade PRs on
  websites/trading-strategy/games from here.
- **B1 run-5 should WAIT for the F-5 ruling** (⚑ OWNER-ACTION 1, HOT — it
  decides how runs 2–3 read and with them the trend headline).
- **The coordinator hourly wake routine is ARMED and RECURRING** (trigger
  `trig_01FnqnAQjLU2T8d16iHwWQ2h`, cron `0 * * * *`, bound to the kit-lab
  coordinator session — ORDER 010 RECORD in `control/status.md`), so the
  next wake is guaranteed. **Independently verified from this close-out
  session's own surface** via `list_triggers`: at 13:52Z *and again at
  14:09Z* the trigger read `enabled=true`, `updated_at` == `created_at`
  (2026-07-10T01:56:06Z — never modified since creation), with observed
  fires at 13:09:18Z and 14:08:17Z and `next_run_at` 15:06:33Z. This
  **contradicts** the "ROUTINE STATE: NOT ARMED / externally stopped
  12:54Z" line the #122 heartbeat recorded from a coordinator relay — two
  observed fires post-date the alleged stop. If you read a NOT-ARMED
  claim anywhere, re-verify with `list_triggers` before believing it.

## 1. First-10-minutes read order (this exact sequence)

1. **This file** — the map; everything else is one hop away.
2. **`control/README.md`** — the fleet protocol you operate under: inbox
   first / status last, one writer per file, the ORDER 007 claim-first
   ritual, the OWNER-ACTION six-field format. Non-negotiable.
3. **`control/inbox.md`** — any `new` order outranks your plans. Note:
   headers stay `status: new` until the MANAGER flips them — diff the inbox
   against status `done=`, never re-execute on `new` alone.
4. **`control/status.md`** — the last heartbeat: phase, blockers, the ⚑
   OWNER-ACTION items (renumbered after the owner's 2026-07-10 #26/#49
   clicks resolved the original items 1–2; **12 items as of the 2026-07-10
   close** — item 11 = enable "automatically update branches", item 12 =
   route the websites ORDER 005 fleet relay, added by #122; the list in
   control/status.md at HEAD is always the truth, ordinals here rot). You
   are its sole writer; overwrite it as your deliberate LAST act.
5. **`docs/CAPABILITIES.md`** — verified walls + THE DISCOVERY RULE.
   Probing a documented wall twice is a bug; declaring an unverified wall
   is a worse one.
6. **`docs/gen2/queue-state.md`** — done / in-flight / next for the whole
   program, committed at wind-down and **reconciled 2026-07-10 (night-cap
   pass)**: 9 of 12 agent-queue items done with verified PR numbers; the
   remainder carry their exact gates. Treat as handoff truth; live GitHub
   wins as time passes.
7. **`docs/current-state.md`** — the living ledger (stability baseline,
   incident ledger, owner gates). Read the **Field notes — incident
   ledger** before trusting merge history: merged ≠ ratified for
   `do-not-automerge`-class PRs (the #22 lesson).
8. **Newest `.sessions/` card** (`ls -t .sessions/ | head`) — what the last
   session actually did and flagged.
9. **`docs/retro/project-review-2026-07-09-gen1-winddown.md`** — the gen-1
   capstone: every friction class you must not re-pay, with exact texts.
10. **`CHANGELOG.md`** (top two sections) — the live release (v1.6.0 at
    wind-down) and what rode it.

## 2. Walking-skeleton check — BEFORE any real work

Prove branch → PR → CI → auto-merge with a trivial control-only commit
BEFORE the first real deliverable:

1. Branch off main; make a control-only touch (or a one-line docs change);
   commit; push.
2. Open the PR **READY, never draft** via MCP `create_pull_request`, then
   **arm auto-merge yourself** with `enable_pr_auto_merge` — MCP-created
   PRs do NOT fire the enabler workflow (gen-1 proved this repeatedly;
   phase-1's #72 merged in ~21 s on the control fast lane this way).
3. Watch it merge on green. If any required check sits "Expected"/queued
   >10 min, the ruleset still names a context no job reports (the P10
   class) — cure with MCP `rerun_failed_jobs` on the stuck run, and flag
   P10 to the owner before relying on auto-merge.

A session's REAL first PR opens born-red: the `.sessions/` card with
`> **Status:** \`in-progress\`` is the first commit, and flipping it to
`complete` is the last (the session gate in `kit-quality` holds the merge
until then).

## 3. KNOWN WALLS — exact error text (verbatim; check `docs/CAPABILITIES.md` for updates)

- **Direct push to main is ruleset-blocked:**

  ```
  GH013: Repository rule violations found ... Changes must be made through a pull request. 2 of 2 required status checks are expected.
  ```

  Everything rides PRs; heartbeats ride the control fast lane (~7–30 s CI).

- **Tag pushes 403 through the git proxy** (live-hit at v1.0.0) — the ONLY
  agent-runnable release path is the `release.yml` `workflow_dispatch` run
  with the `version` input (creates the tag in-Actions, publishes the 3
  assets; proven on all 7 gen-1 releases).
- **Branch deletion is blocked on EVERY agent path:** `git push --delete`
  403; REST DELETE `/git/refs/*` returns

  ```
  Write access to this GitHub API path is not permitted through this proxy
  ```

  GraphQL `deleteRef` is not enabled; the GitHub MCP has no delete-branch
  (and no create-release) tool. Owner cleans branches (⚑ OWNER-ACTION 10
  in the `control/status.md` list as of the 2026-07-10 close — was 7 when
  this doc was written; verify the ordinal against status.md at HEAD).
- **Owner-gated merges are refused on relayed consent** — the auto-mode
  permission classifier denied #17's merge until the owner typed
  "merge 17" live in-session, and denied a worker-spawn containing
  "merge #26" the same way. A relayed "the owner said yes" never clears
  it; only an in-session owner message or the owner's own UI click does.
  Shape such work as "PR open, READY, CI green, ⚑ owner one-click".
- **API-authored PRs may not trigger CI/workflows** — the manager's
  Contents-API PR #27 carried 0 CI runs; MCP-opened PRs don't fire the
  auto-merge-enabler workflow. Always arm auto-merge yourself
  (`enable_pr_auto_merge`); if CI never starts, close/reopen or push a
  real commit.
- **Cross-session messaging: assume absent.** Recorded org-wide wall:

  ```
  send_message: tool is not enabled for this organization
  ```

  In the wind-down environment the tool did not exist at all; the one
  attempt via the harness SendMessage returned:

  ```
  No agent named 'cse_0184Aa1jZ8FvSYAvzSXP5yFU' is reachable.
  ```

  The git bus (committed `control/` files on main) is the designed
  fallback — it never failed in gen-1.
- **Cross-repo reads are allowlisted per session:**

  ```
  Access denied: repository "menno420/fleet-manager" is not configured for this session. Allowed repositories: menno420/superbot-next, menno420/websites, menno420/substrate-kit, menno420/superbot, menno420/trading-strategy
  ```

  **Workaround discovered at wind-down:** the `add_repo` session tool +
  `git clone --depth 1` reached fleet-manager (public repo) and read
  `docs/gen2-blueprint.md` in full — try `list_repos`/`add_repo` before
  declaring a repo unreachable (`docs/CAPABILITIES.md` append log,
  2026-07-09).
- **Runner-queue stalls on the legacy alias contexts** — "Kit test suite"
  and "Cold-adoption smoke (adopt + check --strict)" queue-stalled ~35 min
  twice in gen-1 (~70 min lost). Cure: GitHub MCP
  `actions_run_trigger` method `rerun_failed_jobs` on the stuck run. Root
  cause is P10 (owner swaps the required contexts to `kit-quality`);
  post-P10, delete the two `legacy-alias-*` jobs from `ci.yml`.
- **`api.github.com` direct HTTP is blocked** — GitHub access is
  MCP-tools-only. GraphQL quota is tight; prefer REST-backed MCP tools for
  bulk reads. `enable_pr_auto_merge` rate-limited once in gen-1 — one
  retry cleared it.
- **A non-zero setup-script exit kills the session at provisioning** (the
  PR #47 casualty):

  ```
  fatal: not a git repository (or any of the parent directories): .git
  ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
  ```

  The tested defensive script is [setup.sh](setup.sh) (owner pastes it —
  ⚑ OWNER-ACTION 8 in the `control/status.md` list as of the 2026-07-10
  close — was 9 when this doc was written; verify against status.md at
  HEAD). Also: a
  fresh container has NO pytest
  (`/usr/local/bin/python3: No module named pytest`) — `pip install
  pytest ruff` before running the suite.

## 4. Standing law and facts (do not re-litigate)

- **Pin paths** (`bench/rubric/`, `bench/tasks/`, `bench/seeds/`): the lab
  NEVER merges its own change to the oracle — such PRs carry
  `do-not-automerge` from creation and wait for the owner
  (`scripts/check_bench_integrity.py`). `bench/results/` is append-only,
  history immutable.
- **KF-5**: every release states the benchmark outcome; **KF-8**: no trend
  claim below 3 rows — the threshold was MET 2026-07-10 (run-3 recorded
  via PR #85, family at 3 rows, first trend statement on record in
  `control/status.md` + CHANGELOG; both run-2 and run-3 strict-F-5 FAILs
  stay DISPUTED pending the owner's F-5 A/B ruling).
- **Recorder ≠ judge**: bench rows are the independent judge's verbatim
  verdict, even when unflattering (run-2's strict FAIL is the precedent).
- **One writer per file** on the control bus; never edit `control/inbox.md`.
- **Timestamps only from `date -u`** — gen-1's fleet sweep caught lanes
  stamping local-time-as-Z.
- **The kit never writes to consumer repos (KF-2)** — adopter evidence
  arrives relayed (inbox orders, committed docs, heartbeats).
- **Verification commands**: `python3 -m pytest tests/ -q` (722 green at
  wind-down) · `python3 dist/bootstrap.py check --strict` · dist byte-pin:
  `python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py`.
- **Owner-gated PRs #26 (PL-011) and #49 (seed fix) are MERGED** — the
  owner one-clicked both ~2026-07-10T00:08–00:12Z (drift fixed by the B1
  run-3 session, which verified the merge commits on main; this bullet
  previously described them as open-by-design blockers). PL-011 is ratified
  law and B1 run-3 fired the same night (row 3 + run dir via PR #85). The
  general rule stands for any FUTURE `do-not-automerge` PR: READY, CI
  green, never rebase/update-branch it, terminal state is the owner's click.
