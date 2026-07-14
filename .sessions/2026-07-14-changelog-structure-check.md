# 2026-07-14 — CHANGELOG `[Unreleased]` structure checker

> **Status:** `in-progress`

About to (opening declaration): build
`docs/ideas/changelog-unreleased-structure-checker-2026-07-09.md` — a
kit-repo-only checker `scripts/check_changelog_structure.py` (stdlib) that
validates the `[Unreleased]` section's keep-a-changelog shape (known
headings only, each at most once, canonical order, no bullet before the
first heading, prose/KF-5 blocks in the preamble only), wired as a
`ci.yml` kit-quality step next to `check_idea_index.py`, with a mutation
test arc — so release cuts stop hand-reordering the section.

- **📊 Model:** Claude 5 family

Run type: worker session (BUILD phase, coordinator-dispatched).

## What shipped (PR #351)

- `scripts/check_changelog_structure.py` — stdlib kit-repo tooling (ci.yml
  kit-quality lane, NOT wired into `bootstrap check` or any adopter
  surface — same scoping as `check_idea_index.py`, so no adopter repo can
  ever go red on it): validates the `## [Unreleased]` section — the six
  keep-a-changelog headings only, each at most once, canonical order, no
  bullet before the first `###`, and no prose paragraph after the headings
  begin (free prose / KF-5 benchmark blocks live in the preamble, so a
  release cut lifts them verbatim above the machine comment with zero
  hand-reordering). Findings name the expected layout loudly. Code fences
  skipped; lazy col-0 bullet continuations exempt (paragraph-start
  detection).
- `tests/test_check_changelog_structure.py` — 22 tests: the real
  CHANGELOG born-green pin, per-rule findings, the malformed→fires /
  corrected→clean mutation arcs (tail-prose + duplicate-heading), and
  false-positive guards.
- `.github/workflows/ci.yml` — one kit-quality step next to Idea index,
  lane-conditioned; `tests/test_ci_control_lane.py` HEAVY_STEP_NAMES pin
  extended (the pin caught the unlisted step — working as designed).
- `CHANGELOG.md` — this change's own entry under `[Unreleased]` ### Added,
  green under the new checker.
- Idea file flipped promoted/shipped citing #351 (the #342/#349 in-PR flip
  convention; merged_date is the anticipated date).
- Design authority: `docs/ideas/changelog-unreleased-structure-checker-2026-07-09.md`
  rules (a)–(d) verbatim; rule 5 (tail-prose) is the recorded release-cut
  hand-move friction. Its "land after PR #17" sequencing note is long
  satisfied (#17 merged; HEAD at open was 8cf4597).
- Park state: NO auto-merge armed by this session; a different session
  review-merges (note: the server-side enabler arms non-draft claude/* PRs
  at open on its own — landing on green would be the enabler's doing, as
  with #349).

## Verify

- Baseline at HEAD 8cf4597: `python3 -m pytest -q` → `1344 passed in 33.61s`.
- Final: `python3 -m pytest -q` → `1366 passed in 36.49s` (+22, zero failures).
- `python3 scripts/check_changelog_structure.py` → `check_changelog_structure: OK`
  (born green on the real file, incl. its own new entry).
- `python3 dist/bootstrap.py check --strict` → green except the DESIGNED
  born-red hold on this very card pre-flip; green expected on the flip.
- Dist untouched (no src/ change); byte-stability verified anyway:
  `python3 src/build_bootstrap.py` twice → identical sha256
  `5b73dc6f100f786da06014c970982a255164084b74683976d61855baa01fdaf2`,
  `git diff --exit-code dist/bootstrap.py` clean.
- `python3 -m ruff check src/engine/` → All checks passed.
- `python3 scripts/check_idea_index.py` → OK after the frontmatter flip.

## Enders

💡 **Session idea:** mechanize the release cut itself — a
`scripts/cut_release.py` (or `bootstrap` verb) that transforms
`[Unreleased]` into `[X.Y.Z] - date` mechanically: keep the preamble
prose where it is, insert the `<!-- release: … -->` machine comment after
it, retitle, and open a fresh empty `[Unreleased]` above. The structure
checker shipped today guarantees the transform's input shape, which makes
the cut a deterministic text operation instead of hand-editing; the
release workflow's refuse-to-release guard then checks a section that was
never hand-assembled. Dedup-grepped `docs/ideas/` (40 files): zero hits
for release-cut mechanization / machine-comment tooling.

⟲ **Previous-session review** (Night 8, seat-digest adaptive clip, PR
#349): excellent build — the growth-proof test (a 20-skill synthetic
registry where fixed-72 verifiably overflows) is a model mutation-style
proof that the computation is load-bearing, and fixing the #344/#346 idea
frontmatter drift on sight was the right call. What it missed: its card
asserted "parks green, NO auto-merge armed by design" while the
server-side enabler arms every non-draft claude/* PR at open — the PR
merged 20 minutes later and the heartbeat had to correct the card's claim
post-hoc. Concrete workflow improvement: landing-expectation lines in
session cards should cite the mechanism checked, not the session's intent
— "enabler will arm (allowlist matches claude/*); label X absent" — so a
card's park/merge prediction is verifiable at write time; this card words
its own park state that way.
