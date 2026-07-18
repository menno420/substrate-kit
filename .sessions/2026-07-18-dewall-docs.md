# 2026-07-18 · de-wall the false "agents cannot merge" doctrine

> **Status:** `complete`

Run type: worker session (owner-directed cleanup).

- **📊 Model:** opus-4.8 · medium · docs-only

About to happen (opening declaration): remove the FALSE "the classifier denies
arming auto-merge / ready-flipping / REST-merging; agents do NOT merge their
own or a sibling's PR; landing is server-side, not agent-driven" doctrine from
the kit's own **rendered** operational docs, replacing it with the accurate
rule (automode is OFF, agents merge their own green PRs directly, proven).
Templates are out of scope.

## What shipped (PR #446)

- `docs/CAPABILITIES.md` — replaced the "self-merge classifier" wall row and
  the two dated append-log entries (2026-07-10) that asserted a self-merge
  wall; marked them SUPERSEDED, preserving the historical observations without
  the false wall framing.
- `docs/current-state.md` — rewrote the "Classifier freeze ~2026-07-15" bullet
  and the "Review rhythm" section ("Agents do NOT ready-flip, arm auto-merge,
  or REST/MCP-merge...") to the accurate agent-lands-own-green-PR doctrine.
- `docs/NEXT-TASKS.md` — fixed the "coordinator-relayed wave was
  classifier-denied" attribution, the "agents do NOT arm/merge" upgrade step,
  and §2's description of the merge doctrine.

Not touched (per scope): `src/engine/templates/*.tmpl`, existing `.sessions/*`
cards, `CHANGELOG`, `docs/retro/*`, `docs/planning/*veto*`.

## Decide-and-flag

- ⚑ **Template still carries the false wording.**
  `src/engine/templates/CONSTITUTION.md.tmpl` on `main` still contains "agents
  do NOT ready-flip / arm auto-merge / REST-merge... classifier-denied since
  2026-07-15" (lines ~78-83), contrary to the premise it was already corrected;
  `docs/gen2/next-boot.md`'s relayed-consent merge note is the same class. Both
  left untouched here (templates out of scope) and flagged for a dedicated
  `.tmpl` fix PR.

## Verify

- `python3 -m pytest` → `1726 passed, 1 skipped` (docs-only change; no test
  asserted any removed phrase).

## Enders

💡 **Session idea:** add a `check`-level content guard that reds any
forward-binding doc (not `.sessions/`, `docs/retro/`, `docs/planning/`)
asserting an "agents do NOT / cannot merge / arm auto-merge / ready-flip"
phrase, so a false-wall regression is caught mechanically at the source of
truth (the template) rather than after it has rendered into every adopter —
enforce-don't-exhort applied to the merge doctrine itself.

⟲ **Previous-session review** (2026-07-14, model-line payload lint, PR #352):
a clean model build — the lint shipped with a real mutation-arc test suite and
grammar-identity pins, and it even flagged its own predecessor's drifted Model
line, the self-auditing loop working as designed. What it (and the whole
2026-07-15→17 arc) missed is exactly this session's subject: the "classifier
walls the agent-landing path" doctrine was written into the forward docs AND
the template as settled fact on a single run of observations, then propagated
fleet-wide — a false wall is more expensive than a missing feature. Concrete
system improvement: the content-guard filed as this session's 💡 would have
caught it at the template.

**Documentation audit:** the merge doctrine is now consistent across the three
rendered docs; the template gap is flagged above and in the PR body; nothing
chat-only remains.
