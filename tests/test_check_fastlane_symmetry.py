"""R8 — fast-lane prefix symmetry runtime advisory.

Covers ``engine.checks.check_fastlane_symmetry.check_fastlane_symmetry``: the
runtime promotion of the enabler⇄guard half of the B-3 kit-only meta-test
(``tests/test_fastlane_prefix_symmetry.py``), so ADOPTERS warn when their ci.yml
claims-only fast-lane guard cards a prefix their auto-merge-enabler never arms.
Advisory-only, never exit-affecting. Stdlib-only, no subprocess (matches
tests/test_fastlane_prefix_symmetry.py + tests/test_check_automerge_preflight.py).
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from engine import guards  # noqa: E402
from engine.checks.check_fastlane_symmetry import check_fastlane_symmetry  # noqa: E402

_ENABLER_REL = ".github/workflows/auto-merge-enabler.yml"
_CI_REL = ".github/workflows/ci.yml"


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _enabler_yaml(prefixes) -> str:
    terms = " || ".join(f"startsWith(github.head_ref, '{p}')" for p in prefixes)
    return f"name: auto-merge-enabler\non: pull_request\njobs:\n  arm:\n    if: {terms}\n"


def _ci_yaml(carded_prefixes) -> str:
    arms = "\n".join(f"          {p}*) need_card=1 ;;" for p in carded_prefixes)
    return (
        "name: ci\njobs:\n  kit-quality:\n    steps:\n"
        "      - name: fast-lane guard\n        run: |\n"
        '          case "$head_ref" in\n'
        f"{arms}\n"
        "          *) need_card=0 ;;\n"
        "          esac\n"
    )


# ── self-quiet ───────────────────────────────────────────────────────────────
def test_bare_tree_is_silent(tmp_path):
    """No surface files → no findings."""
    assert check_fastlane_symmetry(tmp_path) == []


def test_only_enabler_is_silent(tmp_path):
    """Needs BOTH surfaces to compare — the enabler⇄config half is another
    check's job, so an enabler-only tree adds nothing here."""
    _write(tmp_path, _ENABLER_REL, _enabler_yaml(["claude/", "claim/"]))
    assert check_fastlane_symmetry(tmp_path) == []


def test_only_ci_is_silent(tmp_path):
    _write(tmp_path, _CI_REL, _ci_yaml(["claude/"]))
    assert check_fastlane_symmetry(tmp_path) == []


def test_ci_without_guard_block_is_silent(tmp_path):
    """A ci.yml with no `case "$head_ref"` guard block is not the planted
    shape — decline to guess."""
    _write(tmp_path, _ENABLER_REL, _enabler_yaml(["claude/", "claim/"]))
    _write(tmp_path, _CI_REL, "name: ci\njobs:\n  kit-quality:\n    steps: []\n")
    assert check_fastlane_symmetry(tmp_path) == []


# ── green: guard carded ⊆ enabler armed ──────────────────────────────────────
def test_agreeing_surfaces_are_green(tmp_path):
    """Guard cards claude/, enabler arms claude/+claim/ → carded ⊆ armed."""
    _write(tmp_path, _ENABLER_REL, _enabler_yaml(["claude/", "claim/"]))
    _write(tmp_path, _CI_REL, _ci_yaml(["claude/"]))
    assert check_fastlane_symmetry(tmp_path) == []


def test_custom_prefixes_are_not_false_walled(tmp_path):
    """A host that armed AND carded a custom prefix is green — the check is a
    pure two-file cross-check with no canonical pivot to false-wall against."""
    _write(tmp_path, _ENABLER_REL, _enabler_yaml(["claude/", "claim/", "bot/"]))
    _write(tmp_path, _CI_REL, _ci_yaml(["claude/", "bot/"]))
    assert check_fastlane_symmetry(tmp_path) == []


# ── advisory red: guard cards a prefix the enabler never arms ─────────────────
def test_guard_cards_unarmed_prefix_warns(tmp_path):
    _write(tmp_path, _ENABLER_REL, _enabler_yaml(["claude/", "claim/"]))
    _write(tmp_path, _CI_REL, _ci_yaml(["claude/", "bot/"]))
    findings = check_fastlane_symmetry(tmp_path)
    assert len(findings) == 1
    f = findings[0]
    assert f.path == _CI_REL and f.kind == "fastlane-symmetry"
    assert "bot/" in f.message and "enabler" in f.message


def test_unreadable_fails_open(tmp_path):
    """A directory where the enabler file should be → OSError on read → no
    verdict (fail open), never a crash."""
    (tmp_path / _ENABLER_REL).mkdir(parents=True)  # a dir, not a file
    _write(tmp_path, _CI_REL, _ci_yaml(["claude/"]))
    # enabler.is_file() is False for a directory → silent, not a crash
    assert check_fastlane_symmetry(tmp_path) == []


# ── posture pins ─────────────────────────────────────────────────────────────
def test_not_a_strict_subcheck():
    """R8 is ADVISORY — deliberately off STRICT_SUBCHECKS and out of
    _extra_check_findings (its enabler⇄config sibling's fleet-bomb reason)."""
    assert "check_fastlane_symmetry" not in guards.STRICT_SUBCHECKS


def test_real_kit_surfaces_are_symmetric():
    """The kit's OWN enabler + ci.yml guard agree — the advisory must not fire
    on the kit repo itself."""
    assert check_fastlane_symmetry(_ROOT) == []
