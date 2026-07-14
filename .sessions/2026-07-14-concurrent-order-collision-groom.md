# 2026-07-14 · concurrent-ORDER collision — close the duplicate, groom the root cause

> **Status:** `complete`

About to happen (opening declaration): this routine lab-loop fire picked up the
two open BUILD sub-items of ORDER 020 (d = A10 friction-outbox `check`
advisory; e = INC-29 dead-lowercase `docs/capabilities.md` → `docs/CAPABILITIES.md`
pointer casing) and built them fully on PR #363 — green, tested, dist
byte-stable. On push, a **concurrent** routine fire's PR **#362** (the SAME two
sub-items) had already merged to main as `e7c0a5e`. Source-wins: #362 is the
record; #363 is a true duplicate and was closed as superseded (no delta to
salvage — #362 shipped both sub-items with tests, and even added a positive
casing pin `test_capabilities_pointer_casing_is_uppercase`). The build slot was
consumed by the collision, so this session ships the genuinely different,
higher-value thing the collision exposed: a groomed backlog idea capturing the
**root-cause coordination gap** — the work-claim system's duplicate scan keys
on branch token, not on ORDER/work overlap, so two sessions on different
branches doing the same order never see each other.

- **📊 Model:** Opus 4.8 · high · idea/planning

Run type: routine · lab

## What shipped (this PR)

- `docs/ideas/order-claim-cross-branch-collision-2026-07-14.md` (new,
  frontmatter `state: captured` / `origin: lab` / ship-fields null /
  `outcome: open`): the concurrent-ORDER collision, evidenced with the live
  #362/#363 pair; a survey of why the existing machinery (`claim.py` /
  `check_claims` branch-keyed dedupe, `check_status_current` heartbeat gate)
  misses it; and a contained, advisory-first mechanism sketch (optional
  `· order NNN` claim-grammar segment + `bootstrap claim --order` writer + a
  cross-branch overlap advisory) with alternatives weighed (hard lease vs.
  coordinator assignment, both rejected as over-heavy / out-of-engine).
- `docs/ideas/README.md` — backlog index line for the new idea
  (`check_idea_index` requires every idea be linked).
- Team memory written on the collision gotcha for the kit-lab loop.

## Decide-and-flag

- **Closed #363 rather than forcing it.** #362 merged first and covers the
  identical scope with tests; reverting merged work to swap in this PR's
  module-vs-inline structure would be self-serving churn for zero functional
  gain (don't-re-litigate / source-wins). The honest record is one merged
  implementation, not two.
- **Groomed the root cause rather than rushing a fix.** The precise gap
  (branch-keyed dedupe misses cross-branch same-work) is buildable, but the
  fix touches the shared EAP §6.8 claim grammar and the lab-loop prompt — it
  deserves a focused session (or coordinator call between advisory vs. lease
  vs. assignment), not a same-session rush after a wasted build slot. Anti-
  stall's blessed fallback when the build slot is spent: groom one genuine,
  well-evidenced idea. This one has two PR numbers of live evidence.

## Verify

- `python3 dist/bootstrap.py check --strict` → green except the DESIGNED
  born-red HOLD naming this card (pre-flip).
- `python3 scripts/check_idea_index.py` → OK (new idea frontmatter valid +
  linked from README; filename ends `-2026-07-14.md` per the cohort-key rule).
- `python3 scripts/preflight.py` → 7 legs green (docs-only change; dist
  untouched — no engine edit this slice).

## 💡 Session idea

Build the cross-branch overlap advisory sketched in the groomed idea —
`bootstrap claim --order NNN` renders an optional ` · order NNN` segment
(from a shared `engine.grammar` constant), and `check_claims` gains an
advisory that fires when ≥2 live `control/claims/` files on different branches
name the same order. It is the direct, contained mechanism against the exact
collision that produced this card, and it slots into the existing
writer==enforcer claim machinery without touching coordinator-owned protocol.
(This is the next-step named in the idea file itself, promoted here so a
future fire finds it as a session ender, not only buried in the backlog.)

## ⟲ Previous-session review

The immediately-prior work is the collision's other half — the concurrent fire
that landed #362. It was a clean, well-tested implementation (inline advisory
+ casing fix + a positive casing pin), and it merged first, so it wins; no
criticism of the code. The reviewable failure is **systemic, and it caught
me too**: nothing surfaced that ORDER 020 was already being worked, so two
sessions paid the full build cost for one deliverable. Concrete workflow
improvement: exactly the groomed idea — claims keyed on the ORDER/work they
serve, with a cross-branch overlap advisory, so the second fire to reach for
an order sees the first's claim before building. The loop's self-improvement
value this session is not a shipped checker but the precise root-causing of a
coordination gap that will otherwise recur every time two fires overlap.

## Documentation audit

Idea file + README index line carry the full story with verifiable PR numbers;
#363 closed with a superseded comment linking #362; `current-state.md` ▶ Next
action updated with the collision + groom (DONE/REMAINS); team memory written;
no CHANGELOG entry (docs-only groom, no shipped capability); nothing chat-only
remains.
