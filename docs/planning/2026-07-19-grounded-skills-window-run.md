# Grounded-skills measurement window — run plan + backlog groom

**Status:** `plan`

Execution plan for the grounded-skills measurement window (opens **2026-07-19**,
target 2026-07-19..26; owner silence accepts) plus a groom of the open ideas
backlog into sized, pickable slices. Authored 2026-07-18 while the buildable
backlog was dry, so the first successor wake on/after 2026-07-19 has turnkey work.

Provenance: fm ORDER 048 standing grant; the pre-registered protocol
`docs/operations/grounded-skills-measurement.md`; wrap report
`docs/reports/2026-07-12-grounded-skills-wrap.md` §3d; heartbeat baton
(`control/status.md` Next-2).

## TL;DR — the honest headline

The window run is **already turnkey and self-authorizing**: the protocol is
pre-registered and frozen (2026-07-15), the harness is built and tested
(`scripts/measure_grounded_skills.py` + `tests/test_measure_grounded_skills.py`),
and no owner sign-off is required — the standing baton authorizes the run and
owner silence accepts the result. So this plan does **not** re-derive the
protocol. Its value is to **de-risk the run** by naming the three traps that
would corrupt or block it (shallow-clone M4, the PL-008 spot-check, report
placement + linking), and to slice the window into pickable units so a wake can
land one slice at a time without holding the whole thing.

## Part A — window-run execution plan

### What gets measured (frozen; amendments are dated in the protocol, never silent)

Four metrics, computed live in one harness run over the fleet roster
(`docs/fleet-repos.txt`), bucketed **before = 2026-07-01..07-11**, boundary day
07-12 excluded, **after = 07-13..run-date**:

- **M1 skill-grounding rate** — session cards referencing a shipped skill.
  Before ~= 0 is pre-committed as expected (skills did not exist pre-07-12); the
  real signal is **after-window uptake**.
- **M2 owner-ask compliance** — six-field + risk-token completeness among
  field-formatted `⚑` ask blocks.
- **M3 capability-ledger activity** — capability append-log lines, bucketed by
  their own date; venue compliance judged only on venue-shaped lines.
- **M4 throughput proxy** — default-branch `(#N)` merge subjects per bucket.

There is **no pass/fail gate**. The deliverable is a published `audit` findings
report with honest nulls. "Owner silence accepts" = the run is authorized by the
standing baton; the published report stands unless the owner objects.

### The three traps (this is why the plan exists)

1. **Shallow clone silently zeroes M4.** A container/CI clone truncates history;
   the harness flags shallow repos and prints M4 as null. **Re-clone full before
   publishing M4** (`--clone` into a fresh `--workdir`; verify depth). Verified
   trap 2026-07-15: 0 before-window merges vs a true count in the hundreds.
2. **The harness is PL-008 UNVERIFIED at first run.** Before publishing,
   **spot-check >=3 per-repo numbers** against the raw files (e.g. hand-count one
   repo's after-window cards and its M1 hits). A number that survives the
   spot-check graduates the harness out of "unverified".
3. **Report placement + linking is a docs-gate surface.** Write the report at
   `docs/reports/2026-07-<DD>-grounded-skills-measurement.md` with Status badge
   `audit`, and **link it from `docs/operations/README.md`**, or the docs-gate
   (reachability) reds the very PR that publishes the finding.

### Sized slices (pick from 2026-07-19 on; land one at a time)

- **GSW-1 · run the harness (S, ~1 session).** From a fresh origin/main
  checkout: `python3 scripts/measure_grounded_skills.py --clone --workdir
  /tmp/gsm --json /tmp/gsm/results.json --out /tmp/gsm/report-skeleton.md`.
  Confirm full (non-shallow) clones; record the private-repo skip
  (pokemon-mod-lab) as an honest skip. Output: `results.json` + skeleton.
- **GSW-2 · spot-check + interpret (S).** PL-008 spot-check >=3 per-repo numbers
  against raw files; apply the frozen interpretation rules (M1-before~=0 expected;
  improvisation proxy = 1 - M1 after, stated with n; nulls published; #247 §6
  confounds carried verbatim). Output: verified numbers + interpretation prose.
- **GSW-3 · publish the findings report (S).** Write
  `docs/reports/2026-07-<DD>-grounded-skills-measurement.md` (`audit`), carry the
  skeleton tables + interpretation, link from `docs/operations/README.md`, and
  flip the baton + the standing ⚑ "silence accepts" block to CLOSED. This is the
  slice that closes the window.
- **GSW-4 · (optional) API latency pass (M). — SHIPPED (PR #477).** The #247 §2
  GitHub-API pass ran from-scratch over all 12 roster repos; no repo nulled.
  Landed as report **§7** (`docs/reports/2026-07-19-grounded-skills-measurement.md`)
  + frozen data `docs/reports/data/2026-07-19-grounded-skills-latency.json` +
  script `scripts/measure_pr_latency.py` (tests `tests/test_measure_pr_latency.py`).
  Headline: fleet median open→merge latency 3.5 min (before) → 4.5 min (after) —
  flat/slightly-slower, confound-heavy (auto-merge-on-green predates the program
  fleet-wide), reported descriptive-only.

GSW-1..3 are the required chain; a single unhurried wake can do all three, or
they split cleanly across wakes. GSW-4 is genuinely optional.

## Part B — backlog groom (2026-07-18)

Swept `docs/ideas/` (README index), the 💡 lines on `.sessions/2026-07-18-*`
cards (the #455–#468 guard-parity era), and the retired/date-parked baton items.

### Buildable-now — named, sized slices a wake can pick

- **B-1 · Guard-surface census meta-test (S, test-only).** A meta-test/doc that
  enumerates ALL enforcing guard surfaces in the kit (ci.yml `kit-quality` steps,
  `bootstrap check --strict` sub-checks, git hooks, any workflow job) and asserts
  each carries a parity pin — so a FOURTH enforcing surface cannot ship unpinned.
  Dedup-checked genuinely new (meta-level over the now-closed 3-surface parity
  thread). Source: PR #466 card 💡. Reversible.
- **B-2 · CI self-row registry-stamp automation (S).** The release-cut card
  defers registry regen to "the aftermath" — the manual hop that leaves the kit's
  own self-row stale in the interim. Automate the self-only half to remove the
  hop. Source: v1.19.0-aftermath card 💡 (Q-0089). Reversible.
- **B-3 · Fast-lane head-prefix <-> enabler branch_patterns symmetry lint (S,
  advisory).** One-file advisory lint asserting the claims-only fast-lane head
  prefixes and the auto-merge-enabler `branch_patterns` stay in sync. Source:
  claims-only-fastlane-guard card. Reversible. *(This is the nearest real,
  unbuilt idea to the dispatch's "claims-guard add-vs-delete false-positive
  exemption" reference — see the honesty note below.)*

### Needs-planning — scope before building

- folded-gate-diff-aware-card, pinned-feed-contract, t5-headless-guard,
  control-board-kit-readiness-cell (all `captured`, no turnkey recipe yet).

### Owner-gated (already ⚑, do not self-start)

- The 23-proposal overnight veto menu
  (`docs/planning/2026-07-16-overnight-veto-menu.md`), including item 15
  (lane-parity added-vs-modified meta-test) — awaits the owner veto pass.
- v1.19.0 adopter wave (~15 currency PRs) — awaits owner authorization.
- The 5 standing ⚑ FOR OWNER blocks in `control/status.md` (kit-lab cron A/B,
  CAPABILITIES denial append, P10 check swap, public-flip-or-PAT).

### Dead / do-not-queue

- **rubric-f5** — historical, RULED.
- **guard-manifest codegen** (drive ci.yml step names from the manifest) —
  RETIRED as a verification-covered null in PR #465; do NOT re-queue.
- **The full 3-surface guard-parity thread** — CLOSED (#459/#463/#465/#466);
  all three enforcing surfaces carry a parity pin. Do NOT re-queue.

### Groom note — stale idea frontmatter

`docs/ideas/guard-parity-kit-vs-adopter-2026-07-18.md` frontmatter reads
`state: captured / outcome: open`, but the idea shipped as PR #459 (extended by
#463/#466). Flagged as stale-open drift; a follow-up may flip it to shipped once
re-confirmed against #459's diff.

### Honesty note — the dispatch's "claims-guard add-vs-delete exemption" reference

No idea or flag using that exact description exists in the tree (searched all
`.sessions/` + `docs/`). PR #466's card 💡 is the Guard-surface census (B-1); its
⚑ flag is the `STRICT_SUBCHECKS` public-API design call. The nearest real
unbuilt ideas are **B-3 (fast-lane head-prefix symmetry lint)** and **veto-menu
item 15 (lane-parity added-vs-modified meta-test)**. Treated as B-3 for the
buildable list; flagged here rather than guessed.

## Bottom line

Tomorrow's wake is not idle: the primary work is **GSW-1..3** (date-gated to
2026-07-19, self-authorizing) and, if a wake needs work before then or in
parallel, **B-1/B-2/B-3** are contained, reversible, test-only/advisory slices.
Everything else is owner-gated or needs scoping.
