---
state: promoted
origin: lab
shipped_pr: 405
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-15
outcome: shipped
---

# Gate test step honors the interview's `verify_command` slot (2026-07-15)

> **Status:** `ideas`
>
> **State:** promoted → **shipped** kit PR #405 (2026-07-15, anticipated
> in-PR date; captured with the increment per the baton note — the 💡 was
> recorded on the #403 session card and built the next wake before its
> idea file existed): `engine.adopt.gate_test_command` reads the
> `verify_command` slot from the state document; a **filled + gate-safe +
> non-default** value drives the generated gate's test step verbatim,
> anything else keeps #403's hardened pytest fallback byte-identical.
> Writer/scanner symmetry: `upgrade.scan_gate_carveouts` computes the same
> verdict from `state.json` (read-only, fail-open) so kit-owned
> verify-step bytes never rescan as a phantom host carve-out.
> **Origin:** the #403 session (adopt-pytest-gate-step) — its planted step
> hardcoded `-m pytest tests/ -q` while the adopt interview already
> records `verify_command` (src/engine/interview/question_bank.py:86,
> routed to templates/CLAUDE.md).

**One line:** the substrate-gate's test step should run the verify command the
interview recorded — the same line the planted CLAUDE.md teaches every session —
instead of a hardcoded pytest invocation, so the CI runner and the doctrine can
never diverge (websites' real verify line is a four-suite pytest invocation plus
the kit gate; non-pytest adopters exist in principle).

**Shape:** one slot read at gate-render time (`gate_test_command`, threaded into
`live_ci_workflow(test_command=...)`), guarded three ways: **filled** only
(provisional/derived answers never drive a workflow every PR executes — the
interview contract), **gate-safe** only (single line, conservative shell-safe
character allowlist, no unfilled `${...}` — the slot is free prose routed into
markdown, and embedding prose reds every PR with a syntax error, not a test
failure), **non-default** only (a plain pytest invocation keeps the fallback
step, which is strictly more robust: `tests/`-absent self-skip + dependency
installs). Engine change → dist byte-pin.

**Size:** small (helper + template branch + rescan symmetry + tests).
