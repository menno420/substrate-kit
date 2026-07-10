"""Setup-script contract checker — the enforcer half of EAP §6.5.

Why + provenance: the fleet ran six divergent hand-rolled environment setup
scripts, and a contract-violating one is a *silent session killer* — a script
that exits non-zero at provisioning kills the session before the worker can
even report (two trading-strategy sessions died exactly this way; the
substrate-kit PR #47 casualty is the same class). The fleet-manager archetype
material (``environments/archetypes.md`` + ``templates/setup-universal.sh``)
distilled the survivorship rules into ONE contract for the per-repo
``scripts/env-setup.sh`` hook every archetype shim prefers, and the kit now
plants that hook from ``env-setup.sh.tmpl`` (EAP program review 2026-07-10
§6.5). This module is the **enforcer half of the writer/enforcer pair**: the
planted template must pass this checker byte-for-byte (a test pins the
agreement), and a host's later edits are nudged back onto the contract.

What it flags (ALL **advisory** — a nudge, never a locked door, the same
posture as the claims/owner-action/staleness warnings):

- ``setup-fatal-posture`` — the script arms a fatal shell mode (``set -e`` /
  ``set -o errexit``): any failing step then aborts provisioning and kills
  the session with no signal. The contract is ``set +e`` + per-step guards.
- ``setup-no-exit0`` — the last effective (non-comment, non-blank) line is
  not an unconditional ``exit 0``: the script's own tail status leaks into
  the shim and a benign install hiccup reads as a provisioning failure.
- ``setup-secret-value`` — a secret-named variable (``*TOKEN*`` / ``*KEY*``
  / ``*SECRET*`` / ``*PASSWORD*`` …) is assigned a literal value. Names and
  placeholders are fine (referencing ``"$GITHUB_TOKEN"`` or documenting
  ``FOO_TOKEN=<SET-IN-CLAUDE-AI>``); a real value in a committed file is
  the one hard "never" the environment registry carries.

Posture is **advisory-only, never exit-affecting**: the script is host-owned
after planting, contract drift migrates by nag (the §6.4 compat guarantee —
no adopter's existing hand-rolled script can red a required check on
upgrade). Input-gated on the script existing — the plant itself is adopt's
job, so a repo without the hook gets no missing-file nag here. The path is
the fleet contract's fixed location (:data:`SETUP_SCRIPT_RELPATH` — the
archetype shims hardcode it, so it is deliberately house-style constant, not
config; a diverging host forks the constant, D-7). Pure stdlib, no
``subprocess`` (§3.2); unreadable files fail open (no verdict).
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding

# The fleet contract's fixed location: every archetype setup shim runs
# `bash scripts/env-setup.sh` when it exists (fleet-manager
# environments/templates/setup-universal.sh). House-style constant on
# purpose (D-7): the shims hardcode this path, so a config knob here could
# only produce a hook the shims never call.
SETUP_SCRIPT_RELPATH = "scripts/env-setup.sh"

# Variable-name fragments that read as credentials. Deliberately coarse —
# the finding is advisory and a committed secret is worth a false nag.
_SECRET_NAME_RE = re.compile(
    r"(TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|PRIVATE_?KEY|ACCESS_?KEY|CREDENTIAL)",
    re.IGNORECASE,
)

# `NAME=value` / `export NAME=value` at line start (shell assignment shape).
_ASSIGN_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$")

# `set -e` posture: a `set` line whose short-option token carries `e`
# (`-e`, `-eu`, `-euo`), or the long form `set -o errexit`.
_SET_LINE_RE = re.compile(r"^\s*set\s+(.+)$")


def _effective_lines(text: str) -> list[str]:
    """Return the script's non-blank, non-comment lines, stripped."""
    lines: list[str] = []
    for raw in text.split("\n"):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(stripped)
    return lines


def _arms_fatal_posture(line: str) -> bool:
    """True when ``line`` is a ``set`` command arming errexit."""
    match = _SET_LINE_RE.match(line)
    if match is None:
        return False
    tokens = match.group(1).split()
    if "-o" in tokens and "errexit" in tokens:
        return True
    return any(
        token.startswith("-") and not token.startswith("--") and "e" in token[1:]
        for token in tokens
        if token not in {"-o"}
    )


def _is_secret_literal(value: str) -> bool:
    """True when an assignment's right-hand side looks like a real value.

    Fine (not flagged): empty, a ``$``-reference (``"$GITHUB_TOKEN"``), a
    ``<PLACEHOLDER>``, or a pure option-ish token starting with ``-``.
    """
    stripped = value.strip().strip("\"'").strip()
    if not stripped:
        return False
    if stripped.startswith(("$", "<", "-")):
        return False
    return True


def check_setup_script(target: Path) -> list[Finding]:
    """Return advisory findings for ``scripts/env-setup.sh`` contract drift.

    Engages only when the script exists (adopt plants it; absence is not a
    finding). Advisory by contract — callers must never count these toward
    an exit code. Fail-open on unreadable files.
    """
    path = target / SETUP_SCRIPT_RELPATH
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []  # fail open — an unreadable file is not a verdict
    findings: list[Finding] = []
    effective = _effective_lines(text)

    for line in effective:
        if _arms_fatal_posture(line):
            findings.append(
                Finding(
                    SETUP_SCRIPT_RELPATH,
                    "setup-fatal-posture",
                    f"`{line}` arms fatal shell posture — a failing step "
                    "then kills the session at provisioning with no signal "
                    "(the two-dead-sessions class). The contract is `set "
                    "+e` with every install step guarded (env-setup.sh "
                    "header, EAP §6.5).",
                ),
            )

    if not effective or not re.fullmatch(r"exit\s+0", effective[-1]):
        findings.append(
            Finding(
                SETUP_SCRIPT_RELPATH,
                "setup-no-exit0",
                "the last effective line is not an unconditional `exit 0` — "
                "the script's tail status leaks to the environment shim and "
                "a benign hiccup reads as a provisioning failure. End the "
                "script with `exit 0` (contract rule 1, EAP §6.5).",
            ),
        )

    for line in effective:
        assign = _ASSIGN_RE.match(line)
        if assign is None:
            continue
        name, value = assign.group(1), assign.group(2)
        if _SECRET_NAME_RE.search(name) and _is_secret_literal(value):
            findings.append(
                Finding(
                    SETUP_SCRIPT_RELPATH,
                    "setup-secret-value",
                    f"`{name}=…` assigns a literal to a secret-named "
                    "variable — committed setup scripts carry NAMES and "
                    "placeholders only; real values live in the "
                    "environment panel (contract rule 2, EAP §6.5). "
                    "Reference the variable (`\"$NAME\"`) or use a "
                    "`<PLACEHOLDER>`.",
                ),
            )
    return findings
