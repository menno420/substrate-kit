"""Fast-lane branch-prefix symmetry — runtime advisory (groom R8 + S11).

Promotes the enabler⇄guard half of the B-3 kit-only meta-test
(``tests/test_fastlane_prefix_symmetry.py``) to a runtime advisory every
ADOPTER runs under ``bootstrap check``, so a host catches its OWN
``auto-merge-enabler.yml`` ⇄ claims-only-guard prefix drift — not just
substrate-kit's own CI. The set of head-branch prefixes that ride the
auto-merge fast lane lives on two host workflow surfaces (the enabler ARMS
them; the ci.yml claims-only guard CARDS them), and nothing kept an adopter's
copies in agreement.

TWO DIRECTIONS
--------------
* **Forward (R8) — ``carded − armed``:** a prefix the guard CARDS but the
  enabler never ARMS is a guard that cards a branch the fast lane never
  touches. Benign but stale — surfaced as a "make the two surfaces agree"
  nudge.
* **Reverse (S11) — ``armed − carded − declared_cardless``:** a prefix the
  enabler ARMS (so it rides the fast lane) that the guard never CARDS merges
  **card-less** — the dangerous #451-race direction. The catch: a card-less
  rider can be *intentional* (``claim/*`` rides the lane card-free by design)
  or *accidental* (a new seat prefix armed but never carded). The runtime
  advisory can only tell them apart from a host-local ground truth, so ci.yml
  **self-declares** its intentional card-less prefixes in a
  ``# fastlane-cardless: <prefix> …`` comment. The reverse leg then flags only
  an armed prefix that is neither carded NOR self-declared card-less — an
  accidental card-less merge hole. It **self-gates on the declaration's
  presence**: a host that has not (yet) added a ``# fastlane-cardless:`` line
  cannot have its card-less prefixes told apart from holes, so the reverse
  direction stays silent — no version-skew noise.

SCOPE — the enabler⇄guard cross-check only
------------------------------------------
The enabler⇄*config* half is already owned by
``engine.checks.check_automerge_preflight`` (``automerge-branch-drift``), so
this check deliberately does NOT re-flag it — it covers the complementary,
otherwise-uncovered surface: the ci.yml claims-only fast-lane guard. Both legs
are pure host-self cross-checks over the host's OWN two workflow surfaces — no
canonical pivot — so neither can false-wall a host that customized its
fast-lane prefixes. Each leg self-gates on BOTH surface files existing; a host
missing either adds nothing.

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
# ci.yml's self-declaration of intentionally card-less fast-lane prefixes —
# ``# fastlane-cardless: claim/ release/`` (one or more, whitespace/comma
# separated). The host-local ground truth the S11 reverse leg reads.
_CARDLESS_DECL = re.compile(r"#\s*fastlane-cardless:\s*(.+)")
_PREFIX_TOKEN = re.compile(r"[A-Za-z][\w./-]*")


def _enabler_armed_prefixes(text: str) -> set[str]:
    """Prefixes the enabler arms — ``startsWith(github.head_ref, 'X')``."""
    return set(_STARTSWITH.findall(text))


def _guard_carded_prefixes(text: str) -> set[str]:
    """Prefixes the claims-only fast-lane guard cards — the ``<prefix>*)`` arms."""
    prefixes: set[str] = set()
    for block in _CASE_BLOCK.findall(text):
        prefixes.update(_CARDED_ARM.findall(block))
    return prefixes


def _declared_cardless_prefixes(text: str) -> set[str]:
    """Prefixes ci.yml self-declares as intentionally card-less.

    Reads every ``# fastlane-cardless: <prefix> …`` comment and collects the
    prefix tokens it names (whitespace/comma separated). This is the host-local
    ground truth the S11 reverse leg uses to tell an INTENTIONAL card-less
    prefix apart from an ACCIDENTAL card-less merge hole.
    """
    prefixes: set[str] = set()
    for decl in _CARDLESS_DECL.findall(text):
        prefixes.update(_PREFIX_TOKEN.findall(decl))
    return prefixes


def check_fastlane_symmetry(target: Path) -> list[Finding]:
    """Advisory: warn on enabler⇄guard fast-lane prefix drift, both directions;
    self-quiet with fewer than both surfaces.

    When BOTH the ``auto-merge-enabler.yml`` and a ci.yml claims-only
    ``case "$head_ref"`` guard exist:

    * **Forward (R8):** every prefix the guard CARDS must be a prefix the
      enabler ARMS — a carded prefix the enabler never arms means the guard
      cards a branch the fast lane never touches.
    * **Reverse (S11):** an enabler-ARMED prefix that the guard never CARDS
      merges card-less; if ci.yml also does not self-declare it card-less
      (``# fastlane-cardless: <prefix>``), it is an accidental card-less merge
      hole. This leg self-gates on the declaration's presence — a host with no
      ``# fastlane-cardless:`` line stays silent (its card-less prefixes cannot
      be told apart from holes).

    Returns one advisory ``Finding`` per fired leg; never exit-affecting.
    """
    enabler = target / _ENABLER_RELPATH
    ci = target / _CI_RELPATH
    if not (enabler.is_file() and ci.is_file()):
        return []  # need both surfaces to compare — a host missing either is silent
    try:
        armed = _enabler_armed_prefixes(enabler.read_text(encoding="utf-8"))
        ci_text = ci.read_text(encoding="utf-8")
    except OSError:
        return []  # unreadable → no verdict (fail open)
    carded = _guard_carded_prefixes(ci_text)
    if not armed or not carded:
        return []  # not the planted shape (no arming / no guard block) — decline to guess

    findings: list[Finding] = []

    # ── Forward (R8): guard cards a prefix the enabler never arms ─────────────
    forward_stray = carded - armed
    if forward_stray:
        findings.append(
            Finding(
                _CI_RELPATH,
                "fastlane-symmetry",
                f"the claims-only fast-lane guard cards {sorted(forward_stray)}, "
                "but the auto-merge-enabler does not arm those prefixes — the "
                "guard cards a branch the fast lane never touches (enabler⇄guard "
                "prefix drift). Arm the prefix in auto-merge-enabler.yml or drop "
                'the ci.yml `case "$head_ref"` arm so the two surfaces agree.',
            )
        )

    # ── Reverse (S11): armed prefix that is neither carded nor declared ───────
    # card-less rides the fast lane card-LESS. Self-gate on the presence of a
    # ``# fastlane-cardless:`` declaration: without it, an intentional card-less
    # prefix (claim/) can't be told from an accidental hole, so stay silent.
    declared_cardless = _declared_cardless_prefixes(ci_text)
    if declared_cardless:
        reverse_stray = armed - carded - declared_cardless
        if reverse_stray:
            findings.append(
                Finding(
                    _CI_RELPATH,
                    "fastlane-cardless-drift",
                    f"the auto-merge-enabler arms {sorted(reverse_stray)}, so "
                    "those prefixes ride the fast lane, but the claims-only guard "
                    "does not card them and ci.yml's `# fastlane-cardless:` line "
                    "does not declare them card-less — they would auto-merge "
                    "CARD-LESS (an accidental fast-lane merge hole, the #451-race "
                    "direction). Card the prefix in the ci.yml `case \"$head_ref\"` "
                    "guard, or — if it is card-less by design — add it to the "
                    "`# fastlane-cardless:` declaration.",
                )
            )

    return findings
