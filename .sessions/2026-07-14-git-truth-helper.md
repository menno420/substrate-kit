# 2026-07-14 — shared git-truth helper (shallow/graft degradation, extracted once)

> **Status:** `complete`

About to (opening declaration): build the #357 card's 💡 ender — extract the
"negative git ancestry answers are unreliable on shallow/grafted clones —
degrade honestly, never false-FAIL" rule into ONE shared module
(`scripts/_git_truth.py`: `is_shallow()`, `provable_ancestry()`), refit its
consumers (`check_idea_index.py` merged-reality leg, `verify_release.py` tag
leg) behavior-preserving, add helper-level tests on tmp git repos, and append
the shallow-graft false-negative finding to `docs/CAPABILITIES.md`.

- **📊 Model:** fable-5 · high · mechanical refactor

Run type: worker session (Night-16 slice, coordinator-dispatched).

## What shipped (PR #358)

- `scripts/_git_truth.py` — the single home of the rule: `is_shallow(run)`
  (tri-state: True/False/None-unknown), `provable_ancestry(run, a, b) ->
  AncestryAnswer` with verdict `yes|no|unprovable` over a minimal injectable
  runner seam (`run(args) -> (rc, stdout, stderr)`), so both consumers keep
  their own subprocess wrappers / test fakes. Module docstring carries the
  graft-severs-ancestry fact + both live hits (#355's 51-of-441-commits
  clone, #357's false negative for v1.15.0's real bump commit).
- **Decide-and-flag (verdict mapping):** rc 1 AND rc 128 both degrade to
  `unprovable` on a confirmed-shallow clone (a depth-1 graft truncates old
  commits away entirely — rc 128 "Not a valid commit name" is the same
  false-negative class, proven by the helper's own test fixture). On a
  NOT-shallow clone, rc 1 is a real `no`; rc 128 is `no` only under the
  opt-in `missing_as_no=True` (check_idea_index's policy — its ref is
  pre-verified and its clone provably full by that point) and stays
  `unprovable` by default (verify_release's "could not test" policy). A
  failed shallow probe (None) never upgrades a negative to unprovable —
  preserves verify_release's shipped FAIL on that edge.
- **Decide-and-flag (three claimed sites, two real):** the dispatch named
  scripts/preflight.py as a third implementation; verified it carries NO
  shallow logic of its own (it subprocess-runs check_idea_index — the "third
  derivation" in the #357 card was check_idea_index's own skip note
  surfacing through the preflight leg). Two call sites refit; preflight
  needed and received no change.
- Refits (behavior-preserving, all existing tests pass unchanged):
  `check_idea_index.py` `load_git_reality` shallow gate + merged-reality
  ancestry advisory; `verify_release.py` `leg_tag` ancestry block — exact
  message texts kept at both call sites.
- `tests/test_git_truth.py` — 13 tests on tmp git repos (full clone real
  answers incl. missing_as_no; depth-1 file:// grafted clone degrades
  negatives, positives still prove; degraded seams: broken git, failed
  shallow probe, non-repo dir).
- `docs/CAPABILITIES.md` — one appended wall+recipe entry (shallow-graft
  ancestry false negatives; import the helper, don't re-implement).

## Verify

- Baseline at HEAD 0d0aac4 (#357): 1463 passed + 1 skipped. Final:
  `python3 -m pytest tests/ -q` → `1476 passed, 1 skipped` (+13, zero
  failures; affected suites test_check_idea_index + test_verify_release
  pass unchanged).
- `python3 scripts/preflight.py` → `preflight: OK — 7 leg(s) green` — and
  the refit shallow skip note fired live on this container's own grafted
  clone through the idea-index leg (the extraction verifying itself).
- `python3 dist/bootstrap.py check --strict` → exit 0; the only hold is the
  DESIGNED born-red gate on this card (pre-existing model-line advisories on
  earlier July-14 cards unchanged; claims-format advisory fixed in-session
  by rewriting the claim bullet to the check_claims grammar).
- `src/engine/` untouched; dist/ untouched — scripts/ + tests/ + docs/ +
  control/ + .sessions/ only (plus the gate-mandated
  `.substrate/guard-fires.jsonl` telemetry delta).

## Enders

💡 **Session idea:** a `bootstrap claim` verb — mechanical, grammar-valid
claim-file writer (`bootstrap claim <branch> "<scope>" <area>` emits the
one-bullet file matching `check_claims`' regexes from `grammar.py`).
Evidence from this session: a hand-written claim bullet missed the grammar
(no backticked token) and fired `claims-format` — an unparseable claim is
INVISIBLE to the duplicate scan, which silently defeats the claim system's
whole purpose during the exact window it exists for. Same mechanical-writer
shape as the heartbeat verb (`docs/ideas/heartbeat-verb-2026-07-09.md`,
which covers only the status file). Dedup: grepped `docs/ideas/` — the
three claim-mentioning files (archive-ready close-out, dispatch-race
reverify, idea-index merged-reality) propose no claim writer.

⟲ **Previous-session review** (Night 15 / PR #357, verify_release): the 💡
ender's precision is the standout — it named the module path, the exact API
(`is_shallow()`, `provable_ancestry(a, b) -> yes|no|unprovable`), and the
docstring's role as the fact's home, so this session built it with
near-zero re-derivation; that is the idea grammar doing its job. The miss:
#357 wrote the THIRD variant of the shallow rule in the same commit that
proposed extracting it — the two-consumer threshold was already met at
#355, and the extraction was contained enough to fold into that session for
roughly one extra hour. Concrete workflow improvement: when a session
catches itself re-implementing a rule that already exists elsewhere in the
repo, prefer extract-now (or extract-first, then consume) over
propose-for-tomorrow when the extraction is contained — the rule-of-three
is a ceiling, not a target, in a repo whose sessions are this cheap to
re-dispatch.
