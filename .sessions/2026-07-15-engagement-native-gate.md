# 2026-07-15 — Engagement gate: declared `native_gate` evidence class (enforcement-native)

> **Status:** `complete`

Intent: ship the baton-named engagement native-consumer quick-win
(docs/ideas/engagement-native-consumer-state-2026-07-12.md) — a declared
`native_gate` field in `substrate.config.json` that the engagement gate
accepts as the CI door when its named workflow exists, so pin-only repos
with real native enforcement (the superbot shape, friction #37) stop
redding `enforcement-unwired`; acceptance surfaces as a visible
`enforcement-native` NOTE, never silently.

## What shipped (PR #401)

- `src/engine/lib/config.py`: opt-in `native_gate` Config field
  (`workflow` repo-relative path + informational `required_context`;
  empty default = undeclared, gate unchanged).
- `src/engine/checks/check_engagement.py`: `_native_gate_declared`
  (malformed shapes read as undeclared — misconfiguration never widens
  the gate) + public `native_gate_note` (fires exactly when the
  declaration is the accepting evidence); the `enforcement-unwired`
  branch accepts a declaration whose workflow exists, and names a dead
  declaration's path in the finding message (PL-011's letter: the door
  must exist in-tree).
- `src/engine/cli.py`: full-lane `check` emits the `enforcement-native`
  NOTE — accepted, never silent.
- `tests/test_check_engagement.py`: the idea's guard recipe — 4 new
  tests (engaged-native fixture, undeclared sibling stays red,
  dead-declaration stays red with path named, moot-when-kit-wired +
  malformed shapes, cmd_check NOTE emission). Suite: 1624 passed,
  1 skipped.
- Dist byte-pin regenerated; CHANGELOG `[Unreleased]` ### Added; idea
  frontmatter → `outcome: shipped` (PR #401) + ideas README entry moved
  to "Shipped (survive window open)".

Baton provenance: named by the heartbeat's next-2 line 1 (not
self-initiated). Verify: `python3 scripts/preflight.py` → 8/8 legs green
at 43028da.

## Session enders

- 💡 **Session idea:** teach the adopter registry (`currency` scan) a
  gate-shape column — kit-gated (`check --strict` workflow) vs
  native-gated (`native_gate` declaration) vs unwired — so the fleet
  roster shows HOW each adopter's door is held, not just that it is;
  one line of why: #401 just created the second legitimate door shape,
  and without registry visibility a native-gated adopter is
  indistinguishable from an unwired one at fleet level.
- **📊 Model:** fable-5 · high · engine feature slice (checker + config)
- ⟲ **Previous-session review:** the #400 wake judged sync direction
  per pair instead of blanket template-wins — the right call, and it
  caught its own keep-a-changelog ordering red locally before pushing.
  Miss: its card's `📊 Model:` line fused two fields ("effort: medium"),
  so the telemetry harvest recorded nothing — this wake's check run
  surfaced the model-line-shape advisory on it. Concrete improvement:
  the card-flip step should re-read the check output's advisory block
  before flipping (the advisory already exists; the flip ritual just
  needs to consume it) — fixing the #400 line itself is a one-line tidy
  for the next docs pass.
