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

## Verification

- The mechanism was **run on itself**: Layer 1 answered in writing with
  citations verified to resolve, then a Layer 2 reviewer call over Vertex
  (credit-funded, per the standing directive).
- Reviewer outcome: 4 substantive objections — **2 conceded, 1 partial, 1
  refuted with evidence** — plus 3 sound follow-ups, all adopted as § 7b.
- The refutation was checked rather than argued: `docs/adopters.md` is generated
  from each repo's committed tree (12 rows, 11 citing a vendored dist header),
  and `.gitmodules` is absent from all 10 sweep clones.
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
