# 2026-07-14 · check_claims own-date fix (false claims-stale)

> **Status:** `complete`

About to happen (opening declaration): fix the `check_claims` work-claim
dating bug found live by the model-line-lint session (its card's
friction→guard recipe) — the checker dates a claim by the FIRST date-string
anywhere in the file, so a dated filename mentioned in the scope text makes
a fresh claim nag as stale. Fix: date the claim by the LAST date on the
bullet line (the taught grammar ends the bullet `· YYYY-MM-DD`), regression
tests, dist regenerated. Advisory posture unchanged.

- **📊 Model:** fable-5 · medium · runtime bugfix

Run type: worker session (coordinator-dispatched build).

## What shipped (PR #353)

- `src/engine/checks/check_claims.py` — the work-claim date is now the LAST
  `YYYY-MM-DD` on the claim bullet line, not the first date anywhere in the
  file. Reproduced first on the unfixed dist (scratch tree): a claim dated
  today whose scope text mentioned `docs/ideas/foo-2026-07-09.md` fired
  `[claims-stale] … work claim dated 2026-07-09 is 5 day(s) old`; gone on
  the fixed dist, exit 0 both times. Side tightening: a date outside the
  bullet line no longer counts — such a claim is `claims-format`
  (unparseable), still advisory.
- `tests/test_check_claims.py` — 3 new tests: the regression pin
  (dated filename in scope + fresh trailing date → clean), the inverse
  (old trailing date still fires despite a fresher dated-filename mention,
  message names the claim's own date), and date-outside-bullet →
  `claims-format`.
- `CHANGELOG.md` — `[Unreleased]` ### Fixed entry.
- Dist regenerated via `src/build_bootstrap.py`, byte-stable across a
  double build (sha256
  `bbe4b57414fd618db958990a16f6b1c3e8b75184edae6a3bfeac6542afb17372`,
  identical both runs). Guard-fires delta committed per the ledger
  convention.
- Park state: NO auto-merge armed by this session (never self-merge; the
  server-side enabler arms non-draft `claude/*` PRs on its own — landing
  on green would be the enabler's doing, as with #349/#351).

## Decide-and-flag

- **Last-date-on-the-bullet-line over a strict positional date field.** The
  grammar (`engine/grammar.py` § work-claim bullet) deliberately allows the
  date "anywhere after the token", so there is no delimited date field to
  isolate; the taught form ends the bullet `· YYYY-MM-DD`, so last-on-line
  is grammar-faithful, immune to dated filenames in scope text, and exactly
  the fallback the #352 card's guard recipe prescribed. Grammar constants
  unchanged; reversible in one function.

## Verify

- Baseline at HEAD `a9145ee` (post-#352): 1391 passed. Final:
  `python3 -m pytest -q` → **1394 passed** (+3, zero failures).
- `python3 -m ruff check src/engine/` → All checks passed.
- `python3 dist/bootstrap.py check --strict` → all checks passed, exit 0
  (only the pre-existing advisory model-line nags from the newest-10 lint).
- Reproduction arc end-to-end on a scratch tree via the dist: false finding
  present pre-fix (verbatim above), absent post-fix, exit 0 both sides.

## Enders

💡 **Session idea:** promote the work-claim bullet to ONE positional parser
in `engine.grammar` — a single parse function returning (token, scope,
date) with the token as the FIRST backticked span and the date as the
trailing field, consumed by `check_claims` AND `work_claim_bullet_example`.
Today's bug was one member of a class: `WORK_CLAIM_BULLET_RE`'s greedy
`.*` captures the LAST backticked token on the bullet, so a backticked
path in scope text shifts the duplicate-scan key the same way a dated
filename shifted the date — a latent sibling bug this session saw but did
not fix (scope discipline). One field-positional parser retires the whole
grep-anywhere-field class for claims, the same move #352 made for the
model line. Dedup-grepped `docs/ideas/` (41 files): no claim-grammar idea
exists; `tests/test_grammar.py` pins examples round-trip but not field
positions.

⟲ **Previous-session review** (Night 10, model-line payload lint,
PR #352): exemplary friction→guard discipline — it hit this very false
positive live, worked around it, and left a recipe precise to the file,
line, fixture home, and preferred fallback, which made this session
near-mechanical (the reproduction matched the recipe's prediction
verbatim). What it missed: the recipe lived only in the card's
"Friction → guard candidates" section, a surface nothing routes — it
landed only because a coordinator read that card. Concrete workflow
improvement: give friction→guard candidates a routed home (an
`docs/ideas/` stub filed at card-close, or a check that a completed card's
"Friction → guard" section carries a pointer to one), so recipes cannot
rot inside cards.

**Documentation audit:** CHANGELOG entry rides the PR; the fix's rationale
lives in the checker's inline comment + this card; control/status.md
carries the one-line outcome; claim file deleted at close; nothing
chat-only remains.
