"""The three v1.21.0 substrate-gate hardenings, upstreamed from fm #833.

Fleet-manager carried all three as hand-edits to the kit-owned generated
workflow, re-applied after every upgrade because the regen dropped them (the
re-apply tax recorded in its ``docs/SKILLS-local.md``). These tests pin the
upstreamed versions so a future template edit cannot silently drop one again:

1. the claims-only fast-lane guard reads PR-author-controlled context
   (``github.head_ref``) via an ``env:`` block, never direct ``${{ }}``
   interpolation into the shell program (Codex P1 — a branch name can carry
   shell metacharacters and ``exit 0`` past the guard);
2. a planted ``repo checkers`` extension step runs the host-owned
   ``scripts/repo_checks.sh`` when present and self-skips otherwise, so host
   checkers survive every regen;
3. a single un-chained ``bootstrap.py check`` verify_command gains the
   explicit absent-card ``--session-log`` sentinel (Codex P2 — CI checkout
   flattens mtimes, and the newest-by-mtime fallback once redded a valid
   main push off a historical in-progress card).
"""

from __future__ import annotations

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import live_ci_workflow
from engine.guards import ADOPTER_CLAIMS_FASTLANE_GUARD, ADOPTER_REPO_CHECKERS


def _step_block(workflow: str, step_name: str) -> str:
    """The text of one named step, up to the next `- name:`/`- uses:` entry."""
    start = workflow.index(f"- name: {step_name}")
    rest = workflow[start + 1 :]
    for marker in ("\n      - name: ", "\n      - uses: "):
        idx = rest.find(marker)
        if idx != -1:
            rest = rest[:idx]
    return workflow[start : start + 1] + rest


class TestClaimsGuardEnvIndirection:
    def test_guard_reads_context_via_env_block(self) -> None:
        block = _step_block(live_ci_workflow(), ADOPTER_CLAIMS_FASTLANE_GUARD)
        assert "env:" in block
        for var in ("HEAD_REF", "BASE_REF", "EVENT_BEFORE", "EVENT_SHA"):
            assert f"{var}: ${{{{ github." in block, f"{var} must come from env"
        run = block[block.index("run: |") :]
        assert "${{" not in run, (
            "no ${{ }} may be interpolated into the guard's shell program — "
            "GitHub expands it before bash parses, so quoting cannot help"
        )
        assert 'head_ref="$HEAD_REF"' in run

    def test_case_dispatch_still_reads_head_ref_variable(self) -> None:
        # check_fastlane_symmetry parses `case "$head_ref" in` — the env
        # indirection must not rename the shell variable it inspects.
        block = _step_block(live_ci_workflow(), ADOPTER_CLAIMS_FASTLANE_GUARD)
        assert 'case "$head_ref" in' in block


class TestRepoCheckersExtensionPoint:
    def test_step_is_planted_and_self_skips(self) -> None:
        wf = live_ci_workflow()
        block = _step_block(wf, ADOPTER_REPO_CHECKERS)
        assert "if [ -f scripts/repo_checks.sh ]; then" in block
        assert "bash scripts/repo_checks.sh" in block
        assert "self-heals when it arrives" in block
        assert "if: steps.lane.outputs.control_only != 'true'" in block

    def test_step_precedes_the_session_gate(self) -> None:
        # Host checkers red fast, before the heavy session-gate work.
        wf = live_ci_workflow()
        assert wf.index(ADOPTER_REPO_CHECKERS) < wf.index(
            "substrate gate (docs + session-log required)"
        )


class TestVerifyCommandSentinel:
    def test_single_bootstrap_check_gains_the_absent_card_sentinel(self) -> None:
        wf = live_ci_workflow(test_command="python3 bootstrap.py check --strict")
        assert (
            "python3 bootstrap.py check --strict "
            "--session-log .sessions/__no-card-in-diff__.md\n" in wf
        )

    def test_sentinel_honors_the_configured_sessions_dir(self) -> None:
        wf = live_ci_workflow(
            sessions_dir=".journal",
            test_command="python3 bootstrap.py check --strict",
        )
        assert "--session-log .journal/__no-card-in-diff__.md" in wf

    def test_chained_commands_stay_verbatim(self) -> None:
        cmd = "python3 bootstrap.py check --strict && echo done"
        wf = live_ci_workflow(test_command=cmd)
        assert f"          {cmd}\n" in wf
        assert cmd + " --session-log" not in wf

    def test_command_with_its_own_session_log_stays_verbatim(self) -> None:
        cmd = "python3 bootstrap.py check --strict --session-log .sessions/x.md"
        wf = live_ci_workflow(test_command=cmd)
        assert wf.count("--session-log") >= 1
        assert f"          {cmd}\n" in wf

    def test_non_check_commands_stay_verbatim(self) -> None:
        cmd = "python3 -m mytests --all"
        wf = live_ci_workflow(test_command=cmd)
        assert f"          {cmd}\n" in wf
        assert "__no-card-in-diff__" not in _step_block(
            wf, "verify suite (the interview's verify_command drives the gate's test step)"
        )

    def test_default_pytest_fallback_carries_no_sentinel(self) -> None:
        wf = live_ci_workflow()
        assert "verify suite" not in wf  # fallback pytest step, not verify
        assert "-m pytest tests/ -q" in wf
