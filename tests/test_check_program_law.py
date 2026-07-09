"""Tests for scripts/check_program_law.py — the PL-register + pointer checker."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import check_program_law as cpl  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

_GOOD_BLOCK = """## [PL-001] A ruling

- status: decided
- date: 2026-07-06
- provenance: superbot Q-0240
- verdict: Agents make reversible-until-a-gate calls themselves with a flag.
"""

_POINTER_OK = """# ${project_name} — constitution

## Program law

Canonical home: `docs/program/rulings.md` — cite PL-001, never copy bodies.
"""


def _seed(root: Path, register: str, *, constitution: str = _POINTER_OK, collab: str = _POINTER_OK) -> Path:
    """Build a minimal fixture tree the checker can run against."""
    program = root / "docs" / "program"
    program.mkdir(parents=True)
    (program / "rulings.md").write_text(register, encoding="utf-8")
    templates = root / "src" / "engine" / "templates"
    templates.mkdir(parents=True)
    (templates / "CONSTITUTION.md.tmpl").write_text(constitution, encoding="utf-8")
    (templates / "collaboration-model.md.tmpl").write_text(collab, encoding="utf-8")
    return root


def _kinds(findings: list[cpl.Finding]) -> set[str]:
    return {f.kind for f in findings}


# ── the real repo is ground truth ────────────────────────────────────────────


def test_real_repo_is_clean() -> None:
    assert cpl.run_checks(REPO_ROOT) == []


def test_real_register_has_the_founding_census() -> None:
    blocks, findings = cpl.parse_register(REPO_ROOT / cpl.REGISTER_RELPATH)
    assert findings == []
    # PL-001..PL-009 founding census + appended amendments (PL-010 …),
    # sequential with no gaps (the register is append-only).
    assert len(blocks) >= 10  # PL-010: the feature-build taxonomy amendment
    assert [b.number for b in blocks] == list(range(1, len(blocks) + 1))
    provenance = " ".join(b.fields["provenance"] for b in blocks)
    for origin in ("Q-0240", "Q-0241", "Q-0247", "Q-0248", "Q-0249", "Q-0120", "Q-0132", "Q-0105"):
        assert origin in provenance


# ── register grammar ─────────────────────────────────────────────────────────


def test_clean_fixture_passes(tmp_path: Path) -> None:
    _seed(tmp_path, _GOOD_BLOCK)
    assert cpl.run_checks(tmp_path) == []


def test_missing_register_is_a_finding(tmp_path: Path) -> None:
    (tmp_path / "docs" / "program").mkdir(parents=True)
    findings = cpl.run_checks(tmp_path)
    assert "register" in _kinds(findings)


def test_missing_provenance_is_a_finding(tmp_path: Path) -> None:
    block = _GOOD_BLOCK.replace("- provenance: superbot Q-0240\n", "")
    _seed(tmp_path, block)
    findings = cpl.run_checks(tmp_path)
    assert any(f.kind == "field" and "provenance" in f.message for f in findings)


def test_missing_verdict_and_bad_status_and_bad_date(tmp_path: Path) -> None:
    block = _GOOD_BLOCK.replace("- status: decided", "- status: maybe").replace(
        "- date: 2026-07-06", "- date: July 6"
    ).replace("- verdict: Agents make reversible-until-a-gate calls themselves with a flag.\n", "")
    _seed(tmp_path, block)
    messages = " | ".join(f.message for f in cpl.run_checks(tmp_path))
    assert "invalid status" in messages
    assert "invalid date" in messages
    assert "`verdict`" in messages


def test_superseded_requires_superseded_by(tmp_path: Path) -> None:
    block = _GOOD_BLOCK.replace("- status: decided", "- status: superseded")
    _seed(tmp_path, block)
    findings = cpl.run_checks(tmp_path)
    assert any("superseded-by" in f.message for f in findings)


def test_malformed_heading_is_a_finding(tmp_path: Path) -> None:
    register = _GOOD_BLOCK + "\n## PL-2 — missing brackets\n\n- status: decided\n"
    _seed(tmp_path, register)
    findings = cpl.run_checks(tmp_path)
    assert any(f.kind == "grammar" and "malformed" in f.message for f in findings)


# ── monotonic ids ────────────────────────────────────────────────────────────


def _block(n: int) -> str:
    return (
        f"## [PL-{n:03d}] Ruling {n}\n\n- status: decided\n- date: 2026-07-07\n"
        f"- provenance: superbot Q-{n:04d}\n- verdict: Ruling number {n} short text.\n\n"
    )


def test_id_gap_is_a_finding(tmp_path: Path) -> None:
    _seed(tmp_path, _block(1) + _block(3))
    findings = cpl.run_checks(tmp_path)
    assert any(f.kind == "ids" and "PL-002" in f.message for f in findings)


def test_duplicate_id_is_a_finding(tmp_path: Path) -> None:
    _seed(tmp_path, _block(1) + _block(1))
    findings = cpl.run_checks(tmp_path)
    assert any(f.kind == "ids" and "duplicate" in f.message for f in findings)


def test_out_of_order_is_a_finding(tmp_path: Path) -> None:
    _seed(tmp_path, _block(2).replace("Q-0002", "Q-0240") + _block(1))
    findings = cpl.run_checks(tmp_path)
    assert any(f.kind == "ids" and "out of order" in f.message for f in findings)


# ── pointer sections ─────────────────────────────────────────────────────────


def test_required_template_without_section_is_a_finding(tmp_path: Path) -> None:
    _seed(tmp_path, _GOOD_BLOCK, constitution="# constitution\n\nno pointer here\n")
    findings = cpl.run_checks(tmp_path)
    assert any(f.kind == "pointer" and "CONSTITUTION" in f.path for f in findings)


def test_missing_required_template_is_a_finding(tmp_path: Path) -> None:
    _seed(tmp_path, _GOOD_BLOCK)
    (tmp_path / "src" / "engine" / "templates" / "collaboration-model.md.tmpl").unlink()
    findings = cpl.run_checks(tmp_path)
    assert any(f.kind == "pointer" and "collaboration-model" in f.path for f in findings)


def test_section_must_cite_register_and_a_pl_id(tmp_path: Path) -> None:
    no_cite = "## Program law\n\nSee the kit repo for rulings, e.g. PL-001.\n"
    no_id = "## Program law\n\nSee `docs/program/rulings.md` for program rulings.\n"
    _seed(tmp_path, _GOOD_BLOCK, constitution=no_cite, collab=no_id)
    messages = " | ".join(f.message for f in cpl.run_checks(tmp_path))
    assert "does not cite the register path" in messages
    assert "cites no PL-ID" in messages


def test_copied_ruling_body_is_a_finding(tmp_path: Path) -> None:
    copied = (
        "## Program law\n\nPer `docs/program/rulings.md` PL-001: Agents make "
        "reversible-until-a-gate calls themselves with a flag.\n"
    )
    _seed(tmp_path, _GOOD_BLOCK, constitution=copied)
    findings = cpl.run_checks(tmp_path)
    assert any(f.kind == "body-copy" and "CONSTITUTION" in f.path for f in findings)


def test_short_label_citation_is_not_a_body_copy(tmp_path: Path) -> None:
    labeled = (
        "## Program law\n\n`docs/program/rulings.md`: PL-001 (reversible calls, "
        "decide-and-flag). Cite ids, never copy bodies.\n"
    )
    _seed(tmp_path, _GOOD_BLOCK, constitution=labeled)
    assert cpl.run_checks(tmp_path) == []


def test_local_planted_docs_are_scanned_when_present(tmp_path: Path) -> None:
    _seed(tmp_path, _GOOD_BLOCK)
    local = tmp_path / "CONSTITUTION.md"
    local.write_text(
        "# c\n\n## Program law\n\nPer `docs/program/rulings.md` PL-001: Agents "
        "make reversible-until-a-gate calls themselves with a flag.\n",
        encoding="utf-8",
    )
    findings = cpl.run_checks(tmp_path)
    assert any(f.kind == "body-copy" and f.path == "CONSTITUTION.md" for f in findings)


# ── owner-gate label gate (rule 4, audit 2026-07-09) ─────────────────────────


def test_label_gate_ignores_ungated_paths() -> None:
    changed = ["docs/current-state.md", "src/engine/loop/telemetry.py", "docs/program/README.md"]
    assert cpl.check_label_gate(changed, [], "pull_request") == []


def test_label_gate_fails_unlabeled_law_change() -> None:
    findings = cpl.check_label_gate(["docs/program/rulings.md"], ["friction"], "pull_request")
    assert len(findings) == 1
    assert findings[0].kind == "label-gate"
    assert "do-not-automerge" in findings[0].message


def test_label_gate_covers_every_owner_gated_surface() -> None:
    findings = cpl.check_label_gate(list(cpl.OWNER_GATED_PATHS), [], "pull_request")
    assert [f.path for f in findings] == list(cpl.OWNER_GATED_PATHS)


def test_label_gate_passes_with_the_label(capsys) -> None:
    changed = ["docs/program/rulings.md", "docs/other.md"]
    assert cpl.check_label_gate(changed, ["do-not-automerge"], "pull_request") == []
    assert "riding review" in capsys.readouterr().out


def test_label_gate_skips_outside_pr_context(capsys) -> None:
    assert cpl.check_label_gate(["docs/program/rulings.md"], [], "push") == []
    assert "not applicable" in capsys.readouterr().out


def _git_fixture_repo(root: Path) -> None:
    """A tiny real repo: main with a clean register, a branch changing it."""

    def git(*args: str) -> None:
        subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True,
            env={**os.environ,
                 "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                 "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
        )

    _seed(root, _GOOD_BLOCK)
    git("init", "-b", "main")
    git("add", "-A")
    git("commit", "-m", "base")
    git("checkout", "-b", "feature")
    (root / "docs" / "program" / "rulings.md").write_text(
        _GOOD_BLOCK + "\n" + _block(2).replace("Q-0002", "Q-0240"), encoding="utf-8"
    )
    git("commit", "-am", "amend the register")


def test_run_label_gate_end_to_end(tmp_path: Path, monkeypatch) -> None:
    _git_fixture_repo(tmp_path)
    monkeypatch.setenv("GITHUB_EVENT_NAME", "pull_request")

    monkeypatch.setenv("PR_LABELS", "")
    findings = cpl.run_label_gate(tmp_path, "main")
    assert [f.kind for f in findings] == ["label-gate"]
    assert findings[0].path == "docs/program/rulings.md"

    monkeypatch.setenv("PR_LABELS", "friction, do-not-automerge")
    assert cpl.run_label_gate(tmp_path, "main") == []


def test_run_label_gate_skips_without_pr_event(tmp_path: Path, monkeypatch, capsys) -> None:
    # No git repo needed — the event check must come BEFORE any git call.
    monkeypatch.delenv("GITHUB_EVENT_NAME", raising=False)
    assert cpl.run_label_gate(tmp_path, "origin/main") == []
    assert "gate skipped" in capsys.readouterr().out


def test_main_label_gate_flag(tmp_path: Path, monkeypatch, capsys) -> None:
    _git_fixture_repo(tmp_path)
    monkeypatch.setenv("GITHUB_EVENT_NAME", "pull_request")
    monkeypatch.setenv("PR_LABELS", "")
    assert cpl.main(["--root", str(tmp_path), "--label-gate", "--base", "main"]) == 1
    assert "label-gate" in capsys.readouterr().out
    monkeypatch.setenv("PR_LABELS", "do-not-automerge")
    assert cpl.main(["--root", str(tmp_path), "--label-gate", "--base", "main"]) == 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def test_main_exit_codes(tmp_path: Path, capsys) -> None:
    _seed(tmp_path, _GOOD_BLOCK)
    assert cpl.main(["--root", str(tmp_path)]) == 0
    assert "OK" in capsys.readouterr().out
    bad = tmp_path / "docs" / "program" / "rulings.md"
    bad.write_text(_GOOD_BLOCK.replace("- provenance: superbot Q-0240\n", ""), encoding="utf-8")
    assert cpl.main(["--root", str(tmp_path)]) == 1
    assert "finding" in capsys.readouterr().out
