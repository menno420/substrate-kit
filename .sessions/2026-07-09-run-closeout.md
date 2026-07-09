# Session 2026-07-09 — run-closeout: docs-drift audit + run report

> **Status:** `complete` *(PR #21 — the run-level close-out increment;
> docs-only, steers clear of every PR #17 hunk.)*

**Scope:** the CLOSE-OUT of the 2026-07-09 run (kit PRs #4–#20 + consumer
companions superbot #1879/#1881/#1882/#1883/#1884, superbot-next #42/#46,
websites #11): full checker sweep, docs-drift audit + fixes, the
pending-only ▶ Next action rewrite, and the run-level enders below.

## Drift found → fixed (each verified, not assumed)

1. **CHANGELOG `[Unreleased]` structure**: six Added entries (KL-3 telemetry
   block + KL-2 governance block) were stranded UNDER `### Fixed` — the KL-4
   session inserted its Fixed section mid-Added. Reordered: one `### Added`,
   one `### Fixed` (the two superbot-next#46 upgrade fixes), keep-a-changelog
   shape restored. **PR #17's pending patch re-creates the same defect**
   (its `### Fixed` lands above the existing Added entries) — flagged on the
   #17 thread for a one-line touch-up at the post-blessing merge; can't be
   fixed from here (owner-gated PR, do-not-touch).
2. **current-state stability baseline**: test count `535 after KL-3` → `618
   after groomed-ideas-1 (PR #19)`.
3. **Wrong upgrade credit, verified live**: current-state said superbot-next
   **#44** upgraded the vendored dist to v1.0.0 — live GitHub shows #44
   merged prematurely (65 s, card-only; the OLD dist's `check` can't hold a
   born-red card) and **#46** ("completes prematurely-merged #44") shipped
   the actual upgrade. Fixed with the incident note.
4. **Stale in-tree-copy reference**: superbot #1879's pin no longer sits
   "next to its in-tree copy" — superbot #1882 removed the in-tree
   `substrate-kit/` tree. Noted at the D2 line.
5. **Recently shipped was missing #20** (pinned-feed-contract doctrine
   capture; provenance superbot #1884 + websites #11 incl. the live
   dict-vs-list consumer bug caught by the contract pass). Row added; the
   #18 row now names its companion superbot PR **#1883** explicitly.
6. **`.session-journal.md` was still all placeholder stubs** after a 17-PR
   run — seeded: quick-reference gate commands, boot notes, four recurring
   problems (tag-push 403 → dispatch path; hand-merge until P10; the
   MCP/enabler race; the CHANGELOG insert trap), two past-mistakes.
7. **Checked, NOT drift**: `telemetry/model-usage.jsonl` is current (6 rows;
   the kl2 card predates the KL-3 feed and stays deliberately unharvested per
   the KL-3 card's ⟲); ideas README backlog/shipped states all match
   frontmatter; `.sessions/README.md` current. **Left alone deliberately**:
   the current-state In-flight bullets + Stability KL-5 tail still say "PR
   #16 (this session)" — stale, but PR #17's patch rewrites exactly those
   hunks; fixing them here would manufacture a conflict with the open
   owner-gated PR.

## ▶ Next action rewrite (the groomed-ideas-1 ⟲ improvement, implemented)

`docs/current-state.md` ▶ Next action is now **pending-only by convention**
(stated inline): six owner gates first, each with a one-line unblock (#17
blessing → B1; P4 → D3; P10 → alias-job deletion; P5 → P6 move; P11-or-P13 →
cross-repo reads; P8 license word), then the six-item agent queue in order
(B1 firing post-#17 · v1.1.0 post-B1 with the KF-5 mandatory-benchmarks note
· PL-004 `feature build` discuss PR · KL-6 blocked pieces as gates open ·
legacy-alias deletion post-P10 · superbot-next 📊-needle verification on its
next upgrade). The DONE paragraphs (KL-6 ✅ rows, the PR #19 recap, the
"done and no longer next" list) moved out — Recently shipped already
carries them.

## Run report (run-level enders — the RUN's, distinct from per-session)

### ⚑ Self-initiated ledger (one line per deviation, decide-and-flag)

1. **LICENSE MIT applied** as the flagged default at KL-1 (PR #8) — owner
   confirm still pending (👤 P8, gate 6).
2. **Legacy-alias bridge jobs** invented in `ci.yml` (PR #6) when the owner
   ruleset landed mid-band pinned to the kickoff's job names.
3. **Enabler fresh-label race guard** (PR #17) after the enabler armed a
   `do-not-automerge` PR at open — disarmed by hand, then guarded.
4. **B4 rows dated `merged_date` pre-merge** (PR #19, its flag 1) — same-day
   merge assumed over a second post-merge PR.
5. **Console-contract filename/home chosen unprompted** (superbot #1884) —
   the pinned feed contract doc placed and named without an owner call.
6. **Websites dict-vs-list bug fixed on sight** (websites #11) during the
   consumer-side contract pass — root-cause fix, not a workaround.

### 💡 Session idea (the run's one new idea, dedup-checked)

**CHANGELOG `[Unreleased]` structure checker** — filed with B4 frontmatter
at `docs/ideas/changelog-unreleased-structure-checker-2026-07-09.md` +
README backlog entry. Evidence-driven friction→guard: two sessions in ONE
run (PR #14 on main, PR #17's pending patch) independently inserted a
mid-section `### Fixed`, and nothing catches it — `check --strict` covers
docs hygiene but not CHANGELOG shape. Guard recipe in the file
(`scripts/check_changelog_structure.py` + test + one `kit-quality` step);
sequenced after #17 merges so it's born green.

### ⟲ Previous-session review — the previous RUN (kickoff, PRs #1–#3)

Honest remark: the kickoff did the extraction right — full tree + 440 tests
in one PR, a real cold-adoption smoke in CI from PR #2, CODEOWNERS — but its
**throwaway CI job names became load-bearing**: the owner ruleset (landed
mid-KL-1) pinned "Kit test suite" / "Cold-adoption smoke" as required
contexts, and this run paid for it with the legacy-alias bridge, two live
merge-gate holes (#7 skipped-alias satisfying a required check, #9 merging
before close-out), and the still-open 👤 P10 swap. KL-0's card already
flagged "arm the ruleset the moment CI exists"; the run-level lesson is one
step earlier. **Concrete workflow improvement:** the kit's seed/kickoff
path should name the required-check-shaped job its durable name from the
FIRST CI commit (the plan's §3.2 one-job `kit-quality` shape) and say so in
the PR body — an owner-side ruleset click can only bake in whatever names
exist when it happens. (The planted `substrate-gate.yml` already does this
for consumers; the lesson is for future repo kickoffs.)

### What surprised / blocked / delighted (real data points from the cards)

- **Surprised:** the owner ruleset appearing mid-band already pinned to
  legacy job names (#6 — coordination-by-portal is invisible until it
  bites); the auto-merge-enabler arming a `do-not-automerge` PR because the
  label call races the payload snapshot (#17); GitHub counting a *skipped*
  required check as satisfied (#7).
- **Blocked:** tag-push 403 through the git proxy (release path redesigned
  to `workflow_dispatch` in-Actions tagging — friction #15 report 2; v1.0.0
  cut that way); MCP file-read staleness during cross-repo verification
  (friction #15 report 1 → lab-loop prompt cross-check step); the owner
  gates themselves (P4/P10/P5/P11/P13 — all still pending at close).
- **Delighted:** all three merge-gate holes found live became *enforcing*
  guards the same day (aliases `if: always()` + hard-fail; `in-progress`
  badge counts incomplete; fresh-label re-read); D4 proven end-to-end in
  one day (friction issue #15 filed by a real consumer, triaged same-day,
  one report already a shipped fix); the very first consumer-side contract
  pass catching a live shape defect (websites #11) — the doctrine idea (#20)
  wrote itself from evidence.

## KPIs / verification (checker sweep, this worktree @ origin/main + this PR)

- `python3.10 -m pytest tests/ -q` → **618 passed**.
- Dist byte-pin: `python3.10 src/build_bootstrap.py` → `git diff dist/`
  empty (byte-clean).
- `python3.10 -m ruff check src/engine/` → clean.
- `python3.10 dist/bootstrap.py check --strict --require-session-log
  --session-log .sessions/2026-07-09-run-closeout.md` → exit 1 while this
  card was born-red (held exactly as designed), green at flip;
  `--session-log` also exercised green against the complete
  groomed-ideas-1 card.
- `python3.10 scripts/check_program_law.py` → OK.
- `python3.10 scripts/check_idea_index.py` → OK (re-run after the new idea
  file + README entry).
- `scripts/check_bench_integrity.py` → **N/A on main** — it rides the open
  bench PR #17; runs once that merges.

- **📊 Model:** fable-5 · high · docs-only
