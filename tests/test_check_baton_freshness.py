"""Next-2 baton deliverable-freshness advisory (S17-card ⟲ note; inverse of S4).

Warns when a ``## Next-2 baton`` entry names a ``check_*`` / ``--flag``
deliverable as work still to build that ALREADY resolves in the tree — the S16
``--api-latency`` stale-baton class that burned a real worker's session.
Advisory only (warn, never exit-affecting); input-gated + fail-open; the mirror
inverse of S4's ``check_baton_resolves`` (which flags a path that does NOT
resolve). Hermetic — no network, no clone.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_baton_freshness")

from engine.checks.check_baton_freshness import (  # noqa: E402
    BATON_STALE_DELIVERABLE_KIND,
    _partition_baton_tokens,
    _baton_section_lines,
    check_baton_freshness,
)


# --- fixtures -----------------------------------------------------------------


def _write_status(root: Path, baton_body: str, name: str = "status.md") -> Path:
    d = root / "control"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    text = (
        "# seat — heartbeat\n\n"
        "## State\nkit: v1.19.0\n\n"
        "## Next-2 baton\n"
        f"{baton_body}\n\n"
        "## Held decision\nnone\n"
    )
    p.write_text(text, encoding="utf-8")
    return p


def _src(root: Path, relpath: str, body: str) -> Path:
    """Write a source file that the deliverable resolver will scan."""
    p = root / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _flag_registration(flag: str) -> str:
    return (
        "import argparse\n"
        "def main():\n"
        "    ap = argparse.ArgumentParser()\n"
        f'    ap.add_argument("{flag}", action="store_true")\n'
    )


# --- fires: a to-build deliverable already resolves ---------------------------


def test_flag_deliverable_already_built_fires(tmp_path: Path):
    _write_status(
        tmp_path,
        "1. Next buildable-now step is S16 (--api-latency harness — needs live GH).",
    )
    _src(tmp_path, "scripts/measure.py", _flag_registration("--api-latency"))
    findings = check_baton_freshness(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == BATON_STALE_DELIVERABLE_KIND
    assert findings[0].path == "control/status.md"
    assert "--api-latency" in findings[0].message


def test_flag_registered_flag_first_over_newline_fires(tmp_path: Path):
    # The real --api-latency registration puts the flag on its own line after
    # add_argument( — the resolver must still match across the newline.
    _write_status(tmp_path, "1. Build S16 (--api-latency mode) next.")
    _src(
        tmp_path,
        "scripts/m.py",
        'import argparse\nap = argparse.ArgumentParser()\n'
        'ap.add_argument(\n    "--api-latency",\n    action="store_true",\n)\n',
    )
    findings = check_baton_freshness(tmp_path)
    assert len(findings) == 1
    assert "--api-latency" in findings[0].message


def test_checker_deliverable_by_def_fires(tmp_path: Path):
    _write_status(tmp_path, "1. Next: build check_foo advisory.")
    _src(tmp_path, "src/engine/checks/check_foo.py", "def check_foo(target):\n    return []\n")
    findings = check_baton_freshness(tmp_path)
    assert len(findings) == 1
    assert "check_foo" in findings[0].message


def test_checker_deliverable_by_filename_fires(tmp_path: Path):
    # Even with no `def check_bar(`, a check_bar.py file present resolves it.
    _write_status(tmp_path, "1. Next: build check_bar.")
    _src(tmp_path, "src/engine/checks/check_bar.py", "# stub, no matching def\n")
    findings = check_baton_freshness(tmp_path)
    assert len(findings) == 1
    assert "check_bar" in findings[0].message


# --- silent: shipped-suppression (the current-tree guarantee) -----------------


def test_shipped_marker_suppresses_even_when_resolves(tmp_path: Path):
    _write_status(
        tmp_path,
        "1. **S16 (--api-latency harness) SHIPPED via PR #479** — done.",
    )
    _src(tmp_path, "scripts/m.py", _flag_registration("--api-latency"))
    assert check_baton_freshness(tmp_path) == []


@pytest.mark.parametrize(
    "marker_line",
    [
        "S16 (--api-latency) merged.",
        "S16 (--api-latency) landed already.",
        "S16 (--api-latency) is done.",
        "S16 (--api-latency) complete.",
        "S16 (--api-latency) already exists.",
        "S16 (--api-latency) shipped #999.",
        "S16 (--api-latency) ✓",
    ],
)
def test_each_completion_marker_suppresses(tmp_path: Path, marker_line: str):
    _write_status(tmp_path, marker_line)
    _src(tmp_path, "scripts/m.py", _flag_registration("--api-latency"))
    assert check_baton_freshness(tmp_path) == []


def test_pr_number_on_line_suppresses(tmp_path: Path):
    _write_status(tmp_path, "1. check_foo advisory (#543).")
    _src(tmp_path, "src/checks/check_foo.py", "def check_foo(t):\n    return []\n")
    assert check_baton_freshness(tmp_path) == []


def test_shipped_suppression_is_file_wide(tmp_path: Path):
    # A token acknowledged done on one line is suppressed even when a later
    # unmarked line mentions it as context (not as a fresh build target).
    body = (
        "1. **S16 (--api-latency) SHIPPED via #479.**\n"
        "2. Next work extends the --api-latency pattern into new territory.\n"
    )
    _write_status(tmp_path, body)
    _src(tmp_path, "scripts/m.py", _flag_registration("--api-latency"))
    assert check_baton_freshness(tmp_path) == []


# --- silent: the deliverable does NOT resolve (genuine future work) -----------


def test_unbuilt_deliverable_is_silent(tmp_path: Path):
    _write_status(tmp_path, "1. Next: build check_not_yet advisory.")
    # tree has no matching def / file / flag
    _src(tmp_path, "scripts/other.py", "def helper():\n    return 1\n")
    assert check_baton_freshness(tmp_path) == []


def test_docstring_mention_does_not_resolve(tmp_path: Path):
    # A prose/comment mention of the flag is NOT an argparse registration, so it
    # must not count as the deliverable existing (the resolves-backstop).
    _write_status(tmp_path, "1. Next: build --new-mode.")
    _src(
        tmp_path,
        "scripts/m.py",
        '"""Someday we might add --new-mode here."""\n# --new-mode is not built\n',
    )
    assert check_baton_freshness(tmp_path) == []


# --- input-gating / fail-open -------------------------------------------------


def test_no_control_dir_is_silent(tmp_path: Path):
    assert check_baton_freshness(tmp_path) == []


def test_no_baton_section_is_silent(tmp_path: Path):
    d = tmp_path / "control"
    d.mkdir()
    (d / "status.md").write_text("# seat\n\n## State\nok\n", encoding="utf-8")
    _src(tmp_path, "scripts/m.py", _flag_registration("--api-latency"))
    assert check_baton_freshness(tmp_path) == []


def test_tests_dir_is_not_a_deliverable_home(tmp_path: Path):
    # A --flag registered only inside a tests/ fixture must not resolve.
    _write_status(tmp_path, "1. Next: build --fixture-only flag.")
    _src(tmp_path, "tests/test_x.py", _flag_registration("--fixture-only"))
    assert check_baton_freshness(tmp_path) == []


def test_bootstrap_py_is_excluded(tmp_path: Path):
    _write_status(tmp_path, "1. Next: build --from-bootstrap flag.")
    _src(tmp_path, "bootstrap.py", _flag_registration("--from-bootstrap"))
    assert check_baton_freshness(tmp_path) == []


def test_multi_lane_status_glob(tmp_path: Path):
    _write_status(
        tmp_path,
        "1. Next: build check_lane advisory.",
        name="status-mining.md",
    )
    _src(tmp_path, "src/checks/check_lane.py", "def check_lane(t):\n    return []\n")
    findings = check_baton_freshness(tmp_path)
    assert len(findings) == 1
    assert findings[0].path == "control/status-mining.md"


# --- token grammar edge cases -------------------------------------------------


def test_endash_range_is_not_a_flag_token(tmp_path: Path):
    # "S2–S17" (en-dash) and single-hyphen words are not `--flag` tokens.
    _write_status(tmp_path, "1. The S2–S17 wave-2 buildable-now ladder is dry.")
    findings = check_baton_freshness(tmp_path)
    assert findings == []


def test_partition_helper_marks_and_suppresses():
    lines = [
        "1. **check_alpha SHIPPED via #543.**",
        "2. Next: build check_beta and --gamma-mode.",
    ]
    candidates, shipped = _partition_baton_tokens(lines)
    assert "check_alpha" in shipped
    assert "check_beta" in candidates
    assert "--gamma-mode" in candidates
    assert "check_beta" not in shipped


def test_section_lines_stop_at_next_h2():
    text = (
        "## Next-2 baton\n"
        "1. build check_foo\n"
        "## Held decision\n"
        "build check_bar\n"
    )
    lines = _baton_section_lines(text)
    joined = "\n".join(lines)
    assert "check_foo" in joined
    assert "check_bar" not in joined


# --- one finding per distinct token per file ----------------------------------


def test_one_finding_per_distinct_token(tmp_path: Path):
    body = (
        "1. Next: build check_dup advisory.\n"
        "2. Really, build check_dup — it is the priority.\n"
    )
    _write_status(tmp_path, body)
    _src(tmp_path, "src/checks/check_dup.py", "def check_dup(t):\n    return []\n")
    findings = check_baton_freshness(tmp_path)
    assert len(findings) == 1


# --- regression: the real baton shape -----------------------------------------


def test_current_baton_shape_is_silent(tmp_path: Path):
    # The live baton names check_recipe_discovery / --api-latency, but every
    # mention sits on a SHIPPED/PR-# line -> shipped-suppressed -> silent, even
    # though both deliverables resolve in the tree.
    body = (
        "1. **S17 (check_recipe_discovery advisory) SHIPPED via PR #543.** "
        "**S16 (--api-latency harness mode) was found ALREADY SHIPPED via PR "
        "#479** — honest-null, swapped to S17.\n"
        "**Baton: S17 (check_recipe_discovery) SHIPPED via PR #543; S16 "
        "(--api-latency harness) already-shipped via #479.**\n"
    )
    _write_status(tmp_path, body)
    _src(
        tmp_path,
        "src/engine/checks/check_recipe_discovery.py",
        "def check_recipe_discovery(t):\n    return []\n",
    )
    _src(tmp_path, "scripts/measure.py", _flag_registration("--api-latency"))
    assert check_baton_freshness(tmp_path) == []


def test_historical_stale_s16_baton_would_have_fired(tmp_path: Path):
    # The pre-correction baton line: S16 named as buildable-now work, no marker,
    # while --api-latency already existed in the tree (#479). This is the exact
    # incident the advisory exists to catch.
    _write_status(
        tmp_path,
        "1. baton retargeted at S16 (--api-latency harness — larger, needs live "
        "GH); S17 (applies-when discovery nudge) remains.",
    )
    _src(tmp_path, "scripts/measure.py", _flag_registration("--api-latency"))
    findings = check_baton_freshness(tmp_path)
    assert len(findings) == 1
    assert "--api-latency" in findings[0].message
