# Differential-oracle testing — the cfgdiff method writeup (gen-1 flagship lesson)

> **Status:** `reference` — ported bench-practice method doc. Provenance:
> source repo `menno420/codetool-lab-sonnet5` @
> `66c3dfc79735db55dc777854eda6087ff9c45e02`; source passages
> `docs/retro/winddown-review-2026-07-09.md` §(ii) (line 51),
> `docs/succession/GEN2-FEEDBACK.md` item 10 (line 63),
> `docs/succession/PROPOSED-CUSTOM-INSTRUCTIONS.md` (lines 38, 73–75),
> `CHANGELOG.md` § [0.1.1], `tests/test_dotenv_differential.py` module
> docstring. Ported 2026-07-13 per fm ORDER 025 / plan ORDER P1-4
> (fleet-manager `docs/planning/2026-07-12-repo-consolidation-plan.md`
> § "Phase 1 — ORDER P1-4"), relayed kit-side as inbox ORDER 019 item 5.
> Content faithful to source; headings/links lightly adapted.

The one-day codetool-lab-sonnet5 arm (cfgdiff, a semantic config
diff/convert/validate CLI) produced one engineering lesson its own retros
rank above everything else it shipped: **running a corpus against a
reference parser found 3 real bugs behind green tests.** The kit's bench
practice carries it here so no lab session re-derives it.

## What happened (wind-down review §(ii), verbatim)

> **Differential-oracle testing — the flagship lesson.** The .env parser had
> 114 green tests and looked done. A differential corpus comparing it
> against python-dotenv (PR #9) found 3 real bugs, each contradicting the
> parser's own docstring: escaped quotes raised ParseError, non-ASCII in
> double quotes mojibaked (`héllo` → `hÃ©llo`), and `COLOR=#ff0000` was
> swallowed to `""`. All fixed in PR #11 with zero owner input. Your own
> tests encode your own misunderstandings; an external oracle does not.

## The three bugs (CHANGELOG § [0.1.1] Fixed, verbatim)

Three `.env` parser bugs found by the differential corpus (each contradicted
the parser's own documented behaviour):

- Escaped double quotes inside double-quoted values (`KEY="a\"b"`) no longer
  raise `ParseError`: the closing-quote scan is now escape-aware, so the
  value parses to `a"b`.
- Non-ASCII text inside double-quoted values (`KEY="héllo"`) is no longer
  mojibaked (`hÃ©llo`): backslash escapes are decoded per-sequence instead
  of round-tripping the whole value through `unicode_escape`, so
  `\n`/`\t`/`\uXXXX` etc. still work while literal Unicode passes through
  untouched. Unknown escapes (`\q`) are kept literally.
- A value-initial `#` in unquoted values (`COLOR=#ff0000`) is no longer
  swallowed as a comment: `#` starts an inline comment only when preceded by
  whitespace (including the whitespace right after `=`, so `KEY= # note` is
  still `""`).

## The method (corpus design, from `tests/test_dotenv_differential.py`)

The corpus targeted the retro's self-identified least-confident area (the
A3 confidence gap: a parser "written from scratch with no
reference-implementation cross-check"). Design, per the module docstring:

- Every case feeds the same file to both parsers — the hand-rolled parser
  and the reference implementation (python-dotenv's `dotenv_values`) — and
  asserts identical key/value readings, across quoting, escaping, comment,
  whitespace, and CRLF edge cases.
- Where the two legitimately diverge, the case is **kept (never deleted)**
  and marked `xfail(strict=True)` with the reason — e.g. "documented
  divergence" where the parser's own docstring deliberately specifies
  different behaviour.
- `strict=True` means fixing a divergence without updating its marker fails
  the suite, so the corpus stays honest in both directions.
- The bugs the corpus surfaced were fixed and became ordinary passing cases,
  with extra regression cases alongside them; the reference implementation
  rides as a dev-only extra (runtime dependencies unchanged).

## The rule (GEN2-FEEDBACK item 10 — proposed fleet-wide, verbatim)

> **Differential-oracle testing for parser/format code (NEW — this lane's
> flagship lesson).** A corpus diffing our .env parser against python-dotenv
> found 3 real bugs in code with 114 green self-written tests. Proposed
> template line: "any code that parses or emits a format with an existing
> independent implementation MUST carry differential tests against it;
> self-written tests alone are insufficient evidence of correctness."

The same rule as the source's proposed custom instructions phrased it: "No
'done' claim without independent verification … Any parser or
format-handling code MUST get differential-oracle tests against an existing
independent implementation, not only self-written cases." — the single
highest-value engineering lesson of the sonnet5 arm; "your own tests encode
your own misunderstandings."

## Why it lives with the bench docs

Kit-lab benchmark practice is built on the same principle at a different
altitude: the graded subject is never the grader (see
[`bench/README.md`](../../bench/README.md) — the integrity law, the pinned
external rubric, the independent judge). Differential-oracle testing is the
code-level instance: an oracle outside the measured system's write reach.
The companion port,
[the cfgdiff v0.1.1 release-decision writeup](2026-07-09-cfgdiff-v0.1.1-release-decision.md),
records the release decision that shipped these fixes.
