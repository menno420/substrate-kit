# Layer 1 — provenance for the provenance mandate itself

> **Status:** `reference`
>
> The actual answer record for
> [`../planning/2026-08-06-provenance-review-mandate.md`](../planning/2026-08-06-provenance-review-mandate.md),
> written BEFORE the Layer 2 call and committed because Codex was right that an
> uncommitted self-test is not evidence of anything (PR #580, P2). The plan
> claimed "Layer 1 earned its place" while the record sat in a scratchpad no
> reader could check — a provenance failure inside the provenance mandate.

Answered in writing before the reviewer call, per § 3. Citations verified to
resolve before submission.

## Q1 · What did you base this on?

| Claim | Basis |
|---|---|
| The estate instruments execution, not judgment | `fleet-manager docs/findings/2026-08-05-foundation-continuation.md:101` — *"This estate instruments execution. It does not instrument judgement."* Not my inference; a prior session's, owner-reviewed. |
| Adopters vendor pinned builds, so a promoted checker cannot red the fleet at once | Commands run 2026-08-06: `substrate.config.json` `kit_version` = 1.20.1 in fleet-manager vs 1.20.2 in the kit; `bootstrap.py` header reads `GENERATED, DO NOT EDIT` at 1.3MB; `.claude/skills/upgrade-distribution/SKILL.md:24` names `gh release download` as the delivery step. |
| The advisory tier was 87%/90% of gate output | `check --strict` run on both trees, line-counted: 41/47 and 80/89. |
| 0 of 11 adopters had a resolving boot pointer | Sweep over 11 shallow clones, 2026-08-06. |
| Thirteen owner corrections, five owner-dependent, two confident-with-false-walls | **OWNER-DEPENDENT.** Stated by the owner. I cannot enumerate or verify them; I hold no record of his corrections beyond what he reports. Flagged per § 7b rather than asserted. |
| A correlation search silently clamped instead of failing | **OWNER-DEPENDENT.** His measurement, his instrument, outside anything I ran. |
| Gemini was wrong about the dependabot deadlock | `fleet-manager docs/findings/2026-08-05-foundation-continuation.md:243` records it. Second-hand: I did not observe that review. |
| Gemini overclaimed on video coverage | **OWNER-DEPENDENT.** Stated by the owner; I have no record. |

## Q2 · Which documents covering this did you read? `path:line`

- `fleet-manager docs/findings/2026-08-05-foundation-continuation.md:101` — the execution/judgment split, and `:68` for the `NOT-VERIFIABLE` position I reuse in § 10.
- `fleet-manager docs/owner-reflection-2026-07-21.md` — read in full this session; the verification-not-capability thesis and the decide-don't-ask instruction.
- `fleet-manager .claude/hooks/route_docs.py:112` — `(REPO / d).is_file()`. This is the prior art § 5 claims to mirror, and I checked it rather than assuming: it filters routes by whether the pointer resolves, and never inspects the doc's content.
- `substrate-kit src/engine/checks/check_session_log.py:417` — `check_added_card`, the existence-and-grammar checker § 5 leans on for the "same division, not called theatre" argument.
- `fleet-manager docs/conventions/vertex-first-for-gemini.md` — the routing rule in § 6.

**Not read, and it bears on § 5:** `substrate-kit src/engine/checks/check_docs.py` in full. I cite its `[reachable]` behaviour from having seen it fire on my own PR today, not from reading its implementation.

## Q3 · Anything asserted impossible or unavailable?

Two, and both are narrower than they may read.

1. **"Gating on soundness is impossible."** Paths tried: verbatim-quote matching (proposed, then defeated — a real line can refute nothing); field-presence checking (kept, but it only catches absence). **A different path I have NOT tried:** a *second* model scoring whether a disposition addresses its objection. I excluded it by argument, not by experiment — it reintroduces prose inference into the gate, which is the rule this estate just adopted. That exclusion is a judgement and could be wrong; the untried experiment is "measure whether an LLM relevance-scorer agrees with the owner on a sample of real dispositions."
2. **"An agent cannot self-diagnose missing tacit knowledge."** Untried path: an agent could ask the owner a targeted question *in the domains § 7b names* rather than either asserting or staying silent. That is strictly more useful than flagging and I have not specified it.

## Q4 · Consequences, and who else they affect

- The gate ships in **substrate-kit**, which distributes to **12 adopters**. Blast radius is bounded by the pinned-vendoring path: adopters receive it only on an explicit upgrade PR, born-red, with a banked rollback.
- Scoped to substrate-kit's own decision surfaces first, so adopter impact is **zero until a deliberate wave**.
- Cost lands on the **owner's prepaid Vertex credit**, not his card, per § 6.
- The real cost is **agent time and context** at every decision surface. If the trigger set is too broad this taxes ordinary work; § 9 measures whether it earns that.

## Q5 · What did you NOT do or verify? What would change this?

- **The mechanism has never been run end to end.** No `gemini_review.py` exists; every claim about its behaviour is a design claim, not a measurement.
- **I did not read `check_docs.py`'s implementation** (Q2) while leaning on its behaviour in § 5.
- **The § 9 ratio has no baseline.** I did not compute today's ratio, so "the ratio moves" currently has nothing to move from. Without a baseline captured *before* rollout the measurement is unfalsifiable — this is the largest hole in the plan and it is cheap to close.
- **The trigger set is unspecified in this version.** I removed the file-path table after it was shown blind to omissions, and did not replace it. The plan currently says "decision surfaces" without defining them.
- **No out-of-bounds test is specified for the reviewer itself** (§ 7a), which is a rule the plan states and then does not apply to its own instrument.

**What would change the conclusion:** if the § 9 ratio does not move after a real sample, or if Layer 1 answers are consistently thin-but-resolving, the gate is ritual and should be removed rather than tuned.
