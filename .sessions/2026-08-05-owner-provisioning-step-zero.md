# 2026-08-05 · The owner's provisioning statements are step 0, not a claim to check

> **Status:** `complete`

- **📊 Model:** opus-5 · high · template

💡 Session idea: THE DISCOVERY RULE tells a session to attempt before declaring
anything impossible — and says nothing about the case where the **owner has
already told it the answer.** So sessions apply verify-first to the person who
provisioned the environment, and spend turns confirming a credential against
its own source. The rule was complete for records and inference. It had no entry
for authority.

## previous-session review

`2026-08-05-comprehension-exception.md` added the exception for a session whose
job is reading. Same shape, different surface: a correct default with no
carve-out for the case that inverts it. Both defaults are right and both were
being applied where they do not fit.

## What landed

- `src/engine/templates/CAPABILITIES.md.tmpl` — **step 0** of THE DISCOVERY
  RULE: an owner statement about provisioning is verified evidence; act on it.
  Carries the reason it is *not* an exception to verify-first, and the boundary
  as an explicit sentence rather than an implication.

## Why it is written the way it is

An entry that reads as *"do not verify"* loses to the surrounding evidence
doctrine, and correctly so — a skeptical session would resolve the conflict
against it and ignore it. So it is framed as the discovery rule **in the right
order**: attempt, then record. Verifying before attempting is the inversion, and
against the owner it is checking a source against its own output.

The boundary is stated flatly for the same reason. He is authoritative on
**provisioning**. He is not claiming a given call returns 200 — proxy paths,
stale refs, rate limits and typos are all still real, so every response is read
and every real error reported verbatim. Removing the pre-flight doubt does not
remove the check; it moves it after the attempt, where step 3 always wanted it.

## Verification

- `python3 src/build_bootstrap.py` → **exit 0**.
- `python3 -m ruff check src/engine/` → **exit 0**.
- `python3 -m pytest tests/ -q` → **exit 0**, `2116 passed, 1 skipped`.
- `python3 dist/bootstrap.py check --strict` → **exit 0**, post-commit.

**Honest nulls.** The measured base rate behind this (seven owner corrections in
one session, all correct) is **fleet-manager's**, and it stays in that repo's
ledger rather than being planted as a kit claim — an adopter's owner is a
different person with a different record. The template asserts the *principle*;
each adopter's evidence is theirs to accumulate. And like every doctrine entry,
this one has **no mechanism** — nothing can gate "a session doubted its owner",
so it binds only by being read.

## ⟲ previous-session review

See above.

## 💡 Session idea

**A session-start line that states what the owner has already settled.** This
entry, the comprehension exception, and the router all share one weakness — they
bind only if read at the moment they apply, and the moment for this one is the
instant an instruction arrives. The durable version is not more doctrine but a
rendered line in the boot file naming the specific provisioning facts the owner
has stated for *this* environment, filled from the interview. Then a session
does not need to remember a principle; it opens knowing the answer.
