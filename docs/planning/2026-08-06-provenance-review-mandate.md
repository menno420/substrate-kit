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

- The **provenance section exists and is non-empty**.
- **Every `path:line` citation in it RESOLVES** — the file exists and has at
  least that many lines. Pure fact extraction, no prose inference. The same
  trick `route_docs.py` already uses: verify the pointer resolves, never judge
  the prose.
- **Commands and error strings are RECORDED but NOT GATED.** Re-executing them
  in CI is unsafe — they are stateful and possibly destructive — and
  regex-matching their shape is theatre.

### What this buys, stated honestly

It catches an **absent** answer, not an unsound one. *"I based this on general
knowledge"* cannot produce a resolving citation, and that is the whole claim.

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
instrument. Before `gemini_review.py` is trusted, feed it two known-bad inputs
and confirm it **flags rather than agrees**:

1. A provenance section whose citations all **resolve but are irrelevant** —
   real `path:line` pointers into unrelated files. A reviewer that passes this
   is checking syntax, not provenance.
2. A confidently-worded claim with **no grounding at all**. A reviewer that does
   not flag it has failed the one job it has.

If it agrees with either, it is not usable and the failure is loud rather than
a quietly degraded score — exactly what § 7a demands of any new instrument.

### Where survived-vs-conceded is recorded, so § 9 can be computed

The session-card section carries one line per objection:

    - [survived] <objection> — <evidence that refuted it>
    - [conceded] <objection> — <what changed>
    - [partial]  <objection> — <what changed, what stood>

Three literal tags, so the § 9 ratio is a count rather than a reading. **An
all-`conceded` record is a smell, not a success**: it is equally consistent with
rigour and with deference, and the tags exist to keep those distinguishable.

### The § 9 baseline, captured BEFORE rollout

The ratio has nothing to move from until a baseline exists. Capture it from the
existing record — the session cards already on `main` — before the first gated
PR, or § 9 is unfalsifiable.

## 7c · The trigger set

An earlier draft's file-path table was removed after the reviewer showed
path-triggers are blind to omissions, and was not replaced. It is replaced here,
and the blindness is stated rather than papered over.

**Fires on:** a diff touching `docs/decisions.md`, `docs/program/rulings.md`,
`CONSTITUTION.md`, `docs/planning/**`, `src/engine/guards.py`; a release tag or
distribution wave; **or a session card that declares a decision, a deferral or
an honest null.**

**Does not fire on:** routine commits, typo fixes, mechanical refactors,
telemetry deltas, roster regens.

**The known hole, stated plainly.** Path triggers fire on modification, card
triggers fire on *acknowledged* choices. Neither fires on a decision the author
does not recognise as one — which is the failure mode that motivated the whole
plan. The card trigger would have fired on 2026-08-06 only because that session
happened to write its deferral down. **This trigger set covers the conscious
subset and no more.** It is not a guarantee and must not be described as one.

## 8 · Build order

1. **The blast-radius exporter** — deterministic, un-gameable, cheapest. At a
   decision surface, extract and print: adopter count, distribution mechanism
   (pinned vs live), upgrade vector, rollback presence, reversibility.
2. **The provenance section + its `path:line` gate** — the Layer 1 list as a
   session-card section, and a checker that verifies the section is non-empty
   and every citation resolves.
3. **The reviewer call** (`gemini_review.py`, Vertex-routed) — un-gated;
   recorded on the card.

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

- **[survived]** *"The pinned-vendoring model is extended to 12 adopters from a
  1-repo check."* — Refuted with evidence. `docs/adopters.md` is generated from
  **each repo's committed tree** (the vendored `bootstrap.py` stamped header),
  not from one repo: 12 rows, 11 citing a vendored dist header. The twelfth,
  `superbot`, is pin-only with no vendored dist — an exception the registry
  already flags rather than a gap in the claim. The reviewer's untested
  sub-claim (submodules / floating refs as an alternate live path) was then
  checked directly: **zero `.gitmodules` across all 10 sweep clones.**

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

**Reviewer accuracy this run:** four substantive objections, two fully correct,
one correct-in-part, one refuted by evidence — plus three sound follow-ups. The
reviewer's known error rate held: it was wrong about something checkable, and
checking it took one command.
