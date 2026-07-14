# EAP project audit — substrate-kit close-out (2026-07-14)

> **Status:** `audit`
>
> Owner-directed EAP close-out audit, written 2026-07-14T08:55Z at
> origin/main `f856ce3` (session PR #366, branch `claude/eap-audit`).
> Definitive record of the EAP program on this repo: measured totals,
> tooling verdicts, verified walls with verbatim denials, friction
> measurements, and a disposition for every finding —
> **FLEET-FIX** (we/the owner fix it, how stated) ·
> **ANTHROPIC** (exact paste-ready ask) · **ACCEPTED** (documented
> wall with a working path). Truth bar: path@SHA / PR # / verbatim
> quotes / dates; "not measured" beats invention.
>
> Complements — never restates — the external
> [2026-07-13 fleet-cleanup audit](../reports/2026-07-13-fleet-cleanup-audit.md);
> the delta is at the end of §1.

## 1. Identity & scale

| Dimension | Measured value |
|---|---|
| Repo / seat | `menno420/substrate-kit` — the fleet's substrate coordinator ("Self Improvement" seat), consumer #0 of its own kit |
| Active window | 2026-07-08 → 2026-07-14 (first commit `fae482a` 2026-07-08T13:20:22+02:00; PR #1 opened 2026-07-08T16:11:55Z) |
| Sessions | **191 session cards** in `.sessions/` (2026-07-09 → 2026-07-14; day 1 predates the card convention) ≈ 32 sessions/day |
| PRs | **361 opened · 350 merged · 8 closed-unmerged** (#30 #53 #56 #57 #62 #226 #293 #363) **· 3 open** (#317, #345 — owner-ratification parks; #366 — this audit's own born-red PR, excluded from all friction stats) |
| Commits | **452** on origin/main at `f856ce3` (2026-07-14T08:29:18Z) |
| Releases | **19 tags, v1.0.0 → v1.15.0** (16 minor lines + 3 patches, all inside the 6-day window) |
| Ideas backlog | **42 idea files**: state 23 promoted / 16 captured / 3 historical; outcome 25 shipped / 17 open |
| Test suite | 442 passed (2026-07-09, PR #6) → **1523 passed** (2026-07-14, PR #365) |

**Delta vs the [2026-07-13 fleet-cleanup audit](../reports/2026-07-13-fleet-cleanup-audit.md)**
(external read-only pass at `main@6de4494`, merged as PR #347 / `cff76fd`) — what changed since it, not what it said:
ORDER 019 completed + the #348–#359 backlog conveyor + ORDER 020 (#362) + the
cross-branch ORDER-collision guard (#364/#365); suite 1284 → 1523; its
suggestion 1 (mechanical heartbeat writer) already shipped as `bootstrap
heartbeat` (PR #346); the fresh-session-cron question it could not see is now
settled (first proven scheduled delivery 2026-07-13T06:10Z, §5); #317/#345
still parked and 👤 P10 still open (§9); its liveness-visibility theme now
extends to *concurrent inside* fires (the #362/#363 twin-build, §7).

## 2. Tooling used

Verdicts derived from `docs/CAPABILITIES.md`, `.sessions/` cards, and
`docs/retro/` at `f856ce3` — not vibes.

| Tool / surface | How this seat used it | Verdict | Citation |
|---|---|---|---|
| GitHub MCP — writes (`create_pull_request`, `enable_pr_auto_merge`, workflow dispatch) | Every session PR opened via MCP or branch push; release cutting via workflow dispatch ("HTTP 204, no auto-mode/classifier/403 wall") | **reliable** | `docs/CAPABILITIES.md` 2026-07-10 (v1.7.0 cut, run 29074386841); `.sessions/2026-07-09-audit-followups.md` (PR #24 "opened born-red READY via MCP") |
| GitHub MCP — reads (`pull_request_read`, `get_job_logs`, Actions runs) | PR-state triage, `mergeable_state` stall diagnosis, job-log truth for red-pings | **flaky** — usable, but three verified read defects: ~25-min-stale PR state, `auto_merge` field omitted, quota exhaustion (§3 B-5/B-6/B-12) | `docs/CAPABILITIES.md` PR #107 entry; job 86578536297 "HOLD (by design)… nothing to investigate" (`.sessions/2026-07-11-archive-prep-close-out.md`) |
| git over HTTPS proxy | Branch pushes, fetch/reset preflight, clones — the workhorse | **reliable for branch push/fetch; painful at the edges** (tag push 403, branch delete 403, shallow-graft history lies — B-3/B-4/B-18) | `docs/CAPABILITIES.md` § Capabilities; "`git fetch` never lied" (`docs/retro/wind-down-addendum-2026-07-09-kitlab-coordinator.md`) |
| python3 / pytest | Full suite before every push; local green tracked CI green throughout | **reliable** | `.sessions/2026-07-09-kl1-ci-delta.md`; `.sessions/2026-07-14-verify-release.md` |
| `dist/bootstrap.py` verbs (29 at `f856ce3`: `check --strict`, `currency`, `upgrade`, `adopt`, `render`, `heartbeat`, `claim`, …) | `check --strict` at every session close; `currency` live fleet scan "18.8s, 10 repos"; `upgrade` drove every adopter regen wave | **reliable**, one shipped-and-fixed bug (session-gate flip-race fail-open, sim-lab V051 repro, PR #342) | `.sessions/2026-07-11-currency-private-repo-fix.md`; `.sessions/2026-07-13-session-gate-false-green.md` |
| kit-quality CI workflow | The merge gate: pytest + dist byte-pin + ruff bans + cold-adopt smoke + session gate | **reliable as enforcement; painful as a signal** — designed born-red hold + 2 `legacy-alias-*` mirror jobs read as failures to observers (the W-9 class, §7) | `.sessions/2026-07-13-night-outcomes.md`; `.sessions/2026-07-11-b1-run-5.md` (job 86498086740 root-caused) |
| auto-merge-enabler workflow | Server-side arming of `claude/*` PRs — the standard landing path around the self-arm classifier | **reliable core; three documented stall/race classes**, each with a shipped recipe or fix (§3 B-8, §4) | armed #240/#241 on MCP-created PRs (`.sessions/2026-07-11-archive-prep-close-out.md`); behind-stall fix (`docs/CAPABILITIES.md` PR #106 entry) |
| Scheduled triggers / cron (`create_trigger`, `send_later`, `list_triggers`) | Self-bound hourly/2-hourly wake crons, send_later chains, fresh-session daily lab loop, 1203-record registry forensics | **self-bound cron reliable** (~14 consecutive hourly fires, 0 misses); **send_later mostly reliable but drops silently with no tombstone**; **fresh-session cron flaky** (0-for-2, then first delivery 07-13; §5) | [`docs/reports/2026-07-12-trigger-forensics.md`](../reports/2026-07-12-trigger-forensics.md); `docs/CAPABILITIES.md` 2026-07-13 entry |
| webagent surface | — | **not measured**: zero relevant hits across `docs/CAPABILITIES.md`, `.sessions/`, `docs/retro/` at `f856ce3` | not measured: no ledger evidence in this repo |
| raw.githubusercontent.com / codeload / releases-download (WebFetch itself unevidenced) | Currency scanner's cross-repo tree-truth transport; release-asset verification | **reliable for public repos; ambiguous for private** — a private repo 404s every raw path (pokemon-mod-lab falsely "not adopted"); fixed via raw → API (walled) → codeload-tarball fallback | `.sessions/2026-07-11-currency-private-repo-fix.md`; `.sessions/2026-07-14-verify-release.md` (828825-byte asset sha-verified) |

## 3. Tooling walled or missing

All 20 walls from the EAP ledger. 14 carry verbatim denial text + dates;
rows without it say so. Honest cross-check first: two "known fleet-wide"
walls are **not evidenced in this repo's ledger** — gh CLI absence (B-2)
and the GraphQL `disablePullRequestAutoMerge` race *by that name* (the
evidenced local variant is the enabler-vs-disarm park race, B-8).

| # | Capability wanted | What happened when tried (verbatim + date) | Workaround | Disposition |
|---|---|---|---|---|
| B-1 | Direct `api.github.com` REST | 3 dated hits: 2026-07-09 "direct `api.github.com` is proxy-blocked for this session (403 \"GitHub access is not enabled\"…)" (`.sessions/2026-07-09-kl1-ci-delta.md`); 2026-07-11 "API probe 403"; 2026-07-14 "workflow leg SKIPPED (api.github.com 403…)" (`.sessions/2026-07-14-verify-release.md`) | MCP tools; codeload tarballs; `releases/download/`; scripts SKIP honestly | **ANTHROPIC** — "Allow read-only GETs to api.github.com through the agent proxy for allowlisted repos (at minimum Actions runs/jobs, repo settings/rulesets, PR `auto_merge`) — the MCP toolset has no ruleset read and omits `auto_merge`, so verification scripts currently SKIP legs they could prove." |
| B-2 | gh CLI | **No attempt or denial recorded in this repo's ledger** (the `gh …` strings in two cards are mined runbook prose / Actions-side, not agent executions) | MCP + dispatch recipes | Known fleet-wide only, not evidenced here; low priority |
| B-3 | git tag push / release create | v1.0.0: "Tag push / release create via git: HTTP 403 from the environment's git proxy" (`docs/CAPABILITIES.md` § Walls; `.sessions/2026-07-09-v1.1.0-release.md`) | `release.yml` workflow_dispatch, proven v1.0.0→v1.15.0; mechanized in `scripts/cut_release.py` (PR #356) | **ACCEPTED** — the dispatch path is strictly better (auditable run) |
| B-4 | Branch deletion | 2026-07-09, all 4 paths: classifier denied `git push --delete` + API fallback; proxy attempt HTTP 403; REST "`Write access to this GitHub API path is not permitted through this proxy.`"; GraphQL "`This GraphQL query is not enabled for this session — only the pinned set of PR-review operations is served.`" (`docs/retro/wind-down-addendum-2026-07-09-kitlab-coordinator.md`); re-verified 2026-07-11 (~48 stale branches, ⚑ OA-10) | none agent-side | **FLEET-FIX** — owner one-click: Settings → General → "Automatically delete head branches" (queued as OA-10 since 2026-07-09) |
| B-5 | Fresh GitHub MCP PR-state reads | 2026-07-09: "The MCP served PR state up to ~25 minutes stale once; `git fetch` never lied." (~30 min polling cost, retro project-review row 9) | `git fetch` cross-check — baked into doctrine templates | **ANTHROPIC** — "GitHub MCP PR-state endpoints can serve ~25-minute-stale data (observed 2026-07-09, ~30 min polling cost); shorten/expose the cache TTL or add a freshness timestamp to responses." |
| B-6 | `auto_merge` state readable from MCP | 2026-07-13: "MCP `pull_request_read` GET omits the `auto_merge` field; the issue timeline is unreachable — so the #317 disarm actor … is unprovable from this seat" (`.sessions/2026-07-13-si-coordinator-close.md`) | no-op-disable + `updated_at`-invariance probe | **ANTHROPIC** — "Include the `auto_merge` object (and issue-timeline reads) in pull_request_read responses — parked-PR disarm state is currently unprovable agent-side and is inferred via a no-op-disable side-effect probe." |
| B-7 | Self-arm / self-merge (auto-mode classifier) | 2026-07-10, verbatim: "Permission for this action was denied by the Claude Code auto mode classifier. Reason: [Auto-Mode Bypass] ... enable_pr_auto_merge and a merge_pull_request fallback that would land the PR with no human review — Merge Without Review" (`docs/CAPABILITIES.md`). Inconsistent: 2026-07-13 an own-PR arm on #342 *succeeded* (then voluntarily disarmed) | open READY, do nothing — the enabler arms server-side | **ACCEPTED** for the merge path + **ANTHROPIC** on consistency: "The Merge-Without-Review classifier boundary is inconsistent across session kinds and days (denied 2026-07-10, permitted on own PR 2026-07-13) — document or stabilize the intended rule." |
| B-8 | Parking a PR against the enabler | Post-flip disarm loses to the enabler re-arming on green: #355 "the post-flip disarm lost the race to the enabler arming"; first on #349. The named GraphQL disable race: **not evidenced under that name here** | park BEFORE green: `do-not-automerge` pre-flip, disarm-verified-before-label; [`auto-merge-disarm.yml`](../operations/auto-merge-guards.md) disarms on label-add ~9 s | **ACCEPTED** (doctrine shipped) — and see §4 for the prose-park no-op class |
| B-9 | Foreground `sleep` / self-wake on the coordinator surface | Verbatim (2026-07-10): "`Blocked: standalone sleep 1500. To wait for a condition, use Monitor with an until-loop (e.g. until <check>; do sleep 2; done). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.`" Plus: no `send_later` tool there; Monitor ~30-min cap, kill does NOT re-invoke the parent | blocking worker until-loop ~25 min (~10 consecutive ticks proven) | **ANTHROPIC** — "Give coordinator-surface sessions a scheduled-wake primitive (send_later or equivalent), or make Monitor timeout/kill notify the parent — today a Monitor death is a silent wake loss and the only reliable pattern is a worker slot burning a 25-minute sleep loop." |
| B-10 | `send_later` delivery guarantees | 2026-07-13: "send_later one-shots can drop platform-side and leave NO tombstone — absent from `list_triggers` entirely (0 hits across 1203 records, 13 pages…) … trig_01USg5i3qna4fCX5ZeePg7Gj, armed 01:34Z for 01:49Z, never delivered; failsafe bridged 02:07Z. Also observed: one tick delivered 25 min late." | two-layer wakes (pacemaker + `0 */2` failsafe cron) | **ANTHROPIC** — "A dropped send_later one-shot vanishes from list_triggers with no tombstone (trig_01USg5i3qna4fCX5ZeePg7Gj, 2026-07-13) — persist dropped triggers with an ended_reason so drops are detectable without gap forensics." |
| B-11 | Fresh-session-per-fire cron delivery | 0-for-2 (2026-07-12): one trigger "VANISHED unfired … no tombstone … hard deletion, actor unknown"; replacement "NEVER self-delivered its 06:08:52Z slot … next_run_at STILL frozen"; first proven delivery 2026-07-13T06:10Z (§5) | ride the self-bound failsafe wake (PR #257 stopgap doctrine) | **ANTHROPIC** — "Scheduler delivery/deletion logs are invisible agent-side: a fresh-session cron missed its slot with next_run_at frozen in the past (trig_01Jm57…, 2026-07-12T06:08:52Z) and its predecessor was hard-deleted with no audit entry (trig_01MHwm…) — expose delivery status/deletion audit; also note a manual fire_trigger sets last_fired_at without advancing next_run_at." |
| B-12 | GitHub API quota under fleet load | "`enable_pr_auto_merge` refused with \"API rate limit already exceeded\" while REST calls … worked" (`.sessions/2026-07-10-eap-64-claims.md`); blocked twice on 2026-07-11 | enabler arms server-side regardless; retry; batch reads | **FLEET-FIX** — pace fleet-wide parallel API load; rely on the enabler |
| B-13 | Cross-repo reads (MCP allowlist) | 2026-07-09 verbatim: "`Access denied: repository \"menno420/fleet-manager\" is not configured for this session. Allowed repositories: …`" | `list_repos` + `add_repo` + `git clone --depth 1` (public); else manager inbox relay | **ACCEPTED** |
| B-14 | `send_message` cross-session | "`send_message: tool is not enabled for this organization`" — INTERMITTENT, "recovered by 02:05Z" (`.sessions/2026-07-10-coordinator-closeout.md`) | retry once per incident before treating as standing | **ACCEPTED** |
| B-15 | Repo settings / rulesets from a session | 2026-07-09: no MCP ruleset tool + B-1 wall; merge bounced **405** "\"2 of 2 required status checks are expected\"" — revealed the owner-landed legacy ruleset | temporary `legacy-alias-*` CI jobs (still live — the §7 signal tax); ruleset swap queued 👤 P10 | **FLEET-FIX** (owner: require `kit-quality`, drop the two legacy contexts — long-queued P10) + B-1's ask covers the read half |
| B-16 | Harness Bash allowlist granularity (bench worker seats) | Run-5 OFF-T5 worker denied 5× ("This command requires approval") for `python -m pytest` (spelling outside allowlist); worker correctly refused a relayed fabricated "approval"; run-6: 7 auto-denials, all self-corrected | add both interpreter spellings; prepare-time permission smoke | **FLEET-FIX** — pre-flight exact allowlisted spellings in `run_ab.py prepare` |
| B-17 | Parallel file-mutating subagents in one clone | venture-lab, kit v1.6.0: "one worker's `git add -A` swept the other's uncommitted files into the wrong commit/PR" (`docs/CAPABILITIES.md` 2026-07-10) | worktree-per-worker or serialize; never `git add -A` in a shared clone | **ACCEPTED** (ledgered + succession pack) |
| B-18 | Git history truth on container clones (shallow/graft) | 2026-07-14: "negative git ancestry answers are UNRELIABLE on shallow/grafted clones … live FALSE `merge-base --is-ancestor` negative for v1.15.0's REAL bump commit `eaf4f23`" (PRs #355/#357) | `scripts/_git_truth.py` (`is_shallow()`, `provable_ancestry() -> yes\|no\|unprovable`) since PR #358; checkers SKIP, never false-FAIL | **ACCEPTED** (fixed-ourselves, centralized) |
| B-19 | Cross-container `/tmp` persistence | 2026-07-11: "the ordered copy-source `/tmp/claude/memory/team/kit-coordinator-gen3-lessons.md` DOES NOT EXIST in this container — probed" | the repo is the only durable home | **ACCEPTED** |
| B-20 | Coordinator-spawn identity cross-wire | 2026-07-10: "Fresh coordinator-spawned sessions provision with a venture-lab-pinned system identity … 3 occurrences tonight" (`docs/retro/coordinator-session-2026-07-10.md` §2) | boot deconflict: `git remote -v`, read all `control/status*.md`, sibling check | **ANTHROPIC** — "Fresh sessions spawned from a coordinator can provision with another Project's pinned identity (3× on 2026-07-10) — bind spawned-session identity to the requested project." |

## 4. Merge & landing friction — measured

Across all **350 merged PRs** (full table generated from the GitHub MCP,
state=all, paginated to exhaustion):

- **Median created→merged: 2.9 min · mean: 22.8 min** · p90 19.0 · p99 482.5.
- **298/350 under 15 minutes.** Distribution: <15 min 298 · 15–30 min 31 · 30–60 min 11 · 1–3 h 3 · 3–24 h 5 · >24 h 2.
- **Worst 5 are all deliberate owner-ratification parks, not CI churn:** #220 (27.6 h), #238 (24.3 h, merged 15 s after #220 — owner cleared the queue in one sitting), #26 (12.5 h), #347 (8.0 h, the external audit held overnight), #181 (8.0 h). The pipeline lands in single-digit minutes; outlier cost is owner latency by design. **ACCEPTED**, with a FLEET-FIX rider: a parked-PR staleness advisory (parks rot into the zero-CI/rebase-first shape within hours at this velocity — see #345 below).
- **>1 real CI round, last 30 PRs (#337–#366):** the failure→success shape is the *designed* born-red session-gate pattern, not friction. PRs with ≥2 failures: **#352 and #355 only — 2/29 ≈ 7%**. Not measured for #1–#336 (runs endpoint pages at 30/page; ~20+ pages).

Incident classes:

- **Park-without-label enabler override (#365, #353) — FLEET-FIX.**
  `control/status.md:35` (at `f856ce3`, verbatim): "PR #365 OPEN, parked for
  review-merge (auto-merge deliberately NOT armed)" — yet GitHub records
  `merged_by: github-actions[bot]` at 2026-07-14T08:29:18Z. #353 is the same
  class 7 hours earlier ("**Not self-merging; no auto-merge armed by this
  session.**" in the body; enabler-merged 3.5 min later, unremarked). The
  enabler arms server-side on every non-draft allowlisted PR unless the
  `do-not-automerge` label is present — **prose-parking is a no-op**. Fix:
  park = the label, with disarm-verified-before-label (existing kit-law-gate
  doctrine, [auto-merge-guards.md](../operations/auto-merge-guards.md));
  plus a check-time advisory flagging any status.md "parked/OPEN" claim whose
  PR is actually merged. Compare #317, which parked *correctly*
  (disarm + label + comment).
- **#340 — conflicted-PR zero-CI-runs (invisible-red).** GitHub creates no
  pull_request-event runs for a `dirty` PR → zero runs / pending-0. Twice-
  documented class; self-healed here (conflict resolved, enabler re-armed on
  `synchronize`, merged 51 min). **ACCEPTED** as platform behavior with the
  documented cure (check `mergeable_state` FIRST when a PR shows no CI).
- **#363 — duplicate ORDER build.** Two routine fires consumed the same
  unacked ORDER 020, 25 s apart; #362 won, #363 closed superseded. Guarded
  same day by #364/#365 (`bootstrap claim --order NNN` + refuse-unless-
  `--force` + `claims-order-collision` advisory). **FLEET-FIX shipped** (§7).
- **#342 — self-arm breach.** `enable_pr_auto_merge` called on own PR 8 s
  after creation; self-caught, disarmed within ~65 s, landed via the normal
  enabler path. Remediated <2 min; also a B-7 consistency data point.
- **Owner-click counts on the open parks:** #317 — green at head `df7b324`,
  **1 click** (Merge). #345 — **zero check runs on current head** `a5d86a3`
  (combined status pending-0; base 100+ commits behind), so **2–3 owner
  actions** (update branch / resolve, wait for CI, merge — the label blocks
  auto-merge).
- **HONEST NULL — #341:** no verbatim denial text for the failed arm attempt
  on #341 exists anywhere — not in PR comments, reviews, or repo docs. The
  only record is the #342 session card's paraphrase: "An earlier enable
  attempt on claim PR #341 failed (checks pending) and never armed." The
  "unstable status" verbatim belongs to **fleet-manager PR #10**, per
  [auto-merge-guards.md](../operations/auto-merge-guards.md) lines 117–125,
  not to #341.

## 5. Scheduling & wake friction

Canonical record: [2026-07-12 trigger forensics](../reports/2026-07-12-trigger-forensics.md).

- **Fresh-session cron: 0-for-2, then first proven delivery.** Trigger 1
  (`trig_01MHwmBrA1bziEp49g6xqGt5`) "VANISHED unfired … No tombstone … hard
  deletion, actor unknown". Trigger 2 (`trig_01Jm57GAjNCFrYJn1oLMiYGE`)
  "NEVER self-delivered its 06:08:52Z slot … next_run_at STILL frozen at the
  past 06:08:52" — while self-bound crons ran 100%. **First proven
  scheduled delivery: 2026-07-13T06:10Z** (`control/outbox.md` ORDER 017;
  note: the dispatch brief for this audit said 07-14 — corrected), and the
  cron kept delivering on 07-14 (two routine fires that morning — which
  produced the #362/#363 twin-build, §7). Disposition: **ANTHROPIC** — the
  B-11 ask in §3, verbatim there.
- **Failsafe/pacemaker chain: the thing that actually worked.** The `0 */2`
  failsafe cron **bridged 4/4 and then 6/6 platform wake-drops** (ORDER
  016/017 tallies); two-layer wakes (15-min send_later pacemaker + cron
  failsafe) "survived the platform drop". Disposition: **ACCEPTED** — this
  is the shipped doctrine, not residual friction.
- **Worker-relay + one-trigger-call-per-worker rider.** The coordinator
  surface lacks trigger calls entirely (no `send_later`; §3 B-9), so trigger
  writes relay through spawned workers; retro W-6: "multi-call trigger-MCP
  workers hung … single-call isolation succeeded first try (~30 s)" — hence
  the one-write-per-worker rider (2026-07-12 hardening report §a.1).
  Disposition: **ANTHROPIC** — the B-9 wake-primitive ask in §3, verbatim
  there; the rider itself is a working ACCEPTED pattern.
- **Registry absence proofs cost full pagination:** proving a trigger absent
  required walking **1203 records / 13 pages** (2026-07-13T10:40Z audit;
  the brief said ~1223 — corrected). `list_triggers` responses also overflow
  the MCP result cap. Disposition: **ANTHROPIC** — covered by the B-10/B-11
  asks (tombstones + delivery audit remove the need for exhaustive walks).
- **send_later tombstone-less drop:** `trig_01USg5i3qna4fCX5ZeePg7Gj`
  (armed 01:34Z for 01:49Z, never delivered, absent from the registry;
  failsafe bridged at 02:07Z; one other tick 25 min late). Disposition:
  **ANTHROPIC** — the B-10 ask in §3, verbatim there. Fleet-side mitigation
  proposed to the manager: sequence-numbered pacemaker ticks (gap detection
  instead of forensics).

## 6. Environment & platform issues

- **Container clone divergence — "88 local-only commits."** This figure
  exists ONLY in container team memory (`kit-release-recipe.md` L42:
  "Container-clone gotcha: the session container's local main can silently
  diverge from origin (88 local-only commits observed)…") — **no committed
  record carries it** (grepped + `git log -S`); flagged honestly as
  team-memory-only. Disposition: **FLEET-FIX (shipped)** — the enforcing fix
  is the planted CLAUDE.md step-0 preflight (`git fetch origin main && git
  reset --hard origin/main`); corollary: `/tmp` team memory is
  container-local and lossy (B-19), durable homes beat memory files.
- **Shallow/graft git false negatives (#355 / #357 / #358).** #355: the
  session's own clone was shallow (**51 of 441 commits** — shipped PRs
  #16–#187 looked absent until `--unshallow`). #357: clone GRAFTED,
  `merge-base --is-ancestor` returned a **false negative for v1.15.0's real
  bump commit `eaf4f23`**. #358 centralized the rule once as
  `scripts/_git_truth.py` after it "had been independently re-derived three
  nights running". Disposition: **ACCEPTED / fixed-ourselves** — residual:
  future ancestry-touching checkers import the helper (checkers SKIP, never
  false-FAIL).
- **Proxy walls** (cross-ref §3 B-1/B-3/B-4): `api.github.com` 403
  ("GitHub access is not enabled"), tag push 403, branch delete 403.
  Dispositions as in §3 — ANTHROPIC (read-only API), ACCEPTED (release
  dispatch path), FLEET-FIX (OA-10 owner click). `scripts/verify_release.py`
  designs around them (assets via `releases/download/`, workflow leg SKIPs
  with the verbatim 403).
- **Harness sleep block (coordinator surface), verbatim:** "`Blocked:
  standalone sleep 1500. To wait for a condition, use Monitor with an
  until-loop (e.g. until <check>; do sleep 2; done). To wait for a command
  you started, use run_in_background: true. Do not chain shorter sleeps to
  work around this block.`" — plus the Monitor ~30-min cap with silent
  wake-loss on kill. Disposition: **ANTHROPIC** — the B-9 ask in §3.

## 7. Process & ceremony cost

**PAID (ceremony that earned its keep):**

- **Session gate / born-red.** Held partial PRs against a 2.9-min-median
  auto-merge pipeline — the exact race it exists for. Its own bugs were
  found and fixed fail-closed: the V051 mtime false-green (a post-merge
  sibling card masks an in-progress card) fixed by merge-base-diff card
  selection with a **proven-red fixture** ("old logic exited 0 on the
  fixture") in PR #342; earlier loopholes W-3 (tail-1 shadowing → #187) and
  W-4 (a 24-s merge slip → #176) closed during the program.
- **Claims.** "Claim-first + born-red-card-first made **~100-PR/day
  parallelism safe** … collision rate stayed at zero duplicated slices"
  (retro lesson 5) — until the one measured gap: #362/#363, two concurrent
  routine fires building the same ORDER (claims keyed on branch token, not
  work). Root-caused and **guarded the same day** (#364 groom → #365
  `claim --order` + refusal + advisory:
  [idea file](../ideas/order-claim-cross-branch-collision-2026-07-14.md)).

**TAX (ceremony/noise that cost without earning):**

- **Legacy-alias 3-red noise.** Two `legacy-alias-*` mirror jobs (whole body:
  `if [ "failure" != "success" ]; then exit 1`) triple every born-red hold
  into a 3-red signal; retro W-9: this class "**dominated diagnosis cost**"
  (a red-ping was investigated as "real defect"; job-log truth: "HOLD (by
  design)… nothing to investigate"). The fix is one owner ruleset click —
  **👤 P10, still open at close**. FLEET-FIX (owner).
- **Heartbeat restamp churn.** ~10 control-only PRs in ~36 h (07-13→07-14)
  existed only to restamp `control/status.md`, including #350 — a whole PR
  to correct one line the enabler race staled. Cost capped by the
  control-only CI fast lane; **mechanized by `bootstrap heartbeat` (#346)**
  + claim-verb restamp (#359). FLEET-FIX (shipped).

**Checkers policing themselves (the meta-loop worked):**

- `check_claims` false-stale (filename date shadowed the claim's real date)
  — found live by #352's session, **fixed same day** by #353 (last-date-on-
  bullet-line + 3 regression tests; pre-fix repro verbatim "[claims-stale] …
  dated 2026-07-09 is 5 day(s) old").
- Model-line drift measured unbounded: **124/178 completed cards drifted
  (174 findings)** — lint shipped windowed to newest-10 (#352); recorded
  irony: the lint-shipping cohort is the lint's biggest offender.
- Kit law [PL-006] "Source wins; a false green is the check's bug" carries
  the superbot #763 false-green precedent; applied in V051 and #355's
  merge-marker matcher (covers both squash and merge-commit styles — the
  exact #763 shape).

## 8. What we fixed ourselves

One line per fix, merge SHAs on origin/main:

- #342 @ `5354786` — session-gate merge-base card selection, fail-closed (V051 false-green)
- #344 @ `4e09862` — enabler INSTALL-time preflight (advisory, fail-open)
- #346 @ `4aacd38` — `bootstrap heartbeat` mechanical restamp verb
- #349 @ `ee3b962` — seat-digest adaptive skills-clip (retires the hand ratchet)
- #351 @ `727f5db` — CHANGELOG [Unreleased] structure checker
- #352 @ `a9145ee` — model-line payload lint (124/178 drift measured)
- #353 @ `a67ccda` — `check_claims` own-date fix (false-stale)
- #354 @ `87aeb4d` — kit-side `scripts/preflight.py` CI-convergence dogfood
- #355 @ `bf231c3` — idea-index merged-reality leg (+ shallow-clone discovery)
- #356 @ `6b9cdd4` — `scripts/cut_release.py` release mechanization
- #357 @ `0d0aac4` — `scripts/verify_release.py` post-release verification
- #358 @ `e564b2d` — `scripts/_git_truth.py` shared shallow/graft-safe helper
- #359 @ `e06624b` — `bootstrap claim` verb + restamp + release-checklist drift pin
- #362 @ `e7c0a5e` — friction-outbox pending-count advisory + INC-29 pointer-casing template fix ("one template fix heals ~14 adopters")
- #364 @ `2a2d92b` / #365 @ `f856ce3` — cross-branch ORDER-collision guard (`claim --order` + refusal + advisory)
- #334/#335/#336 (2026-07-13) — dead-pointer guards (skills/templates)

Suite across the chain: **1284 → 1523 tests**. Honesty row: one rail breach
(#342 worker self-arm) remediated <2 min, team memory written.

## 9. Top 5 remaining pains (ranked)

1. **Scheduler delivery/deletion opacity + trigger tombstones** — the only
   subsystem that failed silently with no agent-side proof path.
   **ANTHROPIC**, two paste-ready asks: "Scheduler delivery/deletion logs
   are invisible agent-side: a fresh-session cron missed its slot with
   next_run_at frozen in the past (trig_01Jm57…, 2026-07-12T06:08:52Z) and
   its predecessor was hard-deleted with no audit entry (trig_01MHwm…) —
   expose delivery status/deletion audit; also note a manual fire_trigger
   sets last_fired_at without advancing next_run_at." And: "A dropped
   send_later one-shot vanishes from list_triggers with no tombstone
   (trig_01USg5i3qna4fCX5ZeePg7Gj, 2026-07-13) — persist dropped triggers
   with an ended_reason so drops are detectable without gap forensics."
2. **Legacy-alias 3-red diagnosis tax (👤 P10)** — every born-red PR pays a
   3-red false signal that "dominated diagnosis cost"; one owner ruleset
   click (require `kit-quality`, drop the two legacy contexts) ends it.
   **FLEET-FIX (owner)** — open since 2026-07-09.
3. **api.github.com read-only for verification legs** — **ANTHROPIC**,
   paste-ready: "Allow read-only GETs to api.github.com through the agent
   proxy for allowlisted repos (at minimum Actions runs/jobs, repo
   settings/rulesets, PR `auto_merge`) — the MCP toolset has no ruleset
   read and omits `auto_merge`, so verification scripts currently SKIP legs
   they could prove."
4. **MCP `auto_merge` field + PR-state staleness** — **ANTHROPIC**,
   paste-ready: "Include the `auto_merge` object (and issue-timeline reads)
   in pull_request_read responses — parked-PR disarm state is currently
   unprovable agent-side and is inferred via a no-op-disable side-effect
   probe." And: "GitHub MCP PR-state endpoints can serve ~25-minute-stale
   data (observed 2026-07-09, ~30 min polling cost); shorten/expose the
   cache TTL or add a freshness timestamp to responses."
5. **Park-by-label doctrine adoption** — prose-parking is a no-op against
   the enabler (#353, #365; §4); park = `do-not-automerge` with
   disarm-verified-before-label, plus a status-vs-merged-reality advisory
   and branch auto-delete (OA-10) as the sibling owner click.
   **FLEET-FIX** — doctrine exists; make the verb/check enforce it.

(Remaining ANTHROPIC asks not in the top 5 — coordinator wake primitive
B-9, classifier consistency B-7, spawn identity B-20 — stay live in §3
verbatim.)

## 10. Wishlist

Deduped against §3/§9 (nothing here repeats an ask already made):

1. GitHub MCP `list_workflow_runs` that paginates full history honestly —
   observed truncated/stale at 30 runs regardless of filters
   (fleet-cleanup audit; also capped this audit's CI-round measurement to
   the last 30 PRs).
2. `list_triggers` filtering (by id/name/state) — absence proofs cost
   13-page/1203-record walks; a `?id=` lookup makes them one call.
3. A branch-delete capability on some sanctioned surface (MCP tool or
   proxy-allowed) — OA-10 covers merged-PR heads only; ad-hoc stale
   branches still accumulate agent-side.
4. gh CLI on the container image — never attempted here (B-2, honest
   null), but would collapse several MCP+proxy workarounds if present.

## 11. Honest gaps — what this audit could not measure

- **#341 verbatim denial text does not exist** — only the #342 session
  card's paraphrase "failed (checks pending)"; the "unstable status"
  verbatim belongs to fleet-manager PR #10 (§4).
- **"88 local-only commits"** — container team-memory only
  (`kit-release-recipe.md` L42), no committed record (§6).
- **webagent / WebFetch usage** — genuinely unevidenced in this repo's
  ledger; verdicts would be invention (§2).
- **gh CLI** — never attempted in this repo; absence is known fleet-wide
  only (§3 B-2).
- **Per-PR CI-round counts** — measured only for the last 30 PRs
  (#337–#366); runs endpoint pages at 30/page (~20+ pages for full
  history).
- **MCP `list_workflow_runs` truncation** limits all CI-run counting
  (§10.1).
- **merged_by for all 350 merged PRs** — list endpoint lacks the field;
  sampled 6/6 = `github-actions[bot]`, no counter-example encountered.
- **#317 / #345 owner-ratification parks are OUTSTANDING** — cited with
  reasons and click counts (§4), not closed by this audit.
- **Found during this audit:** `control/status.md:35` at `f856ce3` still
  claimed "#365 OPEN, parked" after the enabler merged it at
  2026-07-14T08:29:18Z — corrected by this audit's session (PR #366).
