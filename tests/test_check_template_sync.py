"""The template↔local-copy heading-set sync advisory.

Idea authority: ``docs/ideas/template-local-copy-sync-advisory-2026-07-15.md``
— the kit plants adopter docs from ``src/engine/templates/*.tmpl``
(``ADOPT_PLAN``) and carries rendered local copies of the same docs,
hand-synced; a missed sync ships adopters a different contract than the kit
runs (two paid instances in one day, PRs #395/#397). These tests pin the
idea file's own fixture ("a fixture pair where the template gains a
``## New doctrine`` section the local copy lacks must fire the advisory;
byte-identical prose differences under identical headings must stay
silent"), the false-positive firewalls (slot patterns, ``[[fill:``, fences,
live-traffic skips), the adopter self-gate, and the advisory
never-exit-affecting contract.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.checks.check_template_sync import (
    LIVE_TRAFFIC_DESTS,
    TEMPLATES_RELPATH,
    _heading_drift,
    check_template_sync,
)
from engine.cli import cmd_check
from engine.lib.config import Config

# A real ADOPT_PLAN pair with a plain (non-docs_root-remapped) destination —
# the checker anchors on ADOPT_PLAN itself, so fixtures must use real names.
PAIR_TEMPLATE = "control-claims-README.md.tmpl"
PAIR_DEST = "control/claims/README.md"

# A real pair whose template heading carries a ${slot} placeholder.
SLOT_TEMPLATE = "CONSTITUTION.md.tmpl"
SLOT_DEST = "CONSTITUTION.md"


def _plant(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _pair(root: Path, template_text: str, local_text: str) -> None:
    _plant(root, f"{TEMPLATES_RELPATH}/{PAIR_TEMPLATE}", template_text)
    _plant(root, PAIR_DEST, local_text)


def test_template_only_section_fires(tmp_path: Path) -> None:
    """The idea's own fixture: a template-side ``## New doctrine`` fires."""
    _pair(
        tmp_path,
        "# Title\n\n## Shared\n\nbody\n\n## New doctrine\n\nrules\n",
        "# Title\n\n## Shared\n\nolder body\n",
    )
    findings = check_template_sync(tmp_path, Config())
    assert len(findings) == 1
    finding = findings[0]
    assert finding.kind == "template-local-heading-drift"
    assert finding.path == PAIR_DEST
    assert "template-only: 'New doctrine'" in finding.message
    assert "local-only" not in finding.message
    assert PAIR_TEMPLATE in finding.message


def test_local_only_section_fires_named_local(tmp_path: Path) -> None:
    _pair(
        tmp_path,
        "# Title\n\n## Shared\n\nbody\n",
        "# Title\n\n## Shared\n\nbody\n\n## Repo extra\n\nnotes\n",
    )
    findings = check_template_sync(tmp_path, Config())
    assert len(findings) == 1
    assert "local-only: 'Repo extra'" in findings[0].message


def test_prose_divergence_under_identical_headings_is_silent(
    tmp_path: Path,
) -> None:
    """Heading sets, not byte-diff — local prose legitimately diverges."""
    _pair(
        tmp_path,
        "# Title\n\n## Shared\n\ntemplate wording ${project_name}\n",
        "# Title\n\n## Shared\n\ncompletely different local wording\n",
    )
    assert check_template_sync(tmp_path, Config()) == []


def test_slotted_template_heading_matches_rendered_local(
    tmp_path: Path,
) -> None:
    """``Rails specific to ${project_name}`` ↔ the rendered name is NOT drift."""
    _plant(
        tmp_path,
        f"{TEMPLATES_RELPATH}/{SLOT_TEMPLATE}",
        "# C\n\n## Rails specific to ${project_name}\n\nbody\n",
    )
    _plant(tmp_path, SLOT_DEST, "# C\n\n## Rails specific to demo-repo\n\nbody\n")
    assert check_template_sync(tmp_path, Config()) == []


def test_unmatched_slotted_heading_reports_template_only(
    tmp_path: Path,
) -> None:
    _plant(
        tmp_path,
        f"{TEMPLATES_RELPATH}/{SLOT_TEMPLATE}",
        "# C\n\n## Rails specific to ${project_name}\n\nbody\n",
    )
    _plant(tmp_path, SLOT_DEST, "# C\n\n## Something else entirely\n\nbody\n")
    findings = check_template_sync(tmp_path, Config())
    assert len(findings) == 1
    message = findings[0].message
    assert "Rails specific to ${project_name}" in message
    assert "Something else entirely" in message


def test_fill_marker_headings_skip_both_sides(tmp_path: Path) -> None:
    _pair(
        tmp_path,
        "# T\n\n## Shared\n\nbody\n\n## [[fill: hand section]]\n\nx\n",
        "# T\n\n## Shared\n\nbody\n",
    )
    assert check_template_sync(tmp_path, Config()) == []


def test_fenced_headings_never_count(tmp_path: Path) -> None:
    _pair(
        tmp_path,
        "# T\n\n## Shared\n\n```\n## Example inside fence\n```\n",
        "# T\n\n## Shared\n\nbody\n",
    )
    assert check_template_sync(tmp_path, Config()) == []


def test_live_traffic_destinations_skip(tmp_path: Path) -> None:
    """Bus/ledger seeds accumulate live headings by design — never drift."""
    assert "control/status.md" in LIVE_TRAFFIC_DESTS
    _plant(
        tmp_path,
        f"{TEMPLATES_RELPATH}/control-status.md.tmpl",
        "# heartbeat\n\n## Seeded shape\n",
    )
    _plant(
        tmp_path,
        "control/status.md",
        "# heartbeat\n\n## This wake\n\n## Next-2 baton\n",
    )
    assert check_template_sync(tmp_path, Config()) == []


def test_adopter_tree_self_gates(tmp_path: Path) -> None:
    """No src/engine/templates/ (every adopter) → the scan is a no-op."""
    _plant(tmp_path, PAIR_DEST, "# T\n\n## Local only heading\n")
    assert check_template_sync(tmp_path, Config()) == []


def test_missing_destination_contributes_nothing(tmp_path: Path) -> None:
    _plant(
        tmp_path,
        f"{TEMPLATES_RELPATH}/{PAIR_TEMPLATE}",
        "# T\n\n## Anything\n",
    )
    assert check_template_sync(tmp_path, Config()) == []


def test_heading_drift_helper_is_order_insensitive() -> None:
    template_only, local_only = _heading_drift(
        "## B\n\n## A\n",
        "## A\n\n## B\n",
    )
    assert template_only == []
    assert local_only == []


def test_advisory_never_affects_exit_code(tmp_path: Path, capsys) -> None:
    """The contract line: drift warns, exit code is untouched."""
    _pair(
        tmp_path,
        "# T\n\n## Shared\n\n## New doctrine\n",
        "# T\n\n## Shared\n",
    )
    code = cmd_check(tmp_path, strict=False)
    out = capsys.readouterr().out
    assert code == 0
    assert "template-local-heading-drift" in out
    assert "never exit-affecting" in out
