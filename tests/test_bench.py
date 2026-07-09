"""Tests for the bench/ harness (band KL-5, plan §5.0): seeds, M1, recorder."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_BENCH = _REPO / "bench"
if str(_BENCH) not in sys.path:
    sys.path.insert(0, str(_BENCH))
if str(_BENCH / "seeds") not in sys.path:
    sys.path.insert(0, str(_BENCH / "seeds"))

import make_seed  # noqa: E402
import run_ab  # noqa: E402
import score_m1  # noqa: E402

# ---------------------------------------------------------------------------
# make_seed — fresh names, same shape, deterministic, seeded bug present
# ---------------------------------------------------------------------------


def test_make_seed_deterministic(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    make_seed.generate(a, seed=42)
    make_seed.generate(b, seed=42)
    files_a = sorted(p.relative_to(a) for p in a.rglob("*") if p.is_file())
    files_b = sorted(p.relative_to(b) for p in b.rglob("*") if p.is_file())
    assert files_a == files_b
    for rel in files_a:
        assert (a / rel).read_bytes() == (b / rel).read_bytes()


def test_make_seed_fresh_surface_names_per_seed(tmp_path):
    names_1 = make_seed._names(1)
    names_2 = make_seed._names(7)
    assert names_1["project"] != names_2["project"]  # anti-memorization


def test_make_seed_same_shape_every_seed(tmp_path):
    for seed in (1, 7):
        dest = tmp_path / f"s{seed}"
        make_seed.generate(dest, seed=seed)
        packages = [p for p in dest.iterdir() if p.is_dir() and p.name != "tests"]
        assert len(packages) == 1
        module_names = sorted(p.name for p in packages[0].glob("*.py"))
        assert module_names == ["__init__.py", "cli.py", "ops.py", "store.py"]
        assert list((dest / "tests").glob("test_*.py"))
        assert (dest / "README.md").exists()


def test_make_seed_tests_pass_and_bug_is_seeded(tmp_path):
    make_seed.generate(tmp_path, seed=3)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    # The seeded bug: docstring/README promise case-insensitive filtering,
    # the implementation compares raw strings, and no test covers it.
    names = make_seed._names(3)
    ops_text = (tmp_path / names["project"] / "ops.py").read_text(encoding="utf-8")
    assert "case-insensitive" in ops_text  # the promise
    assert 'r["category"] == category' in ops_text  # the raw comparison
    assert "case-insensitive" in (tmp_path / "README.md").read_text(encoding="utf-8")
    tests_text = (tmp_path / "tests" / f"test_{names['project']}.py").read_text(encoding="utf-8")
    assert "lower" not in tests_text  # the gap is untested


# ---------------------------------------------------------------------------
# score_m1 — words before the first mutating action
# ---------------------------------------------------------------------------


def _write_transcript(path, events):
    path.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")


def test_score_m1_counts_until_first_mutation(tmp_path):
    transcript = tmp_path / "t.jsonl"
    _write_transcript(
        transcript,
        [
            {"type": "tool_use", "name": "Read", "input": {"file_path": "x"}},
            {"type": "tool_result", "content": "one two three"},
            {"type": "text", "content": "assistant words never count"},
            {"type": "tool_use", "name": "Bash", "input": {"command": "ls -la"}},
            {"type": "tool_result", "content": "four five"},
            {"type": "tool_use", "name": "Write", "input": {"file_path": "y"}},
            {"type": "tool_result", "content": "after mutation not counted"},
        ],
    )
    record = score_m1.score_transcript(transcript)
    assert record["m1_words_before_first_mutation"] == 5
    assert record["first_mutation"]["tool"] == "Write"


def test_score_m1_bash_mutations_stop_the_count(tmp_path):
    for command, mutating in (
        ("git commit -m x", True),
        ("echo hi > file.txt", True),
        ("sed -i s/a/b/ f", True),
        ("rm -rf build", True),
        ("git log --oneline", False),
        ("grep -r pattern .", False),
        ("python3 -m pytest -q", False),
    ):
        transcript = tmp_path / "t.jsonl"
        _write_transcript(
            transcript,
            [
                {"type": "tool_result", "content": "a b c"},
                {"type": "tool_use", "name": "Bash", "input": {"command": command}},
                {"type": "tool_result", "content": "d e"},
            ],
        )
        record = score_m1.score_transcript(transcript)
        expected = 3 if mutating else 5
        assert record["m1_words_before_first_mutation"] == expected, command


def test_score_m1_block_content_and_no_mutation(tmp_path):
    transcript = tmp_path / "t.jsonl"
    _write_transcript(
        transcript,
        [
            {"type": "tool_result", "content": [{"type": "text", "text": "one two"}]},
            {"type": "tool_result", "content": "three"},
        ],
    )
    record = score_m1.score_transcript(transcript)
    assert record["m1_words_before_first_mutation"] == 3
    assert record["first_mutation"] is None


# ---------------------------------------------------------------------------
# run_ab record — schema-checked, append-only, dedupe by run_id
# ---------------------------------------------------------------------------


def _row(run_id="2026-07-15-run01"):
    return {
        "date": "2026-07-15",
        "kit_version": "1.0.0",
        "run_id": run_id,
        "tasks": ["T2", "T4", "T5"],
        "m1_on": 1700,
        "m1_off": 549,
        "m2": "OFF",
        "m3": "tie",
        "verdict": "FAIL",
        "judge_model": "opus-x",
        "notes": "test row",
    }


@pytest.fixture()
def bench_results(tmp_path, monkeypatch):
    results = tmp_path / "results" / "cold-start"
    results.mkdir(parents=True)
    (results / "index.json").write_text("[]\n", encoding="utf-8")
    monkeypatch.setattr(run_ab, "BENCH_ROOT", tmp_path)
    return results / "index.json"


def test_record_appends_row(bench_results, capsys):
    rc = run_ab.main(["record", "--family", "cold-start", "--row", json.dumps(_row())])
    assert rc == 0
    rows = json.loads(bench_results.read_text(encoding="utf-8"))
    assert len(rows) == 1
    assert rows[0]["run_id"] == "2026-07-15-run01"


def test_record_rejects_missing_keys(bench_results):
    bad = _row()
    del bad["judge_model"]
    with pytest.raises(SystemExit):
        run_ab.main(["record", "--family", "cold-start", "--row", json.dumps(bad)])


def test_record_rejects_duplicate_run_id(bench_results):
    run_ab.main(["record", "--family", "cold-start", "--row", json.dumps(_row())])
    with pytest.raises(SystemExit):
        run_ab.main(["record", "--family", "cold-start", "--row", json.dumps(_row())])
    rows = json.loads(bench_results.read_text(encoding="utf-8"))
    assert len(rows) == 1  # history untouched
