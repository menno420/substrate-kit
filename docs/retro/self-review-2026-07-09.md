# Gen-1 retro self-review — substrate-kit (2026-07-09)

> **Status:** `owner-guidance` — the Project's own answers to
> [QUESTIONS.md](QUESTIONS.md), by ID, per inbox ORDER 005. Honest over
> flattering; every claim tied to a PR/commit/file where the repo can supply
> one; "I don't know" stated plainly where it can't. Written as the
> accumulated substrate-kit lane, from repo evidence verified live on
> 2026-07-09 (PR timestamps re-pulled from the GitHub API, not memory —
> `.session-journal.md` § Past mistakes exists because a remembered count was
> once wrong).

## A. Work & correctness

**A1 — shipped to main vs branches/drafts.** Shipped to main: **41 merged
PRs** (#1–#48 plus none beyond, minus the issue numbers #15/#36–#39 which are
not PRs, minus open #26, minus closed-unmerged #30 — count verified against
the live PR list, including #47 which merged at 17:02:51Z). That work is:
bands KL-0…KL-8 of the founding plan complete
(`docs/current-state.md` § Stability baseline, band-by-band with PR numbers),
five releases cut and published (v1.0.0 through v1.4.0, all dated 2026-07-09
in `CHANGELOG.md`, each with the three assets per `release.yml`), inbox
ORDERS 001–004 executed same-day (ORDER 005 is this document), two judged B1
bench rows (`bench/results/cold-start/index.json`), the two owner reports
(`docs/reports/`), and the friction filings #36–#39. Exists **only on
branches, by design**: the PL-011 ruling text (PR #26, `do-not-automerge`
owner-review — merge is the ratification act, so it must not land agent-side)
and, as of 17:09Z, the make_seed pin-path fix (PR #49, `do-not-automerge` —
`bench/seeds/` is a pin path; the lab never merges its own change to the
oracle). The gap is not drift; both are the law working as written
(`docs/program/rulings.md` §8.3-shape owner gates). The one genuinely
**abandoned** PR is #30 (a control-protocol heartbeat PR, closed unmerged —
superseded within hours by the status-overwrite pattern that KL-8/PR #31
shipped; protocol churn during adoption, honestly counted).

**A2 — external-oracle vs self-verified claims.** Externally verified: the
two B1 verdicts were judged by **claude-opus-4-8**, an independent judge, and
recorded verbatim (`bench/results/cold-start/2026-07-09-run01/report.md` and
`…run02/report.md` line 3 both name the judge; recorder ≠ judge per the #44
card); the v1.2.0 **release-integrity proof** compared tag, main, and the
downloaded asset by sha256 — all `258ab02a…`
(`docs/reports/2026-07-09-fleet-adoption-review.md` §2.3); the auto-merge
guard stack was verified by **live fire** — #23 and #24 armed at open and
merged on green exactly as designed (#23's card records merge 3–4 s after the
required contexts went green); and the engagement gate was proven on a real
half-adopted fixture with verbatim output (fleet review §2.1). Everything
else — the bulk of the engine's correctness claims — rests on the kit's
**own pytest suite** (705 tests at v1.4.0, grown 483→705 across the bands):
a self-oracle. It is a good self-oracle (the dist byte-pin caught real drift,
the MODULE_ORDER guard was born from a live miss), but a suite the same lane
writes is not independent verification, and this review says so.

**A3 — least confident, and the disproving check.** Three candidates, in
order: (1) **the bench rubric's F-5 "none regressing" wording** — run-2's
verdict flipped on whether F-5 is read strictly (M1 token counts regressed →
FAIL) or purposively (the 7k budget as M1's yardstick → PASS); the judge
itself noted both readings
(`bench/results/cold-start/2026-07-09-run02/report.md`; decision brief
`docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md`). The concrete
check: the owner rules the wording (pin path — mandatory upward route), then
run-3 is judged under the ruled reading. (2) **`_enforcement_wired`'s
substring match** — a workflow containing only a comment with
`check --strict` clears the engagement gate (demonstrated on a fixture,
issue #36 report 1). Check: strip `#`-comment content before the substring
test + a known-bad fixture test. (3) **the required-check blind spot** —
agents cannot read branch protection on any fleet repo (issue #36 report 3),
so every "the gate is required" claim is inference from `mergeable_state`.
Check: one owner glance at Settings → Rules per repo, or a read path granted.

**A4 — unnecessary / duplicated / already existed.** (1) PR #30's heartbeat
protocol was **built then abandoned** — the status-overwrite pattern replaced
it the same day (see A1); the cost was one PR's work. (2) The two
`legacy-alias-*` bridge jobs in `.github/workflows/ci.yml` exist only because
the `main` ruleset (owner-landed mid-band with the old context names,
discovered via a 405 — `.sessions/2026-07-09-kl1-ci-delta.md`) still requires
the legacy contexts; they burn a runner per PR and were the root-cause
surface of both incidents. Not duplicated work exactly, but scaffolding that
P10 would have made unnecessary from day one. (3) PR #7 was a card-only PR
that instant-merged red and announced work that actually landed as #8/#9 —
a wasted PR slot caused by the same ruleset gap. (4) Two sessions
independently inserted a mid-section `### Fixed` into CHANGELOG (PRs #14 and
#17, `.session-journal.md` § Recurring problems) — small duplicated mistake,
checker backlogged
(`docs/ideas/changelog-unreleased-structure-checker-2026-07-09.md`).

## B. Errors & friction

**B1 — every error hit.** The honest list, with time lost estimated (the repo
records no durations — see C1) and a preventability verdict:

1. **Tag push → HTTP 403** (session git proxy refuses tag pushes;
   `.sessions/2026-07-09-kl1-release-train.md` line ~123). Cost: part of one
   session; fixed durably by the `release.yml` `workflow_dispatch` path
   (PR #11) — v1.0.0 and every release since cut that way. Genuinely
   external (platform), converted to a documented default.
2. **Remote branch DELETE → 403** plus the auto-mode permission classifier
   denying the API fallback (`.sessions/2026-07-09-audit-followups.md`
   flag 1). Cost: minutes, then correctly not retried. External; the durable
   fix is an owner click (auto-delete-head-branches).
3. **Direct api.github.com → 403** ("GitHub access is not enabled" on every
   ambient token; `.sessions/2026-07-09-kl1-ci-delta.md`). External;
   workaround is the MCP toolset, which lacks a branch-protection reader —
   the A3(3) blind spot.
4. **Ruleset 405** — "2 of 2 required status checks are expected" revealed an
   owner-landed ruleset requiring the legacy context names (same card).
   Preventable by better setup (required checks aligned at seed); bridged
   with the alias jobs (#6), which then enabled…
5. **The skipped-check-satisfies-required-check GitHub footgun** — PR #7
   merged 24 s after opening, red: kit-quality failed as designed but the
   bare-`needs:` alias jobs were *skipped*, and GitHub counts a skipped check
   run as satisfying a required status check (`docs/current-state.md` § P10).
   Platform footgun + our alias design; guarded in #10 (`if: always()` +
   hard-fail).
6. **PR #9 auto-merged before its close-out** (the enabler fires on
   MCP-created PRs mergeable at open). Ours; the engine's in-progress-badge
   gate (#10) is the guard.
7. **The #22 incident** — auto-merge label race (enabler read labels from the
   stale PR-open payload; the `do-not-automerge` label landed +7 s after
   open) compounded by a **~12-min runner-queue lag**
   (day report §3.1). Cost: a law PR merged un-reviewed + two full
   guard-building sessions (#23, #24). Part ours (stale read), part platform
   (queue lag).
8. **MCP file-read staleness** (fed the lab-loop prompt's cross-check fix,
   friction issue #15 triage, PR #14) and the standing rule never to trust
   remembered counts (`.session-journal.md` § Past mistakes). Ours to work
   around; cheap once known.
9. **make_seed generates a SyntaxError seed at 424242** — the drawn measure
   token was the Python keyword `yield`
   (`docs/ideas/make-seed-yield-keyword-bug-2026-07-09.md`); run-2 deviated
   to seed 424243 by rule. Ours (no harness smoke before firing); fix rides
   pin-path PR #49.
10. **Dist MODULE_ORDER hand-list omission** — the byte-pin stayed green
    while the dist's `cmd_check` NameError'd; caught and pinned with a
    dist-completeness guard during KL-8 (PR #31). Ours; now mechanical.
11. **A session died at provisioning** — the owner-configured environment
    setup script assumed the repo clone as cwd and ran an unguarded
    `pip install -r requirements.txt` on a repo with no `requirements.txt`;
    exit 1 killed the session before it could do anything (provision log
    verbatim in PR #47's body). Better setup; corrected script documented in
    `docs/environment-setup-script.md` (merged 17:02Z), owner paste pending.

**B2 — figured out though documented elsewhere.** (1) GitHub's
skipped-check-satisfies-required behavior is documented by GitHub, not by
anything this repo's founding materials carried — it was learned by
incident #7. It should have been in the founding plan's §3.2 CI band (one
sentence would have changed the alias-job design). (2) The owner-landed
ruleset itself: the information "main requires these two contexts" existed
in repo Settings the whole time but is unreadable to agents (issue #36
report 3) — it was discovered by a 405 mid-band. It should be surfaced
somewhere agents can read at the moment they design CI: a committed
`docs/operations/` note (which exists NOW as
`docs/operations/auto-merge-guards.md`, written after the fact) or a granted
read path. (3) The python3.10-not-python3 CI floor and the tag-push 403 were
both re-derivable only from cards until `.session-journal.md`'s Quick
reference consolidated them — the journal is exactly the "where it should
have been", and it worked once it existed.

**B3 — silent breakage.** Four, each discovered late by a different route:
(1) the **dist byte-pin green while the dist itself NameError'd** (the
MODULE_ORDER omission — the pin proves dist == fresh build, not dist runs;
discovered when KL-8 ran the dist, guard-tested since, PR #31); (2)
**`_enforcement_wired` satisfied by a comment** (discovered by the fleet
review's adversarial fixture, §2.1 caveat / issue #36 report 1 — still open);
(3) **the control fast lane riding green past a heartbeat-deleting diff**
(the lane skipped the one checker that validates the files a control-only PR
changes; demonstrated before/after in fleet review §2.2, fixed as D-0008 /
PR #35); (4) **superbot-next#44 merging 65 s after open on an in-progress
card** — the consumer's old vendored dist predates the in-progress-badge
gate, so its required check never went red (day report §3.2). The common
shape: a green that measures the wrong thing. PL-006 ("a false green is the
check's bug") is the house response, and all four became guards or filings.

**B4 — ambiguous instruction lines, quoted.** (1) The bench rubric's F-5
clause — **"none regressing"** (`bench/rubric/cold-start-rubric.md`, F-5
row) — was exactly ambiguous when run-2's first clean M1 measurement came in:
strictly read, any M1 token regression fails the run; purposively read, the
rubric's own 7k orientation budget is M1's yardstick and run-2 passes. The
judge flagged both readings; the strict verdict stands recorded and the
wording decision is ⚑ owner-pending
(`docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md`). (2) ORDER
003's *"add a `kit:` line to the kit's control/status.md template"* — read
literally, a line only in the seed template strands every already-adopted
repo (skip-if-exists never re-renders their status); the session widened it
to template + contract format block + checklist delivery and flagged the
reading (`.sessions/2026-07-09-order003.md` ⚑ flag 3). (3) KF-5's
*"advisory-to-pass by KF-5's letter"* tension — whether a MINOR may cite a
standing bench row instead of a fresh firing was decided-and-flagged twice
(v1.2.0, v1.3.0 cards) without a written rule; it never bit, but it is the
kind of line that should be one sentence of law.

## C. Efficiency

**C1 — time split.** **The repo records no durations** — no session card
carries wall-clock start/end, and telemetry rows have no time field — so this
is an **estimate, labelled as such**, derived from PR open→merge timestamps
(the only clock the repo has). The day span 2026-07-09 runs 02:33Z (PR #4
opened) → 17:02Z (PR #47 merged), ~14.5 h, with **38 PRs merged inside it**.
Median PR open→merge is ~10–20 min, nearly all of it CI wall time; the two
big anomalies are the #17 blessing wait (05:47→11:32, ~5¾ h, owner-gated —
but parallelized: seven PRs, #18–#24, merged inside that window) and the
#22→#24 incident-response arc (~2½ h of guard-building). Best estimate:
building ~35% · verifying ~20% · orientation/reading ~15% · CI/merge
mechanics ~20% · blocked/waiting ~10% (mostly absorbed by parallel work).
**Biggest single sink: CI/merge mechanics plus the guard-building the two
incidents forced** — sessions #23 and #24 exist entirely because of the
label-race incident, and every PR paid the legacy-alias runner tax (P10).

**C2 — context rebuilt that should have been durable.** (1) Merged-PR counts
and file states were re-derived from live GitHub several times because
remembered/cached values proved wrong once (`.session-journal.md` § Past
mistakes — the #44-vs-#46 upgrade-credit miscount); a maintained machine
ledger would be cheaper than re-listing PRs. (2) KL-1 had to re-derive
`_vendor_bootstrap` / `_ref_mine_log` anchors by grep from KL-0's
symptom-only friction notes — the guard-recipe convention
(`.sessions/README.md` § Guard recipes) was created *because* of that
rebuild. (3) This retro itself had to reconstruct the day's shape from PR
timestamps because no durations were ever written down — see F1.

**C3 — most and least value per minute.** Most: the **dist byte-pin +
born-red card gate** pair — both are one-line checks that caught whole drift
classes repeatedly (the pin caught every unbuilt-dist push; the badge gate is
the only reason half-done PRs read red), and the **full local gate
one-liner** (`.session-journal.md` ⚡ Quick reference) which front-loads CI's
verdict for ~1 minute of local compute. Honourable mention: writing
verbatim command output into reports (fleet review §2) — it made every later
claim checkable. Least value per minute: the **legacy-alias jobs** (a whole
duplicate runner per PR, forever, pending one owner click) and **hand-tending
auto-merge** in the pre-#10 window (arming, watching, verifying — the #7/#9
incidents anyway).

**C4 — redo speed and the ordering change.** Knowing what the lane knows now,
the same output is plausibly **~30–40% faster**: no #7/#9/#22 incident
response (three sessions), no alias-job design, no run-2 seed deviation, no
retroactive CHANGELOG rolling. The biggest **ordering** change: **land the
required-check alignment (P10) before any auto-merge use at all** — it is
the root cause under both recorded incidents; second, **ship the engagement
gate (KL-7) before inviting any adopter** — both fresh adopters stranded
half-engaged in exactly the way KL-7 later made impossible; third, **smoke
the bench harness before the first judged firing** (seed sweep + scorer
regression fixtures — run-1's M1 was unmeasurable for want of it, PR #40
fixed it between runs).

## D. Autonomy & owner input

**D1 — every stop for owner input.** (1) **Bless the first bench rubric**
(#17, ~5¾ h open) — genuinely owner-only: founding plan §5.0 makes the first
rubric version an owner-taste gate, and D-0005 records the blessing. (2)
**PL ratifications** (#22 ratify-or-veto after the mechanical merge; #26
PL-011 still open) — owner-only by the program's own law (owner merge =
ratification). (3) **The F-5 wording decision** — owner-only because the
rubric is a pin path (integrity law: the lab never rules on its own
benchmark's pass bar). (4) **Platform clicks P4/P5/P8/P10/P11/P13** — not
taste but access: every one is unblockable by a standing grant (see D4). (5)
**Branch deletion + required-check settings** — permission-blocked in
session (B1 items 2/4). So: the taste gates were truly owner-only; the
platform gates were only owner-only because no grant existed.

**D2 — routed up but should have been decide-and-flag.** Honestly, few: the
lane's law already pushes hard toward decide-and-flag (PL-001/PL-009), and
the flagged-decision lists in the cards show it was used freely (SemVer
calls, KF-5 standing-row readings, ORDER 003's wide reading). The one
candidate: **the MIT license** was handled exactly right as a flagged
default (applied at KL-1, P8 confirm pending) — and the same
apply-default-and-flag shape could have been used for the **auto-delete-head-branches setting request** instead of carrying it as a
recurring ⚑ line. Against that: the F-5 decision and the PL ratifications
*look* routable but are not — the pin-path and ratification laws make the
upward route mandatory, and this review endorses that.

**D3 — decisions taken while unsure, and the rule that would fix it.** (1)
Widening ORDER 003's literal wording (B4.2) — taken, flagged, correct; the
missing rule: *"when an order's literal reading strands existing adopters or
contradicts a shipped invariant, the wider reading is sanctioned
decide-and-flag."* (2) Citing a **standing** B1 row for KF-5 at v1.2.0/v1.3.0
instead of firing fresh (both flagged) — the missing rule: one sentence
defining KF-5's freshness requirement per release class. (3) Run-2's
mid-run **seed bump 424242→424243** when the seed generator produced a
SyntaxError — taken under the run manifest's deviation rule and recorded;
that rule existed and worked, which is what the other two cases were missing.

**D4 — smallest standing-grant set for zero-human end-to-end.** Four grants:
(1) **repo Settings write** scoped to rulesets/required checks + the
auto-delete-head-branches toggle (kills P10-class stalls and branch-cleanup
asks); (2) **a read-only cross-repo path** — public flip (P11) or a
read-only PAT (P13) — unblocking B2–B4 sweeps and adopter verification; (3)
**tag/release permission or a release bot identity** (retires the
`workflow_dispatch` detour — though the detour works and is cheap); (4) **a
pre-blessed first-rubric procedure** (e.g. "owner blesses the rubric *spec*;
the first instantiation ships if byte-faithful to the spec") — the one
taste-gate that cost real wall-clock. Everything else the lane needed, it
already had.

**D5 — was "done" always defined?** For inbox orders, yes — every ORDER
carries a `done-when:` line (`control/inbox.md`) and they were checkable
(release exists, file exists, status acks). For bands, yes — the founding
plan's §10 rows. Two places "done" was genuinely underdefined: (1) **what a
release requires of KF-5** when the paired run is pending (see D3.2 — the
letter was satisfiable by a standing row; the spirit was arguable); (2)
**"done" for the run close-out** — the original ledger counted one incident,
and only the independent audit's cross-repo sweep established the honest
count of two (day report §3, journal § Recurring problems). "Done" for an
audit needed "…including consumer repos" written down; it is now.

## E. Protocol & environment

**E1 — did the control/ ritual fit?** Yes — with one honest cost line. All
five orders were acked and executed same-day (inbox timestamps 12:07Z–16:17Z
against done PRs #28/#29 · #31/#32 · #41 · #46 · this one); inbox-first gave
every session an unambiguous starting read, and the never-edit-inbox rule
was never violated (verifiable: every inbox commit is the manager's Contents
API write — PRs #27/#34/#43/#45). Costs: (1) **the status overwrite is a
full PR round-trip per session** — mitigated but not removed by the control
fast lane (D-0008; overwrite PRs #33/#42/#48 merged in 23–37 s); (2) the
inbox's append-only/one-writer rule is **convention-only** — PR #34 merged
19 s after open with zero validation (issue #36 report 2); the ritual's
integrity currently rests on nobody misbehaving. Skipped: never skipped
outright; ORDER 005 (P1) was deliberately deferred behind ORDER 004 (P2)
against the priority rule, flagged in the ORDER 004 card (⚑ flag 1) — the
right call (a rider retro would have been the rushed, flattering thing the
order forbids), but it was a deviation and is recorded as one.

**E2 — what the ENVIRONMENT should have contained at first boot.** (1) A
**working setup script** — the one configured killed a session (B1 item 11;
PR #47); the corrected script now exists as a doc the owner must paste. (2)
**pytest + ruff preinstalled for python3.10** — sessions repeatedly
`pip install --user` them; the CI floor (`python3.10`, not bare `python3`)
had to be learned and journaled. (3) **A GitHub read surface that includes
branch protection** — the 403/405 family (B1 items 3/4) and the
required-check blind spot all trace to the ambient environment exposing
neither `gh` nor a ruleset reader. (4) Documented **proxy limits** (tag
push, branch delete) so the first session doesn't discover them by 403.

**E3 — what the REPO should have contained at seed.** (1) **Required checks
aligned to the CI the repo actually ships** — the owner-landed ruleset with
legacy context names is the single most expensive seed defect (alias jobs,
#7, contributor to #22). (2) **The control/ bus from day one** — it arrived
at KL-8 (PR #31) and immediately became the coordination spine; before it,
coordination facts lived in PR bodies and relayed chat. (3) **A session
journal seeded with the platform's known limits** (tag-push 403 etc.) rather
than each lane discovering them. (4) **A PR template** — `.github/` has none
(checked); PR bodies converged on a good shape by imitation, but a template
would have made the ritual (born-red card link, gate results, flag list)
mechanical. (5) The **bench harness smoke suite** at the same commit as the
harness itself (C4).

**E4 — what a fresh session would misunderstand first.** The **born-red
discipline**: a fresh session sees a red required check on its own first
commit and every instinct says "fix CI" — the repo's convention is that the
red *is* the ritual (card flips complete as the last commit, then green).
The one document that prevents it: **`.session-journal.md`** (its ⚡ Quick
reference states the session shape in four lines) — it exists and works;
what's missing is only that nothing *forces* a fresh session to read it
first (the CLAUDE.md/AGENT_ORIENTATION read-path makes it likely, not
mandatory). Second-place misunderstanding: that `dist/bootstrap.py` is
generated (edit `src/engine/`, rebuild, byte-pin) — also journaled, also
only advisory.

## F. Redesign (the payload)

**F1 — three founding rules the next Project should get that this one
didn't.**

1. *"Verify the repo's required status checks name exactly the gate your CI
   produces **before** your first auto-merge; if you cannot read them, get
   the owner to state them, and treat every mismatch as a stop-ship."* —
   Both recorded incidents and the #7/#9 near-misses share this root
   (day report §3; `docs/current-state.md` § P10).
2. *"Every PR that changes user-visible behavior carries its CHANGELOG
   `[Unreleased]` bullet in the same diff; every session card records
   wall-clock start and end."* — The first half is the #40/#35 lesson
   (entries rolled retroactively at v1.3.0); the second half is why C1 above
   is an estimate instead of an answer.
3. *"An oracle you built gets smoked before it judges: generators sweep
   their input space, scorers run against known-bad fixtures, before the
   first recorded verdict."* — run-1's M1 was unmeasurable (three
   scorer-taint pairs) and run-2 lost its planned seed to a SyntaxError the
   sweep in PR #49 now catches at draw time.

**F2 — what the manager should have done differently.** The order shape was
good — pointer + why + done-when is exactly right, and same-day execution of
all five proves the sizing was workable. Three improvements: (1) **sequence
against priority inversions** — ORDER 005 (P1) landed mid-flight under a
running P2 session (#45 at 16:29Z, during ORDER 004), forcing the lane to
choose between the priority rule and retro quality (E1); a "queue after
current" marker would have removed the conflict. (2) **ORDER 003's wording**
assumed template-edit = fleet-delivery; the manager relaying *intent*
("every adopter self-reports, existing ones included") rather than
*mechanism* ("add a line to the template") would have avoided the
interpretation risk the session had to flag. (3) **Relay platform facts
with the order** — ORDER 001 fired the bench without relaying that the
runner queue can lag ~12 min, which became half of incident #22.

**F3 — one capability worth almost anything.** **Reading repo settings
(rulesets/branch protection) from inside a session.** It is the smallest
grant with the largest counterfactual: with it, the alias jobs are never
built, #7 and #22 don't happen as they did, the fleet review's three
"unverifiable required check" rows become one API call each, and adopter
verification stops needing owner glances. Write access would be better;
read alone removes the blind spot.

**F4 — ideal seed state, ≤10 bullets.**

- Required checks on `main` naming the shipped gate exactly (one context,
  `kit-quality`-shaped), auto-merge ON, auto-delete-head-branches ON.
- The control/ bus (inbox/status/README contract) planted at seed, with the
  status fast lane and its scoped status gate already in CI.
- `.session-journal.md` pre-seeded with the platform's known limits
  (tag-push 403, branch-delete 403, API 403, runner-queue lag, MCP
  staleness) instead of a blank guidebook.
- The born-red session ritual + PR template in `.github/`, so the ritual is
  mechanical from PR #1.
- The engagement gate (KL-7 shape) in the first release any adopter ever
  sees — adopt must end by printing the TODO checklist it enforces.
- Bench harness *with* its smoke suite (seed sweep, scorer known-bad
  fixtures) and the pin-path/label-gate law, before the first judged run.
- A CHANGELOG-touch advisory for engine-diffing PRs, and durations
  (start/end) as required card markers.
- A read path to repo settings (or a committed, owner-maintained statement
  of them) available to every session.
- Environment: python3.10 + pytest + ruff preinstalled; a setup script that
  cannot kill the session (guarded, `exit 0`).
- Telemetry from row one: model/effort/class *and* time, so the first retro
  can answer its C-section from data.

## G. Addendum — KIT

**G1 — what in the adopt UX invites half-engagement, and the fix beyond
gates.** `adopt` **plants-and-banners but nothing in its output ever forced
the last mile**: pre-KL-7, a successful `adopt` printed success while
render, enforcement wiring, and the first session were separate opt-in
steps — "adopt succeeded" *reads as done*, and both fresh adopters stopped
exactly there (fleet review §1.3/§1.4; the founding evidence for D-0006).
The double-adoption shape is the same UX gap one level up: nothing in adopt
detects "this repo already hosts a Project" and routes the second lane to a
lane-add flow instead of a second full adopt. Kit-side fixes beyond the
KL-7 gate + PL-011: (1) adopt now **ends by printing the engagement
checklist as a TODO script** (shipped, PR #25 — the closing findings list
*is* the to-do list); (2) the #47-class environment doc — a session that
dies at provisioning never reaches the checklist, so the setup-script doc
is part of adoption UX; (3) the `adopt --lane` scaffold idea
(`.sessions/2026-07-09-order004.md` 💡) so the shared-repo second lane has a
one-command shape instead of hand-edits.

**G2 — adopter telemetry in priority order, with cheapest KF-2-clean
transport.** (1) **`kit: v<X.Y.Z> · check: green|red · engaged: yes|no`
heartbeat lines** — shipped (ORDER 003, PR #41): tells the coordinator
version spread, gate health, and engagement in one relayed line; transport
is the **existing status.md heartbeat + manager relay** — zero new access,
the registry (`docs/adopters.md`) is fed entirely by it. (2) **Guard-fire
aggregates** (which checkers fire, how often, per repo —
`.substrate/guard-fires.jsonl` exists adopter-side since KL-3): would tell
the lab which guards earn their keep and which nag; transport: counts
summarized into the same relayed heartbeat or a friction issue — no new
access. (3) **B2 paired-run rows from adopter repos** — the only one
needing new access (P11 public flip or P13 read-only PAT); until granted,
manager-relayed run summaries substitute. The principle across all three:
the cheapest transport is always the channel that already exists — the
status heartbeat — and it stays KF-2-clean because adopters self-report and
the lab never writes outward.

**G3 — release cadence: right pace or churn?** The question was written at
three releases; the day ended at **five version cuts dated 2026-07-09**
(v1.0.0 birth + four MINORs, `CHANGELOG.md`) — so answer it at full
strength: **as a steady state this would be churn, and the fleet already
shows the cost** — the registry (`docs/adopters.md`) has adopters at
v1.2.0 while HEAD is v1.4.0, and superbot's pin sits four releases behind
(⚑ carried in `control/status.md`). As a **bootstrap-day pace it was
right**: each cut was demanded by a real consumer event (birth; KL-7+bench;
ORDER 002's ship-the-protocol done-when; ORDER 003's visibility band; ORDER
004's live adopter misfire), and the upgrade path is cheap and self-checking
(checklist in every release's notes, `upgrade` verb, sha256 assets). Ideal
rhythm once the fleet stabilizes: **batched MINORs on a roughly weekly
cadence** (orders accumulate into one cut; adopters walk one checklist per
week, not four per day), PATCH releases reserved for a broken-gate class of
fix, and the KF-5 pairing run riding each batch instead of each ripple.
