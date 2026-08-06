# Provenance mandate — the review record

> **Status:** `reference`
>
> Split out of
> [`../planning/2026-08-06-provenance-review-mandate.md`](../planning/2026-08-06-provenance-review-mandate.md)
> on the owner's direction, 2026-08-06. **Two artifacts were living under one
> name.** The record of what review found should grow as evidence demands; the
> instruction a session follows at a decision surface must fit working
> attention. While they shared a file, the record's legitimate growth silently
> degraded the instruction.
>
> This is a SPLIT, not a cut — no verified-correct content was deleted. The
> owner's reading of the growth, which reverses the authoring session's own
> worry: *"We should not consider this as a fault in our plan, but exactly the
> plan working as intended."* 28 findings, every one correct, means the spec
> contained 28 real defects; had review found nothing, the document would be
> its original size **and still broken.** Length here is the visible trace of
> the input's defect density — a discovery signal, not a cost signal.
>
> The Layer 1 answers for the plan itself are the sibling file
> [`2026-08-06-provenance-mandate-layer1.md`](2026-08-06-provenance-mandate-layer1.md).

## 11 · The review this plan received — survived, conceded, partial

The mechanism was run on itself before the plan was proposed for merge: Layer 1
answered in writing, then a Layer 2 reviewer call over Vertex. Recorded in the
§ 7b format, because "all objections conceded" is equally consistent with rigour
and with deference and the estate has now been warned about exactly that.

- **[partial]** *"The pinned-vendoring model is extended to 12 adopters from a
  1-repo check."* — **Downgraded from `[survived]` after Codex checked my
  refutation** (PR #580, P2), which is the third-perspective value in one line.

  What stands: `docs/adopters.md` reads **each repo's own stamped
  `bootstrap.py` header**, so "every adopter vendors a pinned dist" is
  per-repo evidence across 12 rows, not a 1-repo extrapolation. The
  `.gitmodules` check is now complete — **0 of 12**, the two I had missed
  (`substrate-kit`, `fleet-manager`) verified since.

  What does **not** stand: I wrote that as though it settled the alternate-live-
  path question. It does not. `currency.py` fetches a repo's config, two known
  bootstrap paths and its heartbeats — **it never enumerates a committed tree**
  — so the registry can establish what a repo VENDORS and cannot establish that
  nothing else is live. Submodules are one alternate mechanism; ruling them out
  does not rule out the class. `superbot` in particular has no vendored dist at
  all, so nothing here characterises how it consumes the kit.

  The claim is now scoped to what the evidence carries, and § 8's exporter spec
  states the same limit at the point of use.

- **[conceded]** *"§ 0 asserts the exporter would have caught none of the
  thirteen owner corrections, while Layer 1 marks those corrections
  owner-dependent and unverifiable."* — Correct, and it is the plan violating
  § 7b inside the document that states § 7b. Fixed in § 0, with the original
  error left visible.

- **[conceded]** *"'A provenance reviewer needs no domain knowledge at all'
  overstates it — telling a genuine source from a confident restatement is still
  semantic judgement."* — Correct. § 2 now splits it by layer: the gate needs
  none, the reviewer needs some.

- **[partial]** *"`path:line` resolution is as gameable as quote-matching, so
  the distinction is not substantive."* — The gameability point stands and § 5
  now says so plainly, including that `path:line` is the **cheaper** of the two
  to fake. What does not follow is the implied conclusion that the gate is
  therefore worthless: it was never claimed to catch unsound answers, only
  absent ones, and *"I based this on general knowledge"* still cannot produce a
  resolving citation. The framing was wrong; the mechanism stands.

- **[conceded]** Three follow-ups, all genuinely unspecified: an out-of-bounds
  test for the reviewer itself, a record format for survived-vs-conceded, and a
  syntax for owner-dependent claims. All three are now § 7b.

**Gemini (Layer 2) accuracy:** four substantive objections — two fully correct,
one correct-in-part, one I judged refuted — plus three sound follow-ups.

## 12 · The Codex review — third perspective, and it earned its place

Requested on PR #580 specifically to find what a Claude/Gemini pair would not,
since a plan reviewed only by an LLM pair is the shared-blind-spot problem § 2
claims to solve. **Nine findings — five P1, four P2 — and eight were correct.**

| | Finding | Disposition |
|---|---|---|
| P1 | The gate passes **vacuously** on zero citations, so its headline claim was false of itself | `[conceded]` — § 5 rules 1–2 |
| P1 | "Card declares a decision/deferral/null" is **not machine-readable** | `[conceded]` — § 7c literal tags |
| P1 | The reviewer **cannot see cited content**, so known-bad case 1 is undetectable | `[conceded]` — § 7b input contract |
| P1 | Known-bad tests alone pass a reviewer that **flags everything** | `[conceded]` — § 7b known-good controls |
| P1 | Un-gated Layer 2 means it can **never run** and nothing notices | `[conceded]` — § 5b markers |
| P2 | Disposition tags **cannot compute** § 9's ratio | `[conceded]` — § 7b origin records |
| P2 | The `[survived]` refutation **overclaims** on alternate live paths | `[partial]` — § 11 rescoped |
| P2 | The Layer 1 record was **never committed**, so the self-test proved nothing | `[conceded]` — now `docs/reviews/` |
| P2 | The exporter spec prints **fleet metadata**, not a decision→impact mapping | `[conceded]` — § 8 mapping |

**The P1 that matters most is the first.** § 5 asserted *"'I based this on
general knowledge' cannot produce a resolving citation, and that is the whole
claim."* It was false of the gate as written: zero citations satisfies "every
citation resolves" vacuously, so the exact string the plan used as its example
would have passed. Neither the author nor Gemini saw it. That single finding is
the argument for a third reviewer.

**The P2 about the uncommitted Layer 1 record is the sharpest process catch.**
The plan claimed Layer 1 earned its place while the evidence sat in a scratchpad
no reader could open — a provenance failure inside the provenance mandate, of
exactly the kind it exists to prevent. The record is now committed at
[`../reviews/2026-08-06-provenance-mandate-layer1.md`](../reviews/2026-08-06-provenance-mandate-layer1.md),
and all six of its citations were verified to resolve.

### Codex round 2 — nine more, all nine correct

Re-review on the revised spec. **Every finding was verified against the cited
file before being accepted**; none was taken on the reviewer's word.

| | Finding | Verified against | Disposition |
|---|---|---|---|
| P1 | Cross-repo citations resolve against nothing — **the mandate's own record would red its own gate** | this repo's tree: 6 of 6 failed | `[conceded]` — § 5 syntax + record rewritten |
| P1 | Owner-dependent exemption needs claim-boundary detection in prose | — | `[conceded]` — slot-level declaration |
| P1 | Program law mapped to "nobody downstream" | `docs/program/README.md:5` — binds *every* repo | `[conceded]` — own path class |
| P1 | ADRs escape the trigger | `docs/house-style.md:48` — `docs/decisions/NNN-*.md` | `[conceded]` — glob added |
| P1 | Build order restates the **pre-correction** gate | § 5 vs § 8 step 2 | `[conceded]` — references § 5 |
| P1 | Semantic exclusions recreate prose classification | § 7c's own rejection of it | `[conceded]` — exclusions removed, explicit label |
| P1 | Release events cannot compute a diff base | `release.yml:23-30` (tag/dispatch), `:39` (no depth) vs `ci.yml:25` | `[conceded]` — previous tag + `fetch-depth: 0` |
| P2 | Overlapping engine path classes have no precedence | `src/engine/templates/**` ⊂ `src/engine/**` | `[conceded]` — most-specific wins |
| P2 | Reviewer qualification never expires | § 6 pins a route, not a version | `[conceded]` — model/prompt/window pinned |

**The first is the important one, and it is the same failure twice.** Round 1
found the gate passing vacuously on the plan's own worked example. Round 2 found
the plan's own committed evidence record failing the corrected gate — six of six
citations using a prose prefix that resolves against nothing. Both times the
spec read fine and was unimplementable; both times the author and the Gemini
reviewer missed it.

**Running total across three reviewers: 22 objections — 19 conceded, 2 partial,
1 refuted.** The concession rate is high because Codex is finding
implementability defects, which are not matters of judgement: either the
checker can compute it or it cannot.

> **`OWNER-DEPENDENT`:** whether this level of specification is proportionate —
> or whether the mandate is now over-engineered for the frequency of decisions
> it will actually gate — is the owner's call, and § 9's ratio is the evidence
> that would settle it after the fact rather than before.

### Codex round 3 — eight more, all eight correct

| | Finding | Disposition |
|---|---|---|
| P1 | One citation for the WHOLE record still passes a `"general knowledge"` Q1 | `[conceded]` — per-slot grounding |
| P1 | Three incompatible `OWNER-DEPENDENT` syntaxes across two docs | `[conceded]` — one exempting form, one non-gated hedge |
| P1 | Record headings `## Qn ·` fail the gated `### Qn` grammar | `[conceded]` — record rewritten |
| P1 | Reviewer told to resolve cross-repo citations CI cannot fetch | `[conceded]` — passed unresolved, reviewer told so |
| P1 | Release trigger has no deterministic card to inspect | `[conceded]` — gate moves to the pre-tag bump PR |
| P1 | `provenance-not-required` is stale-able: `ci.yml` omits `labeled`/`unlabeled` | `[conceded]` — trigger types required before it ships |
| P2 | `[origin:*]` baseline unrecoverable from cards predating the schema | `[conceded]` — prospective baseline |
| P2 | No source maps a template to the adopters that re-render it | `[conceded]` — emits `unknown` and reds |

**Three rounds, 26 findings, 26 correct.** And the mandate's own representative
record has now failed the mandate's own gate **three separate times** — vacuous
on zero citations, then citations that resolve against nothing, then headings
in the wrong grammar. Each fix passed the author's review and Gemini's.

**But round 3's fixes NARROW rather than expand**, which is the first sign of
convergence: the reviewer now admits it cannot judge cross-repo evidence, the
exporter emits `unknown` instead of an understated list, the baseline becomes
prospective instead of reconstructed, and one of two markers stops exempting
anything. Rounds 1–2 added contract; round 3 mostly removed overreach.

> **`OWNER-DEPENDENT` — the open question this creates.** Is a spec that took
> three review rounds to become implementable the right instrument for this
> estate, or is the honest read that a deterministic gate over prose is simply
> expensive and the practice should ship un-gated first? § 9's ratio settles it
> after the fact; nothing settles it before, and it is the owner's call, not a
> reviewer's and not mine.

### Codex round 4 — two findings, and the lesson is the method

| | Finding | Disposition |
|---|---|---|
| P1 | The record still fails the per-slot rule: Q1 and Q3 carry no resolving same-repo citation and no slot exemption | `[conceded]` |
| P2 | Build order re-paraphrases the **pre-round-3 global** citation rule, inside the note warning against stale paraphrase | `[conceded]` — paraphrase deleted, § 5 referenced only |

**Fourth form of one defect, and the cause was the method, not the spec.** In
Codex's words: *"Updating the heading grammar fixed the round-3 symptom, but did
not verify the record against the complete rule set."* Each round I fixed the
symptom that was named and re-read the result, and re-reading is exactly what
this whole mandate exists to distrust.

**The fix is mechanical and now runs:** the record is checked against every § 5
rule by script — slot headings, per-slot resolving same-repo citation, exemption
first-line — rather than by inspection. All three applicable slots pass.
Citations added are load-bearing, not filler: `docs/adopters.md:30` is the
`superbot` pin-only row that makes the registry per-repo evidence,
`src/engine/currency.py:459` is the `fetch(repo, CONFIG_RELPATH)` line proving
it never walks a tree, `src/engine/guards.py:548` is the heuristic-class rule
cited as the reason for excluding a second-model scorer.

**Convergence, measured:** 9 → 9 → 8 → 2 findings, the last two mechanical, and
Codex states the round-3 direction was convergent. The volume curve says
converging; the four-round persistence of one defect class says a deterministic
gate over prose is expensive to specify correctly. **Both are true**, and § 9's
ratio is what decides whether that cost is worth paying — which remains the
owner's open question, not a reviewer's and not mine.
