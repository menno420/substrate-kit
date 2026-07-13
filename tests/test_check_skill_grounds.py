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


def test_dot_led_dead_pointer_in_rendered_doc_detected(tmp_path):
    # Blind spot 1 (the #335 guard's finding, graduated into the checker):
    # a dot-led pointer is judged like any pointer — dead means a finding,
    # including under the state dir when it names no known artifact class.
    doc = tmp_path / ".claude" / "skills" / "custom" / "SKILL.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(
        "# custom\n\nRead `.substrate/no-such-report.md` and "
        "`.claude/missing/thing.md` first.\n",
        encoding="utf-8",
    )
    findings = check_skill_grounds(tmp_path, skills=[])
    assert _kinds(findings) == ["skill-ground-unresolved"] * 2
    spans = " | ".join(f.message for f in findings)
    assert ".substrate/no-such-report.md" in spans
    assert ".claude/missing/thing.md" in spans


def test_dot_led_existing_pointer_resolves(tmp_path):
    skill = _fake_skill(body="Check `.github/workflows/ci.yml` for the gate.")
    assert _kinds(check_skill_grounds(tmp_path, skills=[skill])) == [
        "skill-ground-unresolved"
    ]
    wf = tmp_path / ".github" / "workflows" / "ci.yml"
    wf.parent.mkdir(parents=True)
    wf.write_text("", encoding="utf-8")
    assert check_skill_grounds(tmp_path, skills=[skill]) == []


def test_state_dir_artifact_classes_resolve_on_empty_target(tmp_path):
    # The deliberate replacement for the blanket state-dir skip: known
    # kit-written artifact classes stay grounded by construction even on a
    # target where none of them exist yet.
    body = (
        "After the wave read `.substrate/upgrade-report.md`; the byte\n"
        "backup lands in `.substrate/backup/` and staged docs under\n"
        "`.substrate/skills/review/SKILL.md`.\n"
    )
    assert check_skill_grounds(tmp_path, skills=[_fake_skill(body=body)]) == []


def test_state_dir_classification_follows_configured_state_dir(tmp_path):
    # The classes attach to the CONFIGURED state dir, not the default
    # spelling: under state_dir="kitstate" the same artifact names resolve
    # by class, and an unknown kitstate path is judged dead.
    body = "Read `kitstate/upgrade-report.md`, then `kitstate/ghost.md`."
    findings = check_skill_grounds(
        tmp_path, skills=[_fake_skill(body=body)], state_dir="kitstate"
    )
    assert _kinds(findings) == ["skill-ground-unresolved"]
    assert "kitstate/ghost.md" in findings[0].message


def test_markdown_link_dead_target_detected(tmp_path):
    # Blind spot 2: [text](target) pointers feed the same skip ladder.
    doc = tmp_path / ".claude" / "skills" / "custom" / "SKILL.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(
        "# custom\n\nSee the [report](docs/no-such-file.md) for context.\n",
        encoding="utf-8",
    )
    findings = check_skill_grounds(tmp_path, skills=[])
    assert _kinds(findings) == ["skill-ground-unresolved"]
    assert "docs/no-such-file.md" in findings[0].message


def test_markdown_link_scheme_anchor_and_prose_targets_skipped(tmp_path):
    body = "\n".join(
        [
            "External: [docs](https://example.com/x.md) and",
            "[plain](http://example.com) plus [mail](mailto:a@b.md).",
            "Anchor: [below](#verification).",
            "Prose parenthetical: [rule] (see the ladder above).",
            "Titled: [x](docs/y.md 'the report').",
        ],
    )
    assert check_skill_grounds(tmp_path, skills=[_fake_skill(body=body)]) == []


def test_markdown_link_fragment_stripped_and_existing_target_resolves(tmp_path):
    skill = _fake_skill(body="See [the contract](docs/contract.md#section-2).")
    assert _kinds(check_skill_grounds(tmp_path, skills=[skill])) == [
        "skill-ground-unresolved"
    ]
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "contract.md").write_text("", encoding="utf-8")
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
