# 2026-08-03 · Claims about the owner are asked, not inferred

> **Status:** `complete`

- **📊 Model:** opus-5 · high · docs-only

## What shipped

The `CLAUDE.md.tmpl` "Verifying a claim" section gains a fourth clause:

> **A claim about the owner is checked by asking them.** … the repository is
> evidence of the work, not of the person, and a story that fits the work is not
> thereby true. … **If the owner did not say it, ask — or mark it `inferred` and
> leave it out of the profile.**

## Why it needed its own clause

The rule shipped hours earlier says *"if a statement is checkable with one
command."* A claim about the owner is not. It is checked by asking, and the
adopter session that requested this had just made two such claims in consecutive
messages — inventing how the owner reviews work, then inventing why he
remembers it — both plausible, both fitting the evidence, both wrong, and the
new rule caught neither.

**The stake is structural, and it is why the clause names a file.**
`${owner_profile}` is not a note: it renders into `owner-profile.md.tmpl` **and**
into `CLAUDE.md.tmpl`'s own working-style section. So a wrong inference about the
owner does not sit in a paragraph someone might re-read — it becomes boot context
for every later session, presented as fact, in the file that opens the session.
The owner's own framing, and it is sharper than the one it replaced: *"I wouldn't
want wrong claims about the way I work be documented in the repo."*

`test_owner_claim_rule_names_the_surface_it_protects` pins both slots, so if
either moves, the clause's stated stake fails loudly rather than quietly going
stale.

## Evidence

- `python3 -m pytest tests/ -q` — **2078 passed, 1 skipped**.
- `python3 -m ruff check src/engine/` — all checks passed.
- `python3 tools/check_no_false_walls.py` — **OK** (the clause is phrased as a
  practice; the existing forbidden-word pin still holds over the section).
- `python3 src/build_bootstrap.py` — rebuilt; tree clean after.

## 💡 Session idea

**The claims most worth checking are the ones with no command to check them
with.** A verification rule written around commands will collect exactly the
cases that have commands, and will read as complete while the uncheckable claims
walk past it — which is what happened here, within hours, in the same session
that wrote the rule.

The tell is availability, not importance: `printenv` exists, so "is the
credential there" gets checked; nothing runs to confirm "this is how the owner
works", so it gets asserted. **Where a cheap check exists, behaviour follows it;
where none exists, confidence fills the gap** — and the second set is where the
claims about people live, which is also where being wrong is least visible and
most durable.

The generalisation worth keeping: when writing a verification rule, **enumerate
the claim types that have no command, and name their check explicitly.** For
claims about a person the check is asking. For claims about intent it is
quoting. For claims about the future it is not making them.

## ⟲ Previous-session review

The card three hours ago argued that seeding another rule changes nothing and
that activation is the real problem — correct, and this slice is its first test.
It also predicted the failure mode it did not cover: it framed the rule entirely
around one-command checks, and the very next uncaught error was a claim with no
command behind it.

**Workflow improvement:** that card's own idea section said to ask of any process
rule *"when does it fire?"* The complement is now earned — **also ask what it
does not fire on.** A rule stated as a sufficient condition ("if checkable with
one command…") silently defines everything outside it as fine. Naming the
excluded set inside the rule costs one sentence and is the difference between a
guard and a guard-shaped hole.
