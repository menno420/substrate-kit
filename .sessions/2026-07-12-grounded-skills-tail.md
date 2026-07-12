# 2026-07-12 — grounded-skills program, §7 tail: routines doctrine, Evidence block, preflight reset

> **Status:** `complete`

- **📊 Model:** fable-5 · seat-worker · grounded-skills §7 tail

## Scope (what is about to happen)

Closing the three graduation-map ❌ rows the grounded-skills plan's §7 tail
left as "a small follow-on" (`docs/planning/2026-07-12-grounded-skills-program.md`
§6/§7 tail; map: `docs/reports/2026-07-12-prompt-template-hardening-input.md`
§(b)): (a) NEW `src/engine/templates/routines.md.tmpl` — the routine /
wake-chain doctrine (binding choice + verify-delivery, verbatim create-call
records, probe-not-record re-verification, scheduler-health wedge signature,
sequential pacing, failsafe blind-window check) planted to `docs/ROUTINES.md`
via an ADOPT_PLAN tuple, routed from orientation; (b) a verify-don't-trust
**Evidence** bullet block in `CONSTITUTION.md.tmpl` (probe-not-record ·
tree-over-heartbeat · job-log-over-check-name · stale-read cross-check ·
false-green = a bug in the CHECK, PL-006 · cite-your-evidence); (c) the
preflight fetch + hard-reset as the explicit FIRST orientation step
(one-line rule in `CLAUDE.md.tmpl`, mechanics in
`AGENT_ORIENTATION.md.tmpl`). Content mined from the hardening report
§a.1/a.3/a.5 and `docs/reports/2026-07-12-trigger-forensics.md`, portably
worded (no fleet ids, no env ids). Tests + CHANGELOG `[Unreleased]` entry +
dist rebuild. No new skill, no new checker, no release, no other slices.

Lane claim: `control/claims/claude-grounded-skills-tail.md` (deleted at
close, in-lane per the slice-4/5/8 precedent).

## Close-out

Shipped (PR #287; work commit rebased onto main @ f6365df after the
wave-A close-out #285 merged mid-session — dist regenerated, suite re-run):

- **`src/engine/templates/routines.md.tmpl` → `docs/ROUTINES.md`** (new
  ADOPT_PLAN tuple in `src/engine/adopt.py`, why-comment citing plan +
  map + forensics H2): six doctrine sections — *Choosing the binding*
  (self-bind dies with its session / re-arm at every seat cutover /
  fresh-session-per-fire lifetime rationale PLUS the verified 0-for-2
  vs 100% delivery caveat, "UNVERIFIED-BROKEN until a scheduled fire is
  proven in your environment", choose-by-lifetime-then-VERIFY, and the
  never-hardcode-env/session-ids rule), *Record verbatim* (id, cron,
  binding, next-fire, same-session heartbeat/log), *Re-verify at every
  wake* (a record is a claim / the live registry is the proof; presence =
  first page, absence = walk to exhaustion; no-tombstone hard deletion),
  *Scheduler health* (wedge signature `enabled ∧ next_run_at < now −
  15min`; healthy triggers advance `next_run_at`; manual `fire_trigger`
  sets `last_fired_at` WITHOUT advancing — never read `last_fired_at`
  alone), *Pacing* (sequential, one write at a time; send_later chain =
  live-seat pacemaker, cron failsafe = dead-man backstop), *Failsafe wake
  pattern* (verify the standing loop's last slot delivered — the blind
  window). Badge `binding`; pointers ride `${agreement_home}` (ORDER 015)
  and route trigger findings to `docs/CAPABILITIES.md`.
- **Reachability wiring:** `AGENT_ORIENTATION.md.tmpl` planted-doc list
  gains `docs/ROUTINES.md` (the backtick ref the reachability walk
  follows) + a when-to-open pointer; `CLAUDE.md.tmpl` routed paragraph
  gains the "before arming, deleting, or auditing any scheduled
  trigger/routine" pointer — the SKILLS/CAPABILITIES sibling pattern.
- **`CONSTITUTION.md.tmpl`** working-agreement bullet "Evidence — verify,
  don't trust": probe-not-record; tree wins over a self-report (`kit:`
  lines lag 1–3 releases); a check is judged by its job log, never its
  name; staleness-sensitive reads cross-checked (~25 min stale MCP PR
  reads); false-green = a bug in the CHECK, not a clearance (PL-006);
  every load-bearing claim cites a commit / PR / tag / run.
- **Preflight first step:** `CLAUDE.md.tmpl` orientation gains step 0
  (`git fetch origin main && git reset --hard origin/main`, or
  `checkout -B`), routing mechanics to `AGENT_ORIENTATION.md.tmpl`
  § "Start every session" — which now carries the command, the
  HEAD-vs-`git ls-remote` verification, and the "stop and report, never
  reset over unexplained work" safety note.
- **Tests:** suite **1184 → 1195** (+11, `tests/test_grounded_tail.py`):
  ADOPT_PLAN tuple pin; 20 doctrine-phrase pins (whitespace-insensitive
  `_flat`); portability pin (no `trig_`/`env_0`/`session_0`/`cse_`/
  fleet-owner strings); agreement/capabilities pointer pins; slot-free
  fresh-adopt render; orientation routing pins; END-TO-END reachability
  (fresh adopt → `run_doc_checks` → no orphan finding for ROUTINES.md);
  Evidence-block pins (in the Working-agreement section); preflight
  step-0-before-step-1 ordering + mechanics pins.
- **CHANGELOG:** `[Unreleased]` tail entry prepended; slice-8 entry kept.
- **Dist:** rebuilt via `python3 src/build_bootstrap.py` — 824,717 B;
  byte-pin suite green (rebuilt again post-rebase, byte-identical).

Verify (verbatim tails): `python3 -m pytest tests/ -q` → `1195 passed in
21.37s` · `python3 dist/bootstrap.py check --strict` → the designed
born-red hold naming this card ("HOLD (by design) … nothing to
investigate"), nothing else.

**Decide-and-flag calls (plan/map silent on the detail):**

1. ⚑ Plant target `docs/ROUTINES.md` — neither plan nor map names one; the
   uppercase sibling convention (`docs/SKILLS.md`, `docs/CAPABILITIES.md`)
   decides it.
2. ⚑ No grammar constants for this slice — the slice-2/3/4/5/8 rule homes
   a phrase only when a writer AND an enforcer consume it; no checker
   consumes these doctrine sentences, so the pins are template-direct in
   `tests/test_grounded_tail.py` (the only enforcer in play, the generic
   reachability walk, consumes a path and is exercised end-to-end).
3. ⚑ No new checker — the map rows are template content; PL-008 not
   triggered.
4. ⚑ Preflight split per the brief's default: one-line rule in
   `CLAUDE.md.tmpl` (step 0, before "1. This file"), mechanics in
   `AGENT_ORIENTATION.md.tmpl` — plus a safety clause the reports imply
   but don't state (hard reset discards uncommitted work by design; work
   you did not author = stop and report, never reset over it).
5. ⚑ Routines template says `origin/main` with a "substitute your default
   branch" note rather than growing a config slot — no bank slot exists
   for the default branch and inventing one exceeds the tail's scope.
6. ⚑ The fresh-session-cron caveat is worded as dated observed evidence
   ("observed delivery was 0-for-2 … (2026-07-12 forensics)") with an
   explicit re-verify-in-YOUR-environment instruction — a platform
   observation planted as eternal truth would itself violate the
   Evidence block this PR adds.
7. ⚑ CONSTITUTION Evidence bullet placed before the `${drift_resolution}`
   line (evidence rules generalize the drift rule) rather than a new `##`
   section — the working agreement is the block the boot set actually
   reads.
8. ⚑ Mid-session main advance (#285) handled per mechanics: rebase →
   dist rebuild → full re-run → force-with-lease push. The
   `.substrate/guard-fires.jsonl` append (this session's own check-run
   telemetry) ships with the close-out commit, the established pattern.

**Honest completeness — is the graduation map now fully absorbed?** The
three ❌ rows this PR targets (routines doctrine · Evidence block ·
preflight step) are now ✅ in-kit. Full-map status, row by row: landing-path
doctrine (`landing-path.md.tmpl` ❌ row) was absorbed by slice 2 into the
`session-close` playbook body rather than a planted template (its named
"template home" was "new template OR playbook skill" — satisfied via the
skill lane); heartbeat-grammar ◐ row (negative `**kit:**` example +
adopters.md deference line in the control templates) — NOT verified
absorbed by any slice card; it was not in this brief's three rows and
remains the one map row without a named owner → follow-on candidate.
Known out-of-lane remainders, unchanged: slice 7 (websites-repo
control-plane guard widening, parallel lane) and the fleet-manager-side
half of slice 6 (regen tool consuming the kit blocks, UNIVERSAL vN bump +
owner re-paste).

## Session enders

💡 **Session idea:** a `doctor triggers` advisory subcommand — the kit
already plants the wedge-signature doctrine (`docs/ROUTINES.md`); a
session with trigger-MCP access could pipe `list_triggers` JSON into
`bootstrap.py` and get the doctrine applied mechanically (wedged /
manual-fire-masked / healthy per trigger, using the same `enabled ∧
next_run_at < now − 15min` rule the doc teaches) — enforce-don't-exhort
for scheduler health. Dedup-checked `docs/ideas/` (registry-snapshot-diff
checker is filed as an idea on the #252/#253 cards per the hardening
report §a.1 guard-status line — that diffs recorded state; this reads
live state, complementary).

⟲ **Previous-session review:** slice 8's card set the bar this session
leaned on — its completeness section explicitly named these three rows as
"remain a small follow-on, not covered by any shipped slice", which is
exactly why this session's scope was derivable without re-reading five
slice cards. One genuine improvement it surfaced (and this card acts on):
its own review noted the "tail work assigned to a slice that doesn't know
it owns it" drift class but still left the heartbeat-grammar ◐ map row
unowned — this card names that row as the one remaining unowned item
instead of repeating the pattern.

Documentation audit: CHANGELOG entry present; the new template is
self-indexing via ADOPT_PLAN + orientation routing; doctrine pins live in
tests; the decide-and-flag list above is the complete set of unrecorded
judgment calls; claim file deleted this commit. Capability delta: none —
branch push, MCP PR open, rebase + force-with-lease, checkers, and the
designed-hold gate all behaved as already recorded for this venue.
