"""The OWNER-ACTION ↔ CAPABILITIES cross-reference advisory (queue item 8).

The #68 card's 💡 idea: an ask's ``VERIFIED-NEEDED`` (ORDER 008) and the
capability ledger (ORDER 006) are two halves of one loop — a wall cited by
an owner-ask should be recorded in ``docs/CAPABILITIES.md``, and a ledger
that records the cited surface as verified-WORKING means the ask may rest
on a fallen wall. These tests pin the checker's posture: advisory-only
(never exit-affecting), input-gated on the control/ protocol, coarse
token-overlap matching (fail-open, never a verdict), judgment-shaped asks
out of scope. They cover the two findings — ``owner-ask-wall-unrecorded``
and ``owner-ask-capability-resolved`` — plus the clean and empty paths.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_capability_xref")

from engine.checks.check_capability_xref import (
    CAPABILITIES_RELPATH,
    check_capability_xref,
)
from engine.checks.check_status_current import STATUS_RELPATH
from engine.cli import cmd_check


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _ask(item_id: str, title: str, verified: str) -> str:
    return (
        f"⚑ OWNER-ACTION {item_id} — {title}\n"
        "WHAT: One plain sentence.\n"
        "WHERE: Settings → somewhere\n"
        "HOW: click the button\n"
        "WHY-IT-MATTERS: it matters.\n"
        "UNBLOCKS: the next step.\n"
        f"VERIFIED-NEEDED: {verified}\n"
    )


def _status(asks: str) -> str:
    return (
        "# x · status\nupdated: 2026-07-10T11:00Z\nphase: testing\n"
        "health: green\nlast-shipped: none\nblockers: none\n"
        "orders: acked=001 done=001\n⚑ needs-owner: see below\n\n"
        f"{asks}\n"
        "notes: none\n"
    )


def _ledger(walls: str = "", caps: str = "", log: str = "") -> str:
    return (
        "# x — session capabilities & walls\n\n"
        "## Capabilities — verified working\n\n"
        f"{caps}\n"
        "## Walls — verified blocked (use the workaround; don't rediscover)\n\n"
        f"{walls}\n"
        "## Append log — newest first\n\n"
        f"{log}\n"
    )


# A wall-shaped ask citing the ruleset/api.github.com wall.
RULESET_ASK = _ask(
    "2",
    "required-check swap",
    "no agent path to rulesets exists — direct api.github.com HTTP is "
    "403-blocked through the proxy; Settings → Rules is owner-only UI.",
)
RULESET_WALL = (
    "- **`api.github.com` direct HTTP**: 403-blocked through the proxy —\n"
    "  rulesets are unreachable; GitHub access is MCP-tools-only.\n"
)


# ---------------------------------------------------------------------------
# Input gating + fail-open
# ---------------------------------------------------------------------------


def test_no_control_protocol_no_findings(tmp_path):
    assert check_capability_xref(tmp_path) == []


def test_no_owner_action_blocks_is_clean(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger())
    assert check_capability_xref(tmp_path) == []


def test_unreadable_heartbeat_fails_open(tmp_path):
    (tmp_path / STATUS_RELPATH).mkdir(parents=True)
    assert check_capability_xref(tmp_path) == []


def test_missing_heartbeat_file_is_not_this_checkers_finding(tmp_path):
    # check_status_current owns status-missing; this checker stays silent.
    _write(tmp_path, "control/inbox.md", "# inbox\n")
    assert check_capability_xref(tmp_path) == []


# ---------------------------------------------------------------------------
# Scope — judgment asks and field-less asks are skipped
# ---------------------------------------------------------------------------


def test_judgment_ask_is_out_of_scope(tmp_path):
    # A product/owner-judgment ask never needs a ledger entry — even when
    # its prose contains wall vocabulary ("not a technical wall").
    ask = _ask(
        "8",
        "upgrade decision",
        "the pin is a recorded owner decision — product judgment, "
        "not a technical wall; agents don't overrule a deliberate stance.",
    )
    _write(tmp_path, STATUS_RELPATH, _status(ask))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger())
    assert check_capability_xref(tmp_path) == []


def test_ask_without_wall_markers_is_skipped(tmp_path):
    ask = _ask("5", "confirm MIT", "a license choice is a legal decision.")
    _write(tmp_path, STATUS_RELPATH, _status(ask))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger())
    assert check_capability_xref(tmp_path) == []


def test_ask_without_verified_needed_is_other_checkers_finding(tmp_path):
    # A field-less ask is check_owner_actions' owner-action-fields finding.
    block = "⚑ OWNER-ACTION 1 — do a thing\nWHAT: a thing, 403-blocked.\n"
    _write(tmp_path, STATUS_RELPATH, _status(block))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger())
    assert check_capability_xref(tmp_path) == []


# ---------------------------------------------------------------------------
# The happy path — a cited wall the ledger records is clean
# ---------------------------------------------------------------------------


def test_recorded_wall_is_clean(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(walls=RULESET_WALL))
    assert check_capability_xref(tmp_path) == []


def test_wall_tagged_append_log_entry_also_counts(tmp_path):
    log = (
        "- 2026-07-10 · wall · api.github.com direct HTTP 403-blocked\n"
        "  through the proxy; rulesets unreachable · exact error captured ·\n"
        "  workaround: MCP tools only.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    assert check_capability_xref(tmp_path) == []


# ---------------------------------------------------------------------------
# owner-ask-wall-unrecorded — the ledger doesn't know this wall
# ---------------------------------------------------------------------------


def test_unrecorded_wall_flags(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    # Ledger exists but records a completely different wall.
    _write(
        tmp_path,
        CAPABILITIES_RELPATH,
        _ledger(walls="- **Branch deletion**: refused everywhere.\n"),
    )
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["owner-ask-wall-unrecorded"]
    assert findings[0].path == STATUS_RELPATH
    assert "OWNER-ACTION 2" in findings[0].message
    assert "DISCOVERY RULE" in findings[0].message


def test_missing_ledger_flags_unrecorded(tmp_path):
    # No docs/CAPABILITIES.md at all — the wall is by definition unrecorded.
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["owner-ask-wall-unrecorded"]


# ---------------------------------------------------------------------------
# owner-ask-capability-resolved — only the working side matches
# ---------------------------------------------------------------------------


def test_capability_only_match_flags_resolved(tmp_path):
    caps = (
        "- **rulesets via api.github.com**: reachable again since the proxy\n"
        "  allowlist change — 403-blocked no longer; verified 2026-07-10.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(
        tmp_path,
        CAPABILITIES_RELPATH,
        _ledger(caps=caps, walls="- **Branch deletion**: refused everywhere.\n"),
    )
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["owner-ask-capability-resolved"]
    assert "OWNER-ACTION 2" in findings[0].message
    assert "wall may have fallen" in findings[0].message


def test_wall_side_match_wins_over_capability_side(tmp_path):
    # Recorded as a wall AND echoed on the working side (e.g. a recipe
    # around it) → the wall is recorded; no finding.
    caps = "- **rulesets workaround**: api.github.com data via MCP mirror.\n"
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(walls=RULESET_WALL, caps=caps))
    assert check_capability_xref(tmp_path) == []


# ---------------------------------------------------------------------------
# cmd_check integration — advisory NEVER touches the exit code
# ---------------------------------------------------------------------------


def test_cmd_check_strict_stays_green_on_unrecorded_wall(tmp_path, capsys):
    # No ledger file at all (the by-definition-unrecorded case) — strict
    # stays green because the cross-reference is advisory by contract.
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "owner-ask-wall-unrecorded" in out
    assert "never exit-affecting" in out


def test_cmd_check_status_only_lane_also_warns(tmp_path, capsys):
    # The asks live in the heartbeat files the control fast lane validates,
    # so the nag rides both lanes.
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    assert "owner-ask-wall-unrecorded" in capsys.readouterr().out


def test_cmd_check_quiet_when_xref_clean(tmp_path, capsys):
    # --status-only keeps the run scoped to the control-lane checkers (the
    # planted ledger fixture is deliberately minimal, not a full docs tree).
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(walls=RULESET_WALL))
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    out = capsys.readouterr().out
    assert "owner-ask-wall-unrecorded" not in out
    assert "owner-ask-capability-resolved" not in out
