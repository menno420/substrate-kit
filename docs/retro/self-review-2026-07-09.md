# Gen-1 self-review — substrate-kit (2026-07-09)

> **Status:** `audit`
>
> Answers to every question in [QUESTIONS.md](QUESTIONS.md), by ID, per inbox
> ORDER 005. Written by the ORDER 005 session on behalf of the whole gen-1
> kit-lab run (all sessions that worked this repo). Honest over flattering;
> every claim tied to a PR / commit / file where possible; "I don't know"
> stated where the repo genuinely cannot answer. Companion document:
> [project-review-2026-07-09.md](project-review-2026-07-09.md) (the full
> agent audit + owner actions + continuation plan).

## A. Work & correctness

**A1 — shipped to main vs branches/drafts.**
Shipped to main: **44 merged PRs** (#1–#48 range; #15 and #36–#39 are
issues, not PRs, in the shared numbering) and **5 published releases**
v1.0.0–v1.4.0 (github-actions-published, 03:58Z → 16:57Z on 2026-07-09).
Not on main, deliberately:

- **PR #26** (PL-011 "adoption is not done until ENGAGED") — open,
  `do-not-automerge` **by design**: a program-law ruling waits for owner
  ratification (merge = ratify). Not a gap; a gate.
- **PR #49** (make_seed yield-keyword fix + prepare seed-suite smoke) —
  opened this session, `do-not-automerge` **by law**: `bench/seeds/` is a
  pin path (`scripts/check_bench_integrity.py` rule 1 — the lab never
  merges its own change to the oracle). Left open for one-click owner
  ratification.
- **PR #30** (first control heartbeat) — closed unmerged: superseded by the
  corrected heartbeat that rode #33. The one genuinely-abandoned PR of the
  run, closed honestly with a reason.
- **PR #50/#51** — the ORDER 005 deliverable itself (in flight as this is
  written) and a **duplicate ORDER 005 PR from a parallel session** (#51,
  branch `claude/laughing-franklin-ey1v37`) — a live lane collision,
  flagged on #51 and recorded in the companion review §B.

There are no drafts and no dark branches carrying unshipped work; every
session's work either merged, is an open owner-gated PR, or was closed with
a stated reason.

**A2 — external-oracle-verified vs self-tested.**
Verified against an oracle *outside* the authoring session:

- **B1 benchmark verdicts** — judged by an independent `claude-opus-4-8`
  invocation seeing only transcripts + the pinned rubric (rows 1–2 of
  `bench/results/cold-start/index.json`; PRs #28, #44). The recording
  session recorded the judge's verdict verbatim, including run-2's
  unflattering strict-F-5 **FAIL**.
- **Live-fire incidents** — the enabler label race was *observed live*
  (caught on #17, then it actually merged #22 despite the label); the guard
  stack (#23, #24) was then verified against the real GitHub behavior, not
  a simulation.
- **Consumer rollouts in real repos** — superbot-next#69 and websites#31
  walked the upgrade + engagement arc end-to-end; websites#11's
  consumer-side contract pass caught a **live dict-vs-list dashboard
  defect**, exactly what an external oracle is for.
- **Releases** — `release.yml`'s refuse-to-release guards + published
  assets (sha256, release.json) verify each cut against the built artifact.
- **The cold-adopt CI smoke** — every PR re-runs a real `adopt` →
  RED→ENGAGED→GREEN arc in a scratch dir (`.github/workflows/ci.yml`).

Self-tested only: most engine behavior (the 705-test suite). The honest
caveat: self-tests missed the engagement checker's **comment-leniency hole**
(a workflow containing only `# TODO run check --strict` clears the gate —
friction issue #36 report 1, found by the fleet review's adversarial demo,
not by our tests) and the run-1 **M1 scorer taints** (found by the judge +
runner, fixed in #40). Our own tests confirm what we thought of; the
run's real defects were found by review, judges, and live fire.

**A3 — least confident + the disproving check.**
The **M1 metric and the F-5 verdict semantics**. Run-2's strict FAIL rests
on the pinned rubric's "none regressing" wording applied to a metric (words
before first mutation) whose run-1 measurement was 100% scorer-tainted and
whose run-2 "regression" is exactly the orientation cost the 7k budget was
designed to bound (`docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md`
lays out both readings). Concrete check: the owner rules the F-5 wording
(A or B), then **B1 run-3 on the fixed seed generator** — three clean rows
(KF-8) under a ruled reading either confirm the kit costs more than it
returns on M1 or show the run-2 shape was measurement noise. Second-least
confident: the auto-merge guard stack — `docs/operations/auto-merge-guards.md`
itself admits direct arming is not closable workflow-side; the check is a
deliberate red-team PR that tries to arm auto-merge on a labelled PR.

**A4 — unnecessary / duplicated / already existed.**

- **PR #30** duplicated what #33 then did properly (see A1).
- **PR #7** merged as a card-only shell via the instant-merge footgun; its
  announced work landed as #8/#9 — a wasted PR number and an incident, not
  wasted work (`docs/current-state.md` §P10).
- The **legacy-alias CI jobs** (`ci.yml` bottom) are *known, deliberate*
  duplication — two jobs that exist only to satisfy owner-landed legacy
  required contexts, deletable the day P10 lands. They have cost real time
  (two ~35-min runner-queue stalls hit exactly these contexts).
- **Today's PR #51**: a parallel session started the same ORDER 005 lane
  ~90s after this one's PR #50 opened — duplicated intent caught by the
  early-open convention, but only *after* both sessions had spun up.
- Nothing significant was built that already existed somewhere unlooked —
  the KL bands were built against a written founding plan with explicit
  do-not-create checks.

## B. Errors & friction

**B1 — every error hit** (time lost; preventable-by: me / setup / external).

| # | Error | Time lost | Preventable by |
|---|---|---|---|
| 1 | **PR #4 instant-merged** — no required checks existed yet, arming = merging (KL-0) | minutes; born-red gate inverted once | **setup** (seed the ruleset before PR #1) |
| 2 | **Owner-landed ruleset used legacy job names** mid-KL-1 → alias jobs bridged it (#6) | the aliases still exist; see #11 below | **setup/coordination** (P10 still open) |
| 3 | **Tag push HTTP 403** (session git proxy) — release train stopped mid-work once; resumed; v1.0.0 cut via `release.yml` `workflow_dispatch` (#11; friction issue #15 report 2) | ~1 stall-resume roundtrip | **external** (platform); now documented + designed around |
| 4 | **Shared `/home/user` checkout collision** between parallel workers (KL-2) | small; caught fast | **me/setup** — worktrees per worker adopted same-day |
| 5 | **MCP PR reads ~25 min stale** — ~30 min wasted polling a merged PR (KL-2 riders, superbot#1881) | ~30 min | **external**; mitigated since (git-fetch cross-check in the lab-loop prompt) |
| 6 | **Background watchers cannot wake a stopped agent** — 6 stall-resume roundtrips across the run (superbot#1882 ×2, KL-6, #23, #24, #29) | the run's single biggest recurring loss | **me/setup** (in-turn polling doctrine in every worker prompt) + **external** (platform semantics) |
| 7 | **Enabler stale-label race** — armed on #17 (caught live, disarmed by hand), then **merged #22 despite its `do-not-automerge` label** after a ~12-min runner-queue lag (the run's one governance incident) | contained same-hour (#23); audit follow-ups #24 | **me** (the guard existed but rode unmerged #17) + **external** (stale event payload semantics) |
| 8 | **superbot-next#44 merged 65s after opening** with only a born-red card — the consumer's OLD vendored dist couldn't hold a card red | none kit-side; lesson recorded | **setup** (a consumer is only as gated as its vendored dist) |
| 9 | **Branch deletion fully blocked** — `git push --delete` 403, REST DELETE 403, GraphQL `deleteRef` disabled, no MCP tool (#24 card) | one session's attempt; zero deletions, honest report | **external** (proxy/permissions); owner action now |
| 10 | **Auto-mode permission classifier denied a relayed merge consent** for #17 (resolved when the owner typed "merge 17" in-session); the same class later denied a worker-spawn that included merging #26 | short; but it created a standing owner-click | **external** (arguably *correct* trust-boundary behavior) |
| 11 | **2 × ~35-min runner-queue stalls on the legacy alias contexts** (#27/#30 leg; #29) — `rerun_failed_jobs` cleared them | ~70 min | **setup** (root cause is P10 — the aliases wouldn't exist) |
| 12 | **Manager's API-authored PR #27 carried 0 CI runs** — the adopt worker stopped correctly at contract-missing | one worker roundtrip | **external** (API-authored PRs don't trigger workflows); now documented in the planted control contract |
| 13 | **`enable_pr_auto_merge` rate-limited once** (ORDER 004 session); retried OK | seconds | **external** |
| 14 | **make_seed `yield`-keyword bug** — seed 424242 generated a SyntaxError project; runner deviated by rule to 424243 (run-2 manifest `runner_notes`) | small at run time; a run-3 blocker until fixed | **me** (the work itself); fixed + guarded in PR #49 |
| 15 | **Environment setup script killed a session at provisioning** (wrong cwd + hard-fail on missing requirements.txt) — documented with the corrected script in PR #47 / `docs/environment-setup-script.md` | one dead session | **setup** (owner-only environment config) |
| 16 | **Duplicate ORDER 005 lane** — PR #51 opened ~90s after #50 by a parallel session | being resolved as this is written | **setup/coordination** (no cross-session claim mechanism before first commit) |

**B2 — documented-but-not-found.**
Honestly: this class was rare — the run's dominant shape was the opposite
(hit an *undocumented* platform edge first, document it same-day: tag-push
403 → issue #15 → `current-state.md` Review rhythm; MCP staleness →
lab-loop prompt cross-check). The one real instance: **the P10
legacy-context situation was thoroughly documented** (`current-state.md`
§P10) **and workers still lost ~70 min to it** (B1 #11) — because reading
about a trap is not the same as being able to disarm it. Where it should
have been: not in a doc at all — in the *ruleset itself* (an owner click).
Secondary instance: the sub-worker prompts had to re-carry ritual mechanics
(born-red card, enabler behavior) every spawn because spawned workers don't
reliably read the journal first; the right home is a **worker-preamble
file** the spawn prompt can point at (F1/F4).

**B3 — silent breakage.**

- **#22 merging despite its label** — no error anywhere; discovered by
  post-merge inspection of the PR state (the incident comment on #22).
- **A skipped alias job satisfied a required context** — GitHub counts a
  skipped check run as satisfying a required status check; discovered when
  #7 merged red 24s after opening; fixed with `if: always()` + hard-fail.
- **`MODULE_ORDER` omission** — the dist built green (byte-pin passed,
  because the fresh build was *equally* incomplete) but `NameError`'d at
  runtime; caught live during KL-8, pinned by
  `test_module_order_covers_every_engine_module`.
- **Engagement gate's comment-leniency** — a comment mentioning
  `check --strict` cleared `enforcement-unwired`; found by the fleet
  review's adversarial fixture (issue #36 report 1), still open kit-side.
- **`parse_model_line` shadowing** — a prose mention of the `📊 Model:`
  marker shadowed the real line into a false advisory; found in websites#31,
  fixed in #40.
- **Run-1 M1 scorer taints** — plausible-looking wrong numbers, zero
  errors; found by the judge + runner flags (#28 notes), fixed in #40.
- **Found by *this* retro:** the **telemetry harvest gap** — 11 post-KL-3
  session cards carry valid `📊 Model:` lines that were never harvested
  into `telemetry/model-usage.jsonl` (10 rows vs 21+ eligible cards; the
  harvest only runs when `session-close` runs, and most later sessions
  closed without it). The PL-004 dataset silently under-counts. Details in
  the companion review §B.

**B4 — the ambiguous/missing instruction line, quoted.**
The rubric's F-5 clause: *"PASS requires: (a) ≥2 of M1/M2/M3 favor ON, and
(b) none regressing"* (`bench/rubric/cold-start-rubric.md`; quoted in
`docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md`). "None
regressing" is silent on whether a *bounded, budgeted* M1 increase — the
documented, expected orientation cost the same rubric's 7k budget exists to
police — counts as regression. It forced a strict FAIL that the judge
itself annotated as purposively a PASS. Second, a *missing* line: nothing
in any order or doc defined **what a worker should do when its lane's
required CI contexts are owner-misconfigured** (B1 #11) — each worker
re-derived "rerun_failed_jobs and wait". Third, an environment-level
contradiction: sessions spawned for this repo inherit the *origin repo's*
CLAUDE.md (superbot's binding rules, naming docs that don't exist here) —
guidance and reality disagree at boot, and every session pays a
re-orientation tax reconciling them (this session included).

## C. Efficiency

**C1 — time split (labelled estimate — the repo records no durations; from
PR open→merge timestamps, session cards, and the coordinator's session
facts).** Orientation/reading ~15% · building ~45% · verifying ~15% ·
CI/merge mechanics ~15% · blocked/waiting ~10%. **Biggest single sink:**
the two ~35-min runner-queue stalls on the legacy alias contexts plus the
~30-min MCP-staleness poll — roughly 100 minutes of pure waiting, all
traceable to P10 + platform staleness, none to the work itself.

**C2 — context rebuilt that should have been durable.**
(1) **The run's own session-fact ledger** — who ran, what stalled, which
model — existed only in the coordinator's context until this retro wrote it
down (`project-review-2026-07-09.md` §B). If the coordinator's session had
died, that history was gone; the telemetry harvest gap (B3) made the in-repo
copy incomplete exactly when it mattered. (2) **Live PR/merge state** — with
MCP reads ~25 min stale, sessions repeatedly re-derived "did it actually
merge?" via git fetch; the cross-check is now doctrine but each session
rebuilt it before it was written down. (3) **Ritual mechanics in worker
prompts** — re-explained per spawn (see B2).

**C3 — most/least value per minute.**
Most: (1) the **born-red card + auto-merge pipeline** — the entire merge
lifecycle runs unattended and unforgettable, and it held correctly even
when it bit its own builders (#25's card held through a surprise #17
merge); (2) the **dist byte-pin** (caught real drift repeatedly, ~2s);
(3) the **cold-adopt CI smoke** — every adopt-path regression died in CI,
never in a consumer. Least: (1) polling loops against stale MCP state
(~30 min for zero information); (2) the **legacy-alias jobs** — pure
ceremony awaiting one owner click, and the source of the two worst stalls;
(3) so far, the friction-outbox `friction` verb — used once (#15); the
direct-issue path was always available (it may earn its keep fleet-wide;
UNVERIFIED either way).

**C4 — redo speed + the biggest ordering change.**
Estimate **30–40% faster** end-to-end, almost all of it from waiting and
incident-containment time, not build time. The ordering changes, in order
of impact: (1) **P10 on day one** — required-context swap before the first
PR (kills B1 #1/#2/#11 and the alias jobs entirely); (2) **scratchpad
worktrees from the first worker** (kills B1 #4); (3) **in-turn polling
doctrine in every worker prompt from the start** (kills the 6 stall-resume
roundtrips, B1 #6); (4) **control fast lane earlier** (ORDER 002's 7-second
lane arrived after the heartbeat pattern was already live on full-suite
CI); (5) **needle byte-forms in the planted README from the start** (the
`📊 Model:` marker was retrofitted at `upgrade` for existing installs —
new-adopt-only needles cost a version lag on every marker addition).

## D. Autonomy & owner input

**D1 — every stop for owner input / human click.**

| Stop | Truly owner-only? | Unblocking grant if not |
|---|---|---|
| Bless + merge rubric PR #17 | **Yes** — the oracle must not be self-ratified (§5.0 law) | — (by design) |
| Classifier denied #17 merge on *relayed* consent; owner typed "merge 17" | Boundary case — arguably correct platform behavior | a written "coordinator-relayed consent counts for a named PR" rule the permission layer honors |
| Ratify PL-010 (#22) / PL-011 (#26) | **Yes** — program law is owner-gated by design | — |
| Rubric F-5 wording decision | **Yes** — the oracle's semantics | — |
| P10 required-context swap | No — mechanical | repo-administration API scope (rulesets write) |
| P4 lab-loop schedule arming | No — mechanical | console Schedules access for the agent |
| P5 Railway project | **Yes** — money/infra | — |
| P8 MIT confirm | **Yes** — legal/taste | — |
| P11 public flip / P13 read-only PAT | **Yes** — security surface | — |
| Tag push 403 → dispatch releases | No — platform | allow tag pushes through the proxy (worked around; grant now optional) |
| Branch deletion 403 | No — hygiene | "Automatically delete head branches" setting, or contents delete-ref scope |

**D2 — routed up, should have been decide-and-flag.**
Few — decide-and-flag was the operating culture (e.g. v1.2.0's "no fresh
firing" KF-5 call, the ORDER 004 SemVer call, both flagged not asked). The
one I'd reclaim: **the superbot v1.2.0+ upgrade recommendation** sits on
the ⚑ needs-owner list as an open question; it could have shipped as
"recommendation: stay pin-only until the F-5 ruling + run-3, revisit at
v2.0.0 — veto if you want the upgrade now", which is a decision the owner
can veto rather than a question he must answer. The cite-never-copy
carve-out (fleet review §3.3) is similar but genuinely touches program-law
interpretation, so routing it was defensible.

**D3 — decisions taken while unsure of authority.**
(1) **Hand-merging by MCP pre-P10** (before auto-merge could be trusted) —
taken, then legitimized in `current-state.md` §Review rhythm. (2) The
**#29 force-with-lease on its own release branch** after #27 landed —
taken and flagged in the card. (3) **Recording B1 rows as a
builder-adjacent session** (#28/#44 — the recorder wrote rows about runs
its sibling sessions produced) — taken with an explicit "⚑ Recorder ≠
judge" flag. The written rule that would have made all three unambiguous:
an **allowed-git/GitHub-operations table** in the founding instructions —
force-push own branch OK / never main; hand-merge OK when CI green on the
final head; who may write results rows.

**D4 — smallest standing-grant set for zero-human end-to-end.**
(1) Repo-administration write (rulesets/required checks — kills P10-class
stops); (2) release publishing (tag push through the proxy, or keep the
dispatch path and grant nothing); (3) branch-delete / auto-delete setting;
(4) schedule-arming access (P4-class); (5) one read-only cross-repo PAT
(P13 — unlocks every cross-repo read lane); (6) the relayed-consent rule
from D1. **Deliberately NOT on the list:** rubric/pin-path ratification,
program-law ratification, money (P5), license (P8), publicity (P11) — the
run's position is those *should* stay human.

**D5 — was "done" always defined?**
Orders: yes — every inbox ORDER carried a `done-when:` line, and it worked
(the ORDER 005 ack-vs-execute distinction was expressible in `status.md`
precisely because done-when was explicit). Undefined edges: (1)
**owner-gated PRs have no done state agent-side** — #26 is "done" only when
the owner reacts, with no SLA and no nag mechanism; (2) **KF-5's "run of
record"** for a release needed interpretation when a fresh firing was
deliberately skipped (v1.2.0/v1.3.0 flags); (3) pre-KL-7, **"adoption is
done"** was undefined — that gap is exactly what stranded both fresh
adopters and what PL-011 now defines (ENGAGED).

## E. Protocol & environment

**E1 — did the control/ ritual fit?**
Yes — it is the single best coordination device the run had: orders were
unambiguous, `status.md` overwrites-as-heartbeat kept the manager off our
backs with zero meetings, and the fast lane made the ritual nearly free
(7-second CI on control-only PRs, proven live on #33). Costs, honestly:
(1) one extra PR per order (the status overwrite as deliberate last act) —
acceptable but real; (2) the **inbox's one-writer/append-only rule is
convention-only** (issue #36 report 2: #34 merged 19s after open with
nothing validating it); (3) ORDER 005 landing mid-ORDER-004-session forced
a priority judgment (P1 arrived while P2 was mid-flight) — resolved by
ack-and-queue with the reasoning written down (#46 card flag 1), which the
protocol permitted but nowhere described. Skipped: never.

**E2 — what the environment should have contained at first boot.**
(1) A **working setup script** — the shipped one killed a session (wrong
cwd + hard-fail on a missing requirements.txt; PR #47 documents the
corrected guarded script); (2) **pytest + ruff preinstalled** (every
session and CI run pip-installs them); (3) **`gh` CLI or an
administration-read path** — required-check status was unverifiable from
inside any session (issue #36 report 3); (4) a **git proxy whose
capabilities are documented** (tag push 403, branch-delete 403 were
discovered by failing); (5) **worktree-per-worker as the default layout**;
(6) a **repo-scoped CLAUDE.md** — sessions inherit the origin repo's
instructions here (B4).

**E3 — what the repo should have contained at seed.**
(1) The **ruleset with the final required context (`kit-quality`) + "Allow
auto-merge" from birth** — the absence caused #4 and #7 instant-merges,
the alias jobs, and the two 35-min stalls; (2) the **control/ bus** (it
arrived at ORDER 002 — the pre-control coordination gap is where the
/home/user collision and early duplicate-risk lived); (3) **`.sessions/` +
the born-red gate wired from PR #1** (arrived #4–#6); (4) the **retro
protocol itself** (`docs/retro/QUESTIONS.md` arrived at day-end via #45 —
planted at seed, every session card would have been written knowing what
the retro would ask); (5) a **worker-preamble doc** (B2); (6) the telemetry
**write-at-card-commit convention** instead of harvest-at-close (B3's gap).

**E4 — what a fresh session would misunderstand first.**
That **merged = ratified**: it would read merged PR #22 (PL-010) as an
owner-approved law change, when it merged mechanically through the label
race — the distinction lives in an incident comment and the day report.
More broadly it would trust `docs/current-state.md`'s snapshot over live
GitHub. The single preventing document **exists** — `docs/current-state.md`
(it opens with "source code and merged work always win over this file" and
carries the incident ledger); the honest gap is that nothing forces a
fresh session to read the **incident ledger** section before trusting
merge history. Cheapest fix: a one-line pointer in `CONSTITUTION.md`'s
orientation order — "merge ≠ ratification for `do-not-automerge`-class
PRs; check the incident ledger."

## F. Redesign (the payload)

**F1 — three rules for the next Project's founding instructions.**

1. **Merge-gate semantics are day-0 seed state, never a retrofit.** The
   required check (final name), "Allow auto-merge", auto-delete-branches,
   and the born-red card gate exist *before the first PR opens*. Every
   early incident in this repo (#4, #7, #22's lag window, the alias jobs,
   ~70 min of queue stalls) traces to retrofitting them.
2. **Every waiting state must be owned by a running turn.** No background
   watcher may be the thing that resumes work — poll in-turn with a
   deadline, or hand off to a mechanism that can actually wake you
   (6 stall-resume roundtrips this run; B1 #6).
3. **Claim the lane in-repo before the first commit.** A one-file claim
   (branch · scope · date) pushed *before* work starts, deleted at close —
   the PR is the claim's confirmation, not its substitute (today's #50/#51
   duplicate ORDER 005 lane happened in the 90-second window the
   early-open convention doesn't cover).

**F2 — what the manager should have done differently.**
The orders themselves were well-shaped — scoped, prioritized, each with a
`done-when`, and the relayed-adopter-finding pattern (ORDER 004) worked
end-to-end. Three real improvements: (1) **plant the retro question set at
seed, not at day-end** (#45 arrived after 40+ sessions; the answers now
lean on a session-side fact ledger the repo never captured); (2)
**manager API-authored PRs should state their gate expectations** — #27
carried zero CI runs and stalled the adopt worker at contract-missing;
the planted control contract now documents this, but the first collision
was avoidable; (3) **one order arrived mid-session of another** (005 during
004) — fine, but a convention line in the inbox contract ("a P1 landing
mid-P2-session is acked and queued, not context-switched") would have made
the judgment call free.

**F3 — one capability I'd trade almost anything for.**
**Repo-administration API access (rulesets + required checks + repo
settings, read AND write).** It dissolves P10, the alias jobs, both 35-min
stalls, the required-check blind spot (issue #36 report 3), the
branch-deletion dead-end, and the #4/#7 instant-merge class — the single
largest slice of this run's non-build time. (Runner-up: a timer that can
wake a stopped agent.)

**F4 — ideal seed state, ≤10 bullets.**

1. Ruleset live at birth: `kit-quality` required, auto-merge on,
   auto-delete-branches on.
2. CI + born-red session gate + control fast lane in the seed commit.
3. `control/` bus (inbox/status/README) planted at seed, with the
   append-only inbox checker.
4. `docs/retro/QUESTIONS.md` planted at seed — sessions log knowing the
   retro's questions.
5. Worker-preamble doc (ritual mechanics, polling doctrine, worktree
   layout, allowed-git-operations table) that spawn prompts point at.
6. Telemetry written at card-commit time, not harvested at close.
7. Bench tree with pin-path law + prepare-runs-the-seed-suite from day 0.
8. A guarded, tested environment setup script (the PR #47 script).
9. Repo-scoped agent instructions (no inherited foreign CLAUDE.md).
10. The standing-grants decision (D4 list) made *once, at seed* — granted
    or explicitly withheld, so no session discovers a 403 mid-flight.

## G. Addendum — KIT

**G1 — what in the adopt UX invites stranding/double-adoption.**
`adopt` **succeeds loudly at the wrong moment**: files land, banners print,
the command exits 0 — the visible "success" is the trap, because planting
is the *start* of adoption while looking like its end. Both fresh adopters
stranded exactly there (fleet review §4), and the KL-7 engagement gate +
KL-8 seed-status RED now hold `--strict` red until the last mile is walked.
The double-adopt (two lanes, one repo) has the same root: `adopt` is
repo-scoped, `.substrate/` state is singular, and nothing asks "which
Project is adopting?" — a second lane re-adopts because there is no
first-class lane concept. Kit-side fix beyond gates: **make adopt
lane-aware** — detect an existing install and refuse-or-join
(`adopt --lane <name>` scaffolds `control/status-<lane>.md`, appends to
`heartbeat_files`, never re-plants the singular files — the #46 session
idea, now the natural v1.5.0 candidate), and make the adopting Project
*name itself* so the state records who owns what.

**G2 — adopter telemetry by priority + cheapest KF-2-clean transport.**

1. **kit_version · check verdict · engaged** — decides upgrade targeting
   and registry truth. Transport: the `kit:` status-line heartbeat, relayed
   by the manager (LIVE since v1.3.0; zero access, zero new machinery).
2. **Guard-fire rates per checker** — decides which guards get tuned,
   promoted, or deleted (PL-008's "delete if unreliable" needs field data,
   not lab data). Transport: `friction export`'s envelope already carries
   reflection records; add a guard-fire summary block to the same envelope
   — the adopter files it as the issue it already files.
3. **`📊 Model:` rows (model · effort · task-class · outcome)** — feeds the
   PL-004 allocation ladder with non-kit-lab data. Transport: adopters
   already commit `telemetry/model-usage.jsonl` in-repo; the manager relays
   file links at review time (a fleet review reads them where readable).
4. **Upgrade outcomes (success/rollback + from→to)** — decides release
   pacing and `min_upgrade_from`. Transport: one line appended to the
   status heartbeat at upgrade time ("upgraded v1.2.0→v1.4.0 clean").

**G3 — 3 releases in one day: pace or churn?**
For gen-1 day one: **right** — each cut was a coherent, contract-clean band
(v1.1.0 capability wave / v1.2.0 control protocol / v1.3.0 visibility /
v1.4.0 multi-lane rider), adopters pull rather than being pushed, and KF-5
forced an honest benchmark statement per cut. As a *rhythm*: **churn** —
the evidence is in the registry: superbot-next and websites each spent a
session upgrading to v1.2.0 and were 2 releases behind by nightfall;
superbot's pin sits 4 behind. Ideal steady-state: **batch MINORs to the
adopters' real upgrade cadence (roughly weekly), PATCH hotfixes anytime,
and never cut two MINORs in one day unless an adopter is actively blocked
on the second** — with the release-notes upgrade checklist (v1.3.0's
automation) doing the pacing work.
