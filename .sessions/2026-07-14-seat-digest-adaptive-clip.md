# 2026-07-14 — Seat digest: adaptive description clip (retire the manual ratchet)

> **Status:** `complete`

About to (opening declaration): build
`docs/ideas/seat-digest-adaptive-clip-2026-07-13.md` — compute the
skills-digest description clip in `src/engine/seatdigest.py` from the SKILLS
list + block budget instead of hand-ratcheting a constant (ratcheted
120 → 85 → 72 in two consecutive sessions), floored at a readability minimum
with a name-only fallback; tests + dist byte-pin regen in the same PR.

- **📊 Model:** Fable

Run type: worker session (BUILD phase, coordinator-dispatched).

## What shipped (PR #349)

- `src/engine/seatdigest.py`: the hand-ratcheted skills-description clip
  (120 → 85 → 72 across two same-day sessions) is retired. New
  `_adaptive_skill_clip` computes the widest clip (ceiling `_ROW_LIMIT`)
  where header + every skill row + footer fit
  `SEAT_DIGEST_BLOCK_BUDGET`, floored at `_SKILL_CLIP_FLOOR` (40 chars —
  readability minimum); below the floor, `_skill_rows` degrades to
  name-only rows before any NAME is dropped; `_fit_rows` stays as the
  last-resort "+N more" overflow pointer. Descending linear scan on
  purpose (no monotonicity assumption about word-boundary truncation;
  ~120 candidate renders is negligible). Deterministic given SKILLS —
  the byte-compare drift guard stays meaningful.
  `skills_digest_block(skills=…)` parameterized for growth-proof tests
  (defaults to the registered SKILLS).
- `tests/test_seatdigest.py`: 5 new tests — growth-proof (20-skill
  synthetic registry: every name within budget where a fixed-72 render
  verifiably overflows — the mutation-style proof the computation is
  load-bearing), floor/name-only degradation (28 skills), headroom
  widening (2 skills render descriptions far wider than the retired 72
  clip — the ratchet's permanence cost), overflow-pointer last resort
  (200 skills), determinism on synthetic registries.
- `dist/bootstrap.py` regenerated in the same PR (byte-pin).
- Bonus (frontmatter drift, fixed on sight): `docs/ideas/
  heartbeat-verb-2026-07-09.md` → promoted/shipped PR #346 and
  `docs/ideas/enabler-install-preflight-2026-07-13.md` → promoted/shipped
  PR #344 (both merged 2026-07-13 but still read `state: captured`);
  this idea's own file flipped promoted/shipped citing #349 (in-PR flip,
  the #342 convention; merged_date is the anticipated park-green date).
- Decide-and-flag (selection): top-3 buildable ideas were
  seat-digest-adaptive-clip, changelog-unreleased-structure-checker,
  model-line-payload-lint-advisory — winner on evidence tier
  (twice-reproduced same-day toll), permanent recurrence (every future
  skill), and perfect containment (one engine module).
- Park state: NO auto-merge armed by design — PR #349 parks green for a
  different session/owner to review-merge.

## Verify

- `python3 -m pytest -q` →
  `1344 passed in 27.89s`
  (baseline 1339 + the 5 new seatdigest tests, zero failures).
- `python3 dist/bootstrap.py check --strict` → green except the DESIGNED
  born-red hold on this very card pre-flip (verbatim tail:
  `check: HOLD (by design): session card
  .sessions/2026-07-14-seat-digest-adaptive-clip.md declares an
  in-progress Status — the born-red session gate holds the merge red
  until the card flips complete.`) plus the standing preflight-script
  NOTE; green expected on the flip.
- Dist byte-stability: `python3 src/build_bootstrap.py` run twice →
  identical sha256
  `5b73dc6f100f786da06014c970982a255164084b74683976d61855baa01fdaf2`
  (913802 bytes) both runs.
- `python3 -m ruff check src/engine/` → All checks passed.
- `python3 scripts/check_idea_index.py` → OK after the frontmatter flips.

## Enders

💡 **Session idea:** `check_idea_index` merged-reality leg — cross-check a
shipped idea's `merged_date`/`shipped_pr` against git truth: when the
frontmatter names `shipped_pr: N` and a commit matching `(#N)` exists on
`origin/main`, derive the real merge date from that commit and flag a
mismatched `merged_date` (and a `shipped_pr` whose commit never appears
after, say, 7 days). The in-PR flip convention (this session, #342 before
it) necessarily writes an ANTICIPATED merge date — mechanical
reconciliation beats trusting it forever. Dedup-grepped `docs/ideas/`:
frontmatter files exist but none covers verifying ship fields against git;
the checker (`scripts/check_idea_index.py`) validates shape only, never
reality.

⟲ **Previous-session review** (the ORDER-019 night arc, #342–#348): strong
arc — the seat consumed the full worklist top-down, one card per item, and
every engine item landed with tests plus a dist byte-pin in the same PR
(the #346 heartbeat card even dogfooded its own verb for the close-out
restamp — live proof beats a test). What it missed: two of the ideas it
shipped (#344, #346) were left `state: captured` in their `docs/ideas/`
frontmatter — the ORDER-driven build path skips the idea-file flip step
that the groom-driven path performs naturally, and this session had to fix
the drift on sight. Concrete workflow improvement: make the flip mechanical
— when a session card cites a `docs/ideas/<file>` as the thing being built,
session-close (or a checker leg) should require that file's frontmatter to
flip in the same PR; that plus the 💡 idea above (post-merge date
reconciliation) closes the class from both ends.
