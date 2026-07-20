# 2026-07-20 · fix check_no_false_walls clearing vocabulary (5 idea-engine false positives)

> **Status:** `complete`

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
generated dist), rebuild `dist/bootstrap.py`, add a mutation test, keep every
existing `_MUST_FAIL` caught / `_MUST_PASS` cleared.

**Adversarial-review revision (fm ORDER 048):** the first cut used section-based
(dated-heading) + cross-line-block clearing, which BLINDED the gate — a genuine
standing wall under a dated heading or beside an unrelated repudiation went
green. Retightened to ATTACHMENT-BASED clearing: a wall clears only when a
repudiation/date is attached to the wall claim itself (same clause of the same
line, a `false "…"` quote naming the wall, or a tight one-line wrapped-sentence
lookback that a "but…"/dated neighbour can't trigger). Consequence, SAFETY WINS:
`CAPABILITIES.md:91/133` and `seat-digest.md:46` clear; but `CAPABILITIES.md:139`
and `:149` are section-dated incident records with NO inline date, so they stay
RED rather than weaken the gate — they need a light inline-date rewording in the
adopter doc (resident/upgrade-PR note). Real-tree net: 3 findings (139, 149,
SKILLS.md:22).

- **📊 Model:** opus-4.8 · high · engine-bugfix

Run type: owner-directed (fm ORDER 048 + coordinator go-ahead).

## What shipped

- **`src/engine/checks/check_no_false_walls.py`** — rewrote the clearing logic to be
  **ATTACHMENT-BASED**: a wall phrase clears only when a repudiation cue / inline date /
  uppercase `FALSE` label lands in the **same clause** (clauses split on `; — : .`), or a
  `false "…"` quote whose quoted content **contains the matched wall phrase**, or one **tight
  wrapped-sentence lookback** to the previous line's trailing clause (gated so a `but …`
  contrast or a dated-bullet neighbour can't bleed). A dated append-log bullet clears only its
  own physical line. Removed the earlier dated-heading section sheltering and the cross-line
  block window entirely (they blinded the gate — a genuine standing wall under any ISO-dated
  heading or beside an unrelated repudiation went green).
- **`dist/bootstrap.py`** — rebuilt deterministically from the engine source (currency test
  green); the 186-line dist delta mirrors the engine change, no other drift.
- **`tests/test_check_no_false_walls_leg.py`** — added `TestClearingVocabulary`, a MUST-RED /
  MUST-CLEAR matrix pinning: bare wall under a dated heading (incl. dated-heading-last-in-file),
  `never self-merge` under a dated heading, `classifier-denied` standing under a dated heading,
  neighbour-bleed continuation of a dated bullet, first-line-repudiates-a-DIFFERENT-capability
  continuation, unrelated `false "weather"` quote, `not walled` in a different clause, the
  genuine `docs/SKILLS.md:22 never self-merge` — all stay RED; the three attached repudiations
  (`CAPABILITIES.md:91`, `:133`, `seat-digest.md:46`) clear.
- **Verification (cited):** full kit suite **2057 passed, 1 skipped** (PR #549 body); all
  existing `_MUST_FAIL` caught / `_MUST_PASS` cleared; `dist/bootstrap.py check --strict` clean
  except the by-design born-red HOLD on this card (kit-quality job 88278684120 log line "HOLD
  (by design)").
- **Real idea-engine tree — net 3 findings:** `CAPABILITIES.md:91/:133`, `seat-digest.md:46`
  now clear; `SKILLS.md:22` (`never self-merge`) correctly stays RED; `CAPABILITIES.md:139/:149`
  stay RED — **SAFETY WINS**: they are section-dated incident records with no inline date, and
  clearing them would require reopening the heading-section sheltering that blinds the gate.
  They need a light inline-date rewording in the adopter doc (resident/next-upgrade note for
  idea-engine), not a gate weakening.

### Known non-blocking follow-up hardenings (from adversarial re-review — file as next-session guards)

- **(a) wrapped-lookback punctuation-gated bleed.** The one-line wrapped-sentence lookback can
  still bridge from a previous line whose trailing clause **repudiates a DIFFERENT capability**
  than the wall on the current line. The `but …` / dated-bullet gates catch the common cases,
  but a same-shape repudiation of an unrelated capability on the prior line's trailing clause
  can still clear the current wall. Harden: the lookback should confirm the prev-line clause's
  repudiation names/targets the **same** capability as the current wall phrase before bridging.
  Guard anchor: `check_no_false_walls.py` wrapped-lookback branch of `is_cleared`; extend
  `TestClearingVocabulary` with a prev-line-repudiates-different-capability MUST-RED case.
- **(b) `match_blocklist` one-hit-per-line masking.** Clearing is evaluated per-match, but a
  physical line carrying BOTH a repudiated `false "…"` quote AND a genuine standing wall can
  have the genuine wall masked when only the first hit on the line is graded. Harden: evaluate
  **all** wall matches on a line independently, so a genuine wall sharing a line with a
  repudiated false-quote still reds. Guard anchor: the per-line match loop feeding
  `match_blocklist` / the finding collector; add a MUST-RED test with two matches on one line
  (one repudiated, one genuine).

- **📊 Model:** opus-4.8 · high · engine-bugfix

- **💡 Session idea:** **`check_inline_date_suggest` — an adopter-side advisory that names the
  exact inline-date rewording for a section-dated wall.** This session's two residual reds
  (`CAPABILITIES.md:139/:149`) are section-dated incident records the attachment-based gate
  correctly can't clear without re-blinding itself; the adopter fix is mechanical (add
  `(2026-07-16)` / `— 2026-07-16` to the line, or restructure as a `- 2026-07-16 · …` append-log
  row). An advisory (never exit-affecting) that detects "a red wall sits under a dated heading
  whose date it could inherit inline" and prints the precise one-line rewrite turns a
  head-scratching red into a copy-paste fix — the same friction→guard instinct as the existing
  `dateless-wall` advisory, but aimed at the section-vs-inline-date gap this fix deliberately
  left open. Deduped against the dateless-wall advisory (that one flags *undated* walls; this
  flags *section-dated-but-not-inline* walls — the exact residual class here).

- **⟲ Previous-session review:** the previous session (release cut v1.20.0, card
  `2026-07-20-cut-release-v1.20.0.md`) was an honest, well-cited close — it drained a ~30-PR
  release backlog and flagged its own `verify_release.py` `is-the-bump` structural FAIL rather
  than hiding it, then proposed the exact fix (dispatch pinned to the bump SHA) that THIS
  release cut (Phase 2) is directed to use. The one thing it could have done better: it shipped
  the false-wall detector (`check_no_false_walls`) as part of v1.20.0 while the detector still
  carried the 5-false-positive vocab bug this session fixes — a pre-release adopter dry-run
  against idea-engine would have surfaced the FPs before the tag, not after.
  **System improvement:** the release-cut runbook should include a "dry-run every engine leg
  against the newest adopter tree" step before publishing, so a detector regression is caught
  at cut time rather than by an adopter red the next day.

- **Doc audit:** no durable doc home is left stale by this change — the fix is engine
  source + dist + test only; the `CAPABILITIES.md:139/:149` inline-date rewording is an
  **adopter-repo** (idea-engine) task, already captured as the resident/next-upgrade note in
  PR #549's body and this card's real-tree finding table, so nothing in substrate-kit's own
  docs needs updating. CHANGELOG `[Unreleased]` will carry this detector fix into the v1.20.1
  cut (Phase 2).
