# 2026-07-12 — grounded-skills program, slice 5: capability refresh + venue-scoping + staleness

> **Status:** `in-progress`

- **📊 Model:** fable-5 · seat-worker · grounded-skills slice 5

## Scope (what is about to happen)

Implementing §7 slice 5 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263) —
§4.2 in full: venue-scoped capability-ledger schema (venue tokens + extended
append-line grammar, homed in `src/engine/grammar.py` from the start per the
slice-4 lesson), CAPABILITIES.md.tmpl refresh (marker-fenced kit-owned seed
section, venue × operation seed rows with LAST-VERIFIED dates, two-line
posture decision rule, DISCOVERY RULE step 5 staleness clause on the
`cadence.staleness_days` knob), the NEW upgrade-time fenced-seed refresh in
`src/engine/upgrade.py` (the only channel reaching consumer-edited ledgers;
modified fences downgrade to a report line, never clobbered; the report
carries the Q-0270 collapse wording), and `check_capability_xref` extended in
place, advisory-only (append-line grammar + staleness advisories). Tests +
CHANGELOG `[Unreleased]` entry + dist rebuild. No other slices, no adopter
work, no release.

**Provenance flag:** Coordinator proceeded on plan §8 defaults (Q2=B
advisory, Q4=A) — provenance flagged per program rules.

Lane claim: `control/claims/claude-grounded-skills-slice5.md`
(deleted at close, this commit).

## Close-out

Shipped (PR #274; work commit 681f17e):

- **Grammar — one home from day one** (`src/engine/grammar.py`, new
  capability-ledger section, per the slice-4 ⟲ lesson): venue tokens
  (`CAPABILITY_VENUE_TOKENS` = owner-live · autonomous-project ·
  routine-fired · subagent · any), entry tags, the taught append format
  `- YYYY-MM-DD · capability|wall · <venue> · finding · evidence ·
  workaround` (`CAPABILITY_LOG_TAUGHT_FORMAT`, carried verbatim by the
  template, test-pinned), the entry/venue-shape/LAST-VERIFIED regexes, the
  seed-fence BEGIN/END markers (prefix constants for matching so a wording
  tweak can't orphan a fence), and `capability_log_line_example()`
  rendering both the venue form and the legacy five-field form. Enforcer
  identity is test-pinned (checker + upgrade refresher consume the grammar
  module's own objects); old five-field lines are read as venue `any` and
  never flagged — backward compatibility is a pinned contract.
- **`CAPABILITIES.md.tmpl`**: marker-fenced kit-owned SEED block wrapping
  the posture rule + THE DISCOVERY RULE + the seeded Capabilities/Walls;
  the consumer `## Append log` stays outside, never touched. Seed rows are
  (venue × operation) records with LAST-VERIFIED dates. Two-line posture
  decision rule (owner-live = assume no special limitations, act and merge
  directly, superbot Q-0269; autonomous/routine-fired = pre-route around
  known stall classes, park only on a real denial, Q-0270). DISCOVERY RULE
  step 5: an entry older than `cadence.staleness_days` (default 14) that
  your work depends on is a claim, not a fact — one cheap re-verify,
  APPEND the result, never edit (a refuted wall can self-resolve
  platform-side; no freshness data means confidently stale).
- **Upgrade fence refresh** (`src/engine/upgrade.py`
  `refresh_capability_seed`, wired between doc classification and the
  report in `run_upgrade`, mirrored in `run_apply_docs_posthoc`): for a
  consumer-edited/diverged ledger, ONLY the fenced block is re-rendered;
  everything outside is preserved byte-for-byte (test-pinned). A fence the
  consumer modified downgrades to a report line with the restore recipe —
  never clobbered. A pre-fence ledger whose seed region (discovery rule →
  Walls, anchored line-start to dodge the marker's own mid-line
  `## Append log` mention) matches the old template verbatim adopts the
  fence automatically; otherwise a one-time hand-adopt report line. The
  upgrade report gains a "Capability-ledger seed refresh" section carrying
  the Q-0270 collapse note. This is the ONLY channel reaching
  consumer-edited ledgers — `--apply-docs` never covers them.
- **`check_capability_xref` extended in place, advisory-only** (§8 Q2=B;
  PL-008 unverified/kill-switch header on the slice-5 checks):
  `capability-log-malformed` (undated bullet / tag naming neither side),
  `capability-log-venue-unknown` (venue-shaped field-3 token outside the
  grammar set), `capability-entry-stale` (a dated entry — append bullet or
  LAST-VERIFIED seed row, continuations included — older than the config
  window that the newest date-named session card cites, via the module's
  existing anchor-overlap machinery). The OWNER-ACTION xref is unchanged;
  `_ledger_sides` fields[1] tag attribution with a venue column at field 2
  is pinned by test. `cli.py` xref call site gains one argument
  (`config=config`); no other cli surface changed.
- **Tests:** suite **1116 → 1147** (+31: grammar identity/examples/venue
  shapes, template↔grammar pins incl. fence-before-append-log ordering and
  per-row venue+freshness, fence-refresh fixtures — refresh/preserve/
  modified-fence downgrade/legacy adoption/legacy downgrade/improved
  pointer/run_upgrade end-to-end with Q-0270 report wording/post-hoc
  mirror + idempotence — xref grammar + staleness advisories, knob
  default-on-missing, no-card fail-open, strict-exit pins, rendered-
  template dogfood scan).
- **CHANGELOG:** `[Unreleased]` slice-5 entry appended; slice-3 + slice-4
  entries kept.
- **Dist:** rebuilt via `python3 src/build_bootstrap.py` — builder print
  779399 B == on-disk 779399 B; byte-pin suite green.

Verify (verbatim tails): `python3 -m pytest tests/ -q` → `1147 passed in
19.99s` · `python3 -m ruff check src/engine/` → `All checks passed!` ·
`scripts/check_idea_index.py` / `check_program_law.py` /
`check_bench_integrity.py` → OK · `python3 dist/bootstrap.py check
--strict` → exit 0 pre-flip with the designed hold banner naming this
card; zero capability advisories on the kit's own tree.

Accept criteria (§7.5): upgrade on a consumer-edited ledger refreshes only
the fenced seed block ✔ (fixture-pinned, outside-fence byte-equality
asserted); xref checker validates the new grammar ✔ (venue + malformed
kinds, old-format never flagged); superbot's Q-0270 collapse documented in
the upgrade report ✔ (`CAPABILITY_POSTURE_COLLAPSE_NOTE`, test-pinned in
both the in-run and post-hoc report rewrites).

**Decide-and-flag calls (plan silent on the detail):**

1. ⚑ Posture rule placed INSIDE the fence (not the file's blockquote
   header): the fence is the only channel that ever reaches a
   consumer-edited ledger, so kit-owned doctrine that must stay updatable
   belongs inside it. "In the header" is honored as the fence's first
   section.
2. ⚑ Fence refresh runs UNCONDITIONALLY at upgrade, not gated on
   `--apply-docs` — §4.2c's own wording ("refreshed at upgrade the way
   staged artifacts regenerate") names staged-artifact semantics.
3. ⚑ `run_apply_docs_posthoc` mirrors the refresh (the briefed
   recommendation, taken): an operator who skipped the in-run window
   recovers the fence the same way they recover doc improvements;
   idempotent by test.
4. ⚑ A consumer-untouched (`template-improved`) ledger gets a pointer
   line, not a fence-only write — the whole-file `--apply-docs` channel
   owns that class, and a partial write would desync the recorded hash.
5. ⚑ After a fence refresh the doc hash is deliberately NOT re-recorded —
   the file stays consumer-owned and must keep classifying that way
   (test-pinned via `doc_is_untouched` false after refresh).
6. ⚑ Pre-fence ledgers auto-adopt the fence only on a byte-exact old-seed
   match; anything fuzzier downgrades to a one-time hand-adopt report
   line — never a guessed merge.
7. ⚑ Seed LAST-VERIFIED dates set from the evidence dates the plan cites
   (2026-07-10 for the ORDER-006-era rows, 2026-07-11 for the
   create_trigger refutation, 2026-07-12 for the wave/night-review rows) —
   blanket-stamping today would be the inverse of the confidently-stale
   lie.
8. ⚑ The "Environment / routine / Project creation" seed wall now records
   the create_trigger partial refutation (the heartbeat's own OWNER-ACTION
   3 resolution) — exactly the §4.2b self-resolving-wall class this slice
   exists for; its old "queue under the flag token" phrasing was reworded
   neutrally (the PR #273 false-nudge class).
9. ⚑ Staleness citation scan reads the NEWEST date-named card only
   (lexicographic on the `YYYY-MM-DD-` names, never mtime — the CI
   checkout trap), fed by one `config` parameter carrying both
   `cadence.staleness_days` (default-on-missing, the triggers.py:100
   pattern) and `sessions_dir`; `today` is injectable for tests.
10. ⚑ Claim landed in-lane (created+deleted within this PR), the slice-4
    precedent, rather than a separate control fast-lane claim PR.
11. ⚑ The kit's own planted `docs/CAPABILITIES.md` is left on the normal
    upgrade channel (consumer #0 receives the fence at its next
    self-upgrade) — hand-re-rendering it here would blur the mechanism's
    own field test.

## Session enders

💡 **Session idea:** venue auto-detection at session start — a
SessionStart-hook step (or `session-close` preamble) that establishes the
boot-triad venue mechanically (owner-live vs routine-fired vs subagent,
from the harness's own signals, the `Run type: routine · lab` line
precedent) and stamps it into the session card header. Payoff is twofold:
ledger appends get their venue token written from detected fact rather
than self-report, and `check_capability_xref` could then scope its
staleness/citation advisories to entries matching the CURRENT venue
(a stale `routine-fired` wall shouldn't nag an owner-live session).
Dedup-checked `docs/ideas/` (nearest: engagement-native-consumer-state —
different axis; nothing on venue detection).

⟲ **Previous-session review:** slice 4's card is the strongest
prerequisites block of the program so far — all five slice-5 items held
exactly as written (grammar-from-day-one, the twice-proven checker-extension
pattern, the fence as the slice's main engineering with a fixture test, the
`staleness_days` knob name, the Q-0270 report wording as in-slice work),
and "home the venue tokens in grammar.py FROM THE START" saved this session
the exact extraction rework slice 4 had to do. One genuine improvement: its
"extend check_capability_xref in place; NO cli.py changes needed" line
half-held — the advisory *wiring* needed nothing, but the plan's own §4.2d
config parameter required a one-argument cli call-site change; a
prerequisites block that asserts a negative ("no changes needed in X")
should cross-check the assertion against the plan section it summarizes,
or scope it ("no new advisory wiring") so the next worker doesn't read it
as a constraint.

Documentation audit: CHANGELOG entry present (slice-3/4 entries kept); no
new doc needs an index entry; the upgrade-report wording lives in code +
tests, not in a doc needing wiring; the decide-and-flag list above is the
complete set of unrecorded judgment calls. Claim file deleted this commit.
Capability delta: none — no new wall or capability discovered in this
venue (branch push, PR open via MCP, and CI all behaved as recorded).

**Slice-6 prerequisites discovered (fleet-manager single-source render):**

- The `{{WALLS}}` seat-prompt slot's source is now the venue-scoped ledger
  — the seat digest should filter rows by the seat's venue
  (`autonomous-project` + `any` for Project seats), which the venue column
  makes mechanical instead of editorial.
- The fence markers are a stable machine anchor: fleet-manager's regen
  tool can extract the kit-owned seed digest via
  `CAPABILITY_SEED_BEGIN_PREFIX`/`END_PREFIX` without parsing prose —
  document that pair as the extraction contract when slice 6 lands.
- The next distribution wave (first release carrying this slice) runs the
  fence refresh in-run and unconditionally: expect `capability-seed:`
  lines in every adopter's upgrade report — `refreshed`/`adopted` on
  clean trees, the one-time `hand-adopt once` line on any adopter that
  edited inside its old seed region. The wave runbook reading should treat
  the hand-adopt line as a lane-owed item, not a wave failure.
- superbot (deliberate v1.0.0 pin, OWNER-ACTION 7 in the kit heartbeat)
  receives no fence until its pin decision — its Q-0270 local-prose
  collapse therefore waits on that decision; record it in the wave report
  rather than expecting it automatically.
- `docs/gen2/`-era CAPABILITIES copies and the fleet-manager
  `docs/capabilities.md` master are OUTSIDE the planted-doc contract —
  slice 6's aggregation design should state explicitly which copy defers
  to which (the §4.2e "no third copy" rule).
