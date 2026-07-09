"""Tests for scripts/check_bench_integrity.py — the §5.0 bench pin, layer 1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import check_bench_integrity as cbi  # noqa: E402


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


@pytest.fixture()
def repo(tmp_path):
    """A scratch git repo with a committed bench/ tree on branch main."""
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    results = tmp_path / "bench" / "results" / "cold-start"
    results.mkdir(parents=True)
    (results / "index.json").write_text(
        json.dumps([{"run_id": "r1", "verdict": "FAIL"}]) + "\n", encoding="utf-8",
    )
    run_dir = results / "2026-07-01-run01"
    run_dir.mkdir()
    (run_dir / "report.md").write_text("old report\n", encoding="utf-8")
    rubric = tmp_path / "bench" / "rubric"
    rubric.mkdir(parents=True)
    (rubric / "cold-start-rubric.md").write_text("rubric v1\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "seed")
    _git(tmp_path, "checkout", "-q", "-b", "work")
    return tmp_path


def _commit_all(repo_path: Path) -> None:
    _git(repo_path, "add", "-A")
    _git(repo_path, "commit", "-q", "-m", "change")


def _run(repo_path: Path, *, labels="", event="pull_request") -> int:
    return cbi.main(["--base", "main", "--root", str(repo_path), "--labels", labels, "--event", event])


# ---------------------------------------------------------------------------
# Rule 1 — the pin-path label gate
# ---------------------------------------------------------------------------


def test_rubric_change_without_label_is_red(repo, capsys):
    (repo / "bench" / "rubric" / "cold-start-rubric.md").write_text("rubric v2\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="") == 1
    assert "do-not-automerge" in capsys.readouterr().out


def test_rubric_change_with_label_is_green(repo):
    (repo / "bench" / "rubric" / "cold-start-rubric.md").write_text("rubric v2\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="do-not-automerge,extra") == 0


def test_pin_gate_skipped_outside_pr_context(repo):
    (repo / "bench" / "rubric" / "cold-start-rubric.md").write_text("rubric v2\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="", event="push") == 0


def test_new_task_file_needs_the_label_too(repo):
    tasks = repo / "bench" / "tasks"
    tasks.mkdir()
    (tasks / "T6.md").write_text("new task\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="") == 1


# ---------------------------------------------------------------------------
# Rule 2 — append-aware results immutability
# ---------------------------------------------------------------------------


def test_index_append_is_allowed(repo):
    index = repo / "bench" / "results" / "cold-start" / "index.json"
    rows = json.loads(index.read_text(encoding="utf-8"))
    rows.append({"run_id": "r2", "verdict": "PASS"})
    index.write_text(json.dumps(rows) + "\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="") == 0


def test_index_row_edit_is_red(repo, capsys):
    index = repo / "bench" / "results" / "cold-start" / "index.json"
    index.write_text(json.dumps([{"run_id": "r1", "verdict": "PASS"}]) + "\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="") == 1
    assert "append-only" in capsys.readouterr().out


def test_index_row_removal_is_red(repo):
    index = repo / "bench" / "results" / "cold-start" / "index.json"
    index.write_text("[]\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="") == 1


def test_results_artifact_modify_is_red(repo, capsys):
    report = repo / "bench" / "results" / "cold-start" / "2026-07-01-run01" / "report.md"
    report.write_text("rewritten history\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="") == 1
    assert "immutable" in capsys.readouterr().out


def test_results_delete_is_red(repo):
    (repo / "bench" / "results" / "cold-start" / "2026-07-01-run01" / "report.md").unlink()
    _commit_all(repo)
    assert _run(repo, labels="") == 1


def test_new_run_dir_is_allowed(repo):
    new_run = repo / "bench" / "results" / "cold-start" / "2026-07-15-run02"
    new_run.mkdir()
    (new_run / "report.md").write_text("new run\n", encoding="utf-8")
    (new_run / "transcript.jsonl").write_text("{}\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="") == 0


def test_no_bench_changes_is_green(repo):
    (repo / "other.txt").write_text("x\n", encoding="utf-8")
    _commit_all(repo)
    assert _run(repo, labels="") == 0
