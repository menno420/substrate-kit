# 2026-07-20 · fix check_no_false_walls clearing vocabulary (5 idea-engine false positives)

> **Status:** `in-progress`

About to happen (opening declaration): the v1.20.0 engine leg
`check_no_false_walls` reds adopters on lines that CORRECTLY repudiate or
date-record a past false capability wall, because the clearing logic
(`is_cleared` + `_REPUDIATION_CUES` / `_FALSE_LABEL`) has too-narrow
vocabulary and checks strictly line-by-line. On adopter idea-engine
(branch `claude/kit-upgrade-v1.20.0`, sha 039b75b) it produces 6 findings,
5 of which are detector false positives:

- `docs/CAPABILITIES.md:91` [self-merge-classifier] — repudiation "is NOT
  walled (corrects a prior false 'self-merge classifier' entry)" wraps
  90→91; the wall phrase lands alone on 91. → FP, must clear.
- `docs/CAPABILITIES.md:133` [agent-negated-capability] — "they do not
  establish that agents cannot merge" (a repudiation). → FP.
- `docs/CAPABILITIES.md:139` [classifier-denied-standing] — dated incident
  record under the `### 2026-07-16 — auto-mode-classifier denials` heading. → FP.
- `docs/CAPABILITIES.md:149` [review-label-prohibition] — dated incident
  record ("reported label '[Merge Without Review]' … DENIED"). → FP.
- `docs/seat-digest.md:46` [self-merge-classifier] — "is NOT walled
  (corrects a prior false …)"; lowercase "false" + "NOT walled" phrasing. → FP.
- `docs/SKILLS.md:22` [never-agent-side] — skill-table row literally
  "…never self-merge." with NO repudiation/date. → GENUINE stale wall, MUST STAY RED.

Fix the ENGINE SOURCE (`src/engine/checks/check_no_false_walls.py`, not the
generated dist), rebuild `dist/bootstrap.py`, add a mutation test asserting
the 5 FP shapes clear and the bare wall stays flagged, validate against the
real idea-engine tree (exactly 1 finding = SKILLS.md:22 remains), and keep
every existing `_MUST_FAIL` caught / `_MUST_PASS` cleared.

- **📊 Model:** opus-4.8 · high · engine-bugfix

Run type: owner-directed (fm ORDER 048 + coordinator go-ahead).

## What shipped

(to be filled at close-out)
