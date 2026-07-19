"""Tests for the no-false-walls ENGINE leg — the propagated `check --strict`
guard that reds EVERY adopter (not just substrate-kit) when a session
documents a FALSE agent-capability limitation into its own forward docs.

The grammar/blocklist/clearing logic lives once in
``engine.checks.check_no_false_walls`` (the standalone ``tools/`` wrapper
delegates to it — no duplicate logic). These tests cover the engine surfaces an
ADOPTER has (live ``docs/``, root ``CONSTITUTION.md`` / ``CAPABILITIES.md``,
live ``.claude/**``) and the exit-affecting wiring through ``cmd_check``. The
#449 must-fail / must-pass fixtures are re-exercised here on the adopter surface
so the shared core stays honest.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.checks.check_no_false_walls import (
    _UNKNOWN_RULE_CORRECTION,
    WALL_CORRECTIONS,
    check_no_false_walls,
    scan_text,
)
from engine.cli import cmd_check
from engine.lib.config import Config, save_config

# The #449 spread — each is a standing FALSE capability wall (owner directive
# 2026-07-18): subject-negated, owner-only, or platform-walled.
_MUST_FAIL = (
    "agents do NOT arm auto-merge — classifier-denied since 2026-07-15\n",
    "The owner is the merge authority for every session PR.\n",
    "A green PR is agent-unlandable; route it to the owner.\n",
    "Sessions may not self-merge their own PRs.\n",
    "agents cannot delete branches\n",
    "sessions are not allowed to update Railway variables\n",
    "branch deletion is owner-only\n",
    "deploying is classifier-denied for agent seats\n",
    "the owner must merge PRs\n",
    "merging is owner-gated\n",
    "the bot cannot push to protected branches\n",
)

# The phrasing we WANT adopters to keep — corrected doctrine, CODE rules,
# genuine dated walls, missing-input requests.
_MUST_PASS = (
    "merging is normal agent work; never route a mergeable green PR to the owner\n",
    "there are NO owner-imposed limitations\n",
    "services must not import views\n",
    "utils/ may not import services\n",
    "never call pool.execute directly outside utils/db\n",
    "needs a Stripe account from the owner\n",
    "session tokens cannot create repos (gen-1 wall)\n",
    "this repo's sessions cannot read fleet-manager directly\n",
)


def _plant(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


# ── The shared core stays honest on the #449 fixtures ─────────────────────────


class TestSharedCoreParity:
    def test_must_fail_lines_are_caught(self) -> None:
        for text in _MUST_FAIL:
            assert scan_text(text), f"shared core should catch: {text!r}"

    def test_must_pass_lines_are_cleared(self) -> None:
        for text in _MUST_PASS:
            assert scan_text(text) == [], f"shared core tripped on: {text!r}"


# ── The engine leg on each adopter surface ────────────────────────────────────


class TestAdopterSurfaces:
    def test_flags_false_wall_in_live_docs(self, tmp_path: Path) -> None:
        _plant(tmp_path, "docs/current-state.md", _MUST_FAIL[0])
        findings = check_no_false_walls(tmp_path, Config())
        assert len(findings) == 1
        assert findings[0].kind.startswith("false-wall:")
        assert findings[0].path == "docs/current-state.md"

    def test_flags_false_wall_in_root_constitution(self, tmp_path: Path) -> None:
        _plant(tmp_path, "CONSTITUTION.md", _MUST_FAIL[1])
        findings = check_no_false_walls(tmp_path, Config())
        assert [f.path for f in findings] == ["CONSTITUTION.md"]

    def test_flags_false_wall_in_live_claude_skill_body(self, tmp_path: Path) -> None:
        # An adopter's live .claude skill/rule body is a forward-binding surface.
        _plant(tmp_path, ".claude/skills/merge/SKILL.md", _MUST_FAIL[3])
        findings = check_no_false_walls(tmp_path, Config())
        assert [f.path for f in findings] == [".claude/skills/merge/SKILL.md"]

    def test_every_must_fail_variant_reds(self, tmp_path: Path) -> None:
        for text in _MUST_FAIL:
            _plant(tmp_path, "docs/d.md", text)
            assert check_no_false_walls(tmp_path, Config()), f"missed: {text!r}"

    def test_every_must_pass_variant_is_silent(self, tmp_path: Path) -> None:
        for text in _MUST_PASS:
            _plant(tmp_path, "docs/d.md", text)
            assert check_no_false_walls(tmp_path, Config()) == [], f"tripped: {text!r}"


# ── Exclusions carried over from #449 ─────────────────────────────────────────


class TestExclusions:
    def test_historical_dir_is_skipped(self, tmp_path: Path) -> None:
        _plant(tmp_path, "docs/retro/old.md", _MUST_FAIL[0])
        assert check_no_false_walls(tmp_path, Config()) == []

    def test_dated_filename_is_skipped(self, tmp_path: Path) -> None:
        _plant(tmp_path, "docs/2026-07-12-report.md", _MUST_FAIL[0])
        assert check_no_false_walls(tmp_path, Config()) == []

    def test_dated_ledger_bullet_is_cleared(self, tmp_path: Path) -> None:
        _plant(
            tmp_path,
            "docs/CAPABILITIES.md",
            "- 2026-07-16 · wall · An agent session cannot merge a SIBLING PR "
            "— the classifier denies it.\n",
        )
        assert check_no_false_walls(tmp_path, Config()) == []

    def test_false_quote_repudiation_is_cleared(self, tmp_path: Path) -> None:
        _plant(
            tmp_path,
            "docs/d.md",
            '> FALSE "agents do NOT ready-flip / arm — classifier-denied"\n',
        )
        assert check_no_false_walls(tmp_path, Config()) == []


# ── Self-quiet + honors a non-default docs_root ───────────────────────────────


class TestSelfGating:
    def test_bare_tree_is_silent(self, tmp_path: Path) -> None:
        assert check_no_false_walls(tmp_path, Config()) == []

    def test_honors_configured_docs_root(self, tmp_path: Path) -> None:
        cfg = Config(docs_root="documentation")
        _plant(tmp_path, "documentation/d.md", _MUST_FAIL[0])
        assert check_no_false_walls(tmp_path, cfg), "non-default docs_root missed"

    def test_skips_state_and_sessions_dirs(self, tmp_path: Path) -> None:
        # A false wall inside a dated session card / staged kit material is
        # history, not forward doctrine — never scanned.
        _plant(tmp_path, ".sessions/2026-07-18-x.md", _MUST_FAIL[0])
        _plant(tmp_path, ".substrate/claude/CLAUDE.md", _MUST_FAIL[0])
        assert check_no_false_walls(tmp_path, Config()) == []


# ── S6: the finding message inlines the rule's per-rule ground-truth correction ─


class TestFindingCarriesCorrection:
    def test_message_inlines_the_rule_specific_correction(self, tmp_path: Path) -> None:
        # Every must-fail line's finding message names its rule AND carries the
        # rule's WALL_CORRECTIONS sentence (or the unknown-rule fallback) inline —
        # not just the generic blurb — so the red gate states the specific truth.
        for text in _MUST_FAIL:
            _plant(tmp_path, "docs/d.md", text)
            findings = check_no_false_walls(tmp_path, Config())
            assert findings, f"expected a finding for: {text!r}"
            for f in findings:
                rule = f.kind.split("false-wall:", 1)[1]
                expected = WALL_CORRECTIONS.get(rule, _UNKNOWN_RULE_CORRECTION)
                assert expected in f.message, (
                    f"finding for rule {rule!r} must inline its correction; "
                    f"got: {f.message!r}"
                )
                # The rule name is still surfaced in the message for the reader.
                assert f"[{rule}]" in f.message
        # Belt-and-braces: no must-fail carries a stale generic-only message.
        assert "agents have no owner-imposed" not in "".join(
            f.message for f in check_no_false_walls(tmp_path, Config())
        )

    def test_every_rule_has_a_correction_so_no_fallback_ships(self) -> None:
        # The fallback is a safety net; every real blocklist rule should carry a
        # dedicated correction (mirrors tests/test_explain_wall.py coverage).
        from engine.checks.check_no_false_walls import all_rule_names

        missing = sorted(all_rule_names() - WALL_CORRECTIONS.keys())
        assert not missing, f"rules missing a WALL_CORRECTIONS entry: {missing}"


# ── Exit-affecting wiring through cmd_check (the propagation goal) ─────────────


class TestCmdCheckWiring:
    def test_strict_reds_and_names_the_leg(self, tmp_path: Path, capsys) -> None:
        save_config(tmp_path, Config())
        _plant(tmp_path, "docs/current-state.md", _MUST_FAIL[4])
        rc = cmd_check(tmp_path, strict=True)
        out = capsys.readouterr().out
        assert rc == 1
        assert "[false-wall:" in out
        # It rides the HARD finding block, not an advisory "never exit-affecting"
        # warning — the whole point of the propagation is a red gate.
        for line in out.splitlines():
            if "false-wall" in line:
                assert "never exit-affecting" not in line

    def test_clean_docs_leave_the_leg_silent(self, tmp_path: Path, capsys) -> None:
        save_config(tmp_path, Config())
        _plant(tmp_path, "docs/current-state.md", _MUST_PASS[0])
        cmd_check(tmp_path, strict=True)
        out = capsys.readouterr().out
        assert "false-wall" not in out
