# Session 2026-07-09 — make_seed yield-keyword fix + prepare seed-suite smoke (pin-path, do-not-automerge)

> **Status:** `in-progress`

**Scope (about to do):** fix the run-2 make_seed bug (idea
`docs/ideas/make-seed-yield-keyword-bug-2026-07-09.md`): seed 424242 draws
the harvest/`yield` domain and `yield` is a Python keyword, so the generated
seed project is a SyntaxError. Ship (1) a keyword/builtin-safe measure
vocabulary + an identifier screen in `bench/seeds/make_seed.py` (seed 424242
generates a valid project), (2) a `prepare` smoke leg in `bench/run_ab.py`
that runs the generated seed's own pytest in BOTH arms and aborts prepare on
red, (3) regression tests pinning 424242 + a seed-sweep keyword-safety test.
`bench/seeds/` is a PIN PATH — this PR carries `do-not-automerge` from
creation and is LEFT OPEN for owner review (merge = ratification; unblocks
B1 run-3).
