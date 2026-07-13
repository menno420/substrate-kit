"""Auto-merge-enabler branch-allowlist preflight (enabler-install-preflight,
2026-07-13 night-run finding).

The offline-verifiable half of the install preflight: a self-silencing
advisory that flags when the installed ``auto-merge-enabler.yml``'s branch
allowlist drifts from ``automerge.branch_patterns``. These tests pin the
writer/enforcer agreement (the kit's own generated enabler passes the
enforcer with zero findings), the drift detection (a stale allowlist reds an
advisory), and the posture (advisory-only, never exit-affecting; input-gated;
version-skew-robust because it compares the branch expr, not the whole file).
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_automerge_preflight")

from engine.adopt import (
    AUTOMERGE_ENABLER_RELPATH,
    DEFAULT_AUTOMERGE_BRANCH_PATTERNS,
    automerge_enabler_workflow,
)
from engine.checks.check_automerge_preflight import (
    _branch_terms,
    check_automerge_preflight,
)
from engine.cli import cmd_check
from engine.lib.config import Config


def _write_enabler(root: Path, text: str) -> Path:
    path = root / AUTOMERGE_ENABLER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _kinds(findings) -> list[str]:
    return [f.kind for f in findings]


# ── the enforcer accepts the writer's own output ─────────────────────────────


def test_generated_enabler_passes_clean(tmp_path):
    """The kit's own generated enabler (default patterns) is silent against a
    default config — the writer can never drift from the enforcer."""
    _write_enabler(tmp_path, automerge_enabler_workflow())
    assert check_automerge_preflight(tmp_path, Config()) == []


def test_generated_enabler_matches_custom_config(tmp_path):
    """A custom branch-pattern config regenerates a matching enabler → silent.

    The comparison canonicalizes both sides through the same generator, so
    order and duplication carry no meaning."""
    patterns = ["feature/*", "hotfix"]
    _write_enabler(tmp_path, automerge_enabler_workflow(patterns))
    config = Config(automerge={"branch_patterns": patterns})
    assert check_automerge_preflight(tmp_path, config) == []


# ── the enforcer flags drift ─────────────────────────────────────────────────


def test_stale_allowlist_missing_claim_reds(tmp_path):
    """A pre-`claim/*` enabler (arms only claude/) drifts from the default
    config that covers claude/* AND claim/* — the kit PR #293 stall class."""
    _write_enabler(tmp_path, automerge_enabler_workflow(["claude/*"]))
    findings = check_automerge_preflight(tmp_path, Config())
    assert _kinds(findings) == ["automerge-branch-drift"]
    msg = findings[0].message
    assert "claim/*" in msg  # names the expected (config) allowlist
    assert "automerge.branch_patterns" in msg  # points the fix at config


def test_hand_edited_branch_reds_against_config(tmp_path):
    """A workflow hand-armed on a branch config would not regenerate → drift
    (the idea-engine hand-patch-clobber class)."""
    _write_enabler(tmp_path, automerge_enabler_workflow(["claude/*", "claim/*"]))
    config = Config(automerge={"branch_patterns": ["feature/*"]})
    findings = check_automerge_preflight(tmp_path, config)
    assert _kinds(findings) == ["automerge-branch-drift"]


# ── input-gating + fail-open ─────────────────────────────────────────────────


def test_no_enabler_no_findings(tmp_path):
    """A repo without the planted enabler adds nothing (absence is not a nag)."""
    assert check_automerge_preflight(tmp_path, Config()) == []


def test_no_head_ref_terms_stays_silent(tmp_path):
    """A workflow whose arming condition mentions no head_ref term is off the
    kit's generated shape — the checker declines to guess."""
    _write_enabler(
        tmp_path,
        "name: auto-merge-enabler\n"
        "on:\n  pull_request:\n"
        "jobs:\n  enable-auto-merge:\n"
        "    if: github.event.pull_request.draft == false\n"
        "    runs-on: ubuntu-latest\n",
    )
    assert check_automerge_preflight(tmp_path, Config()) == []


# ── posture: advisory-only, never exit-affecting ─────────────────────────────


def test_drift_never_reds_strict_check(tmp_path, capsys):
    """A drifted enabler warns but exits 0 under --strict — a required-check
    red here would be a fleet bomb during version skew."""
    _write_enabler(tmp_path, automerge_enabler_workflow(["claude/*"]))
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "auto-merge-enabler advisory" in out
    assert "automerge-branch-drift" in out


def test_status_only_lane_skips_the_advisory(tmp_path, capsys):
    """Workflows are not control-lane traffic: --status-only stays silent."""
    _write_enabler(tmp_path, automerge_enabler_workflow(["claude/*"]))
    cmd_check(tmp_path, strict=True, status_only=True)
    assert "auto-merge-enabler advisory" not in capsys.readouterr().out


# ── the term parser ──────────────────────────────────────────────────────────


def test_branch_terms_parse_both_shapes():
    """A trailing-`*` config pattern → a prefix term; anything else → exact."""
    expr = (
        "startsWith(github.head_ref, 'claude/') || "
        "github.head_ref == 'release'"
    )
    assert _branch_terms(expr) == {("prefix", "claude/"), ("exact", "release")}


def test_branch_terms_ignore_non_head_ref_guards():
    """The repo/draft/label guards carry no head_ref term and are ignored."""
    guards = (
        "github.event.pull_request.head.repo.full_name == github.repository && "
        "github.event.pull_request.draft == false && "
        "!contains(github.event.pull_request.labels.*.name, 'do-not-automerge')"
    )
    assert _branch_terms(guards) == set()


def test_default_patterns_round_trip():
    """The default patterns and their generated workflow share a term set —
    the property the self-silence relies on."""
    from engine.adopt import _automerge_branch_expr

    expr = _automerge_branch_expr(list(DEFAULT_AUTOMERGE_BRANCH_PATTERNS))
    live = _branch_terms(automerge_enabler_workflow())
    assert _branch_terms(expr) == live
