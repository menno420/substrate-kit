# 2026-08-03 · Verify-before-assert enters the agreement template

> **Status:** `complete`

- **📊 Model:** opus-5 · high · docs-only

## What shipped

`CLAUDE.md.tmpl` gains a **"Verifying a claim"** section, so every future seed
and every `upgrade --apply-docs` carries it. Pinned by
`tests/test_verify_before_assert.py`; `dist/bootstrap.py` rebuilt.

> **If a statement is checkable with one command, run the command before writing
> the sentence.** … Provenance discipline applies at the moment of **stating**,
> not at the moment of writing the doc. … **A plausible cause is not a checked
> cause**, and that includes plausible explanations for your own mistakes.

## Why it is not "another rule"

The adopter session that produced this had the rule already. Its rendered
agreement routes to the capability ledger *before declaring any wall*, with the
discovery rule inline — **step 2 of which is check the env.** That is
`printenv`. It was in context the whole session and was quoted in the very
ledger entry that violated it. The adopter also had provenance labelling and
applied it *correctly*, in the same file where an unchecked assertion sits four
paragraphs above its own provenance block.

**So distribution worked and activation did not** — which is the owner's own
diagnosis, and it decides the shape of the fix. Seeding another rule would have
changed nothing. What was missing is that provenance labelling **fires when you
write a provenance block**, so provenance blocks are honest and prose is not.
This section moves the trigger from the artifact to the assertion. That is its
whole content; everything else in it is worked examples.

Third pin is deliberate and defensive: the section must read as a **practice**,
never as a declared limitation, because `check_no_false_walls` scans
`src/engine/templates/*.tmpl` and the owner's principle there is that forward
surfaces record capabilities, never walls. The test asserts the section contains
no "cannot / can't / unable to / not allowed to / no access".

## Evidence

- `python3 -m pytest tests/ -q` — **2077 passed, 1 skipped**.
- `python3 -m ruff check src/engine/` — all checks passed (the 3 findings in a
  full-tree `ruff check .` are pre-existing; confirmed by stashing this change
  and re-running).
- `python3 tools/check_no_false_walls.py` — **OK**.
- `python3 src/build_bootstrap.py` — re-run after the edit; `dist/bootstrap.py`
  carries the new template and the tree is clean afterwards.

## 💡 Session idea

**A rule that is delivered but not activated is indistinguishable, from the
outside, from a rule that was never written — and the two have opposite fixes.**
Every instinct on seeing a repeated fault is to write the rule down. Here it was
already written down, seeded by design into every adopter, sitting in the boot
file, and read at session start. Writing it again would have produced a
better-documented fleet and the same errors.

The distinction worth keeping: **delivery is solved by seeding; activation is
solved by making a rule fire at the moment of the action, not at the moment of
reading.** Provenance labelling works precisely because it fires at a keystroke.

A cheap test to apply to any process rule in this kit: **ask when it fires.** If
the answer is "when someone remembers it", it is documentation. If the answer is
"at the keystroke where the mistake is made", it is a guard. Both are worth
having — but only the second one changes behaviour under load, and shipping the
first while believing you shipped the second is how a fault survives three
sessions of being written up.

## ⟲ Previous-session review

The last card here closed the Self Improvement seat cleanly and left the
templates as the fleet's forward surface. That framing is what made this change
one file instead of twenty: the rule lands once in the template and reaches every
adopter through the normal seed/upgrade path, with no per-repo wiring — the same
shape `check_no_false_walls` used when its grammar moved into the engine.

**Workflow improvement:** this rule arrived because an adopter session made the
same class of error three times in one day and the owner caught all three. The
kit has no path for *"an adopter learned something the template should carry"*
other than someone noticing. A one-line convention would close it: **when a
session card's lesson would apply to a session that is not this one, it belongs
in the template, not the card** — a card is a record, the template is a rule.
