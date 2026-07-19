# S6 — inline WALL_CORRECTIONS into check_no_false_walls Finding

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S6 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md) — wire each blocklist rule's per-rule `WALL_CORRECTIONS` ground-truth sentence into the emitted `check_no_false_walls` engine `Finding`, so an adopter's red gate names the specific capability correction inline instead of the generic blurb. Provenance: fm ORDER 048 standing grant + coordinator dispatch (S5 shipped #520; baton advanced to S6).

## What I'm about to do
Change the engine `check_no_false_walls` Finding message to embed `WALL_CORRECTIONS.get(hit.rule, _UNKNOWN_RULE_CORRECTION)` — behavior-preserving on detection (same `false-wall:<rule>` kind, same paths, same exit-affecting-under-strict semantics; only the human-readable message text gains the rule-specific correction). Required-check parity preserved. Add a leg test asserting each finding's message carries its rule's correction. Rebuild dist (module ships in `dist/bootstrap.py`) + byte-pin.

- **📊 Model:** opus-4.8 · medium · feature build
- **⚑ Self-initiated:** [[fill: on flip]]
- **💡 Session idea:** [[fill: on flip]]
- **⟲ Previous-session review:** [[fill: on flip]]
