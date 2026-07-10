# Project review — substrate-kit (2026-07-09)

> **Status:** `audit` (dated snapshot — written by the ORDER 005 retro
> session, same PR as [self-review-2026-07-09.md](self-review-2026-07-09.md);
> facts verified against live GitHub + the working tree at
> 2026-07-09 ~17:15Z; source code and merged PRs win over this file)

## (a) What this Project is, and its true current state

**substrate-kit is the fleet's substrate coordinator — the kit-lab.** It
builds, benches, and releases the substrate kit (`dist/bootstrap.py`, a
generated single-file stdlib-only engine) that the fleet's repos adopt for
session discipline, checks, telemetry, and the control/ coordination bus; it
never writes to adopter repos (KF-2) and improves the kit from relayed
adopter evidence. Founding charter:
`docs/planning/kit-lab-founding-plan-2026-07-07.md`.

True state, verified live (not from memory):

- **v1.4.0 is the live release**; five version cuts all dated 2026-07-09
  (v1.0.0–v1.4.0 in `CHANGELOG.md`, each published via the `release.yml`
  `workflow_dispatch` path with bootstrap.py + sha256 + release.json
  assets).
- **41 merged PRs** (live PR list: #1–#48 range minus issue numbers
  #15/#36–#39, minus open #26, minus closed-unmerged #30; #47 — the
  environment-setup-script doc — merged 2026-07-09T17:02:51Z under the
  owner account; whether it was hand-clicked or automation cannot be
  determined from the repo). **38 of the 41 merged on 2026-07-09 alone.**
- **Test suite: 705 passing** (`python3.10 -m pytest tests/ -q` on this
  review's tree, matching the v1.4.0 card's count; grown 483 → 705 across
  the bands).
- **Bands KL-0…KL-8 complete** (`docs/current-state.md` § Stability
  baseline, band-by-band with PRs); **inbox ORDERS 001–004 done, ORDER 005
  is this PR** (`control/inbox.md` / `control/status.md`
  `orders: acked=001-005 done=001-004`).
- **Open PRs at review time:** #26 (PL-011 ruling text — owner-gated by
  design, merge = ratification), #49 (make_seed pin-path fix,
  `do-not-automerge`, opened 17:09Z — owner merge unblocks B1 run-3), plus
  the in-flight ORDER 005 work itself — see the duplication note in (b).
- **4 open friction issues** #36–#39 (filed by the fleet review, PR #35).
- **B1 cold-start family at 2 rows**
  (`bench/results/cold-start/index.json`): run-1 **PASS**, run-2 **FAIL
  (strict F-5, advisory per KF-5)** — both judged by claude-opus-4-8; no
  trend claim (KF-8 needs ≥3).
- **Adopter registry** (`docs/adopters.md`): kit-lab HEAD (consumer #0) ·
  superbot-next v1.2.0 ENGAGED · websites v1.2.0 ENGAGED · superbot v1.0.0
  pin-only (deliberate; now four releases behind) · superbot-games — the
  two-lane adopter, version/engagement not yet relayed · trading-strategy
  planned.
- **Two incidents on 2026-07-09** — kit#22 (label-race auto-merge of a law
  PR) and superbot-next#44 (65-second merge on an in-progress card) — both
  guarded since (`docs/reports/2026-07-09-kit-lab-run.md` §3).

## (b) Agent audit — every session that worked this Project

Model attribution is exactly as strong as the repo's evidence: the `📊
Model:` line convention began at KL-3 (PR #13), so **everything earlier is
honestly "cannot be determined"**. Where a card exists it is cited; PR
timestamps are from the live API. Stall/death causes are classified **(a)
our instructions/setup · (b) platform limit/bug · (c) the work itself**.

| Session (card) | PRs | Model (evidence) | Outcome / incidents |
|---|---|---|---|
| Repo population + CI + CODEOWNERS (no cards — pre-card era, 2026-07-08) | #1–#3 | cannot be determined (no card, no telemetry existed) | Clean; driven by the coordinator session. |
| KL-0 dogfood seed (`2026-07-09-kl0-dogfood-seed.md`) | #4/#5 | cannot be determined — card predates the KL-3 Model-line convention | Card-only PR #4 auto-merged alone 15 s after open (**no required checks existed yet** — cause (a) setup). |
| KL-1 CI delta (`2026-07-09-kl1-ci-delta.md`) | #6 | cannot be determined (no Model line) | Friction: direct api.github.com 403 (b); 405 revealing the owner-landed legacy required contexts (a+b) → alias bridge jobs. |
| KL-1 release train (`2026-07-09-kl1-release-train.md`) | #7–#11 → v1.0.0 | cannot be determined (no Model line) | #7 instant-merged red — skipped-check-satisfies-required footgun (b, with (a) alias design); #9 auto-merged pre-close-out (a); tag-push HTTP 403 → dispatch path (b). |
| KL-2 governance home (`…kl2-governance-home.md`) | #12 | fable-5 · high · docs-only + test writing (compound, off-taxonomy class) | Clean. |
| KL-3 telemetry (`…kl3-telemetry.md`) | #13 | fable-5 · high · kernel/architecture design | Clean; Model-line convention starts here. |
| KL-4 lab loop + friction (`…kl4-lab-loop.md`) | #14 | fable-5 · high · kernel/architecture design | Clean (issue #15 filed + triaged same day). |
| KL-5 auto-draft (`…kl5-auto-draft.md`) | #16 | fable-5 · high · kernel/architecture design | Clean. |
| KL-5 bench tree (`…kl5-bench-tree.md`) | #17 | fable-5 · high · kernel/architecture design | `do-not-automerge` by design; owner-blessed + owner-merged after ~5¾ h (ledgered in `docs/decisions.md`). |
| KL-6 unblocked (`…kl6-unblocked.md`) | #18 | fable-5 · high · kernel/architecture design | Clean. |
| Groomed ideas 1 (`…groomed-ideas-1.md`) | #19 | fable-5 · high · kernel/architecture design | Clean. |
| Pinned-feed idea (`…pinned-feed-contract-idea.md`) | #20 | fable-5 · high · idea/planning | Clean. |
| Run close-out (`…run-closeout.md`) | #21 | fable-5 · high · docs-only | Undercounted incidents (1 vs the true 2) — corrected by #24. |
| PL-004 feature-build (`…pl004-feature-build.md`) | #22 | fable-5 · high · feature build | **Incident kit#22**: `do-not-automerge` law PR auto-merged via the enabler's stale-label read + ~12-min runner-queue lag (a+b). |
| Enabler-race hotfix (`…enabler-race-hotfix.md`) | #23 | fable-5 · high · runtime bugfix | Clean; verified merged via auto-merge as designed. |
| Audit follow-ups (`…audit-followups.md`) | #24 | fable-5 · high · feature build | Clean; branch-delete 403 + permission-classifier denial hit and correctly abandoned (b). |
| P0 engage gate (`…p0-adopt-engage-gate.md`) | #25 (+#26 opened) | fable-5 · high · feature build | Clean; #26 deliberately left open (owner gate). |
| B1 record (`…b1-record.md`) | #28 | fable-5 · high · docs-only | Clean; recorder ≠ judge held. |
| v1.1.0 release (`…v1.1.0-release.md`) | #29 | fable-5 · high · **release** (off-taxonomy class) | Clean. |
| KL-8 control band (`…kl8-control-protocol-band.md`) | #31 | fable-5 · high · feature build | Clean; caught the silent MODULE_ORDER dist NameError live and pinned it. |
| v1.2.0 release (`…v1.2.0-release.md`) | #32 | fable-5 · high · **release** (off-taxonomy class) | Clean. |
| ORDER 002 status overwrite (no card — control-only fast-lane ride) | #33 | cannot be determined | Clean (23-s lane merge, by design). |
| Fleet adoption review (`…fleet-adoption-review.md`) | #35 | fable-5 · high · review/verify | Clean; filed #36–#39; shipped the fast-lane status gate. |
| Run-2 harness prep (`…run2-harness-prep.md`) | #40 | fable-5 · high · runtime bugfix | Clean. |
| ORDER 003 (`…order003.md`) | #41 (+overwrite #42, no card) | fable-5 · high · feature build | Clean → v1.3.0. |
| B1 run-2 record (`…b1-run2-record.md`) | #44 | fable-5 · high · docs-only | Clean; FAIL verdict recorded verbatim. |
| ORDER 004 (`…order004.md`) | #46 (+overwrite #48, no card) | fable-5 · high · **feature build + release cut** (compound class) | Clean → v1.4.0; deferred ORDER 005 with a flagged priority deviation. |
| Heartbeat protocol attempt (no card) | #30 — **closed unmerged** | cannot be determined | The lane's one abandoned PR: superseded same-day by the status-overwrite pattern (KL-8) — cause (a), protocol churn during adoption. |
| The session that died at provisioning (no card — evidenced only by PR #47's body) | none — delivered nothing | cannot be determined (it never reached the repo) | Killed by the owner-configured environment setup script: assumed repo cwd + unguarded `pip install -r` on a repo with no requirements.txt; exit 1 ends the session — cause (a) owner-configured script bug + (b) platform behavior (setup exit 1 is fatal). |
| Manager/coordinator inbox writes (Contents API, no sessions in-repo) | #27/#34/#43/#45 | cannot be determined from this repo | Clean; #34's 19-s unvalidated merge is issue #36 report 2. |
| B1 bench **judge** (not a builder session) | — | **claude-opus-4-8**, recorded verbatim in both `bench/results/cold-start/*/report.md` | Grader ≠ builder per the allocation ladder; both verdicts recorded unedited. |
| Env-setup doc session (PR body names session `…01Y5uPEhxhYUvC8qMpoDDvJ7` — a worker of this wake-up session) | #47 | fable-5 (inherited from this wake-up session) | Merged 17:02:51Z under the owner account after a branch update; who clicked is not determinable from the repo. |
| **This wake-up session** (2026-07-09, this PR + its workers: repo survey, audit gather, the #47 steward above, this author, a status-overwrite worker to follow) | this PR | **claude-fable-5** (stated per repo convention as fable-5); all workers inherit it | In flight. |

**⚠ Duplication note (live, as of ~17:15Z):** a sibling session
(`…01CJfdy7YxUw8oXj4Wfngdyc` — the same session ID as the fleet-review §4
rollout session) opened **PR #49** (the pin-path seed fix, correctly
owner-gated) and then **PR #50 at 17:10:07Z — a second, parallel ORDER 005
attempt targeting these same two file paths**. Two lanes picked up the same
P1 order within minutes of each other; whichever lands second will conflict.
This is itself gen-1 evidence for the retro's coordination findings (no
claim/lease mechanism on orders — the inbox marks status `new` until the
manager flips it, so two readers can both see "new" and both execute). This
review proceeded per its own order; the collision is flagged here rather
than silently raced.

**Stall/death census:** one dead-at-provisioning session (a+b, above); one
abandoned PR (#30, a); two premature-merge incidents (kit#22 a+b;
superbot-next#44 — consumer-side, old vendored dist, a); zero sessions lost
to the work itself (c). Where a fate or model is not knowable from the repo,
the table says so — no invented attribution.

## (c) Retro answers

The full gen-1 self-review — every `docs/retro/QUESTIONS.md` ID answered
with evidence — is
[**self-review-2026-07-09.md**](self-review-2026-07-09.md).

## (d) Honest efficiency verdict

**Where time actually went** (derived from PR open→merge timestamps — the
repo records no durations, see self-review C1): the day ran 02:33Z → 17:02Z
with 38 merged PRs. The genuinely productive spine — bands KL-2…KL-8, the
bench, the orders — moved at roughly one substantial PR per 25–35 minutes.
The visible sinks: (1) **CI/merge mechanics and incident guard-building** —
sessions #23 and #24 exist wholly because of incident #22, and the #7/#9/#10
arc exists wholly because the required-check ruleset didn't match the
shipped CI; add the legacy-alias runner burned on every one of 41 PRs. (2)
**The ~5¾-h #17 blessing wait** (05:47→11:32Z) — the one long owner-gated
stall, and per the day report it was **parallelized well**: seven PRs
(#18–#24) merged inside that window, so the wall-clock cost to the lane was
near zero even though the bench band's completion moved by half a day. (3)
**Bench rework between runs** — run-1's M1 was unmeasurable (scorer taints),
so PR #40 rebuilt scorer parts and run-2 repeated the measurement; a
pre-run smoke would have collapsed that loop.

**What I'd redo, in order:** (1) **P10 first — before any auto-merge use**:
the required-check swap is the root cause under both incidents and the
alias-job tax; it is one owner click and it was still pending at day's end.
(2) **Land the engagement gate before inviting adopters**: both fresh
adopters stranded half-engaged in exactly the shape KL-7 (PR #25) later made
impossible — the gate was built as a P0 *reaction* to the stranding review
rather than a precondition of the invitations. (3) **Bench harness smoke
before run-1**: the seed sweep + scorer known-bad fixtures (now riding
PR #49 / shipped in #40) would have made run-1's M1 measurable and saved the
run-2 deviation.

## (e) ⚑ Owner actions — exact steps, and what each unblocks

1. **P10 — required-check swap** (root cause of both incidents).
   github.com/menno420/substrate-kit → **Settings** → **Rules → Rulesets**
   (or **Branches** → the `main` branch-protection rule, whichever the repo
   uses) → edit the rule for `main` → under required status checks,
   **remove** the two legacy contexts **"Kit test suite"** and
   **"Cold-adoption smoke (adopt + check --strict)"** (these are the alias
   jobs' display names in `.github/workflows/ci.yml` lines 226/238) →
   **add** required check **"kit-quality"** (source: GitHub Actions) → save.
   Leave "Require branches to be up to date" OFF. *Unblocks:* deleting the
   two `legacy-alias-*` jobs from `ci.yml` (agent-queue item), stops paying
   a duplicate runner per PR, and retires the incident class.
2. **Auto-delete merged branches + clean the stale ones.** Settings →
   **General** → scroll to **Pull Requests** → tick **"Automatically delete
   head branches"** → then open the repo's **Branches** page and delete the
   stale merged `claude/*` branches listed there (agents get HTTP 403 on
   branch deletion — `.sessions/2026-07-09-audit-followups.md` flag 1).
   *Unblocks:* branch hygiene without a recurring ⚑ line.
3. **Ratify PL-011 — merge PR #26.** Open
   github.com/menno420/substrate-kit/pull/26 → read the one-page ruling
   ("adoption is not done until ENGAGED") → **Merge = ratification**; to
   veto, comment on the PR instead. *Unblocks:* PL-011 becomes program law
   on main; issue #37's "native-substrate consumer" state design follows
   it.
4. **Ratify or veto PL-010 retroactively** (it reached main via incident
   #22, not review). Comment on PR #22 (a 👍 or "ratified" suffices per
   `docs/current-state.md` owner-gate 2), or add a stamp block to
   `docs/program/rulings.md` per that file's convention. To veto: say so —
   a revert PR restores the 8-class taxonomy.
5. **Rule the rubric F-5 wording** (pin path — it rules B1 run-3's
   verdict). Read
   `docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md` → reply
   with **strict** ("none regressing", any M1 regression fails) or
   **7k-budget** (the orientation budget is M1's yardstick). Note the pin
   path: the wording-fix PR must carry `do-not-automerge` and your merge.
6. **Merge PR #49** (one click — the make_seed keyword-safety fix +
   prepare smoke; `bench/seeds/` is a pin path so owner merge =
   ratification). *Unblocks:* B1 run-3 on a valid seed 424242.
7. **Paste the environment setup script.** The corrected script is already
   on main (`docs/environment-setup-script.md`, PR #47 — merged) — the
   remaining step is owner-only: open the Claude Code web UI → this
   Project's **environment settings** → replace the setup script with the
   doc's fenced script verbatim → save. *Unblocks:* no more sessions dying
   at provisioning (one already did — PR #47's body has the provision
   log).
8. **The standing platform gates** (all carried in `control/status.md` ⚑):
   **P4** arm the lab loop (Console → Schedules → paste the prompt from
   `docs/operations/lab-loop.md` § Arming, cron `0 6 * * *` UTC, fresh
   session per fire — unblocks D3); **P5** create Railway project
   `kit-lab` (region europe-west4, no spend caps per PL-005 — unblocks the
   P6 console move); **P11** flip the repo public **or** **P13** a
   read-only PAT (either unblocks cross-repo reads: the merged console +
   B2–B4 sweeps); **P8** confirm MIT (one word).
9. **Fleet-side clicks** (carried from the fleet review §5 in
   `control/status.md`): make the kit gate a **required** status check on
   superbot-next's main (its PRs #51/#68 merged red without it); decide
   **superbot's upgrade** (deliberate v1.0.0 pin now four releases behind
   v1.4.0); one glance at **websites** Settings → Rules to confirm its
   `quality` check is required; rule the **cite-never-copy carve-out**
   (fleet review §3.3 — pick shape 1/2/3; everything in §3.4 beyond the
   no-conflict items waits on it).

## (f) Continuation — zero owner input needed, in order

1. **Run-2 harness follow-ups, ordinary lane** — starts **immediately after
   this PR lands**: the `run_ab.py prepare` RED→ENGAGED→GREEN engagement-arc
   scripting (`docs/ideas/run-ab-prepare-engagement-arc-2026-07-09.md`), the
   `render --live` CLAUDE.md gap
   (`docs/ideas/render-live-claude-md-gap-2026-07-09.md`), and the
   `_adopt_sessions_readme` Model-line checker false-red
   (`docs/ideas/model-line-checker-false-red-2026-07-09.md`). (The fourth
   follow-up — the make_seed fix + prepare seed-smoke — already rides
   pin-path PR #49 and waits on the owner, not on the lane.)
2. **B1 run-3** once PR #49 is owner-merged (or, if it stays open, fired
   under the documented seed-bump deviation rule) — ideally after the F-5
   wording ruling so the verdict lands under the ruled reading; family
   reaches 3 rows and KF-8 trend claims become possible.
3. **`_enforcement_wired` real-parse fix** (issue #36 report 1): strip
   comment content before the substring test + known-bad fixture test —
   closes the "ENGAGED with a dead door" hole.
4. **Inbox-grammar validator** (issue #36 report 2): control-lane checker —
   `control/inbox.md` diffs must be pure-append vs merge-base + ORDER-block
   grammar; composes with the scoped status gate on the same fast lane.
   (The ORDER-005 double-execution recorded in §(b) is fresh evidence for
   also adding an order-claim convention while in there.)
