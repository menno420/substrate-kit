"""Fast-lane branch-prefix symmetry — runtime advisory (groom R8).

Promotes the enabler⇄guard half of the B-3 kit-only meta-test
(``tests/test_fastlane_prefix_symmetry.py``) to a runtime advisory every
ADOPTER runs under ``bootstrap check``, so a host catches its OWN
``auto-merge-enabler.yml`` ⇄ claims-only-guard prefix drift — not just
substrate-kit's own CI. The set of head-branch prefixes that ride the
auto-merge fast lane lives on two host workflow surfaces (the enabler ARMS
them; the ci.yml claims-only guard CARDS them), and nothing kept an adopter's
copies in agreement: a seat prefix carded by the guard but never armed by the
enabler is a guard that cards a branch the fast lane never touches.

SCOPE — the enabler⇄guard cross-check only
------------------------------------------
The enabler⇄*config* half is already owned by
``engine.checks.check_automerge_preflight`` (``automerge-branch-drift``), so
this check deliberately does NOT re-flag it — it covers the complementary,
otherwise-uncovered surface: the ci.yml claims-only fast-lane guard. It is a
pure two-file cross-check — every prefix the guard cards must also be a prefix
the enabler arms — so it needs no canonical pivot and can never false-wall a
host that customized its fast-lane prefixes (both files are the host's own).
Each leg self-gates on BOTH surface files existing; a host missing either adds
nothing.

POSTURE — advisory-only, never exit-affecting
---------------------------------------------
On the same ``posture="advisory"`` seam as its R5/R7 siblings (NOT
``_extra_check_findings`` / ``STRICT_SUBCHECKS``). The R8 recipe body named the
strict seam, but an installed enabler legitimately lags its regenerated form
during a kit version-skew window (an adopter upgrades config before rerunning
``upgrade``), and ``check_automerge_preflight`` already pins that exact drift
class ADVISORY for the reason its ``test_drift_never_reds_strict_check`` states:
"a required-check red here would be a fleet bomb during version skew." An
enabler⇄guard mismatch is the same shape — surface it as a regenerate nudge,
never a locked door.

Stdlib-only string/regex parsing (the same convention as the meta-test and
``check_automerge_preflight`` — no YAML parser, no subprocess).
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding

_ENABLER_RELPATH = ".github/workflows/auto-merge-enabler.yml"
_CI_RELPATH = ".github/workflows/ci.yml"

# ``startsWith(github.head_ref, 'claude/')`` — the enabler's arming terms.
_STARTSWITH = re.compile(r"startsWith\(\s*github\.head_ref\s*,\s*'([^']+)'\s*\)")
# The claims-only guard's ``case "$head_ref" in`` block, and its ``<prefix>*)``
# carded arms (the bare ``*)`` fallback rides card-free and names no prefix).
_CASE_BLOCK = re.compile(r'case\s+"\$head_ref"\s+in(.*?)esac', re.DOTALL)
_CARDED_ARM = re.compile(r"([A-Za-z][\w./-]*)\*\)")


def _enabler_armed_prefixes(text: str) -> set[str]:
    """Prefixes the enabler arms — ``startsWith(github.head_ref, 'X')``."""
    return set(_STARTSWITH.findall(text))


def _guard_carded_prefixes(text: str) -> set[str]:
    """Prefixes the claims-only fast-lane guard cards — the ``<prefix>*)`` arms."""
    prefixes: set[str] = set()
    for block in _CASE_BLOCK.findall(text):
        prefixes.update(_CARDED_ARM.findall(block))
    return prefixes


def check_fastlane_symmetry(target: Path) -> list[Finding]:
    """Advisory: warn on enabler⇄guard fast-lane prefix drift; self-quiet with
    fewer than both surfaces.

    When BOTH the ``auto-merge-enabler.yml`` and a ci.yml claims-only
    ``case "$head_ref"`` guard exist, every prefix the guard CARDS must be a
    prefix the enabler ARMS — a carded prefix the enabler never arms means the
    guard cards a branch the fast lane never touches (the two host surfaces
    disagree on which prefixes are fast-lane seats). Returns one advisory
    ``Finding`` naming the stray prefixes; never exit-affecting.
    """
    enabler = target / _ENABLER_RELPATH
    ci = target / _CI_RELPATH
    if not (enabler.is_file() and ci.is_file()):
        return []  # need both surfaces to compare — a host missing either is silent
    try:
        armed = _enabler_armed_prefixes(enabler.read_text(encoding="utf-8"))
        carded = _guard_carded_prefixes(ci.read_text(encoding="utf-8"))
    except OSError:
        return []  # unreadable → no verdict (fail open)
    if not armed or not carded:
        return []  # not the planted shape (no arming / no guard block) — decline to guess
    stray = carded - armed
    if not stray:
        return []
    return [
        Finding(
            _CI_RELPATH,
            "fastlane-symmetry",
            f"the claims-only fast-lane guard cards {sorted(stray)}, but the "
            "auto-merge-enabler does not arm those prefixes — the guard cards a "
            "branch the fast lane never touches (enabler⇄guard prefix drift). "
            'Arm the prefix in auto-merge-enabler.yml or drop the ci.yml `case '
            '"$head_ref"` arm so the two surfaces agree.',
        )
    ]
