# 2026-08-06 · The restate requirement belongs in the prompt, not in a skill

> **Status:** `complete`

- **📊 Model:** opus-5 · high · template

💡 Session idea: `intake` has always required a session to state back its
understanding before acting. A session opened from a `continuation-prompt`
handoff has **invoked no skill yet** — so the requirement lived somewhere the
reader would never open. A rule the reader never opens is not a rule; it is a
note to whoever already agreed with it.

## What happened

The owner recorded a session starting from a kit-generated handoff prompt. Its
entire first substantive response:

> *"I'll start by getting oriented — checking the environment, then landing
> #602 as instructed."*

A statement of first **action**, not of **understanding**. Nothing in it the
owner could correct, so his one cheap chance to redirect the session was spent
on an announcement. The rest of that session was strong — it caught a PR state
that contradicted its own handoff, caught a stale required-checks claim, and
measured an 85 % advisory-noise ratio. **This is not what a careless session
looks like.** It is what a good session looks like when the instruction is
somewhere it will not read.

The requirement was already written down, in `intake` § RESTATE step 2, and had
been for a long time.

## The change

`_CONTINUATION_PROMPT_BODY` gains a **`BEFORE YOUR FIRST TOOL CALL`** section,
emitted **verbatim into every generated prompt** — explicitly not as a link:

> state back what you think this task is. Inline in your first reply, not as a
> question, in a few sentences: the goal in your own words, the specs and
> constraints it implies, the scope you take it to cover, and the follow-on the
> owner probably wants but did not spell out.

With the two traps that make the block worthless if missed:

- **A plan is not an understanding.** *"I'll verify state, then classify the
  checkers"* restates the prompt. What is wanted is what the prompt did not say
  — what the goal implies, what it likely extends to.
- **It is not a question.** Stated inline, then proceed. Blocking for approval
  spends the owner's attention rather than saving it, inverting the purpose.

## Why placement, not emphasis

The owner offered two options — link the document, or put the request in the
prompt. **Linking is the weaker one**, and 2026-08-05 is the evidence: three
rules were written that day and each was broken within hours by the session that
wrote it. A pointer a session may or may not follow is the failure mode, not the
fix. `intake` binds a session that invokes `intake`; a handoff is consumed by a
session that has invoked nothing.

Same reasoning as THE DISCOVERY RULE step 1 in the CAPABILITIES template.

## Verification

- `python3 -m pytest` → **2116 passed, 1 skipped** (was 1 failed before the
  rebuild: `test_committed_bootstrap_is_current` correctly caught that
  `dist/bootstrap.py` had not been regenerated from the edited source).
- `python3 src/build_bootstrap.py` → rebuilt, 1 370 234 bytes.
- `python3 dist/bootstrap.py check --strict` → recorded at close.

## Honest nulls

- **Unmeasured whether it changes behaviour.** One incident motivated it; no
  session has yet been observed receiving a prompt that carries the block.
- **Adopter repos do not get this until they upgrade.** fleet-manager's local
  copy was edited directly in the same change; every other repo carries the old
  body until a distribution wave reaches it.
- **`implementation-prompt` is not in the kit** — it is fleet-manager-local and
  was fixed there, so the two skills are only in sync by hand today.
