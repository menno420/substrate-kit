"""Next-2 baton path/anchor resolver advisory (wave-2 groom S4).

Warns when a ``## Next-2 baton`` entry in ``control/status*.md`` cites a
repo-relative path/anchor that no longer resolves on disk — a stale baton
pointer strands the next wake. Advisory only (warn, never exit-affecting);
input-gated + fail-open.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_baton_resolves")

from engine.checks.check_baton_resolves import (  # noqa: E402
    BATON_UNRESOLVED_KIND,
    check_baton_resolves,
    _looks_like_path,
)


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


def _touch(root: Path, relpath: str, body: str = "# doc\n") -> Path:
    p = root / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


# --- fires on a dangling path -------------------------------------------------


def test_dangling_path_fires(tmp_path: Path):
    _write_status(
        tmp_path,
        "1. Next work in `docs/planning/2026-07-19-nope.md`.",
    )
    findings = check_baton_resolves(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == BATON_UNRESOLVED_KIND
    assert findings[0].path == "control/status.md"
    assert "docs/planning/2026-07-19-nope.md" in findings[0].message


def test_resolving_path_is_silent(tmp_path: Path):
    _touch(tmp_path, "docs/planning/2026-07-19-real.md")
    _write_status(
        tmp_path,
        "1. Next work in `docs/planning/2026-07-19-real.md`.",
    )
    assert check_baton_resolves(tmp_path) == []


# --- anchor resolution --------------------------------------------------------


def test_resolving_path_bad_anchor_fires(tmp_path: Path):
    _touch(
        tmp_path,
        "docs/recipes/thing.md",
        "# Thing\n\n## Real Section\ntext\n",
    )
    _write_status(
        tmp_path,
        "1. See `docs/recipes/thing.md#ghost-section`.",
    )
    findings = check_baton_resolves(tmp_path)
    assert len(findings) == 1
    assert "#ghost-section" in findings[0].message


def test_resolving_path_good_anchor_is_silent(tmp_path: Path):
    _touch(
        tmp_path,
        "docs/recipes/thing.md",
        "# Thing\n\n## Real Section\ntext\n",
    )
    _write_status(
        tmp_path,
        "1. See `docs/recipes/thing.md#real-section`.",
    )
    assert check_baton_resolves(tmp_path) == []


# --- fail-open / input-gating -------------------------------------------------


def test_no_control_dir_fails_open(tmp_path: Path):
    assert check_baton_resolves(tmp_path) == []


def test_no_baton_section_fails_open(tmp_path: Path):
    d = tmp_path / "control"
    d.mkdir()
    (d / "status.md").write_text("# seat\n\n## State\nkit: v1\n", encoding="utf-8")
    assert check_baton_resolves(tmp_path) == []


def test_non_path_codespans_never_fire(tmp_path: Path):
    # The baton's real non-path code spans must never be mistaken for a file.
    _write_status(
        tmp_path,
        "1. Run `check --strict`; trigger `trig_01194PdaWChtHGNKASURxdLx` "
        "cron `2 */2 * * *`; `kit: v1.19.0`; verify every `## Next-2 baton` "
        "entry.",
    )
    assert check_baton_resolves(tmp_path) == []


def test_section_closes_at_next_h2(tmp_path: Path):
    # A dangling path OUTSIDE the baton section (under a later H2) is not graded.
    d = tmp_path / "control"
    d.mkdir()
    (d / "status.md").write_text(
        "# seat\n\n"
        "## Next-2 baton\n1. all good.\n\n"
        "## Elsewhere\nsee `docs/planning/2026-07-19-nope.md`.\n",
        encoding="utf-8",
    )
    assert check_baton_resolves(tmp_path) == []


def test_duplicate_token_fires_once(tmp_path: Path):
    _write_status(
        tmp_path,
        "1. Work in `docs/planning/2026-07-19-nope.md`.\n"
        "2. Still `docs/planning/2026-07-19-nope.md`.",
    )
    findings = check_baton_resolves(tmp_path)
    assert len(findings) == 1


def test_per_lane_status_files_each_graded(tmp_path: Path):
    _write_status(
        tmp_path,
        "1. `docs/planning/2026-07-19-nope.md`.",
        name="status-mining.md",
    )
    _write_status(
        tmp_path,
        "1. `docs/planning/2026-07-19-other.md`.",
        name="status-exploration.md",
    )
    findings = check_baton_resolves(tmp_path)
    assert len(findings) == 2
    paths = {f.path for f in findings}
    assert paths == {"control/status-mining.md", "control/status-exploration.md"}


# --- token filter unit --------------------------------------------------------


def test_looks_like_path_filter():
    assert _looks_like_path("docs/planning/x.md")
    assert _looks_like_path("src/engine/checks/check_baton_resolves.py")
    assert _looks_like_path("docs/recipes/thing.md#real-section")
    # non-paths
    assert not _looks_like_path("## Next-2 baton")
    assert not _looks_like_path("check --strict")
    assert not _looks_like_path("kit: v1.19.0")
    assert not _looks_like_path("v1.19.0")
    assert not _looks_like_path("trig_01194PdaWChtHGNKASURxdLx")
    assert not _looks_like_path("2 */2 * * *")
    assert not _looks_like_path("docs/planning")  # dir, no file ext
