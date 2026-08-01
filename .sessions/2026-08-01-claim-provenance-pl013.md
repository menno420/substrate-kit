# PL-013 — a measured claim carries its instrument (+ its advisory checker)

> **Status:** `complete`

**Session:** 2026-08-01 · consumer-driven rule extraction · substrate-kit
**Baton:** owner-directed. Working in spider-swing, the owner asked for a
claim-provenance marker convention and then said: *"I want you to also add_repo
the /substrate-kit and add it there, you should be able to determine the correct
place to add it, if not then the substrate kit itself is failing."* The kit's
navigability was explicitly the thing under test.

**About to do:** (A) append `## [PL-013]` to `docs/program/rulings.md`;
(B) build `check_claim_provenance` as an advisory checker + its test file;
(C) wire it into `cli.py`'s `posture="advisory"` seam, `MODULE_ORDER`, and the
remediation registry; (D) one citing line in `docs/house-style.md`; (E) rebuild
`dist/bootstrap.py`. Then adopt in spider-swing as the first consumer.

- **📊 Model:** opus-5 · high · feature build (new advisory checker + ruling)
- **⚑ Self-initiated:** NOT self-initiated — owner-directed, quoted above. The
  *placement* was mine to determine; the work was asked for.

## Where it belonged, and why (the owner's actual question)

The kit answered its own routing question, and the answer was more constraining
than "put the rule in a doc":

- `provenance` is **already a required field** in the `[PL-NNN]` grammar, and
  **PL-008** already demands a provenance + reliability header on every adopted
  tool. The doctrine existed; measurement *output* was simply not covered by it.
- **PL-007 — "Enforce, don't exhort"** — decided the shape. A prose-only
  convention would have violated the kit's own law, which puts written rules
  last on the ladder behind checker / CI / test → hook. So this ships as a
  ruling **plus** an enforcing check, not as a paragraph asking sessions to
  remember.
- **PL-006 — "source wins"** — supplied the actual argument for the rule. A
  number with **no stated instrument has no source to lose to**: nothing can
  ever show it wrong, so it is unfalsifiable by construction and compounds
  silently into every decision taken on top of it.

## What prompted it (the consumer evidence)

One spider-swing session published ~14 claims the owner then corrected. The
*measurements* were overwhelmingly sound; the **summary sentences** were not.
The load-bearing case ran three layers deep: `4.71 taps/s` was sampled at 30 fps
from a natively **60 fps** recording; a design constraint was built on that
number; the constraint was then cited as the reason the design was trustworthy.
Each layer was internally consistent, so no gate could see any of them. It was
caught only because the owner knew how fast he taps.

That is why "measured" is not sufficient on its own in PL-013's verdict: the
method *was* named on that claim. The **instrument's resolution** was not, and
that is precisely the gap the number fell through.

## What shipped

- `docs/program/rulings.md` — `## [PL-013]`. Scope declares it deliberately
  advisory; `check_program_law` green.
- `src/engine/checks/check_claim_provenance.py` — advisory, input-gated,
  fail-open, full PL-008 provenance + reliability + kill-switch header. One
  finding per *document*, never per row.
- `tests/test_check_claim_provenance.py` — 33 tests, weighted toward the
  load-bearing negatives (out-of-scope directory, non-result badge, no numeric
  table, one-row threshold, unreadable file) **and the sensitivity cases the
  first draft failed** (see below).
- `src/engine/cli.py` — import + `posture="advisory"` seam, mirroring
  `check_dateless_walls` exactly. Off `STRICT_SUBCHECKS` by design.
- `src/engine/checks/check_remediate.py` — `claim-provenance` remediation block
  (S8 coverage lesson: every emittable advisory kind carries one).
- `src/build_bootstrap.py` + rebuilt `dist/bootstrap.py`.
- `docs/house-style.md` — one line citing PL-013 by ID, body not copied.

**A collision the kit caught, not me.** My first draft defined a private
`_BADGE_RE`; `test_check_namespace.py` failed with
`_BADGE_RE: check_claim_provenance.py vs check_docs.py`. The dist concatenates
every engine module into one namespace, so the duplicate would have silently
shadowed. The fix was better than the original: use the exported
`check_docs.badge_token()` — the kit's own "one badge reader, not per-module
copies" — which already fails open on an unreadable file.

## The checker was wrong, and the corpus is what caught it

Worth recording in full, because the rule is about exactly this.

The first draft tested for the **vocabulary alone** — does `measured`,
`inferred` or `assumed` appear anywhere. It passed 23 tests, survived three
mutants, and worked end-to-end through the dist. Then it was run against the
**seven real spider-swing documents PL-013 was extracted from**, and fired on
**zero of seven**. Every one of them already used "measured" in ordinary prose
— *"the exploit is now measured"*, *"measured per track in isolation"* — so the
check had essentially **no sensitivity on the only corpus that mattered**.

Bolding was tried next as a discriminator and also failed: two of the seven
carry *bolded* incidental uses.

What survived was requiring a **labelled** statement — the literal word
"provenance" — AND the vocabulary. That measures **7/7 before the retrofit,
0/7 after**. It also gives PL-013 something the word-sprinkle version never
had: the instrument becomes greppable.

**This is the ruling's own failure mode, committed while writing the ruling.**
"The checker guards this class" was a claim about the world, it went into a
PR body and a session card before it was tested against real data, and it was
false. It is recorded in PL-013's `form` field rather than quietly fixed,
because a silently-corrected false claim teaches nobody.

**Verify.** `python3 -m pytest -q` → 2107 passed, 1 skipped.
`python3 dist/bootstrap.py check --strict` → exit 0, new advisory silent on this
repo (input-gated: the kit has no measurements directory).

**Falsified before trusting it.** Three mutants against the test file:
never-fires → 8 failures; ignore-markers → 4; drop-the-directory-gate → 1; all
restored green. End-to-end through the **built dist** on a synthetic tree.
Then the one that actually mattered — the real corpus, both states, above. The
five verbatim prose sentences that beat the first draft are now parametrized
regression cases in `test_incidental_prose_use_still_fires`.

## 💡 Session idea

**The advisory that would have caught the compounding, not just the source.**
PL-013 makes a number falsifiable; it does nothing about the third layer, where
a *constraint derived from* the number gets cited as evidence that the design is
sound. A cheap complement: warn when a doc cites a figure that another doc marks
`inferred` or `assumed` while presenting it as settled. Deduped: grepped
`docs/ideas/` and `docs/recipes/` — the nearest is `check_claims`, which checks
claim→evidence linkage within one doc, not provenance *decay across* docs.
Advisory-only, disposable, and genuinely might not be worth it — the honest
version of this idea is that I do not yet know if the cross-doc case is common
enough to earn a checker.

## ⟲ Previous-session review

**previous-session review:** the t5 doc/status reconcile (PR #552 follow-up)
landed a factual correction and named the right systemic lesson — *when a
session ships something that falsifies a premise written elsewhere, reconcile
that doc in the same session*. This session is the same lesson at one remove:
the spider-swing corrections falsified a premise about how measurement docs
should be written, and rather than fix the six affected documents in place, the
rule and its checker come back to the kit so the next repo never writes them
that way. What the previous card did well and I have copied: it verified PR #480
against GitHub ground truth **before** editing anything rather than trusting the
session record. The equivalent here was mutating the checker three ways before
believing its green.
