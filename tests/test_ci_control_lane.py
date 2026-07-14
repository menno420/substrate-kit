"""Pin the kit's own CI control fast lane (band KL-8, ORDER 002).

The heartbeat-lane lesson (2026-07-09): control-only PRs (a status overwrite,
a manager inbox append) must AUTO-MERGE — which means the required
`kit-quality` context must always REPORT. A `paths-ignore` would leave the
required check pending forever and jam the lane, and an unconditioned session
gate would hold a card-less heartbeat PR red. These are textual pins on
`.github/workflows/ci.yml` (stdlib-only — no YAML parser in the test deps),
the same posture as the dist byte-pin: if the workflow regresses, a test
names the law it broke.
"""

from __future__ import annotations

import re
from pathlib import Path

CI_PATH = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"

SKIP_IF = "if: steps.lane.outputs.control_only != 'true'"

# Every heavy step must be lane-conditioned: a control-only diff runs none of
# them (fast + card-less), a normal diff runs all of them.
HEAVY_STEP_NAMES = (
    "Install dev tools",
    "Kit test suite (§3.2 item 1)",
    "Dist byte-equality pin (§3.2 item 2)",
    "Engine lint bans (§3.2 item 3 — no print/assert/subprocess)",
    "Idea index (§5.4 — B4 frontmatter + backlog consistency)",
    "CHANGELOG structure ([Unreleased] keep-a-changelog shape)",
    "Program law (§8.3 — PL register grammar + planted pointers + owner-gate label)",
    "Bench integrity (§5.0 — pin-path label gate + append-only results)",
    "Cold-adoption smoke (§3.2 item 4 — the KL-7 RED→ENGAGED→GREEN arc)",
    "Session gate (§3.2 item 5 — dogfood, the born-red discipline)",
)


def _ci_text() -> str:
    return CI_PATH.read_text(encoding="utf-8")


def test_lane_detect_step_exists_and_fails_safe():
    text = _ci_text()
    assert "id: lane" in text
    assert "grep -v '^control/'" in text
    # Empty/unreadable diffs fail safe onto the full suite (default false).
    assert "control_only=false" in text
    assert 'echo "control_only=$control_only" >> "$GITHUB_OUTPUT"' in text


def test_every_heavy_step_is_lane_conditioned():
    text = _ci_text()
    for name in HEAVY_STEP_NAMES:
        block = text.split(f"- name: {name}", 1)
        assert len(block) == 2, f"step missing: {name}"
        # The condition must appear in the step header (before its run:).
        header = block[1].split("run:", 1)[0]
        assert SKIP_IF in header, f"unconditioned heavy step: {name}"
    # setup-python is conditioned too (the slow toolchain pull).
    assert text.count(SKIP_IF) == len(HEAVY_STEP_NAMES) + 1


def test_short_circuit_reports_green_and_no_paths_ignore():
    text = _ci_text()
    # The job still REPORTS on control-only diffs — the required context can
    # never sit pending (that is the whole point vs paths-ignore).
    assert "if: steps.lane.outputs.control_only == 'true'" in text
    # No live paths-ignore key (the word may appear in warning comments).
    assert "paths-ignore:" not in text
    # And the session gate is among the skipped steps: a heartbeat PR carries
    # no session card and must not be held by the born-red gate.
    gate = text.split("- name: Session gate", 1)[1].split("run:", 1)[0]
    assert SKIP_IF in gate


def test_fast_lane_runs_the_status_scoped_gate():
    # The fleet-adoption-review fix (2026-07-09): a control-only diff edits
    # exactly the files check_status_current validates, so the lane must NOT
    # skip that one checker — a heartbeat-deleting control PR used to ride
    # the lane GREEN while `check --strict` on the same tree exits 1, and the
    # red landed on the NEXT unrelated PR instead. The lane now runs the
    # scoped `check --strict --status-only` gate (stdlib-only, no
    # setup-python, session-log-free — heartbeat PRs still need no card).
    text = _ci_text()
    step = "- name: Control-status gate"
    block = text.split(step, 1)
    assert len(block) == 2, "fast lane misses the status-scoped gate step"
    body = block[1].split("- name:", 1)[0]
    # Runs ON the lane (== 'true'), not skipped by it.
    assert "if: steps.lane.outputs.control_only == 'true'" in body
    assert "check --strict --status-only" in body
    # And stays cheap: plain system python3 against the vendored dist.
    assert "python3 dist/bootstrap.py check --strict --status-only" in body


def test_cold_smoke_walks_the_heartbeat_arc():
    text = _ci_text()
    # The smoke pins the KL-8 leg of the arc: still RED on the seed status,
    # GREEN after the first real heartbeat overwrite.
    assert "expected RED while control/status.md is still the seed" in text
    assert re.search(r"updated: \$\(date -u \+%FT%TZ\)", text)


def test_inbox_append_gate_runs_on_both_lanes_with_a_git_extracted_base():
    # The inbox append-only gate (issue #36 report 2): control/inbox.md is
    # append-only by protocol, but nothing enforced it (PR #34 merged in 19 s).
    # The step must (1) exist, (2) run on BOTH lanes — no lane condition, an
    # inbox edit can ride either — and (3) extract the merge-base blob in bash
    # and hand it in via --inbox-base (the engine never shells out to git).
    text = _ci_text()
    step = "- name: Inbox append-only gate"
    block = text.split(step, 1)
    assert len(block) == 2, "CI misses the inbox append-only gate step"
    body = block[1].split("- name:", 1)[0].split("- uses:", 1)[0]
    # Unconditioned by the lane: the SKIP_IF guard must NOT appear in it.
    assert SKIP_IF not in body
    # git does the diff/extract; the engine only gets a file path.
    assert "git merge-base" in body
    assert "git show" in body
    assert "check --strict --status-only --inbox-base" in body
