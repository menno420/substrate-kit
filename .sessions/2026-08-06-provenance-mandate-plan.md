# 2026-08-06 · The provenance mandate — spec, reviewed by its own mechanism

> **Status:** `complete`

- **📊 Model:** opus-5 · high · idea/planning

💡 Session idea: **Layer 1 earned its place before any API call was made.**
Writing the five answers down — in particular *"what did you NOT verify?"* —
surfaced three holes in my own plan before the reviewer saw it: no § 9 baseline,
an undefined trigger set, and a § 7a out-of-bounds rule the plan stated and then
failed to apply to its own instrument. The owner's claim that most of the value
sits in the fixed list, not the call, held on the first run.

## previous-session review

This session first proposed a narrower plan — build only the deterministic
blast-radius exporter, and keep adversarial review as an un-gated practice. The
owner corrected two things: the exporter and the reviewer catch **different
error classes** and are not alternatives, and the reviewer should ask about
**provenance, not correctness**, which is what stops it inventing a domain
opinion it does not have.

He also flagged the report style: three objections raised, three conceded,
presented as rigour — equally consistent with deference. § 11 of the plan
records survived / conceded / partial as three literal tags for that reason.

## What landed

- `docs/planning/2026-08-06-provenance-review-mandate.md` — the full spec: the
  two instruments, the provenance principle, the two-layer split with different
  authors, the narrow `path:line` gate, Vertex routing, the two practices
  (out-of-bounds testing, owner-dependent flagging), the trigger set with its
  known hole stated, measurement, and § 11's review record.
- `docs/current-state.md` — linked from the read path.

## Provenance

### Q1 · What did you base this on?

The gate's three-of-four-clauses-are-free claim is checked, not taken:
`src/engine/lib/config.py:248` — `_default_session_markers()` returns
`{label, needle}` substring pairs, config-driven, already enforced by the
session gate. Owner-stated and confirmed here rather than assumed.

### Q2 · Which documents covering this did you read? `path:line`

`docs/program/rulings.md:410` (PL-014, the ruling PL-015 extends) ·
`src/engine/checks/check_session_log.py:417` (the added-card lane this gate
would ride) · `fleet-manager:docs/findings/2026-08-05-foundation-continuation.md:101`
(the execution/judgment split, cross-repo — recorded, not gated).

### Q3 · Anything asserted impossible or unavailable?

Yes, and it is now the gate's stated boundary: no script settles whether a
citation is RELEVANT. Paths tried across five review rounds — verbatim-quote
matching, per-claim exemption inference, a second model scoring relevance —
each produced a finding. `src/engine/guards.py:548` is the heuristic-class rule
that says why. Untried and named: measuring whether an LLM relevance-scorer
agrees with the owner on a sample of real dispositions.

### Q4 · What are the consequences, and who else do they affect?

Two of four clauses are `substrate.config.json` markers, which reach every
adopter on their next upgrade. Scoped to substrate-kit's own decision surfaces
first; no adopter sees it until a deliberate wave.

### Q5 · What did you NOT do, check, or verify?

`check_provenance` is not built — this PR is spec plus PL-015. The § 9 baseline
is not collected. The hook (the next build) is not started. Whether the
mechanism is proportionate overall is undecided and only § 9's ratio settles it.

### Layer 2: completed — [`../docs/reviews/2026-08-06-provenance-mandate-review-record.md`](../docs/reviews/2026-08-06-provenance-mandate-review-record.md)

Five rounds, 34 findings, all correct. Model: `gemini-3.6-flash` via Vertex
(Layer 2 proper) and Codex via the GitHub connector (third perspective).

## Verification

- The mechanism was **run on itself**: Layer 1 answered in writing first —
  record committed at
  [`docs/reviews/2026-08-06-provenance-mandate-layer1.md`](../docs/reviews/2026-08-06-provenance-mandate-layer1.md),
  all six citations verified to resolve — then a Layer 2 reviewer call over
  Vertex (credit-funded, per the standing directive). The record is committed
  because Codex was right that an uncommitted self-test is evidence of nothing.
- Reviewer outcome: 4 substantive objections — **2 conceded, 1 partial, 1
  refuted with evidence** — plus 3 sound follow-ups, all adopted as § 7b.
- The refutation was checked rather than argued — and then **downgraded to
  `[partial]` when Codex checked it back**. `docs/adopters.md` reads each repo's
  own stamped `bootstrap.py` header (12 rows, 11 with a header), and
  `.gitmodules` is now confirmed absent on **all 12**. But `currency.py` fetches
  four file paths and **never enumerates a committed tree**, so the registry
  cannot settle the alternate-live-path question — an earlier version of this
  card said "generated from each repo's committed tree", which overstates what
  it does.
- `dist/bootstrap.py check --strict` → exit 0 post-commit.
- The deterministic `[reachable]` checker caught this plan as an orphan before
  it landed — the tier promoted earlier today doing its job on the next PR.

**Honest nulls.**

- **Nothing is built.** This is a spec; `gemini_review.py`, the exporter and
  `check_provenance` do not exist. Every claim about their behaviour is a design
  claim.
- **The § 9 baseline is still not captured**, so the ratio has nothing to move
  from. The plan says to capture it before the first gated PR; this session did
  not.
- **The trigger set covers the conscious subset only.** A decision the author
  does not recognise as a decision fires neither a path nor a card trigger —
  which is the failure mode that motivated the plan. Stated in § 7c rather than
  papered over.
- **The reviewer has not had its own out-of-bounds test** (§ 7b specifies it;
  it has not been run, because the instrument does not exist yet).
