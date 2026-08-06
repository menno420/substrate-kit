# The provenance mandate — two instruments for the judgment half

> **Status:** `plan`
>
> Owner-specified 2026-08-06. Supersedes the narrower proposal that would have
> built only the blast-radius exporter. **Both instruments get built; they cover
> different error classes and are not alternatives.**
>
> Parts of this spec were earned by running the mechanism on itself — the owner
> ran it against his own work while specifying it, and the layer split, the
> gate's narrowness and the two practices in § 7 all came out of that run.

## 0 · The two instruments, and why neither replaces the other

The estate instruments execution and not judgment. Two different judgment
failures need two different instruments:

| Instrument | Catches | Misses |
|---|---|---|
| **Blast-radius exporter** (§ 8a) — deterministic fact extraction at a decision surface | Wrong assumptions about consequence and reach ("promoting this reds 22 repos") | Everything about how a claim was arrived at |
| **Provenance review** (§ 2–5) — a fixed self-answered list plus an outside reviewer | Unsourced claims, confidence exceeding evidence, skipped reading | Whether a well-sourced claim is *correct* |

The exporter would have killed the 2026-08-06 version-skew error outright by
printing the fact the assumption contradicted. **`OWNER-DEPENDENT`:** the owner
reports that his thirteen corrections that day were unsourced claims, overstated
confidence and unread documents — a class *"how many adopters"* does not
address. I cannot enumerate those corrections and do not assert a count against
them.

> This paragraph is the plan's own § 7b violation, caught by the Layer 2
> reviewer: an earlier draft asserted flatly that the exporter "would have caught
> **none** of the thirteen" while the Layer 1 answers marked those same
> corrections owner-dependent and unverifiable. Left visible rather than quietly
> fixed — it is the cheapest available demonstration that the rule is easy to
> break inside the document that states it.

## 1 · The measured case

`MEASURED` 2026-08-05/06. The owner flagged thirteen problems in agent output.
Not one was an execution error — CI was green throughout. Every one was a
judgment call: a rule scoped one word too narrow, a mis-recorded root cause, a
capability declared unavailable on the strength of one failed probe, a coverage
figure stated flat that was false.

Two of the highest-yield catches were **confident sentences containing false
walls**. Confidence was the signal, not the shield.

## 2 · The principle: ask about PROVENANCE, not correctness

This is the design's load-bearing decision and the answer to the standing
objection that a second model cannot review a first one.

A reviewer asked **"is this right?"** must form a domain opinion. Where it has
none it will invent one — which is precisely the shared-blind-spot,
mutual-agreement-bias failure that makes LLM-as-judge unsound in an open domain.

A reviewer asked **"what is this based on?"** needs **far less** domain
knowledge: mostly it has to notice whether an answer exists, which is a question
about the shape of the record rather than about the world.

**Not zero, though** — and an earlier draft claimed zero. Telling a genuine
source from a confident restatement is still semantic judgement. The honest
split is by layer: **the GATE (§ 5) needs none** — a path resolves or it does
not — while **the REVIEWER needs some**, just far less than a correctness
verdict would, and it never has to be right about the domain to be useful.

So the reviewer never rules on correctness. It asks where a claim came from, and
the absence of an answer is the finding.

### How the reviewer behaves — modelled on how the owner actually works

- **Ask, don't assert.** It does not demand changes. The agent decides.
- **Probe claims stated confidently and without hedge.** Confidence is a reason
  to probe, not a reason to accept.
- **Probe load-bearing claims even when they look correct** — especially then.
- **Correct framing, not only facts.** *"Two identities, not three paths"*
  turned a descriptive model into a predictive one; no individual fact changed.
- **Where something is well-founded, say so plainly and move on.** Manufactured
  balance costs tokens, context and trust.

## 3 · Layer 1 — the fixed list, answered by the agent, in writing, before the call

**Most of the value is captured here.** The call only catches what survives
being written down. An agent that answers these honestly has usually found its
own gap before any reviewer sees it.

1. **What did you base this claim on?** A source, a command, an exact error —
   not a feeling.
2. **Which documents covering this did you read?** Cite `path:line`.
3. **If you asserted something is impossible or unavailable:** which paths did
   you try, and what would a DIFFERENT path look like? *Naming the untried path
   is the point.*
4. **What are the consequences, and who else do they affect?**
5. **What did you NOT do, check, or verify? What would change this conclusion?**

### Why question 5 is scoped the way it is

Q5 is **coverage-of-effort** — *"what did I not run?"* — which an agent can
answer, because it knows what it did.

It is deliberately **not** *"am I overconfident?"*, which is a blind spot by
definition: an agent that knew the honest hedge would have used it. That half
belongs to Layer 2.

The distinction is not academic. A coverage figure stated flat on 2026-08-05
was false not because the effort was incomplete but because **the instrument was
wrong** — Q5 asked honestly would still have returned "nothing missing."

## 4 · Layer 2 — the reviewer, which did not write the plan

**Two authors, deliberately.** An agent generating its own adversarial questions
has no distance from its own blind spots, so it is never asked to. Layer 1 is a
*fixed* list precisely so the agent cannot choose easy questions.

The reviewer supplies:

- **Context-specific follow-ups** the fixed list cannot anticipate.
- **"Which claims are stated more confidently than their evidence supports?"** —
  the half Q5 structurally cannot cover.

## 5 · The gate — narrower than either side first proposed

Gating on *soundness* is impossible. Verbatim-quote matching is gameable — a
real quoted line can refute nothing — and **`path:line` resolution is gameable
in exactly the same way, and is in fact the CHEAPER of the two to fake**, since
citing `file.py:1` costs less than finding a line worth quoting. An earlier
draft implied the second was substantively stronger. It is not. It is chosen for
being **cheap and safe to check**, not for being harder to game.

What makes it worth having anyway is the honest, small claim below. Gate on
exactly this:

1. **All five Layer 1 slots are present**, as literal machine-detectable
   headings `### Q1` … `### Q5`, each with a non-empty body. Answering Q1 and
   dropping Q2–Q5 must red.
2. **At least ONE resolving `path:line` citation**, unless every claim in the
   section carries the `` `OWNER-DEPENDENT` `` marker — the single, precisely
   defined exemption, because an owner-held fact has no citable source and
   marking it is the honest answer.
3. **Every `path:line` citation present RESOLVES** — the file exists and has at
   least that many lines. Pure fact extraction, no prose inference; the trick
   `route_docs.py` already uses.
4. **A Layer 2 outcome marker exists** — see § 5b.
5. **Commands and error strings are RECORDED but NOT GATED.** Re-executing them
   in CI is unsafe — they are stateful and possibly destructive — and
   regex-matching their shape is theatre.

> **Rules 1 and 2 exist because Codex found the gate passed vacuously without
> them** (PR #580, P1). An earlier draft gated only on "section non-empty" plus
> "every citation resolves" — so a card reading `## Provenance` / *"Based on
> general knowledge"* satisfied both: non-empty, and zero citations means all
> citations resolve. The gate's own headline claim, that *"'I based this on
> general knowledge' cannot produce a resolving citation"*, was false of the
> gate as specified. It is true only once a citation is REQUIRED.

### 5b · Layer 2 must leave a mark

The reviewer call is un-gated on **success**, never on **occurrence**. Without
this a triggered PR passes every check and merges with Layer 2 never having run,
and the two-layer mandate silently collapses to Layer 1 exactly when time or API
availability is inconvenient (Codex, P1).

One of three literal markers is required:

    ### Layer 2: completed — <path to the recorded exchange>
    ### Layer 2: attempted-failed — <verbatim provider error>
    ### Layer 2: deferred — <reason>

Fail-open on the provider being down; **never** fail-open on the record.

### What this buys, stated honestly

It catches an **absent** answer, not an unsound one. With rules 1–2 in place,
*"I based this on general knowledge"* genuinely cannot pass — which is what the
earlier draft claimed and did not deliver.

This is the same division the estate already runs and does not call theatre: the
session-card checker verifies the card exists and is complete; the owner judges
whether it is any good.

## 6 · Routing

**Vertex** for review volume — prepaid credit, no daily cliff.

`GEMINI_API_KEY` (free tier) is fine for AI Studio calls and serves the
Interactions API, but carries ~20 req/day on flagship Flash.
`GEMINI_API_KEY_PAID` bills a real card and is for two cases only: Vertex has
actually failed, or Deep Research, which exists on no other path. Full recipe
and billing chain: `docs/conventions/vertex-first-for-gemini.md` (fleet-manager).

## 7 · Two practices this spec adopts

Both came out of running the mechanism on real work, and both are missing from
every earlier version of this plan.

### a) Test a new instrument out of bounds BEFORE trusting it

`MEASURED` 2026-08-05: a coverage figure was wrong because a correlation search
**silently clamped** instead of failing when asked for a value outside its
range. It returned a plausible number, not an error. One known-bad input would
have exposed it.

**Rule:** when introducing a measurement tool, feed it a case you know it cannot
handle and confirm it fails **loudly**. A tool that degrades quietly is worse
than no tool, because its output looks like data.

### b) Flag owner-dependent claims explicitly

`MEASURED`: five of the owner's thirteen corrections came from ground truth only
he holds — his screen, his thumb, his console, his billing page.

An agent cannot self-diagnose missing tacit knowledge, but it **can recognise
the domains**: anything about what the owner did, saw, intended or decided, and
anything about hardware or accounts it cannot read. In those domains, **mark the
claim owner-dependent rather than asserting it.**

## 7b · Specifications the review found missing

All four came out of the 2026-08-06 run: three from the Layer 2 reviewer's
context-specific follow-ups, one from the author's own Q5.

### The owner-dependent marker (§ 7b needs a syntax)

Inline: **`` `OWNER-DEPENDENT` ``** immediately before the claim. Machine-visible
so the checker can count them, human-visible so a reader sees the hedge without
hunting. A claim carrying it is exempt from the citation requirement by design —
it has no citable source, which is the point of marking it.

### The out-of-bounds test for the reviewer itself (§ 7a, applied reflexively)

The plan states the rule and an earlier draft did not apply it to its own
instrument. Before `gemini_review.py` is trusted, feed it **four** cases — two
it must flag and two it must accept — and confirm it discriminates:

**Known-bad — it must FLAG all of these:**

1. A provenance section whose citations all **resolve but are irrelevant** —
   real `path:line` pointers into unrelated files. A reviewer that passes this
   is checking syntax, not provenance.
2. A confidently-worded claim with **no grounding at all**.

**Known-good — it must ACCEPT all of these:**

3. A claim with a **relevant** resolving citation.
4. A claim **appropriately hedged** to its evidence, including one correctly
   marked `` `OWNER-DEPENDENT` ``.

> **Cases 3–4 exist because Codex found the known-bad set alone is not a test**
> (PR #580, P1): a reviewer that flags *everything* passes both known-bad inputs
> while having zero discrimination. That failure is worse than useless here — it
> manufactures objections, burns the owner's attention, and would make § 9's
> instrument-origin ratio look like it improved. Sensitivity without specificity
> is not a qualification.

**The input contract this implies.** Case 1 is undetectable unless the reviewer
can SEE the cited text: a resolving-and-relevant pointer and a
resolving-and-irrelevant one are observationally identical to a model that
receives only the claim. So `gemini_review.py` must **resolve each citation and
include a bounded window of the cited lines** alongside the claim. Without that
the reviewer collapses to the syntax check § 5 explicitly rejects (Codex, P1).

If it fails any of the four, it is not usable — loudly, not as a degraded
score.

### Where survived-vs-conceded is recorded, so § 9 can be computed

**Two records, because they answer different questions** — an earlier draft
conflated them and could not compute § 9 (Codex, P2).

**(i) Objection disposition** — one line per Layer 2 objection, for honesty
about deference:

    - [survived] <objection> — <evidence that refuted it>
    - [conceded] <objection> — <what changed>
    - [partial]  <objection> — <what changed, what stood>

**An all-`conceded` record is a smell, not a success**: it is equally consistent
with rigour and with deference.

**(ii) Correction origin** — one line per CORRECTION actually made, which is
what § 9 counts. Disposition tags cannot supply this: `[survived]` contains no
correction at all, `[partial]` mixes corrected and surviving material, and a
correction the agent found while answering Layer 1 gets no objection tag ever.

    - [origin:self-reread]  <what changed>
    - [origin:layer1]       <what changed>
    - [origin:layer2]       <what changed>
    - [origin:instrument]   <what changed> — <which checker/exporter>
    - [origin:owner]        <what changed>

§ 9's ratio is then `(layer1 + layer2 + instrument) / total`, over a stated
observation window. **Both records are required; neither substitutes for the
other.**

### The § 9 baseline, captured BEFORE rollout

The ratio has nothing to move from until a baseline exists. Capture it from the
existing record — the session cards already on `main` — before the first gated
PR, or § 9 is unfalsifiable.

## 7c · The trigger set

An earlier draft's file-path table was removed after the reviewer showed
path-triggers are blind to omissions, and was not replaced. It is replaced here,
and the blindness is stated rather than papered over.

**Fires on a PATH:** a diff touching `docs/decisions.md`,
`docs/program/rulings.md`, `CONSTITUTION.md`, `docs/planning/**`,
`src/engine/guards.py`; or a release tag / distribution wave.

**Fires on a CARD TAG** — three literal headings, not prose inference:

    ### Decision: <one line>
    ### Deferral: <one line>
    ### Honest null: <one line>

> **The tags are literal because Codex showed the prose version was
> unimplementable** (PR #580, P1). An earlier draft said the trigger fires on "a
> card that declares a decision, a deferral or an honest null" — which a checker
> can only reach by keyword matching (misses rephrasings, fires on incidental
> discussion) or by model classification (which makes a gate advertised as
> deterministic nondeterministic). A literal heading is neither.

**Fallback if the tags prove unusable in practice: trigger on every session
card.** Noisier, still deterministic, and strictly better than a gate nobody can
implement.

**Does not fire on:** routine commits, typo fixes, mechanical refactors,
telemetry deltas, roster regens.

**The known hole, stated plainly.** Path triggers fire on modification, card
triggers fire on *acknowledged* choices. Neither fires on a decision the author
does not recognise as one — which is the failure mode that motivated the whole
plan. The card trigger would have fired on 2026-08-06 only because that session
happened to write its deferral down. **This trigger set covers the conscious
subset and no more.** It is not a guarantee and must not be described as one.

## 8 · Build order

1. **The blast-radius exporter** — deterministic, un-gameable, cheapest.

   **It must map a specific change to its specific consequence, not print fleet
   metadata** (Codex, P2): an implementation that emits the same adopter count
   and distribution mode for a docs-only edit and a breaking dist change
   satisfies a loose spec while detecting nothing. Required:

   - **Input:** the diff's changed paths (authoritative: `git diff --name-only`
     against the merge base).
   - **Mapping, deterministic per path class:**
     `dist/bootstrap.py` or `src/engine/**` → every adopter, on their next
     upgrade PR · `src/engine/templates/**` → adopters that re-render that
     template · `docs/**` (kit-local) → nobody downstream ·
     `.github/workflows/**` → this repo only.
   - **Adopter set + versions:** `docs/adopters.md`, whose limits are stated
     below.
   - **Rollback:** presence of a banked artifact under `.substrate/backup/`,
     reported per affected repo — a fact about this change, not about the fleet.
   - **Reversibility:** derived from the path class (a generated artifact is
     regenerable; a hand-edited planted doc is not).

   **Stated limit:** `docs/adopters.md` is generated by `currency.py`, which
   fetches a repo's config, two known bootstrap paths and its heartbeat files —
   **it does not enumerate committed trees.** It therefore establishes what each
   repo VENDORS and cannot establish the absence of some other live linkage. The
   exporter must not claim otherwise.
2. **The provenance section + its `path:line` gate** — the Layer 1 list as a
   session-card section, and a checker that verifies the section is non-empty
   and every citation resolves.
3. **The reviewer call** (`gemini_review.py`, Vertex-routed) — un-gated on its
   RESULT, but its **occurrence is gated** by § 5b: one of
   `completed` / `attempted-failed` / `deferred` must appear on the card. An
   earlier draft of this line said flatly "un-gated", which contradicted § 5b
   the moment that section was added.

Both scoped to **substrate-kit's decision surfaces first**, before any adopter
sees them.

## 9 · Measurement — this is testable, unusually for a process change

Track the **ratio of corrections originating from an instrument or reviewer
versus from an agent re-reading its own work.**

If the mandate works, that ratio moves. If it does not move, this is ritual and
we will know. Record the ratio, not a satisfaction judgement.

## 10 · What this does not claim

- It does **not** instrument judgment. It raises the odds that an unsourced or
  overconfident claim meets one question before it lands.
- **False-negative rate is `NOT-VERIFIABLE`** by construction — the estate's
  standing position (`fleet-manager
  docs/findings/2026-08-05-foundation-continuation.md` § 2). What is measurable
  is § 9's ratio.
- The reviewer has a **known error rate**. One prior review was flatly wrong
  about a dependabot deadlock; another overclaimed on video coverage and was
  caught only by independent measurement. **Record what survived review, not
  only what was conceded** — a report of "all objections conceded" is equally
  consistent with rigour and with deference, and the two must be
  distinguishable.

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
