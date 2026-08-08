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

## 5 · The gate — facts only, and it claims nothing more

> **⚠ SUPERSEDED 2026-08-07 — owner decision: v1 ships UN-GATED. The gate below
> is not built.** Round 6 removed its cheap-implementation premise
> (`session_markers` is global, not conditional — the BLOCKING note below), and
> the owner resolved that fork by dissolution: with no gate, the
> global-vs-conditional question does not arise. The **principle box
> immediately below survives as doctrine** — it is part of the retained core
> that took zero findings across all rounds; only the enforcement mechanism is
> dropped. Layer 1 and Layer 2 ship as practice (§ 8), their occurrence
> recorded on the card but not gated.

> ### MECHANISE FACTS. NEVER MECHANISE MEANING.
>
> **Facts a script settles:** does the file exist · does the line resolve · are
> the headings well-formed · is the section present. Cheap, exact, already
> proven here.
>
> **Meaning no script settles:** is this citation *relevant* · is this claim
> *genuinely* sourced. Four review rounds on one defect class is what trying
> looks like.
>
> The line was drawn correctly by instinct once already and is worth naming:
> when round 4 added citations, a script verified they RESOLVED and the author
> judged whether they were LOAD-BEARING — and said so rather than pretending
> the script had checked it. That is the rule, in one commit.
>
> This is `fleet-manager
> docs/findings/2026-08-05-foundation-continuation.md` § 5 restated:
> deterministic checkers to hard gates, heuristics off the agent's path. **A
> deterministic checker over PROSE is neither** — it is the category error, and
> five review rounds demonstrated it from four angles before it was named.

### ⚠ BLOCKING — the free clauses are free in COST but GLOBAL in SCOPE

`MEASURED` 2026-08-06, Codex round 6, verified in this tree:
`check_session_log.missing_markers` scans **every configured needle against
every completed card**, and `check_added_card` calls `check_log(path, markers)`
on any added card. `session_markers` has no conditional form.

So putting the provenance and Layer 2 clauses in `session_markers` does **not**
implement the § 7c conditional trigger set. It silently implements the
*fallback* — **gate every session card** — in every adopter that upgrades, and
reds unrelated work that never touched a decision surface.

**This undercuts a premise of the 2026-08-06 scope decision**, which rested on
"three of four clauses are free". They are free to run and cannot be made
conditional by that route. The options are a conditional checker (so all four
clauses land in `check_provenance`, and "mostly free" is no longer true), or
accepting gate-every-card as the actual design and saying so. **Owner decision;
not resolved here.** The table below describes the intended clauses and is not
implementable as written until that is answered.

### The four clauses, and what each costs

| Clause | Mechanism | Cost |
|---|---|---|
| Provenance section present, non-empty | a `{label, needle}` entry in `session_markers` (`lib/config.py:248`) | **free** |
| Layer 2 occurred | same — a `### Layer 2:` needle | **free** |
| ≥1 citation present | `check_provenance` | cheap |
| Every same-repo `path:line` resolves | `check_provenance` | the one clause with four rounds against it |

Three of four ride machinery that already exists and is already required: the
session gate became a **required** check this morning and caught two real misses
on hub cards the same day. Only the last two clauses need new code, and they are
one small checker.

### What it claims — and this is the whole claim

**It catches an ABSENT answer. Nothing else.**

Not an unsound one, not an irrelevant citation, not a well-formed lie. A
resolving `path:line` can point at something that refutes nothing, and it is
*cheaper to fake than a verbatim quote*. That limitation is **not a defect to be
fixed in a later round** — it is the boundary between fact and meaning, and
every attempt to cross it produced a finding.

`"I based this on general knowledge"` cannot produce a resolving citation. That
sentence is the entire warranty. Anything stronger has been tried and failed:
verbatim-quote matching, per-claim exemption inference, a second model scoring
relevance.

### Cross-repo citations

`repo:path:line`. **Recorded, never gated** — CI has no sibling checkout, and
pinning external trees to make a doc check pass would be faking verification,
which is the thing PL-015 exists to stop.

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
can SEE the cited text. So `gemini_review.py` resolves **same-repo** citations
and includes a bounded window of the cited lines alongside the claim.

**Cross-repo citations are passed as UNRESOLVED, and the reviewer is told so**
(Codex, round 3, P1). CI has no sibling checkout — § 5 says so — and an earlier
draft nonetheless required the script to resolve *each* citation, which is
unsatisfiable for exactly the citations the mandate's own record leans on. The
reviewer therefore **cannot judge relevance of cross-repo evidence and must not
pretend to**; it reports them as unverified pointers. That is a real reduction
in coverage and it is preferable to a reviewer that appears to check something
it never saw.

If it fails any of the four, it is not usable — loudly, not as a degraded
score.

**Qualification is pinned, not perpetual** (Codex, P2). A qualification run
certifies one *configuration*, and § 6 selects a route but no version. Each
review record must carry the **exact model id, the prompt version, and the
citation-window size**, and the four controls **must be re-run whenever any of
them changes**. Without this, a model alias moving underneath the route can turn
the reviewer into one that accepts everything — or flags everything — with no
recorded check ever going stale.

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

The ratio has nothing to move from until a baseline exists — and it **cannot be
recovered from the existing cards**, which predate the `[origin:*]` schema and
contain none of it (Codex, round 3, P2). Reading origins back out of them means
undocumented retrospective classification, not comparable with a structured
post-rollout count.

So the baseline is **prospective**: run Layer 1 + Layer 2 and record
`[origin:*]` lines for a stated number of sessions **with the gate OFF**, then
enable it. If that costs more than the measurement is worth, the honest move is
to drop § 9's claim to be testable — not to fake a baseline.

## 7c · The trigger set

An earlier draft's file-path table was removed after the reviewer showed
path-triggers are blind to omissions, and was not replaced. It is replaced here,
and the blindness is stated rather than papered over.

**Fires on a PATH:** a diff touching `docs/decisions.md`,
**`docs/decisions/NNN-*.md`** (the repo's ADR shape, defined at
`docs/house-style.md:48`, and a distinct surface from the ledger — an ADR
avoided the trigger entirely in an earlier draft), `docs/program/**`,
`CONSTITUTION.md`, `docs/planning/**`, `src/engine/guards.py`; or a release tag
/ distribution wave.

> **Implementation note, 2026-08-07 (Codex round 5, dispositioned):** any
> implementation of this path trigger must use `git diff --name-status -M` (or
> equivalent) and treat a rename's **source** path as governed — `--name-only`
> drops it, so moving a governed file out of a triggered directory would escape
> both the trigger and the impact mapping.

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

**Does not fire on:** any diff touching none of the paths above and carrying
none of the three tags. That is the whole exclusion rule — it is the complement
of the fire rule, and needs no judgement.

> **The semantic exclusions are GONE** (Codex, P1). An earlier draft excluded
> "routine commits, typo fixes, mechanical refactors" — categories a checker can
> only reach by classifying a diff, which is exactly the prose-classification
> problem this section rejects two paragraphs earlier, and which additionally
> collided with the path rule (a typo fix under `docs/planning/**` matched both,
> with no precedence defined).
>
> The escape hatch is explicit, not inferred: a PR labelled
> **`provenance-not-required`** skips the gate, and the label is recorded. A
> human opting out on the record beats a checker guessing what "routine" means.
>
> **The label bypass requires a CI trigger change** (Codex, round 3, P1).
> `ci.yml` declares a bare `pull_request:` with no `types:`, so it uses the
> default activity set, which **excludes `labeled` and `unlabeled`**. A PR could
> pass while exempt, have the label removed, and keep the green required check
> straight through auto-merge — never supplying provenance. The gate must add
> `types: [opened, synchronize, reopened, labeled, unlabeled]` and re-evaluate
> the CURRENT label state on each run. Without that trigger change the exemption
> is a stale-able bypass and must not ship.

**The known hole, stated plainly.** Path triggers fire on modification, card
triggers fire on *acknowledged* choices. Neither fires on a decision the author
does not recognise as one — which is the failure mode that motivated the whole
plan. The card trigger would have fired on 2026-08-06 only because that session
happened to write its deferral down. **This trigger set covers the conscious
subset and no more.** It is not a guarantee and must not be described as one.

## 8 · Build order

> **⚠ AMENDED 2026-08-07 — after the mechanism was finally RUN** (measured
> record: fleet-manager
> `docs/findings/2026-08-06-provenance-mechanism-measured.md`). The intro line
> below ("ship the gate stripped…") is superseded: **v1 ships with NO gate**
> (§ 5 marker). Step 0's trigger and payload are superseded: a framed reviewer
> run showed **`UserPromptSubmit` fires before the agent has read, run or
> concluded anything**, so its question has no referent — the 11/11 below
> scored event *coverage*, not askability. The trigger is **`Stop`**; the
> payload is a **procedure, not a one-line injection** (the one-line constraint
> fell with the payload type); and the shape built first is the hook **running
> the review itself** — transcript → framed reviewer call → questions as the
> block reason — which removes agent initiative entirely. Built and
> chain-tested live in fleet-manager (`.claude/hooks/owner_review.py`,
> 2026-08-07) before any adopter sees it. The scoring table, the
> no-hardcoded-frequency rule and the named gap below survive as the record
> that got here.

**Decided by the owner 2026-08-06, after five review rounds:** ship the gate
**stripped to what a script can factually check**, claiming nothing beyond
*"this catches an absent answer"*. Not "no gate" — a small, honest one.

0. **The hook — and it is next, ahead of the exporter.** A skill cannot be the
   mechanism: `intake` § RESTATE has required the restate step for a long time
   and did not fire, because no session invoked it. Agent initiative is exactly
   as unreliable as everything else this mandate distrusts. The doc-routing
   hook, by contrast, fired 4+ times unprompted today including in a session
   that was not its author's.

   Scored against 11 attributed failures from 2026-08-06:

   | trigger | coverage | note |
   |---|---|---|
   | `git push` | 7/11 (63%) | misses every chat-only claim; mostly catches what CI catches anyway |
   | card write | 6/11 (54%) | — |
   | `Stop` (turn end) | 11/11 | the claim is already written; the fix is a rewrite |
   | **`UserPromptSubmit`** | **11/11** | same coverage, but **before** the claim — the fix is a sentence of framing |

   The four `git push` would miss are precisely the ones where the owner is
   currently the only instrument: *"403-walled"*, the skipped restate, the
   skipped read path, the growth misread. None touched git; all reached him as
   prose.

   **No hardcoded frequency.** "Once per session" fails because a session has no
   fixed length — 3 turns and 200 turns mean entirely different things. The rate
   must be set by the work: the doc-routing hook has **no counter at all**, it
   dedupes on topic touched, and its rate emerges from what the session did.
   Here, `UserPromptSubmit`'s rate is the owner's message cadence. Zero
   constants.

   **Cost constraint that follows:** firing before every owner message means the
   content is **ONE LINE**. Not a checklist. Longer, and it becomes the advisory
   noise field the checker classification just removed.

   **Named gap, not solved:** a claim asserted mid-turn with no state change and
   no new prompt — an agent talking itself into something across a long
   autonomous stretch. There is no factual signature for it. Left named rather
   than invented around.

> **⚠ DEFERRED 2026-08-07 — specified over data the estate does not have.** Its
> own stated limits are disqualifying for v1: template impact is `unknown` by
> construction, `docs/adopters.md` cannot refresh in CI (agent-generated, 16
> days stale at review time), the kit sits inside its own adopter set, and
> `release.yml` is downstream-facing. Same test the gate failed — specifying it
> correctly has cost more than it has returned. Rebuild only when a sourceable
> per-template data model exists (the registry addition named in the note
> below).

1. **The blast-radius exporter** — deterministic, un-gameable, cheapest.

   **It must map a specific change to its specific consequence, not print fleet
   metadata** (Codex, P2): an implementation that emits the same adopter count
   and distribution mode for a docs-only edit and a breaking dist change
   satisfies a loose spec while detecting nothing. Required:

   - **Input:** the diff's changed paths, `git diff --name-only`. Base by event:
     **PR** → the merge base. **Release** → the gate runs on the **pre-tag
     version-bump PR, not at tag time** (Codex, round 3, P1): a release diff
     spans every card since the previous tag, so selecting "the latest card"
     validates an unrelated session and selecting none makes the trigger a
     no-op. The tag job verifies the bump PR carried a passing provenance
     record and reds if it did not. The exporter's diff base at release is the
     previous `v*` tag, with
     `fetch-depth: 0` added to `release.yml`'s checkout, which today requests no
     depth at all while `ci.yml:25` explicitly sets it — so the changed-path
     input is currently uncomputable at the one trigger that most needs it
     (Codex, P1). If a base still cannot be resolved, the exporter **records
     `base-unresolved` and reds**; it never silently reports an empty diff.
   - **Mapping, MOST-SPECIFIC PATTERN WINS** (Codex, P2 — `src/engine/templates/**`
     matches both the template rule and `src/engine/**`, and without precedence
     two conforming implementations report different blast radii for the same
     change):

     | Pattern (most specific first) | Affected |
     |---|---|
     | `src/engine/templates/**` | **`unknown` — reds** (see note below) |
     | `src/engine/**`, `dist/bootstrap.py` | every adopter, on next upgrade |
     | `docs/program/**` | **every program repo** — canonical program law, cited not copied (`docs/program/README.md:5`); an earlier draft folded this into `docs/**` → "nobody downstream" and would have understated exactly the governance changes the trigger set exists to catch (Codex, P1) |
     | `docs/**` (kit-local) | nobody downstream |
     | `.github/workflows/**` | this repo only |
   - **Adopter set + versions:** `docs/adopters.md`, whose limits are stated
     below.
   > **Template impact is `unknown`, not a guess** (Codex, round 3, P2). An
   > earlier draft mapped `src/engine/templates/**` to "adopters that re-render
   > that template" — a set NO available source can produce. `docs/adopters.md`
   > carries versions and heartbeat state; `currency.py` fetches a config, two
   > bootstrap paths and heartbeats. Neither records which planted templates an
   > adopter re-renders. The exporter emits `unknown` and **reds** rather than
   > printing an understated adopter list that reads as fact. Fix it by adding a
   > per-template record to the registry, not by inferring one.

   - **Rollback:** presence of a banked artifact under `.substrate/backup/`,
     reported per affected repo — a fact about this change, not about the fleet.
   - **Reversibility:** derived from the path class (a generated artifact is
     regenerable; a hand-edited planted doc is not).

   **Stated limit:** `docs/adopters.md` is generated by `currency.py`, which
   fetches a repo's config, two known bootstrap paths and its heartbeat files —
   **it does not enumerate committed trees.** It therefore establishes what each
   repo VENDORS and cannot establish the absence of some other live linkage. The
   exporter must not claim otherwise.
> **⚠ Amended 2026-08-07:** the card **section** ships (Layer 1 as practice);
> the **checker does not** — § 5 is superseded, v1 is un-gated.

2. **The provenance section + its gate** — the Layer 1 list as a session-card
   section, and a checker implementing **the four clauses in § 5's table**. Deliberately
   NOT paraphrased here — read § 5. An earlier draft summarised it as "≥1
   resolving same-repo citation", which is the pre-round-3 GLOBAL rule, so an
   implementer following this checklist would have rebuilt the very gate § 5
   had just been corrected to reject (Codex round 4, P2 — the stale-paraphrase
   failure recurring in the note that warns against it).

   > Stated as a reference to § 5 rather than a paraphrase, because the
   > paraphrase drifted: an earlier draft of this step still said "non-empty and
   > every citation resolves" — the **pre-correction** contract — so an
   > implementer following the build order would have rebuilt the exact
   > zero-citation vacuous gate § 5 had just been fixed to reject (Codex, P1).
> **⚠ Amended 2026-08-07:** occurrence is **recorded, not gated** — v1 is
> un-gated throughout. And the reviewer's **system prompt is the load-bearing
> component**, measured: the same model, unframed, endorsed a known-wrong
> design and praised its specific defect. Use the owner-stand-in prompt
> committed verbatim in fleet-manager findings § 7, never a bare
> "review this" call.

3. **The reviewer call** (`gemini_review.py`, Vertex-routed) — un-gated on its
   RESULT, but its **occurrence is gated** by § 5b: one of
   `completed` / `attempted-failed` / `deferred` must appear on the card. An
   earlier draft of this line said flatly "un-gated", which contradicted § 5b
   the moment that section was added.

Both scoped to **substrate-kit's decision surfaces first**, before any adopter
sees them.

## 9 · Measurement — this is testable, unusually for a process change

> **⚠ SUPERSEDED 2026-08-07 — the primary metric measured the wrong thing.**
> Owner reframe, after the mechanism was run: the deliverable is **legibility,
> not prevention** — reasoning made checkable by a reader who does not already
> know the answer. The primary metric is **cost-to-falsify** (how much must the
> reader already know to check the claim?); the ratio below is kept as a
> secondary signal, computed with `[origin:owner]` rows excluded from the
> denominator (Codex round 6, dispositioned).

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


## 11 · The review record lives elsewhere

Seven review rounds (Gemini once, Codex six — **44 findings**: 42 inline + 2 in
a review body, script-counted against the API; 36 fixed · 1 partial · 7 open at
the 2026-08-06 freeze, all seven dispositioned 2026-08-07)
are recorded in
[`../reviews/2026-08-06-provenance-mandate-review-record.md`](../reviews/2026-08-06-provenance-mandate-review-record.md).

Kept out of this file deliberately: **this document is the instruction a session
follows at a decision surface, and it has to fit working attention.** The record
grows with evidence; the instruction must not grow with it.
