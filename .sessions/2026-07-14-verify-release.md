# 2026-07-14 — verify_release mechanization (release runbook §5 as one command)

> **Status:** `in-progress`

About to (opening declaration): build the #356 card's 💡 ender —
`scripts/verify_release.py <version>`, mechanizing the runbook §5 three-way
post-release verification (tag → bump commit · release.json sha256 == downloaded
asset sha256 == committed dist/bootstrap.py at the bump SHA · release.yml run
green), PASS/FAIL/SKIPPED per leg with expected-vs-actual, honest degradation on
network walls, read-only (never pushes/dispatches). Plus tests.

- **📊 Model:** Fable 5 · high · feature build

Run type: worker session (post-EAP backlog build, coordinator-dispatched).

## What shipped (PR #357)

- `scripts/verify_release.py <version>` — runbook §5 as one read-only
  command, three legs with per-check PASS/FAIL/SKIPPED + expected-vs-actual
  and a paste-ready release-record line (tag object · commit · hash · run
  id). Leg 1 tag: resolve (local tag, else read-only `ls-remote origin`),
  ancestry to origin/main, version in all three homes at the commit,
  is-the-bump (parent's KIT_VERSION differs). Leg 2 sha256: release.json
  field == downloaded asset == committed dist at the tag commit
  (github.com/…/releases/download/ path only — api.github.com is the
  CAPABILITIES wall). Leg 3 workflow: the release.yml run at the tag
  head_sha concluded success (Actions API; SKIPs with the verbatim 403 in
  this environment).
- **Decide-and-flag (exit policy):** exit 1 iff any check FAILs; SKIPPED
  never fails the run (a wall is not a verification failure) but is never
  upgraded to a pass — all-skip exits 0 with a loud NOTHING-WAS-VERIFIED
  warning; partial sha coverage passes only via real 2-way agreement and
  the summary names every skipped fact. Exit 2 = usage error.
- **Decide-and-flag (shallow-clone ancestry):** live-hit building this —
  the container clone is GRAFTED (2 entries in .git/shallow), and
  `merge-base --is-ancestor` returns a FALSE negative for v1.15.0's real
  bump commit eaf4f23. On a shallow clone a negative ancestry answer now
  SKIPs (unprovable), a positive still PASSes; full clones FAIL honestly.
- **Decide-and-flag (leg settling):** a leg whose only passes are setup
  facts (tag resolved, one uncompared hash) reads SKIPPED, never green —
  `Leg.settle(substantive)` pins it; the record-line hash requires ≥2
  agreeing voices.
- **Decide-and-flag (claim placement):** the work claim rode this PR's
  first commit (visible on the open PR head immediately) instead of a
  separate main-landed fast-lane PR — the born-red PR itself is the
  in-flight signal; deleted before the flip per convention.
- `tests/test_verify_release.py` — 20 tests, all on tmp fixture repos +
  injected fake fetchers (suite never networks): golden 3-leg PASS,
  record-line evidence, ls-remote fallback, tampered release.json/asset
  FAILs (each pairwise mismatch), release.json version mismatch, tag
  missing / tag-past-the-bump / version-home mismatch / true not-ancestor
  FAILs, workflow failure FAIL, network-dead SKIP (exit 0 + warnings),
  all-skip NOTHING-VERIFIED, shallow-negative-ancestry SKIP, run-not-found
  and in-progress SKIPs, `--offline`, malformed-version usage error,
  Leg.settle unit pin, plus a `VERIFY_RELEASE_LIVE=1`-gated live golden.
- `docs/operations/release-runbook.md` §5 — one "Mechanized:" pointer line
  (mirrors §2's from #356).

## Verify

- Baseline at HEAD 6b9cdd4 (#356): suite was 1444. Final: `python3 -m
  pytest tests/ -q` → `1463 passed, 1 skipped` (+19 run, +20 files' tests
  incl. the env-gated live one, zero failures).
- `python3 scripts/preflight.py` → `preflight: OK — 7 leg(s) green`.
- `python3 dist/bootstrap.py check --strict` → green except the DESIGNED
  born-red hold naming this card (pre-existing model-line advisories on
  earlier July-14 cards unchanged).
- dist/ untouched (`git status` clean on dist/) — scripts/-only, no regen.
- Live golden run against real v1.15.0 (executed once, this environment):
  `verdict: 2 PASS · 0 FAIL · 1 SKIPPED -> exit 0` — tag leg PASS
  (resolve via ls-remote: object 0b26d4168fd5 -> commit eaf4f23ca3cd;
  ancestry SKIPPED shallow; version-homes/dist-stamp/is-the-bump PASS with
  parent 1.14.0), sha256 leg PASS (all three voices
  25d22af9d9d81b2a7dc6d8d500234b6aa0f3f1c6a0400284ce2381baaeac650e, asset
  828825 bytes), workflow leg SKIPPED (api.github.com 403 — the
  CAPABILITIES wall, verbatim in the output).

## Enders

💡 **Session idea:** extract a shared git-truth degradation helper. The
"container clones are shallow/grafted — degrade, don't false-FAIL" rule
has now been independently re-derived three times in three nights:
check_idea_index's merged-reality leg (#355, 51/441 commits), this
script's ancestry check (#357, a live FALSE `merge-base --is-ancestor`
negative for v1.15.0's real bump commit), and the preflight idea-index
skip note. A tiny shared module (e.g. `scripts/_git_truth.py`:
`is_shallow()`, `provable_ancestry(a, b) -> yes|no|unprovable`) would make
the fourth consumer import the rule instead of writing a fourth variant —
and its docstring is the natural home for the graft-severs-ancestry fact.
Dedup: `docs/ideas/` (42 files) has no shared-helper proposal; the
merged-reality idea file covers only its own checker's degradation.

⟲ **Previous-session review** (Night 14, cut_release mechanization, PR
#356): strong pairing of mechanization with self-verification (importing
check_changelog_structure's rules instead of duplicating them is exactly
the writer==enforcer pattern), and it followed its own ⟲ advice — declared
flip-and-let-merge as a mechanism prediction and attempted no post-flip
disarm, ending the #349/#355 park-race class recurrence. What it left
open: its FOLLOWUP_CHECKLIST embeds a verbatim copy of runbook §§3–6 in
the script, and nothing pins the two texts together — the runbook says
"canonical" but a future runbook edit silently strands the checklist (the
drift class check_template_pointer_guard exists to catch elsewhere).
Concrete improvement: a checklist↔runbook consistency pin (test asserting
the checklist's step names appear in the runbook, or the checklist
printing section pointers instead of copied prose). This session kept its
own §5 pointer to one line in the runbook, prose uncopied, for that
reason.

