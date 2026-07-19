"""The folded-gate diff-aware advisory (needs-planning §2 / folded-gate idea).

A host that hand-FOLDED the session gate into its own CI can freeze at the
pre-#19 newest-by-mtime card picker, misgrading a sibling's `complete` card in
a flat-mtime CI checkout. This checker surfaces that at the kit's own `check`
layer — the only kit surface that runs in adopter repos. It is advisory-only
(warn, never exit-affecting), so it returns a single ``list[Finding]`` with no
gate tier.

The substring-trap guard is the load-bearing test: ``--require-session-log``
contains ``session-log``, so a naive ``"session-log" in text`` matcher would
read the locked-door flag as diff-aware and the advisory would NEVER fire. The
clean-fixture tests below pin that the diff-aware form stays silent.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_folded_gate")

from engine.checks.check_folded_gate import (
    FINDING_KIND,
    REMEDIATION_SNIPPET,
    check_folded_gate,
)

# A folded gate that froze at the pre-#19 mtime picker: it invokes the
# locked-door gate but passes no diff-aware selection flag.
_FOLDED_GATE = """\
name: CI
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: session gate
        run: python3 bootstrap.py check --strict --require-session-log
"""

# The diff-aware form (kit PR #19 / the planted substrate-gate): passes
# --session-log, so it must stay silent. This is the substring-trap guard —
# the text still contains "--require-session-log".
_DIFF_AWARE_GATE = """\
name: CI
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: session gate
        run: |
          cards="$(git diff --name-only "$range" -- '.sessions/*.md')"
          if [ -z "$cards" ]; then
            python3 bootstrap.py check --strict --require-session-log
          else
            python3 bootstrap.py check --strict --require-session-log --session-log "$card"
          fi
"""

# The added-card diff-aware variant — also silent.
_ADDED_CARD_GATE = """\
name: CI
on: [pull_request]
jobs:
  gate:
    steps:
      - run: python3 bootstrap.py check --strict --session-log "$card" --added-card "$card"
"""

# A workflow that never invokes the session gate at all.
_NO_GATE = """\
name: lint
on: [push]
jobs:
  lint:
    steps:
      - run: python3 -m pytest -q
"""


def _write_workflow(root: Path, name: str, text: str) -> Path:
    wf_dir = root / ".github" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    path = wf_dir / name
    path.write_text(text, encoding="utf-8")
    return path


def test_folded_gate_fires(tmp_path: Path):
    # A workflow folding the gate WITHOUT diff-awareness -> exactly one advisory.
    _write_workflow(tmp_path, "ci.yml", _FOLDED_GATE)
    findings = check_folded_gate(tmp_path)
    assert len(findings) == 1
    finding = findings[0]
    assert finding.kind == FINDING_KIND
    # The message must name the offending file so the session can act on it.
    assert finding.path == ".github/workflows/ci.yml"
    assert "ci.yml" in finding.message


def test_diff_aware_gate_is_silent(tmp_path: Path):
    # The substring trap: --require-session-log contains "session-log", but the
    # diff-aware --session-log flag is present, so the advisory must NOT fire.
    _write_workflow(tmp_path, "ci.yml", _DIFF_AWARE_GATE)
    assert check_folded_gate(tmp_path) == []


def test_added_card_gate_is_silent(tmp_path: Path):
    # --added-card is also a diff-aware selection flag -> silent.
    _write_workflow(tmp_path, "gate.yml", _ADDED_CARD_GATE)
    assert check_folded_gate(tmp_path) == []


def test_non_gate_workflow_is_silent(tmp_path: Path):
    # A workflow that never grades sessions is not our concern.
    _write_workflow(tmp_path, "lint.yml", _NO_GATE)
    assert check_folded_gate(tmp_path) == []


def test_absent_workflows_dir_fails_open(tmp_path: Path):
    # No .github/workflows/ dir (e.g. a docs-only repo) -> [] , no exception.
    assert check_folded_gate(tmp_path) == []


def test_yaml_extension_is_scanned(tmp_path: Path):
    # Both *.yml and *.yaml are scanned.
    _write_workflow(tmp_path, "ci.yaml", _FOLDED_GATE)
    findings = check_folded_gate(tmp_path)
    assert len(findings) == 1
    assert findings[0].path == ".github/workflows/ci.yaml"


def test_mixed_workflows_flag_only_the_folded_one(tmp_path: Path):
    # A repo with one folded and one diff-aware workflow flags exactly the folded.
    _write_workflow(tmp_path, "folded.yml", _FOLDED_GATE)
    _write_workflow(tmp_path, "clean.yml", _DIFF_AWARE_GATE)
    _write_workflow(tmp_path, "lint.yml", _NO_GATE)
    findings = check_folded_gate(tmp_path)
    assert len(findings) == 1
    assert findings[0].path == ".github/workflows/folded.yml"


def test_folded_gate_emits_paste_ready_remediation(tmp_path: Path):
    # R12: the advisory must carry a paste-ready diff-aware card-derivation
    # block, not just name the fix in prose — a host fixes the fold in one paste.
    _write_workflow(tmp_path, "ci.yml", _FOLDED_GATE)
    message = check_folded_gate(tmp_path)[0].message
    assert REMEDIATION_SNIPPET in message
    # The snippet is a real diff-aware gate: it derives cards from the PR diff
    # and grades THIS PR's own card via --session-log.
    assert "git diff --name-only --diff-filter=d" in message
    assert "--require-session-log --session-log" in message


def test_remediation_snippet_is_itself_diff_aware(tmp_path: Path):
    # The embedded port target must itself be a CORRECT diff-aware gate: if a
    # host pasted it verbatim into a workflow, the checker would stay silent (it
    # is not a folded gate). Guards against shipping a broken snippet.
    _write_workflow(tmp_path, "pasted.yml", REMEDIATION_SNIPPET)
    assert check_folded_gate(tmp_path) == []


def test_not_in_strict_subchecks():
    # This checker is advisory-only and must stay OFF the exit-affecting strict
    # surface (guards.STRICT_SUBCHECKS is pinned to the =7 floor by the parity
    # meta-test). A regression that classified it strict would redden every
    # adopter that legitimately folds its gate.
    guards = pytest.importorskip("engine.guards")
    assert "folded-gate-mtime-picker" not in guards.STRICT_SUBCHECKS
    assert "check_folded_gate" not in guards.STRICT_SUBCHECKS
