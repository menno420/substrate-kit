"""Tests for check_skill_grounds — the slice-2 command-grounding advisory.

Pins the slice's accept criterion ("each body names only commands that
exist" — the kit skill set is fully grounded), the detection classes (fake
command, missing path, rendered-doc scan), the fail-open skip ladder, and
the advisory posture: findings NEVER touch the exit code (§8 Q2=B).
"""

from pathlib import Path

from engine.checks.check_skill_grounds import check_skill_grounds
from engine.cli import cmd_check

KIT_ROOT = Path(__file__).resolve().parents[1]


def _fake_skill(body: str = "", grounds: list[str] | None = None) -> dict:
    return {
        "name": "fake",
        "description": "fake",
        "capabilities": [],
        "body": body,
        "grounds": grounds or [],
    }


def _kinds(findings):
    return [f.kind for f in findings]


# ---------------------------------------------------------------------------
# The accept criterion — the kit's shipped skill set is fully grounded
# ---------------------------------------------------------------------------


def test_kit_skill_set_fully_grounded_at_kit_root():
    # Every backticked span + grounds entry in the shipped SKILLS resolves
    # against the kit repo itself — slice 2's accept criterion as a test.
    assert check_skill_grounds(KIT_ROOT) == []


def test_kit_skill_set_grounded_even_on_empty_target(tmp_path):
    # The kit-shipped path set + executable whitelist carry the shipped
    # bodies on ANY target — an adopter with no kit files yet gets no nag
    # from the kit's own skills.
    assert check_skill_grounds(tmp_path) == []


# ---------------------------------------------------------------------------
# Detection classes
# ---------------------------------------------------------------------------


def test_fake_command_in_body_detected(tmp_path):
    findings = check_skill_grounds(
        tmp_path,
        skills=[_fake_skill(body="Run `frobnicate --explode` to finish.")],
    )
    assert _kinds(findings) == ["skill-ground-unresolved"]
    assert "frobnicate --explode" in findings[0].message
    assert findings[0].path == "skills/fake/SKILL.md"


def test_fake_ground_entry_detected(tmp_path):
    findings = check_skill_grounds(
        tmp_path,
        skills=[_fake_skill(grounds=["frobnicate --explode"])],
    )
    assert _kinds(findings) == ["skill-ground-unresolved"]
    assert "grounds entry" in findings[0].message


def test_missing_path_detected_and_existing_path_resolves(tmp_path):
    skill = _fake_skill(body="Run `scripts/missing.py now` first.")
    assert _kinds(check_skill_grounds(tmp_path, skills=[skill])) == [
        "skill-ground-unresolved"
    ]
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "missing.py").write_text("", encoding="utf-8")
    assert check_skill_grounds(tmp_path, skills=[skill]) == []


def test_rendered_skill_docs_are_scanned(tmp_path):
    doc = tmp_path / ".claude" / "skills" / "custom" / "SKILL.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("# custom\n\nRun `frobnicate --explode`.\n", encoding="utf-8")
    findings = check_skill_grounds(tmp_path, skills=[])
    assert _kinds(findings) == ["skill-ground-unresolved"]
    assert findings[0].path == ".claude/skills/custom/SKILL.md"


# ---------------------------------------------------------------------------
# The fail-open skip ladder — prose shapes never produce a verdict
# ---------------------------------------------------------------------------


def test_ambiguous_span_shapes_all_skipped(tmp_path):
    body = "\n".join(
        [
            "Slot-bearing: `${verify_command}` renders per project.",
            "Placeholder: `<repo>: vOLD → vNEW` and `.sessions/<date>.md`.",
            "Flag prose: `--apply-docs` and bracket prose `[Unreleased]`.",
            "Status tokens: `complete`, `in-progress`, `do-not-automerge`.",
            "Directory prose: `control/claims/` listing.",
            "State artifacts: `.substrate/upgrade-report.md` post-upgrade.",
            "Version placeholder: `vX.Y.Z` (uppercase pseudo-extension).",
        ],
    )
    assert check_skill_grounds(tmp_path, skills=[_fake_skill(body=body)]) == []


def test_whitelisted_executables_and_mcp_verbs_resolve(tmp_path):
    body = (
        "Run `git fetch origin main && git reset --hard origin/main`, then\n"
        "`gh release view vX.Y.Z`, `sha256sum bootstrap.py.new`, and the\n"
        "MCP call `create_pull_request` with the born-red card.\n"
    )
    assert check_skill_grounds(tmp_path, skills=[_fake_skill(body=body)]) == []


def test_unreadable_rendered_doc_fails_open(tmp_path):
    doc = tmp_path / ".claude" / "skills" / "bad" / "SKILL.md"
    doc.parent.mkdir(parents=True)
    doc.write_bytes(b"\xff\xfe\x00broken")
    assert check_skill_grounds(tmp_path, skills=[]) == []


# ---------------------------------------------------------------------------
# cmd_check integration — advisory NEVER touches the exit code (§8 Q2=B)
# ---------------------------------------------------------------------------


def test_cmd_check_strict_stays_green_on_unresolved_ground(tmp_path, capsys):
    doc = tmp_path / ".claude" / "skills" / "custom" / "SKILL.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("# custom\n\nRun `frobnicate --explode`.\n", encoding="utf-8")
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "skill-grounds advisory" in out
    assert "skill-ground-unresolved" in out
    assert "never exit-affecting" in out


def test_cmd_check_status_only_lane_skips_grounds_scan(tmp_path, capsys):
    doc = tmp_path / ".claude" / "skills" / "custom" / "SKILL.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("# custom\n\nRun `frobnicate --explode`.\n", encoding="utf-8")
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    assert "skill-ground" not in capsys.readouterr().out
