# 2026-07-13 — template pointer guard (dead-pointer class → enforcing test)

> **Status:** `complete`

⚑ Self-initiated: converted the verified CI coverage gap behind ORDER 015's
dead-boot-pointer fix into an ENFORCING kit test (Q-0194 friction → guard).

Did: re-verified at HEAD 3d58a46 that (1) `check_docs.check_links` validates
only markdown links while backtick refs feed only the reachability walk
(dead refs silently dropped by the `nxt.exists()` filter), (2) pointers
outside docs/ are checked by nothing, (3) no test asserted template pointers
are ADOPT_PLAN destinations. Shipped `tests/test_template_pointer_guard.py`
(4 tests): extracts every backtick + markdown-link path pointer from every
template (45 distinct today), resolves each via ADOPT_PLAN / kit-generated
artifacts / lane-heartbeat pattern / kit-self refs (existence asserted) /
attributed cross-repo refs / an explicit commented whitelist (2 entries),
and fails LOUD naming template + pointer + fix path. Mutation-tested (an
injected dead pointer reds with a useful message). Stale-entry hygiene tests
keep the accounting tables from rotting. Deliberately a kit test, NOT a
`check_docs` extension — adopter-facing check behavior unchanged.

Verify: pytest 1265 → 1269 passed; `dist/bootstrap.py check --strict` exit 0
(red only on this card's own designed born-red hold pre-flip). No src/engine
changes → no dist regen. guard-fires.jsonl telemetry delta committed (#331).

💡 Session idea: extend the pointer guard to the OTHER kit-emitted surfaces
that carry path pointers — the skill documents (`src/engine/skills/skills.py`
bodies) and the staged CLAUDE.md — since a dead pointer in an installed
SKILL.md misroutes a session exactly like a template one; the extractor +
resolution tables in `tests/test_template_pointer_guard.py` are reusable
as-is (dedup-checked `docs/ideas/`: no existing entry covers skill-body
pointer validation).

⟲ Previous-session review: #332 (ORDER 018 check-parity) cleanly converged
local `check --strict` with the CI gate's inbox + preflight legs, with the
documented one-carve-out subprocess boundary — good discipline. One gap it
surfaced (visible in this session's own check run): the kit repo itself
ships no `scripts/preflight.py`, so every local check emits the "preflight
script not found — skipped" NOTE and the kit's own local ritual still isn't
byte-converged with its CI; planting a minimal preflight for consumer #0
would finish the order's intent on the kit itself.

📊 Model: Claude 5 family
