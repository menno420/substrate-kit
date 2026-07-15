---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Template↔local-copy sync advisory — heading-set drift between planted templates and the kit's own rendered copies (2026-07-15)

> **Status:** `ideas`
>
> **State:** captured (groomed from the 2026-07-15 heartbeat-delegated-tally
> session card's 💡 — PR #395 — which observed the class live; PR #397 then
> paid for a second instance by hand the same day. Filed by the 2026-07-15
> groom slice so the idea stops living card-only.)

## The class

The kit plants adopter docs from `src/engine/templates/*.tmpl`
(`ADOPT_PLAN` in `src/engine/adopt.py` maps template → destination), and the
kit's own repo carries **rendered local copies of the same docs** (e.g.
`control/README.md`, `control/claims/README.md`). Template and local copy
are hand-synced: every doctrine edit must land **twice by hand**, and a miss
ships adopters a different contract than the kit itself runs — or leaves the
kit running an older contract than the one it distributes.

## Evidence — two live instances in one day (2026-07-15)

1. **Observed divergence** (the #395 session, card
   `.sessions/2026-07-15-heartbeat-delegated-tally.md` 💡): the kit's
   `control/README.md` carries an "Enforced vs. convention" block its
   template `control-README.md.tmpl` lacks, and per-lane wording differs.
2. **Paid instance** (PR #397, card
   `.sessions/2026-07-15-order-claim-collision-completion.md`): the kit's
   `control/claims/README.md` lagged the shipped
   `control-claims-README.md.tmpl` by a whole feature paragraph — the
   `--order NNN` verb line, the "Serving an inbox ORDER?" paragraph, and the
   `claims-order-collision` advisory row all existed template-side only
   (shipped to adopters in #365) while the kit's own copy taught the old
   contract for a full day. Fixed by hand in #397; a checker would have
   caught it mechanically at #365's own preflight.

## The fix (quick-win shape)

A cheap **advisory-only** leg in `check`'s full lane: for each
`ADOPT_PLAN` pair whose destination exists in the kit's own tree, compare
the `## ` section-heading **sets** between the template and the local copy;
report headings present in one but not the other
(`template-local-heading-drift: <file> — local-only: […] · template-only:
[…]`). Heading sets, not byte-diff, because local copies legitimately
diverge in prose (the local claims README carries repo-specific notes);
what must not silently diverge is **doctrine structure** — a whole section
existing on only one side is exactly the paid class. Placeholder-bearing
headings (`[[fill:…]]`) skip. Advisory, never exit-affecting: the kit repo
is the only tree where both sides exist, so this costs adopters nothing.

## Guard recipe

Anchors: `ADOPT_PLAN` (`src/engine/adopt.py`, template→destination pairs) is
the mapping source of truth — never a second hand-list; heading extraction
can share the section-scan style of the existing structure checkers
(`check_changelog_structure` precedent). Test: a fixture pair where the
template gains a `## New doctrine` section the local copy lacks must fire
the advisory; byte-identical prose differences under identical headings must
stay silent. Engine change → dist byte-pin regen.
