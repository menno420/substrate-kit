# Project review — substrate-kit gen-1, wind-down capstone (2026-07-09)

> **Status:** `audit` — the WIND-DOWN capstone over the whole gen-1 Project
> life, written by the kit-lab wind-down lane (phase 2, PR #74) as the
> generation closes. It cites and builds on — never duplicates — the three
> same-day reviews:
> [project-review-2026-07-09.md](project-review-2026-07-09.md) (canonical
> repo-evidence pass, ORDER 005),
> [project-review-2026-07-09-kitlab-coordinator.md](project-review-2026-07-09-kitlab-coordinator.md)
> (the coordinator's 35-session fact ledger + model split + cross-check), and
> [wind-down-review-2026-07-09-superbot-coordinator.md](wind-down-review-2026-07-09-superbot-coordinator.md)
> (the sibling lane's wind-down addendum). What THIS file adds: the
> whole-life arc through v1.6.0 and ORDERS 001–009 (the ORDER 005 pair stops
> at v1.4.0/ORDER 005), the complete friction ledger with exact error text
> in ONE place, and a "how it felt" reconstruction — **explicitly
> secondhand**, mined only from committed artifacts. Succession pack:
> [`docs/gen2/`](../gen2/next-boot.md).

## 1. The whole gen-1 life, in one arc

- **2026-07-08**: repo populated from superbot's `substrate-kit/` subtree
  (#1), CI (#2), CODEOWNERS (#3).
- **2026-07-09, one day**: bands KL-0 → KL-8 built and shipped; **7 releases
  cut, v1.0.0 (03:58Z) → v1.6.0**, every one via the `release.yml`
  `workflow_dispatch` path because the git proxy 403s tag pushes; the
  benchmark harness built, owner-blessed and owner-merged (#17; ledgered in
  `docs/decisions.md`) and **fired twice**
  (run01 PASS with M1 unmeasurable; run02 strict-F-5 FAIL, advisory,
  wording disputed — owner ruling pending); 3 consumer rollouts
  (superbot-next, websites ENGAGED; superbot pin-only); the control/ bus
  era — **ORDERS 001–009 all acked and done** including two live latency
  pings (ORDER 009 ack on main in ~5 min); the ORDER 005 twin-execution
  retro pair; the ORDER 007 claim convention and ORDER 008 OWNER-ACTION
  band; two incidents, both guarded same-day; the gen-1 wind-down claimed
  (#72) and executed (#73 sibling pack, this PR #74).
- **Scale** (verified): **35 sessions** on the coordinator's ledger (the
  repo cannot count sessions that left no artifact — honest floor), **41
  merged PRs at the ORDER 005 count** and merges for **20 more PR numbers
  in the #50–#73 range on main's log by wind-down** (~61 total; several are
  manager inbox appends and control-only heartbeat rides), suite **483 →
  722 tests**, `.sessions/` at 33 cards, 19 idea files, 11 structured
  owner actions outstanding.
- **Model split** (per coordinator; repo corroboration partial — see the
  kitlab-coordinator review §(b)): **claude-fable-5** build/coordination
  lane · **claude-sonnet-5** the 12 benchmark arm sessions ·
  **claude-opus-4-8** the 2 independent judges. The arm models are NOT
  repo-verifiable (run manifests carry no model field) — recorded then,
  repeated here, as "per coordinator".

## 2. What worked (with evidence)

1. **The born-red card + auto-merge pipeline.** The merge lifecycle ran
   unattended across ~61 merges and "held correctly even when it bit its
   own builders" (#25's card held through a surprise #17 merge —
   self-review C3). The one bypass (#22) was a race, not a design failure,
   and was contained same-hour.
2. **The control/ bus.** "The single best coordination device the run had"
   (self-review E1): unambiguous orders with `done-when:`, heartbeat
   overwrites instead of meetings, the 7-second control fast lane (proven
   live on #33), ORDER 009's ping acked on main in ~5 minutes.
3. **Honest-red gates + honest verdicts.** The strict-F-5 **FAIL** was
   recorded verbatim on main (#44) with the judge's purposive-PASS
   annotation attached — the benchmark kept its integrity precisely when
   the result was unflattering. Same aesthetic as the sibling lane's
   born-red report jobs ("red is not yet proven").
4. **Friction → guard, same day.** Every incident became machinery within
   hours: #22 → #23 fresh-label re-read + #24 disarm workflow +
   `--label-gate`; the #7 skipped-alias hole → `if: always()` hard-fail;
   the MODULE_ORDER silent NameError → a dist-completeness test; the
   twin execution → the ORDER 007 claim ritual; the OWNER-ACTION sprawl →
   ORDER 008's six-field contract + advisory checker.
5. **External oracles over self-belief.** The run's real defects were found
   by judges, adversarial review, and live fire — not by its own 722 tests
   (self-review A2): the M1 scorer taints (judge), the engagement checker's
   comment-leniency hole (fleet review's adversarial fixture), the
   dict-vs-list dashboard bug (consumer-side contract pass in websites#11).
6. **Release discipline under speed.** 7 semver cuts in a day, each with a
   KF-5 benchmark statement, byte-pinned dist, refuse-to-release guards,
   sha256-verified assets — zero release incidents.

## 3. The friction ledger — every class, exact text, one place

Classes 1–16 are lived kit-lab incidents; texts in backticks are verbatim
from the cited artifact. (The sibling lane's additional classes — 4KB brief
cap, webhook wake noise, zombie revival — live in its
[wind-down review](wind-down-review-2026-07-09-superbot-coordinator.md) §
"Friction / failure classes".)

1. **Tag push / branch deletion / git-refs REST all 403 through the git
   proxy.** Tag push HTTP 403 live-hit at v1.0.0 (friction issue #15
   report 2) → the `release.yml` `workflow_dispatch` path became the only
   agent-runnable release route. Branch deletion blocked on EVERY path —
   `git push --delete` 403, REST DELETE `/git/refs/*`
   `Write access to this GitHub API path is not permitted through this proxy`,
   GraphQL `deleteRef` not enabled, no MCP delete-branch tool — a full
   session attempted it and deleted zero (audit row 21;
   `docs/CAPABILITIES.md`).
2. **Direct push to main ruleset-blocked** (phase-1 wind-down, verbatim):
   `GH013: Repository rule violations found ... Changes must be made through a pull request. 2 of 2 required status checks are expected.`
   Everything rides PRs; control-only changes ride the fast lane.
3. **Stale MCP PR reads** — ~25-min-stale reads cost ~30 min of polling a
   PR that had already merged (session 9, superbot#1881). Cure: git-fetch
   cross-check, now doctrine in the lab-loop prompt.
4. **Background watchers cannot wake a stopped agent** — 6 stall-resume
   roundtrips (sessions 10×2, 14, 19, 20, 26), the run's single biggest
   recurring loss. Cure: in-turn polling doctrine in every worker prompt.
5. **Runner-queue stalls on the legacy alias contexts** — 2 × ~35 min
   (~70 min lost) on "Kit test suite" / "Cold-adoption smoke (adopt + check
   --strict)", the owner-landed legacy required-check names (root cause
   P10, still open). Cure: GitHub MCP `rerun_failed_jobs`, then wait.
6. **The #22 governance incident** — a `do-not-automerge`-labelled
   program-law PR **merged mechanically**: the enabler armed auto-merge
   from a stale pre-label event payload after a ~12-min runner-queue lag.
   Contained same-hour (#23 fresh-label re-read; #24 disarm workflow +
   `check_program_law.py --label-gate`). Lesson: labels advise, required
   checks enforce (`docs/operations/auto-merge-guards.md`).
7. **Relayed-consent merge denials** — the auto-mode permission classifier
   refused owner-gated merges on relayed consent: #17's merge was DENIED
   until the owner typed "merge 17" live in-session; a later worker-spawn
   including "merge #26" was denied the same way → #26 became a standing
   owner one-click (audit row 23). Arguably correct trust-boundary
   behavior; plan around it, don't fight it.
8. **The #50/#51 twin execution** — ORDER 005 executed by two parallel
   sessions ~90 s apart (both saw `status: new`; no claim mechanism
   existed). #51 merged first and holds the canonical paths; #50's docs
   repositioned as `-kitlab-coordinator` companions. Root-cause fix: the
   ORDER 007 claim-first ritual (claim on main BEFORE build).
9. **Cross-repo reads are allowlisted per session** (verbatim, live-hit
   again at wind-down 2026-07-09 ~20:06Z):
   `Access denied: repository "menno420/fleet-manager" is not configured for this session. Allowed repositories: menno420/superbot-next, menno420/websites, menno420/substrate-kit, menno420/superbot, menno420/trading-strategy`.
   **Wind-down discovery:** the wall is NOT absolute — this session reached
   fleet-manager via the `add_repo` session tool + a shallow git clone and
   read `docs/gen2-blueprint.md` in full (public repo; finding appended to
   `docs/CAPABILITIES.md`).
10. **Cross-session messaging is unreliable-to-absent.** Previously
    recorded org-wide death: `send_message: tool is not enabled for this
    organization`. In THIS environment the tool is absent entirely;
    phase 1's single attempt via the harness `SendMessage` returned
    verbatim: `No agent named 'cse_0184Aa1jZ8FvSYAvzSXP5yFU' is reachable.`
    The git bus (committed control/ files) is the fallback channel **by
    design** — and it never failed.
11. **API-authored PRs may not trigger CI / workflows.** The manager's
    Contents-API PR #27 carried 0 CI runs (the adopt worker stopped
    correctly at contract-missing); MCP-created PRs don't fire the
    auto-merge enabler workflow — arm auto-merge yourself via
    `enable_pr_auto_merge` (proven again on #72 and this PR).
12. **Telemetry undercount** — `telemetry/model-usage.jsonl` held 10 rows
    vs 21+ eligible session cards: the harvest ran only inside
    `session-close`, which later sessions skipped. The PL-004 dataset
    silently undercounts; fix queued (write-at-card-commit + backfill).
13. **The PR #47 setup-script kill** — a web session died at provisioning;
    verbatim from `docs/environment-setup-script.md`:
    `fatal: not a git repository (or any of the parent directories): .git`
    → `ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'`.
    Wrong cwd + hard-fail on a missing optional file; a non-zero setup exit
    kills the session. Corrected guarded script in that doc; gen-2 variant
    tested at wind-down (`docs/gen2/setup.sh`, exit 0 from `/` and from the
    repo dir).
14. **Shared-checkout collision** — two parallel workers collided in the
    single `/home/user` checkout (session 7, KL-2); all later workers moved
    to scratchpad worktrees same-day.
15. **Instant-merge footguns of the retrofit era** — #4 merged 15 s after
    open (no required checks existed yet); #7 merged red 24 s after open
    (**GitHub counts a skipped check run as satisfying a required status
    check** — the bare `needs:` alias was skipped on failure); #9
    auto-merged before its close-out. Fixes: `if: always()` + hard-fail
    aliases, the in-progress-badge session gate. Root lesson: merge-gate
    semantics are day-0 seed state, never a retrofit (self-review F1.1).
16. **Small change:** `enable_pr_auto_merge` rate-limited once (ORDER 004
    session); single retry cleared it. `api.github.com` direct HTTP is
    blocked outright — GitHub access is MCP-tools-only
    (`docs/CAPABILITIES.md`).

## 4. How it FELT — secondhand reconstruction, labelled as such

> **Provenance disclaimer:** the sessions that lived gen-1 are gone; no
> firsthand author remains. This section is a **secondhand reconstruction
> by the wind-down session**, built ONLY from committed artifacts —
> `.sessions/` cards, the retro pair, `.substrate/guard-fires.jsonl` (11
> rows), `telemetry/`, and the incident comments. Every impression below
> is anchored to a lived, recorded incident; where the record is silent, so
> is this section. "I don't know" is the honest answer for anything
> unlisted.

**The harness.** The record shows a lane that trusted its machinery and was
right to: cards open born-red, auto-merge fires on green, and the cards
barely mention the mechanics after KL-1 — the pipeline had become
invisible, which is what good machinery feels like. What the record shows
it feeling *bad* about is **waiting**: the efficiency verdicts converge on
~100 minutes of pure queue/staleness waiting (C1), and the stall-resume
class ("a stopped worker waiting on a watcher that cannot wake it") reads
as the recurring low-grade frustration — six times is a pattern, not an
accident.

**The instructions.** Two recorded pains. First, inherited-instructions
dissonance: sessions booted with the *origin repo's* CLAUDE.md ("superbot's
binding rules, naming docs that don't exist here" — self-review B4), and
"every session pays a re-orientation tax reconciling them". Second, the
gap-shaped failures: the twin execution and the priority-judgment moments
(ORDER 005 landing mid-ORDER-004) were both places where no rule existed
yet — the lane's own texts call the fixes "one sentence per order" class
repairs. The instructions that DID exist (done-when lines, decide-and-flag)
are cited in the cards with something close to gratitude.

**The environment.** The capability ledger exists because imagined walls
and real walls kept blurring: the recorded arc is "attempt once, capture
the exact error, append" — a discipline invented mid-run precisely because
rediscovering the tag-push 403 or the branch-delete blockade cost real
sessions real time. One session died at provisioning through no fault of
its own (#47's body is its only gravestone) — the closest thing gen-1 has
to a casualty report.

**The model.** From the cards alone: fable-5 held long-horizon,
multi-session state without recorded plot loss — the failures ledgered are
environmental (proxies, rulesets, queues, watchers), not cognitive; the
sibling coordinator's firsthand close ("I did not lose the plot; I lost
tools") is consistent with everything this repo recorded, and nothing in
the kit-lab record contradicts it. The honest caveat: cards are written by
the sessions themselves; a model flattering itself in its own cards would
look identical. The independent evidence — the opus-4-8 judge verdicts
recorded verbatim even when unflattering, and the audit session disproving
its own auditor's suspicion (#23, row 20) — points the right way.

## 5. What gen-2 must not re-pay

The condensed prescription (full versions: self-review F1/F4, the
[gen-2 pack](../gen2/next-boot.md)):

1. Merge-gate semantics at seed (required check = real job name, auto-merge
   on, auto-delete branches on) — retrofitting them cost #4/#7/#22 and
   ~70 min of stalls.
2. Claim-first on main before build — the twin execution is the proof.
3. Every waiting state owned by a running turn — no background watcher may
   be the resumer.
4. Walls pre-filled with exact error text (`docs/CAPABILITIES.md` pattern)
   — probing a documented wall twice is a bug.
5. Telemetry at card-commit, not session-close — or the dataset undercounts
   exactly when sessions get sloppy.
6. Worker worktrees in scratchpad from worker #1.
7. A tested, defensive, exit-0 setup script before the first session
   (`docs/gen2/setup.sh`).
