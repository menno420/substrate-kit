"""The setup-script contract checker + template (EAP program review §6.5).

The fleet's per-repo ``scripts/env-setup.sh`` hook has one contract (from
the fleet-manager archetype material): always exit 0, defensive ``set +e``
posture, no secret values, guarded installs. These tests pin both halves of
the writer/enforcer pair:

- **writer**: ``env-setup.sh.tmpl`` renders slot-free (no markdown banner
  can ever be prepended to a shell file), plants at ``scripts/env-setup.sh``
  via adopt (skip-if-exists), and passes the checker with zero findings —
  the template can never drift from the grammar the enforcer checks;
- **enforcer**: ``check_setup_script`` flags ``setup-fatal-posture`` /
  ``setup-no-exit0`` / ``setup-secret-value``, is advisory-only (never
  exit-affecting under ``--strict``), input-gated on the script existing,
  and fail-open on unreadable files;
- **surfaces**: shell plants are excluded from the engagement gate's
  unrendered scan / ``render --live`` set (shell ``${VAR}`` is not an
  interview slot).
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_setup_script")

from engine.adopt import ADOPT_PLAN, adopt
from engine.checks.check_engagement import scan_relpaths
from engine.checks.check_setup_script import (
    SETUP_SCRIPT_RELPATH,
    check_setup_script,
)
from engine.cli import cmd_check
from engine.lib.config import Config, load_config
from engine.lib.state import JsonStateBackend, default_state
from engine.render import find_placeholders, load_templates, render


def _write_script(root: Path, text: str) -> Path:
    path = root / SETUP_SCRIPT_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _kinds(findings) -> list[str]:
    return [f.kind for f in findings]


GOOD = "#!/usr/bin/env bash\nset +e\necho hi\nexit 0\n"


# ── the writer: the template itself ─────────────────────────────────────────


def test_template_is_slot_free():
    """No ${slot} placeholders: a shell file must never earn the markdown
    UNRENDERED banner, and shell syntax must never read as a slot."""
    text = load_templates()["env-setup.sh.tmpl"]
    assert find_placeholders(text) == set()
    assert find_placeholders(render(text, {})) == set()


def test_template_passes_the_enforcer(tmp_path):
    """Writer/enforcer agreement: the planted template is contract-clean."""
    _write_script(tmp_path, load_templates()["env-setup.sh.tmpl"])
    assert check_setup_script(tmp_path) == []


def test_template_in_adopt_plan():
    assert ("env-setup.sh.tmpl", SETUP_SCRIPT_RELPATH) in ADOPT_PLAN


# ── the enforcer: findings ───────────────────────────────────────────────────


def test_missing_script_is_not_a_finding(tmp_path):
    assert check_setup_script(tmp_path) == []


def test_clean_script_no_findings(tmp_path):
    _write_script(tmp_path, GOOD)
    assert check_setup_script(tmp_path) == []


@pytest.mark.parametrize(
    "line",
    ["set -e", "set -eu", "set -euo pipefail", "set -o errexit", "set -x -e"],
)
def test_fatal_posture_flagged(tmp_path, line):
    _write_script(tmp_path, f"#!/usr/bin/env bash\n{line}\nexit 0\n")
    assert "setup-fatal-posture" in _kinds(check_setup_script(tmp_path))


@pytest.mark.parametrize("line", ["set +e", "set -x", "set -o pipefail"])
def test_non_fatal_set_lines_not_flagged(tmp_path, line):
    _write_script(tmp_path, f"#!/usr/bin/env bash\n{line}\nexit 0\n")
    assert "setup-fatal-posture" not in _kinds(check_setup_script(tmp_path))


def test_missing_exit0_flagged(tmp_path):
    _write_script(tmp_path, "#!/usr/bin/env bash\nset +e\necho done\n")
    assert "setup-no-exit0" in _kinds(check_setup_script(tmp_path))


def test_mid_file_exit0_does_not_satisfy_the_tail_rule(tmp_path):
    _write_script(tmp_path, "set +e\nexit 0\necho after\n")
    assert "setup-no-exit0" in _kinds(check_setup_script(tmp_path))


def test_trailing_comments_and_blanks_ignored_for_exit0(tmp_path):
    _write_script(tmp_path, "set +e\nexit 0\n# trailing comment\n\n")
    assert check_setup_script(tmp_path) == []


def test_secret_literal_flagged(tmp_path):
    _write_script(
        tmp_path,
        "set +e\nexport GITHUB_TOKEN=ghp_abc123def\nexit 0\n",
    )
    assert "setup-secret-value" in _kinds(check_setup_script(tmp_path))


@pytest.mark.parametrize(
    "line",
    [
        'GITHUB_TOKEN="$GITHUB_TOKEN"',  # a reference, not a value
        "API_KEY=<SET-IN-CLAUDE-AI>",  # the registry's placeholder form
        "MY_TOKEN=",  # empty
        "PY=python3",  # not secret-named
    ],
)
def test_non_secret_assignments_not_flagged(tmp_path, line):
    _write_script(tmp_path, f"set +e\n{line}\nexit 0\n")
    assert "setup-secret-value" not in _kinds(check_setup_script(tmp_path))


def test_empty_script_flags_exit0_only(tmp_path):
    _write_script(tmp_path, "")
    assert _kinds(check_setup_script(tmp_path)) == ["setup-no-exit0"]


def test_unreadable_script_fails_open(tmp_path):
    path = _write_script(tmp_path, GOOD)
    path.write_bytes(b"\xff\xfe\x00bad")
    assert check_setup_script(tmp_path) == []


# ── posture: advisory-only, never exit-affecting ─────────────────────────────


def test_findings_never_red_strict_check(tmp_path, capsys):
    """A contract-violating script warns but exits 0 under --strict —
    the §6.4-style compat guarantee (no adopter reds on upgrade)."""
    _write_script(
        tmp_path,
        "set -e\nexport MY_TOKEN=literalvalue\necho no exit zero\n",
    )
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "setup-script contract advisory" in out
    assert "setup-fatal-posture" in out
    assert "setup-no-exit0" in out
    assert "setup-secret-value" in out


def test_status_only_lane_skips_setup_advisories(tmp_path, capsys):
    """The hook is not control-lane traffic: --status-only stays silent."""
    _write_script(tmp_path, "set -e\necho nope\n")
    cmd_check(tmp_path, strict=True, status_only=True)
    assert "setup-script contract" not in capsys.readouterr().out


# ── surfaces: adopt plants it; engagement/render skip shell ──────────────────


def _adopt_backend(root: Path, config: Config):
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return backend


def test_adopt_plants_the_hook_and_readopt_keeps_it(tmp_path):
    root = tmp_path / "repo"
    config = Config()
    backend = _adopt_backend(root, config)
    report = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert f"planted: {SETUP_SCRIPT_RELPATH}" in report
    planted = (root / SETUP_SCRIPT_RELPATH).read_text(encoding="utf-8")
    # Slot-free plant: never bannered, and contract-clean on arrival.
    assert not planted.startswith(">")
    assert check_setup_script(root) == []
    # Skip-if-exists: a host-edited hook is never clobbered.
    (root / SETUP_SCRIPT_RELPATH).write_text(GOOD, encoding="utf-8")
    report2 = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert f"kept: {SETUP_SCRIPT_RELPATH}" in report2
    assert (root / SETUP_SCRIPT_RELPATH).read_text(encoding="utf-8") == GOOD


def test_shell_plants_excluded_from_unrendered_scan(tmp_path):
    """A hand-rolled hook full of shell ${VAR} syntax must never count as
    unfilled interview slots (nor be rewritten by render --live)."""
    config = load_config(tmp_path)
    relpaths = scan_relpaths(config)
    assert SETUP_SCRIPT_RELPATH not in relpaths
    assert all(not rel.endswith(".sh") for rel in relpaths)
