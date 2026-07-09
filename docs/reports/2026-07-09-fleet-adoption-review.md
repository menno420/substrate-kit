# Fleet adoption review — 2026-07-09 (owner-directed)

> **Status:** `audit` (dated snapshot — written by the fleet-adoption-review
> session, PR [#35](https://github.com/menno420/substrate-kit/pull/35);
> source code and merged PRs win over this file)
>
> Owner-directed review of how every fleet repo handles the kit, consolidated
> from five completed read-only assessments (substrate-kit · superbot ·
> superbot-next · websites · context self-sufficiency), each verified against
> files / git history / the GitHub API — not report prose. Assessment tips:
> substrate-kit `4a7edc7` · superbot `7480a5f` · superbot-next `27e5277` ·
> websites `992c045`. Kit reference: v1.2.0
> (asset sha256 `258ab02a…`).

## 0. Executive summary

The kit keeps its own promises — the engagement gate demonstrably fires on a
half-adopted install and the v1.2.0 release assets are byte-identical to the
tag and to main — and the fleet's worst adoption state (superbot-next: 10
unrendered docs on main behind a false-green v1.0.0 dist) is already being
closed by the live rollout session (superbot-next #69, websites #31), whose
work this review verified and deliberately did not duplicate. One medium
kit defect was shipped in this review's own PR (the control fast lane
skipped the one checker that validates control files); six further gaps were
filed as friction issues (#36–#39); five decisions are ⚑ needs-owner,
headlined by the **cite-never-copy vs. superbot-independence tension (§4)**,
which is explicitly routed to the owner, not resolved.

| Repo | Verdict | One line |
|---|---|---|
| substrate-kit | **OK** | Promises verified (gate fires, release integrity, bench append-only); med fast-lane gap → **fixed in PR #35**; P10 ruleset swap still owner-gated. |
| superbot | **OK (pin-only)** | Deliberately not an adopted install; native machinery fully engaged (866 cards, born-red gate in required CI); pin 2 releases behind with the upgrade lane unowned; telemetry-append leak → sibling fix PR. |
| superbot-next | **DEGRADED** | Kit genuinely installed but fails the ENGAGED bar on main: 10 unrendered docs, false-green v1.0.0 dist, gate in a NON-required CI job, session loop/telemetry unused. #69 covers the two biggest gaps; the required-check weakness remains after it. |
| websites | **OK (recovered)** | The morning "zero CI" finding is stale: self-engaged same day (33 CI runs, session_count 12, ORDER 001 done); residual gap set = exactly rollout PR #31's scope. Repo is one day old — cadence unproven, not broken. |

## 1. Per-repo findings

### 1.1 substrate-kit — OK

Verified-clean: v1.2.0 release assets == tag `v1.2.0` (`4f4f1ba`, ancestor of
main) == origin/main `dist/bootstrap.py`, all sha256
`258ab02aa54811d91b013f67a15d4bf13e8fc917421434746dd3ca26bc59098c`,
release.json self-consistent (§3.3); `bench/results/` history append-only
intact (single non-add commit `d4f31f5` verified a pure `[]`→1-row append);
no unrendered banners/slots in the kit's own docs; `check --strict` on a
scratch copy of main exits 0; CI green on the last 8 main runs; exactly one
open PR (#26 — owner-review by design, untouched by this session).

| # | Gap | Sev | Evidence | Durable fix | Disposition |
|---|-----|-----|----------|-------------|-------------|
| 1 | Control fast lane skipped `check_status_current` — the only checker that validates the files a control-only PR changes. A heartbeat-deleting control PR rode the lane GREEN while `check --strict` exits 1; the red deferred onto the NEXT unrelated PR. Same lane planted into every consumer via `substrate-gate.yml`. | med | `.github/workflows/ci.yml` lane detect + `if:` guards (pre-fix); `src/engine/checks/check_status_current.py:10-27`; before/after demo §3.2 | Status-scoped gate step ON the lane: `check --strict --status-only` (new scoped mode) in kit CI + the planted template; pinned by tests | **SHIPPED — this PR (#35)**; D-0008 |
| 2 | `control/inbox.md` one-writer/append-only rule convention-only; inbox writes ride the lane with zero validation (PR #34 merged 19 s after open). | low-med | PR #34 timestamps (API); `control/README.md:13-16`; no inbox checker exists (grep) | Control-lane inbox checker: pure-append diff vs merge-base + ORDER grammar; honesty note that writer identity is unenforceable in-repo | **FILED** [#36](https://github.com/menno420/substrate-kit/issues/36) |
| 3 | Engagement gate's `enforcement-unwired` leg satisfied by a workflow COMMENT containing `check --strict` (demonstrated: 0 findings on a comment-only fixture). A repo can look ENGAGED with a dead door. | low | `src/engine/checks/check_engagement.py:123-139`; demo in the assessment §c1 | Strip `#`-comment content before the substring test + known-bad fixture test | **FILED** [#36](https://github.com/menno420/substrate-kit/issues/36) |
| 4 | PL-011 ("adoption is not done until ENGAGED") is not program law on main — register ends at PL-010; PL-011 rides open owner-review PR #26 while the checker (KL-7) has shipped since v1.1.0 (enforcement precedes the law's ratification). | low | `docs/program/rulings.md` (last block PL-010); PR #26 open, `do-not-automerge` | None agent-side — correctly parked per §8.3 | **⚑ needs-owner** (merge #26 = ratify) |
| 5 | 👤 P10 unfinished: the main ruleset requires the two LEGACY contexts served by `legacy-alias-*` bridge jobs, not `kit-quality` — documented root cause of incident #7 and contributor to #22; burns an extra runner per PR. | med | `ci.yml` alias jobs; `docs/current-state.md` §P10; `control/status.md` ⚑ line | Portal action: swap required checks to `kit-quality`, delete the aliases | **⚑ needs-owner** |
| 6 | Benign ledger lag (current-state "In flight" still names #32; ORDER 003 unacked at assessment time). | low | `docs/current-state.md`; `control/inbox.md` ORDER 003 | Per-session ritual covers it | this session acks 003 in its status overwrite |

### 1.2 superbot — OK (pin-only, the origin substrate)

Assessed against its documented, deliberate stance: **pin-only, not an
adopted install** (`telemetry/README.md`, `.sessions/2026-07-09-kit-version-pin.md`).
Native machinery fully engaged: 866 session cards, 6 PRs merged the
assessment day, born-red session gate in required CI. Docs clean (no
banners/slots — no kit-planted docs at all; the native doc set predates the
kit).

| # | Gap | Sev | Evidence | Durable fix | Disposition |
|---|-----|-----|----------|-------------|-------------|
| 1 | `kit_version` pin = 1.0.0 vs latest v1.2.0 (2 behind) and the upgrade lane is **unowned** — kit agent-queue item 1 names superbot, but 0 open PRs and an empty claims dir; the rollout session targets superbot-next + websites only. | med | `substrate.config.json` (PR #1879); kit queue item 1; `list_pull_requests` → `[]` | Manager-side pin-freshness sweep (compare consumers' `kit_version` vs latest release → ORDER when stale). Whether superbot upgrades is a stance change (pin-only → adopted). | **⚑ needs-owner** (stance) |
| 2 | PL-011 tension: pin = adoption evidence, but no workflow contains `check --strict` → superbot would red `enforcement-unwired` despite the fleet's strongest native enforcement — a false positive on the origin repo. | low (latent; med on upgrade) | `check_engagement.py:70`; grep over superbot workflows = 0 hits | Kit-side: define the "native-substrate consumer" state (input to the PR #26 ruling, not a change to it) | **FILED** [#37](https://github.com/menno420/substrate-kit/issues/37) |
| 3 | Telemetry append rule unenforced and already leaking: 3 rows in `telemetry/model-usage.jsonl` while ≥4 card-adding sessions since the lane shipped appended nothing. | med | `wc -l` = 3; card-vs-telemetry git timestamps | Extend the session gate: a card-adding PR must also touch the telemetry feed (engage-only-on-card-adding, no deadlocks) | **SHIPPED by sibling session**: [superbot #1894](https://github.com/menno420/superbot/pull/1894) (`claude/telemetry-gate-guard`) |
| 4 | No `control/` heartbeat in superbot (coordinator Project's control files live in superbot-next) — manager reads superbot only via the fleet manifest. | low | `git ls-tree` → no `control/`; PR #1892 diff | Manager decision: seed status.md in superbot or record the covering-heartbeat in the manifest | needs-manager (routed via this review's visibility to the owner/manager) |
| 5 | Rollback vacuous on a pin-only host: no vendored dist / `.substrate/` → upgrade would run as fresh install with nothing banked; `--rollback` restores nothing. | low | `find` = 0 hits; `src/engine/upgrade.py:329-357` | Kit one-liner: upgrade on a pin-only host prints "first-install: no prior state banked — rollback will be a no-op" | filed as part of #36's triage note (kit-side polish; ride the next engine pass) |
| 6 | Telemetry README class-count drift: superbot says 8 task classes; kit law (PL-010) says 9. Stale local copy of law — the KF-6 cite-don't-copy instinct, violated by a count restated locally. | low | superbot `telemetry/README.md`; kit `rulings.md:218` | One-line superbot doc fix (8 → 9) or point at the kit README | suggest to superbot's next session (out of this repo's write scope) |

### 1.3 superbot-next — DEGRADED

Kit machinery genuinely installed (vendored dist, config, `.substrate/`
state, CI runs `check --strict`, control/ planted, upgrade/rollback path
proven intact) — but the repo fails the ENGAGED bar on main.

| # | Gap | Sev | Evidence | Durable fix | Disposition |
|---|-----|-----|----------|-------------|-------------|
| 1 | **10 docs unrendered on main** (UNRENDERED banner + `${...}` slots incl. `CONSTITUTION.md:1`, `docs/current-state.md:1`); status.md itself admits the current-state template is unrendered. The exact "looks onboarded, isn't" stranding PL-011 names. | high | grep at `27e5277`; PR #69 body (8 open slots) | v1.2.0's KL-7 engagement findings make it self-enforcing once the dist is upgraded AND the gate is required | **covered-by-rollout** (PR [#69](https://github.com/menno420/superbot-next/pull/69)) |
| 2 | **kit_version pin = 1.0.0 → false-green checks**: the v1.0.0 dist predates `check_engagement` (`grep -c check_engagement bootstrap.py` = 0), so local/CI `check --strict` exits 0 at main despite gap 1. The checker fleet is only as strict as the vendored dist. | high | config/state/`bootstrap.py:82`; local run exit 0 | Pull-based §4.3 upgrade | **covered-by-rollout** (#69 — sha256 target verified correct) |
| 3 | **Kit gate installed but NOT required, and weaker than the wired form**: `ci.yml:61-62` runs plain `check --strict` (no `--require-session-log`, no diff-aware card, no control lane) in the non-required `checkers` job. Proven non-required: PR #51 merged with `checkers` red; PR #68 merged 37 s after open with its `report` check failing after merge. Branch-protection API read denied to agents (§ friction f). | high | ci.yml:61-62; PR #53/#68/#69 bodies + check-run timestamps | Owner designates the gate REQUIRED; workflow gains the wired form | **⚑ needs-owner** (required-check) + **FILED** [#38](https://github.com/menno420/substrate-kit/issues/38) (workflow half, post-#69) |
| 4 | Session loop not running: `session_count` 0, 2 kit-plumbing cards vs ~68 merged PRs — the repo's real memory (`docs/status/`, D-ledger) is high quality but outside the kit loop; post-upgrade `session-loop-idle` still passes on the 2 old cards, so only #3's `--require-session-log` enforces it. | med | state.json; `ls .sessions/`; PR list | `--require-session-log` in a required gate | **FILED** [#38](https://github.com/menno420/substrate-kit/issues/38) |
| 5 | Telemetry not flowing: no `telemetry/`, no guard-fires (v1.0.0 dist predates the writers); existing cards never harvested. | med | `ls` at `27e5277` | v1.2.0 dist (#69) + first `session-close` harvest | dist half covered-by-rollout; harvest ritual remains open (see §5) |
| 6 | control/ heartbeat stuck: status.md on main is still the manager-seeded placeholder; the project's own first heartbeat (PR #60, 12:28Z) is open and stale (describes work that shipped hours ago); ORDER 002 unacked. | med | main status.md; PR #60; inbox | v1.2.0 `check_status_current` + control fast lane (with the #35 status gate); the repo's own session should overwrite fresh and close #60 | flagged to the live build session (not duplicated here) |
| 7 | Upgrade/rollback path INTACT (committed `.substrate/backup/`, upgrade-report, `--rollback` in dist); golden-parity `report` leg red-by-design is documented posture, not a gap. | — | files cited in the assessment | — | no action |

### 1.4 websites — OK (recovered)

Headline re-verification: the morning **"zero CI on main" is NO LONGER
TRUE** — workflow `quality` (id 309945369) created 12:53 CEST the same day
(PR #16), 33 runs by assessment time, kit-check-wired
(`check --strict --require-session-log` + diff-aware card selection folded
into the single `quality` check). The born-red arc is demonstrably live: run
33 on PR #31 failed on the in-progress card — the kit's RED doing its job.
Context the review must weight: **the repo is one day old** (first commit
`aec1cd5` dated 2026-07-09) — "least-engaged this morning" was trivially
true; the correct framing now is *fastest self-engagement in the fleet
today; sustained cadence unproven because there is no history yet.*

| # | Gap | Sev | Evidence | Durable fix | Disposition |
|---|-----|-----|----------|-------------|-------------|
| 1 | kit_version 1.0.0 vs 1.2.0 | med | config; `bootstrap.py:84` | §4.3 upgrade, sha256-verified | **covered-by-rollout** (PR [#31](https://github.com/menno420/websites/pull/31)) |
| 2 | Staged `.substrate/` artifacts carry unfilled `${...}` despite ALL slot_values filled (regeneration lag from pre-slot-fill adopt) — a class the engagement gate does not see. | low | `.substrate/claude/CLAUDE.md:17,27,34,39`; `agents/architect.md:12-14` | #31 regenerates; kit-side regeneration-lag checker | covered-by-rollout + **FILED** [#39](https://github.com/menno420/substrate-kit/issues/39) |
| 3 | No `.claude/` wiring on main (templates staged only) | med | `git ls-tree` → empty | PR #31 scope | **covered-by-rollout** (#31) |
| 4 | `updated:` heartbeat not ISO-8601 (`2026-07-09 (session)`) — fails the v1.2.0 checker on arrival | low | `control/status.md:2` | PR #31 scope 4 | **covered-by-rollout** (#31) |
| 5 | Required-check on main not directly verifiable by agents; indirect evidence positive (PR #31 `mergeable_state:"behind"` occurs only under required-status-checks strict). | low | API 403; no MCP ruleset tool | One owner glance at Settings → Rules; kit-side verify-or-say-unverified | **⚑ needs-owner** (one glance) + **FILED** [#36](https://github.com/menno420/substrate-kit/issues/36) (report 3) |
| 6 | Sustained engagement unproven (1-day-old repo) | info | first commit date | Re-review at the 20-session/20-PR reconciliation mark | noted for the lab loop |

## 2. The kit's own promises — proofs

### 2.1 Engagement gate fires on a half-adopted fixture (KL-7)

Fixture: v1.2.0 `dist/bootstrap.py` (byte-equal to main) → `adopt` → all 13
interview slots answered → `render --live` (0 unfilled placeholders). Then,
verbatim:

```
$ python3 bootstrap.py check --strict
check: 3 finding(s):
  [enforcement-unwired] .github/workflows/: no CI workflow runs `check --strict` — install the staged gate: copy .substrate/ci/substrate-gate.yml to .github/workflows/ (or `adopt --wire-enforcement`).
  [session-loop-idle] .sessions: no session has ever run (session_count 0, no session card) — write the first born-red card under .sessions/ and run `bootstrap.py session-close` at close.
  [status-no-heartbeat] control/status.md: no parseable `updated:` ISO-8601 heartbeat — still the adopt seed? Overwrite the whole file with your real status as the session's LAST step (control/README.md).
check: no session log under .sessions/ (advisory — not a failure).
EXIT CODE: 1
```

Walking the printed checklist (install the staged gate, first complete card,
real heartbeat) → `check: all checks passed.` exit 0. The bare `adopt`
printed `adopt: NOT ENGAGED — check --strict holds RED until these 12
item(s) are done:`. **Gate fires as promised.** (Caveat that became friction
#36 report 1: replacing the workflow with a file containing only
`# TODO someday run check --strict here` still cleared `enforcement-unwired`.)

### 2.2 Control fast lane bypass — before and after the fix (shipped in this PR)

Before (assessor's demonstration, lane logic run verbatim on a fixture whose
control-only PR deleted the heartbeat; reproduced independently by this
session before fixing):

```
lane verdict: control_only=true  -> heavy suite (incl. check --strict) SKIPPED, job reports GREEN
--- what the skipped check would have said:
check: 1 finding(s):
  [status-no-heartbeat] control/status.md: no parseable `updated:` ISO-8601 heartbeat — still the adopt seed? Overwrite the whole file with your real status as the session's LAST step (control/README.md).
check --strict exit: 1
```

After (the new fast-lane step, same broken tree, fixed dist):

```
$ python3 bootstrap.py check --strict --status-only
check: 1 finding(s):
  [status-no-heartbeat] control/status.md: no parseable `updated:` ISO-8601 heartbeat — still the adopt seed? Overwrite the whole file with your real status as the session's LAST step (control/README.md).
fast-lane step exit: 1 -> lane goes RED
```

And a *healthy* heartbeat overwrite on the same lane:

```
$ python3 bootstrap.py check --strict --status-only
check: control-status check passed (--status-only).
fast-lane step exit: 0 -> heartbeat PR still merges fast
```

Fix ledgered as **D-0008**; shipped to both the kit's `ci.yml` and the
planted `substrate-gate.yml` template (adopters receive it with the next
release — no version was bumped by this review, per its mandate).

### 2.3 Release integrity — v1.2.0 assets == tag == main

```
$ git rev-parse v1.2.0^{commit}          -> 4f4f1bacecdc9f4b6c699f29ced84acec52360e9  (ancestor of origin/main: YES)
sha256(dist/bootstrap.py @ v1.2.0)      = 258ab02aa54811d91b013f67a15d4bf13e8fc917421434746dd3ca26bc59098c
sha256(dist/bootstrap.py @ origin/main) = 258ab02aa54811d91b013f67a15d4bf13e8fc917421434746dd3ca26bc59098c
sha256(downloaded release asset)        = 258ab02aa54811d91b013f67a15d4bf13e8fc917421434746dd3ca26bc59098c
$ sha256sum -c bootstrap.py.sha256      -> bootstrap.py: OK
release.json: {version: "1.2.0", sha256: 258ab02a…, breaking: false, requires_state_migration: false,
  min_upgrade_from: "1.0.0", changelog_anchor: …/CHANGELOG.md#120---2026-07-09, upgrade_steps: […]}
```

**No mismatch.** (Note: this review's PR advances `dist/bootstrap.py` on
main past the v1.2.0 asset — expected between releases; the byte-pin
compares dist to a fresh build, and release integrity compares *assets to
tags*.)

## 3. Context self-sufficiency (owner-directed lens)

**Owner's verbatim goal:** *"one of the eventual goals is that each repo
gets enough context of its own so that we can eventually abandon the
superbot repo as source of truth."*

### 3.1 Ratings

| Repo | Rating | Basis |
|---|---|---|
| substrate-kit | **MEDIUM** | Program law + engine fully local; but 6 pointer stubs, the bench task-spec, and the fleet-coordination canonical spec (incl. a template planted into every adopter) live in superbot. |
| superbot-next | **MEDIUM-LOW** | Day-to-day code + a rich D-ledger are local, but the entire rebuild spec corpus (canonical plan, design spec, frozen L0 specs, discovery foundations) and the parity oracle are superbot-resident by explicit design ("read-only oracle"). Concrete drift proof: `parity/README.md` links `../docs/planning/rebuild-design-spec-2026-07-02.md`, which does not exist in superbot-next. |
| websites | **MEDIUM-HIGH** | Best doc self-containment of the three consumers (own architecture/ownership/router/decisions/current-state); residual ties are the runtime JSON feeds produced+committed in superbot, the superbot-resident kickoff plan, and the control canonical-spec pointer. |
| superbot | **N/A — it IS the source** | Canonical home of the program-founding planning docs, the rebuild spec corpus, the Q-router provenance root, the fleet-coordination protocol spec, the bench task texts, and the exporters feeding websites. |

### 3.2 Load-bearing dependency inventory (highlights)

The sharpest single finding: **the kit propagates superbot-dependence to
every future adopter** — `src/engine/templates/control-README.md.tmpl:5`
plants *"Canonical spec: `menno420/superbot` →
`docs/planning/fleet-coordination-protocol-2026-07-09.md`"* into every
adopted repo (and it is compiled into `dist/bootstrap.py`).

Load-bearing (LB) items by repo (full inventory with PROV/INC
classifications in the assessment corpus):

- **substrate-kit**: 4 planning + 2 idea pointer stubs whose canonical body
  is superbot-resident ("never copy the body in"); `bench/README.md:37,39`
  + `bench/rubric/cold-start-rubric.md:12,15` resolve the T1–T5 task texts
  and pass bar to superbot URLs; the control-README template above (+ the
  kit's own `control/README.md:3` copy). The PL-register itself is **clean**
  — ruling bodies are local by design, superbot is audit trail only.
- **superbot-next**: the rebuild's governing documents do not exist in the
  repo — `rebuild-canonical-plan-2026-07-06.md`, the design spec, frozen L0
  specs 01–14, `docs/analysis/rebuild-discovery/foundations/**` are
  superbot-only; `rebuild-amendments.yml` encodes it as architecture
  (corpus roots `superbot:`, rule-4 resolution "advisory-skipped" locally);
  `parity/parity.yml` pins the oracle at superbot `7f7628e1` (goldens ARE
  local — 482 files byte-identical — so replay works offline, but
  re-capture needs the oracle); the question router live-instructs
  cross-checking superbot's Q-router.
- **websites**: `botsite/data_source.py:30` / `dashboard/data_source.py:38,42`
  fetch raw.githubusercontent superbot JSON whose **exporters live in
  superbot**; README links the founding plan at superbot; control README
  pointer. If superbot vanished the sites keep rendering last-committed
  JSON but freeze.

### 3.3 The cite-never-copy law vs. the independence goal — ⚑ NEEDS-OWNER, not resolved here

The law, exactly as written (`docs/program/README.md` § "The citation rule —
cite, never copy", item 2):

> **Consumers cite PL-IDs, never copy bodies.** Planted
> CONSTITUTION/collaboration-model templates carry a short "Program law"
> pointer section (this directory's URL + the PL-IDs). A consumer's local
> decision ledger / question router holds **repo-local** rulings only; when
> a local ruling is promoted program-wide, its local block is replaced by a
> pointer to the new PL. A copied ruling body in a consumer repo is drift by
> construction — two texts, one law, no sync mechanism.

Ledgered in the kit's decisions ledger as the founding cite-never-copy
ruling (2026-07-09, "consumers cite, never copy"), checker-enforced
(`scripts/check_program_law.py`), and
the same instinct governs the pointer stubs ("if superbot moves it, update
the URL here, never copy the body in").

The tension: for **program law proper** there is no conflict — KF-6 already
moved the canonical home to the kit, and the law works *for* independence.
But the same never-copy instinct applied to the second class of documents
whose one home is **superbot** (the 4+2 stubs, the bench spec, the fleet
protocol cited from a template planted into every adopter, the websites
kickoff plan, and superbot-next's entire rebuild corpus) **structurally
prevents those repos from ever becoming self-sufficient**: copying in is
"drift by construction" (and, for PL-shaped text, a CI finding), while
citing keeps superbot load-bearing forever. No agent can migrate them
unilaterally without violating that ruling's spirit.

Three possible carve-out shapes (options for the owner — a new PL-block or an
amendment/supersession of the cite-never-copy ledger entry; **this review
deliberately does not pick one**):

1. **"Move-the-home" (relocation, not copy):** cite-never-copy constrains
   *copies*, not *relocations* — a canonical doc may be moved once to its
   rightful long-term home, with the superbot original replaced by the same
   pointer-stub pattern in reverse. One home preserved at every instant;
   only the address changes.
2. **"Archive-tier snapshot":** declare superbot a frozen archive at a named
   SHA (the oracle pattern superbot-next already uses, `@ 7f7628e1`);
   permit *pinned, checksummed, never-edited* copies of archived-repo
   documents — drift is impossible against a frozen source, dissolving the
   "no sync mechanism" objection.
3. **"Graduate-to-register":** keep never-copy fully intact; *promote* the
   still-live content into kit-canonical documents minted fresh with
   superbot cited as provenance (the exact KF-6 pattern that moved the
   founding rulings). Slower, zero law change; superbot decays to
   provenance-only naturally.

### 3.4 Migration sketch (direction-setting; NOT this-session work)

- **Phase 0** — owner picks a carve-out shape (§3.3); without it only
  no-law-conflict items ship.
- **Phase 1** — cut the *exported* dependency: re-home the
  fleet-coordination-protocol spec into the kit and re-point
  `control-README.md.tmpl` — stops new superbot-dependence from spreading;
  the highest-leverage single move in the fleet.
- **Phase 2** — self-contain the kit's working set: bench task texts +
  pass bar into `bench/` with provenance (the founding plan's KL-5 row
  already half-ordered this); archive-tier annotations on the 4+2 stubs.
- **Phase 3** — superbot-next spec corpus (needs carve-out 1 or 2): import
  the rebuild's governing docs as a sha-pinned, checksummed snapshot
  (mirroring the golden-corpus import mechanics); un-break the
  `parity/README.md` link; flip `rebuild-amendments.yml` corpus roots
  local (rule 4 stops being advisory-skipped — a checker gets stronger).
- **Phase 4** — websites data plane: move the exporters + JSON home per the
  already-planned P6 console move; until the live bot is replaced, superbot
  legitimately keeps producing *data rows* (a product feed, not a
  source-of-truth doc dependency).
- **Phase 5** — provenance freeze + retirement test: declare superbot's
  router/history archive-tier (readable history, never required for
  action), then cold-start a session in each repo with superbot access
  deliberately withheld; friction routes through the kit inbox. Clean runs
  ⇒ superbot can be archived.

Shippable-now shortlist (contained, reversible, no law tension): fix
superbot-next's broken `parity/README.md` link; the Phase-1 re-home +
template re-point; the bench task-text copy-in with provenance;
archive-tier annotations on the kit's 6 pointer stubs.

## 4. Rollout coordination note

The live rollout session (`cse_01CJfdy7YxUw8oXj4Wfngdyc`) is mid-flight on
the v1.2.0 upgrades. Both its PRs were reviewed by this fleet review and
found **correct-so-far; deliberately not duplicated here**:

- **superbot-next [#69](https://github.com/menno420/superbot-next/pull/69)** —
  dist v1.0.0 → v1.2.0 + walk the engagement gate to GREEN. Target sha256
  matches the real v1.2.0 asset digest; scope covers findings 1.3-1/1.3-2;
  its body honestly names the non-required-check weakness and mitigates
  procedurally (auto-merge armed only after the card flips). Re-verify the
  payload diff when pushed (dist byte-match, kit_version in config+state,
  no `${...}` remnants, consumer-edited docs untouched).
- **websites [#31](https://github.com/menno420/websites/pull/31)** — upgrade
  + engagement audit (staged-artifact regeneration, control fast lane
  folded into the single required `quality` check, ISO heartbeat, `.claude`
  wiring). Scope is sound against kit intent; the
  fast-lane-in-one-required-check choice is right.

**Still open AFTER #69 and #31 land:**

1. superbot-next: REQUIRED-check designation for the gate on main
   (owner-only — §5).
2. superbot-next: workflow upgrade — `--require-session-log` + diff-aware
   card + control fast lane (with the #35 status-scoped step) in `ci.yml`
   (**filed**: [#38](https://github.com/menno420/substrate-kit/issues/38)).
3. superbot-next: first telemetry harvest (`session-close`) + a fresh
   control heartbeat — stale heartbeat PR
   [#60](https://github.com/menno420/superbot-next/pull/60) should be
   refreshed-or-closed by that repo's own session; ORDER 002 in its inbox
   is unacked.
4. websites: verify a friction-outbox envelope actually lands post-upgrade.

## 5. Fixed vs Filed vs ⚑ Needs-owner

**Fixed (this review's own increment):**

- Control fast-lane status gate — kit `ci.yml` + planted
  `substrate-gate.yml` + new `check --status-only` scope + tests + D-0008
  (**PR [#35](https://github.com/menno420/substrate-kit/pull/35)**, §2.2).
- superbot telemetry-append leak — shipped by the sibling session as
  **[superbot #1894](https://github.com/menno420/superbot/pull/1894)**
  (branch `claude/telemetry-gate-guard`): card-adding PRs must touch the
  telemetry feed.

**Filed (friction protocol, label `friction`):**

- [#36](https://github.com/menno420/substrate-kit/issues/36) — kit: (a)
  `enforcement-unwired` comment leniency; (b) inbox one-writer/append-only
  unenforced (PR #34 precedent); (c) required-check verifiability for
  agents (document the `mergeable_state` inference or grant a viewer path).
- [#37](https://github.com/menno420/substrate-kit/issues/37) — superbot:
  PL-011 needs a "native-substrate consumer" state (input to the PR #26
  ruling).
- [#38](https://github.com/menno420/substrate-kit/issues/38) —
  superbot-next: workflow half of the gate fix, once #69 lands.
- [#39](https://github.com/menno420/substrate-kit/issues/39) — websites/kit:
  regeneration-lag checker for staged artifacts (filled slot_values,
  unfilled `${...}`).

**⚑ Needs-owner (decisions only the owner can take — each with its one-line
unblock):**

1. **superbot-next: designate the kit gate a REQUIRED status check on
   main** — branch-protection API is denied to agents; non-required proven
   by PRs #51/#68 merging red. Unblock: repo Settings → Rules on
   superbot-next.
2. **Kit 👤 P10: swap the main ruleset's required contexts to
   `kit-quality`**, then the `legacy-alias-*` bridge jobs get deleted
   (root cause of both recorded incidents; burns a runner per PR).
3. **superbot: decide the v1.2.0 upgrade** — the directed lane is unclaimed
   and an upgrade changes superbot's deliberate pin-only stance
   (pin-only → adopted install).
4. **Cite-never-copy carve-out ruling** for the superbot-independence goal
   (§3.3 — pick shape 1 / 2 / 3 or a mix; everything in §3.4 beyond the
   no-law-conflict items waits on this).
5. **websites: one glance at Settings → Rules** to confirm the `quality`
   check is required on main (agents can only infer from
   `mergeable_state`).
