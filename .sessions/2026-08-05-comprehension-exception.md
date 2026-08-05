# 2026-08-05 · The comprehension exception — when reading IS the job

> **Status:** `complete`

- **📊 Model:** opus-5 · high · template + skill

💡 Session idea: the kit's boot template tells every adopter *"That is the
whole boot set"* and argues that reading further *"buys ceremony, not
context — measured."* That default is right and the measurement is real. But
it has no exception for the session whose job **is** the reading, and on
2026-08-05 that missing exception cost a fleet-manager session the single
document its own repo introduces as *"read this if you read nothing else."*

## previous-session review

`2026-08-04-seed-skill-router.md` (#552 family) closed the loop between
planting skills and getting them loaded — routing in the one file every
session reads. This session finds the adjacent hole: the same file tells
sessions where to **stop** reading, with no way to say "not this time." A
router that loads the right skill still loses if the orientation it sits on
declared itself complete.

## Scope

Two changes at the source, both propagating to every adopter:

1. `src/engine/templates/CLAUDE.md.tmpl` — the boot set is a **floor for
   acting**, not a ceiling on reading; name the comprehension exception.
2. `src/engine/skills/skills.py` — promote `continuation-prompt` into the
   kit. It is the skill that writes every handoff prompt in the estate and
   it currently exists in **exactly one repo** (verified: 15 repos probed,
   only fleet-manager has it), so a fix to it propagates nowhere.

## What landed

- `src/engine/templates/CLAUDE.md.tmpl` — the boot set is now *"the whole boot
  set **for acting** — a floor, not a ceiling"*, plus a **comprehension
  exception**: the owner phrases that trigger it, an instruction to read the
  corpus rather than the list, a warning that this hand-maintained section can
  omit a document the repo elsewhere calls essential, and an acceptance test
  for orientation.
- `src/engine/skills/skills.py` — `continuation-prompt` promoted into the
  starter pack (15 skills), placed after `session-close` as its lifecycle
  sibling. Body carries the comprehension exception and the imperative-beats-
  aspiration trap.
- `tests/test_skills.py` — starter-pack order pin updated.
- `dist/bootstrap.py` — rebuilt.

## Measured

**The skill existed in exactly one repository.** Probed 15 repos over the
GitHub API for `.claude/skills/continuation-prompt/SKILL.md`: only
fleet-manager returned 200; substrate-kit itself returned 404. So the procedure
that writes every handoff prompt in the estate shipped to no adopter, and the
fix that came out of the incident had nowhere to propagate. That is the reason
this PR exists rather than a one-line edit in fleet-manager.

**The template governs real repos, verified not assumed:**
`superbot-next/.claude/CLAUDE.md` carries *"That is the whole boot set"*
verbatim from this template.

## Verification

- `python3 src/build_bootstrap.py` → **exit 0**.
- `python3 -m ruff check src/engine/` → **exit 0**.
- `python3 -m pytest tests/ -q` → **exit 0**, `2116 passed, 1 skipped`.
- `python3 dist/bootstrap.py check --strict` → **exit 0** post-flip (before the
  flip its only finding was this card's own designed born-red hold).
- Propagation proved two ways: a whitespace-normalized search confirms both
  changes are present in the built `dist/bootstrap.py`, and
  `tests/test_adopt.py` asserts every registered skill is planted
  (`len(glob("skills/*/SKILL.md")) == len(SKILLS)`) — green at 15.

**Honest nulls.** A synthetic end-to-end render into a blank repo was attempted
and abandoned: planting is gated on a staged interview, so a bare `init` plants
nothing. The adopt test covers the same property and is the stronger evidence,
but **no adopter has actually received this yet** — that needs a release and a
distribution wave, which this PR deliberately does not trigger. The skill body
is also **unverified in use**: it has not yet written a prompt, and its
fleet-manager predecessor looked correct too.

## ⟲ previous-session review

`2026-08-04-seed-skill-router.md` closed the loop between planting skills and
getting them loaded. Its blind spot is visible only from the other side: it
routed sessions *to* skills through the working agreement, while that same
agreement told sessions where to stop reading — and the router cannot help with
a skill the kit does not ship. Worth carrying: **when a fix lands in one repo,
check whether the mechanism it fixes is kit-shipped before calling it done.**
Fleet-manager has 27 local skills against the kit's 14; the other 13 are
estate-wide procedures living in exactly one place.

## 💡 Session idea

**Ship a `check_local_skill_drift` advisory.** This session found a skill that
had been estate-critical and repo-local for weeks, and only found it because an
owner asked a question that happened to require probing 15 repos. That should
not depend on luck.

The checker is cheap and stdlib-only: diff `.claude/skills/*/` against
`.substrate/skills/*/` in an adopter, and report skills that exist locally with
no kit counterpart. Most will be legitimately local (fleet-manager's image and
audio skills are estate-specific by design). But the output is the shortlist of
**candidates for promotion** — procedures that other repos would benefit from
and cannot currently get — and it turns "is this worth promoting?" from an
archaeology question into a one-command read. Same shape as the S3/S5/S9
advisory trio: never merge-blocking, disposable, and it makes an invisible
class of drift visible.
