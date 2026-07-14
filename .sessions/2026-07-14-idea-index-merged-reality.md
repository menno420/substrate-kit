# 2026-07-14 — check_idea_index merged-reality leg (grace-windowed git truth)

> **Status:** `complete`

About to (opening declaration): build the `check_idea_index.py`
merged-reality leg from PR #349's session-idea ender (ranked #2 in the
Night-12 triage) — cross-check shipped-idea frontmatter (`shipped_pr`,
`merged_date`, optional `merged_sha`) against actual local git history
(no GitHub API), with a grace window so ideas whose shipping PR is still
in flight never false-red, graceful self-skip on shallow/gitless trees,
plus the four-case mutation test arc.

- **📊 Model:** Claude (Fable family) · high · feature build

Run type: worker session (BUILD phase, coordinator-dispatched).

## What shipped (PR #355)

- `scripts/check_idea_index.py` — enforcement item 6, the merged-reality
  leg (`load_git_reality` + `check_merged_reality` + `_find_pr_commit`,
  `_git` subprocess facade; new CLI flag `--no-reality` for hermetic
  runs). Per shipped idea whose `shipped_repo` matches the local origin:
  `shipped_pr` must have a merge marker on main — strictest pattern first
  (squash `(#N)` tail → `Merge pull request #N` → `(#N)` anywhere, the
  #106 multi-PR-subject style) so date derivation lands on the true merge
  commit; the derived real merge date reconciles `merged_date` (drift >
  ±1d → advisory `merged-date-drift` naming the real date); an optional
  `merged_sha` must be 7–40 hex (malformed → ENFORCING `bad-merged-sha`,
  text-only, no git needed) and, well-formed, an ancestor of the ref
  (`git merge-base --is-ancestor`).
- **Design (decide-and-flag):** advisory-first for every
  reachability/date leg (printed `[advisory]`, never exit-affecting);
  enforcing only for malformed SHA syntax. **Grace window 7 days** from
  `merged_date` (filename cohort-date fallback; no parseable date =
  within grace) — 7d over the suggested 48h because the in-PR flip
  convention writes ANTICIPATED dates on PRs that park for days on
  owner-gated review (#317/#345 live right now); 7d is also the number
  the originating idea proposed.
- **Graceful degradation, proven live:** this session's own container
  clone WAS shallow (51 of 441 commits — PRs #16–#187 looked absent
  until `--unshallow`), so the leg self-skips with a note on shallow
  clones, gitless trees, unresolvable refs, and foreign `shipped_repo`
  claims. CI is unaffected: the kit-quality checkout already runs
  `fetch-depth: 0`, so the leg verifies for real there.
- `tests/test_check_idea_index.py` — 15 new tests (33 → 48): the
  four-case mutation arc on REAL temp git repos
  (`test_arc_a_unreachable_claims_past_grace_advise` ·
  `test_arc_b_really_merged_is_clean` ·
  `test_arc_c_fresh_claim_within_grace_is_clean` ·
  `test_arc_d_malformed_sha_is_enforcing_even_without_git`), plus
  date-drift fires / ±1d tolerated / merge-commit style / foreign-repo
  skip / shallow-clone note / non-git note / unshipped-untouched /
  `--no-reality` / advisory-exit-0 / malformed-exit-1 / live-repo-clean.
- Idea file `docs/ideas/idea-index-merged-reality-2026-07-14.md`
  (promoted/shipped citing #355, anticipated merged_date — itself the
  leg's first live grace-window dogfood) + backlog README entry +
  CHANGELOG `[Unreleased]` Added entry.
- **Wiring:** none needed — ci.yml kit-quality already runs
  `scripts/check_idea_index.py` and `scripts/preflight.py` already
  carries it as leg 4. `src/engine/` untouched → **no dist regen needed**
  (byte-pin unaffected).
- Park state: NO auto-merge armed by this session — PR #355 parks for a
  different session/owner to review-merge; enabler arm state verified at
  close and disarmed if armed (park-green seat convention).

## Verify

- `python3 -m pytest tests/ -q` → `1425 passed in 27.76s`
  (baseline 1410 at HEAD 87aeb4d + the 15 new tests, zero failures).
- `python3 scripts/preflight.py` → `preflight: OK — 7 leg(s) green`
  (pytest · dist-byte-pin · ruff · idea-index · changelog-structure ·
  program-law · bench-integrity).
- `python3 scripts/check_idea_index.py` → `check_idea_index: OK` — the
  real corpus (24 kit-shipped ideas incl. #16–#187 era) is fully clean
  against full history: zero enforcing findings, zero advisories.
- `python3 dist/bootstrap.py check --strict` → green except the DESIGNED
  born-red hold on this very card pre-flip (plus pre-existing advisory
  model-line notes on earlier July-14 cards); green expected on the flip.
- `git diff dist/bootstrap.py` → empty (scripts/-side change only).

## Enders

💡 **Session idea:** `check_idea_index --reconcile` — a write-mode for the
merged-reality leg: the `merged-date-drift` advisory already derives and
prints the REAL merge date, so a `--reconcile` flag could rewrite the
idea file's `merged_date` (and flip a stale anticipated date) in place,
turning every drift advisory into a zero-cost mechanical fix instead of a
hand edit a future session must remember. Same pattern as `bootstrap
heartbeat` (mechanical writer beats exhortation). Dedup-grepped
`docs/ideas/`: no existing idea covers write-mode reconciliation.

⟲ **Previous-session review** (the Night-12 triage arc, #349→#354): a
strong conveyor — five ranked backlog ideas landed in sequence, each with
tests, an idea-file flip, and a heartbeat restamp, and the preflight
dogfood (#354) retired a standing NOTE the kit itself had shipped. What
it missed: the model-line payload lint it built mid-arc (#352) fires on
the arc's OWN cards — `check --strict` today shows four same-day cards
with unparseable `📊 Model:` payloads (e.g. bare `Fable`, a
non-PL-004 task class), so the cohort that shipped the lint is the
lint's biggest offender. Concrete improvement: a session that ships a new
card-grammar check should sweep the same-day cohort's cards in the same
PR (self-clean), and `.sessions/README.md`'s taught form should appear in
the born-red card template so the line is right from the first commit.
