"""The ``bootstrap heartbeat`` verb (ORDER 019 item 7).

Pins the idea file's contract (``docs/ideas/heartbeat-verb-2026-07-09.md``)
plus the non-destructive rider from the ORDER 019 worklist: the restamp lane
rewrites ONLY the mechanical heartbeat fields — a realistic seat status.md
(⚑ blocks, ORDER ledger lines, ``claimed-by`` annotations, decorated
``updated:`` line) survives byte-identical outside the touched tokens; the
restamped output always satisfies the enforcer grammar (``UPDATED_LINE_RE``
/ ``KIT_LINE_RE`` — the write → parse round-trip the idea file names);
``--dry-run`` writes nothing; missing/unparseable inputs error with the fix
named, never a silent clobber.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from engine.checks.check_status_current import parse_heartbeat
from engine.cli import main
from engine.grammar import (
    KIT_CHECK_FIELD_RE,
    KIT_ENGAGED_FIELD_RE,
    KIT_LINE_RE,
    KIT_VERSION_TOKEN_RE,
    UPDATED_LINE_RE,
)
from engine.heartbeat import (
    HeartbeatError,
    full_status,
    restamp_status,
    utc_stamp,
)

_NOW = datetime(2026, 7, 14, 3, 30, 45, tzinfo=timezone.utc)
_STAMP = "2026-07-14T03:30:45Z"

# A realistic seat heartbeat — decorated updated: line, plain kit: line,
# shipped ledger, ⚑ OWNER-ACTION block, orders line with a live claim.
_REALISTIC = """\
# Self Improvement seat — heartbeat
updated: 2026-07-13T23:25Z · coordinator session live (v3.6 boot) · phase: ACTIVE

## Routines
- Failsafe: trig_01Example · 0 */2 * * * · bound to live coordinator.

## Shipped 2026-07-13
- #325 adopters.md regen (d916d94) · #344 enabler preflight.

## Parked
- PR #317 — owner ratification park (do-not-automerge). Never arm/close/rebase.

## Registry state
kit: v1.15.0

⚑ OWNER-ACTION
WHAT: flip the example setting to on
WHERE: Settings → Example → the toggle
HOW: one checkbox
RISK: ↩️ reversible — flip the toggle back to undo
WHY-IT-MATTERS: the lane stalls without it
UNBLOCKS: the next slice starts moving the moment it's done
VERIFIED-NEEDED: attempted via the API — 403, owner-only surface

orders: acked=001-018 · done=001-018 · claimed-by: 019 self-improvement 2026-07-13T22:43:51Z
"""

_CONTRACT = """\
# demo · status
updated: 2026-07-13T12:00:00Z
phase: building the widget
health: green
kit: v1.14.0 · check: green · engaged: yes
last-shipped: #12 — the widget
blockers: none
orders: acked=001 done=001
⚑ needs-owner: none
notes: all quiet
"""


# ── restamp_status: the non-destructive preserve-and-restamp lane ────────────


def test_restamp_preserves_everything_but_the_timestamp_token():
    out = restamp_status(_REALISTIC, now=_NOW)
    # Byte-identical outside the one replaced token: reconstructing the
    # input by swapping the stamp back yields the original text exactly.
    assert out == _REALISTIC.replace("2026-07-13T23:25Z", _STAMP)
    # The decorated tail of the updated: line survives byte-for-byte.
    assert f"updated: {_STAMP} · coordinator session live (v3.6 boot) · phase: ACTIVE" in out
    # ⚑ block, ORDER ledger, claimed-by line, parked section all intact.
    for preserved in (
        "⚑ OWNER-ACTION",
        "VERIFIED-NEEDED: attempted via the API — 403, owner-only surface",
        "claimed-by: 019 self-improvement 2026-07-13T22:43:51Z",
        "- PR #317 — owner ratification park (do-not-automerge).",
        "kit: v1.15.0",
    ):
        assert preserved in out


def test_restamped_output_satisfies_the_enforcer_grammar():
    out = restamp_status(_REALISTIC, now=_NOW)
    match = UPDATED_LINE_RE.search(out)
    assert match is not None
    assert match.group(1) == _STAMP
    assert parse_heartbeat(out) == _NOW
    kit = KIT_LINE_RE.search(out)
    assert kit is not None
    assert KIT_VERSION_TOKEN_RE.search(kit.group(0)).group(1) == "1.15.0"


def test_restamp_updates_only_the_named_fields():
    out = restamp_status(
        _CONTRACT,
        now=_NOW,
        fields={"orders": "acked=001-002 done=001-002", "phase": "shipping"},
        kit_version="1.16.0",
    )
    assert "orders: acked=001-002 done=001-002\n" in out
    assert "phase: shipping\n" in out
    # kit: version token swapped, decorations preserved.
    assert "kit: v1.16.0 · check: green · engaged: yes\n" in out
    # Untouched fields byte-identical.
    assert "last-shipped: #12 — the widget\n" in out
    assert "blockers: none\n" in out
    assert "notes: all quiet\n" in out
    assert parse_heartbeat(out) == _NOW


def test_restamp_refuses_an_unparseable_heartbeat():
    seed = "# demo · status\nupdated: (seeded at adopt — overwrite me)\n"
    with pytest.raises(HeartbeatError, match="--full"):
        restamp_status(seed, now=_NOW)


def test_restamp_refuses_a_missing_field_line():
    with pytest.raises(HeartbeatError, match="no `phase:` line"):
        restamp_status(_REALISTIC, now=_NOW, fields={"phase": "x"})


def test_restamp_refuses_kit_version_without_a_kit_line():
    text = "# demo · status\nupdated: 2026-07-13T12:00:00Z\n"
    with pytest.raises(HeartbeatError, match="kit:"):
        restamp_status(text, now=_NOW, kit_version="9.9.9")


# ── full_status: the contract-shape whole-file lane ──────────────────────────


def test_full_status_defaults_honestly_and_parses():
    out = full_status("demo", "1.15.0", phase="first heartbeat", now=_NOW)
    assert out.startswith("# demo · status\n")
    assert f"updated: {_STAMP}\n" in out
    assert "blockers: none\n" in out
    assert "⚑ needs-owner: none\n" in out
    assert "orders: acked= done=\n" in out
    assert parse_heartbeat(out) == _NOW
    kit = KIT_LINE_RE.search(out)
    assert kit is not None
    line = kit.group(0)
    assert KIT_VERSION_TOKEN_RE.search(line).group(1) == "1.15.0"
    assert KIT_CHECK_FIELD_RE.search(line).group(1) == "green"
    assert KIT_ENGAGED_FIELD_RE.search(line).group(1) == "yes"


def test_utc_stamp_round_trips_through_the_parser():
    stamp = utc_stamp()
    assert parse_heartbeat(f"updated: {stamp}\n") is not None


# ── the CLI verb ─────────────────────────────────────────────────────────────


def _control_host(tmp_path: Path, status: str | None = _REALISTIC) -> Path:
    root = tmp_path / "host"
    (root / "control").mkdir(parents=True)
    (root / "control" / "inbox.md").write_text("# inbox\n", encoding="utf-8")
    if status is not None:
        (root / "control" / "status.md").write_text(status, encoding="utf-8")
    return root


def test_cli_restamps_in_place(tmp_path, capsys):
    root = _control_host(tmp_path)
    rc = main(["heartbeat", "--target", str(root)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "heartbeat: wrote control/status.md" in out
    text = (root / "control" / "status.md").read_text(encoding="utf-8")
    stamped = parse_heartbeat(text)
    assert stamped is not None
    # A real now replaced the original stamp.
    assert stamped != parse_heartbeat(_REALISTIC)
    # Preservation holds through the CLI too.
    assert "⚑ OWNER-ACTION" in text
    assert "claimed-by: 019 self-improvement" in text


def test_cli_dry_run_writes_nothing(tmp_path, capsys):
    root = _control_host(tmp_path)
    before = (root / "control" / "status.md").read_text(encoding="utf-8")
    rc = main(["heartbeat", "--target", str(root), "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "DRY RUN" in out
    assert "-updated: 2026-07-13T23:25Z" in out  # a real diff was printed
    assert "+updated: " in out
    assert (root / "control" / "status.md").read_text(encoding="utf-8") == before
    # No temp file left behind either.
    assert not (root / "control" / "status.md.tmp").exists()


def test_cli_refuses_outside_a_control_carrying_host(tmp_path, capsys):
    root = tmp_path / "bare"
    root.mkdir()
    rc = main(["heartbeat", "--target", str(root)])
    assert rc == 2
    assert "no control/ bus" in capsys.readouterr().out


def test_cli_errors_on_a_missing_status_file(tmp_path, capsys):
    root = _control_host(tmp_path, status=None)
    rc = main(["heartbeat", "--target", str(root)])
    assert rc == 2
    assert "not found" in capsys.readouterr().out
    assert not (root / "control" / "status.md").exists()


def test_cli_errors_on_the_adopt_seed_and_names_full(tmp_path, capsys):
    root = _control_host(
        tmp_path,
        status="# demo · status\nupdated: (seeded at adopt — overwrite me)\n",
    )
    rc = main(["heartbeat", "--target", str(root)])
    assert rc == 2
    assert "--full" in capsys.readouterr().out


def test_cli_full_writes_the_contract_shape(tmp_path, capsys):
    root = _control_host(tmp_path, status=None)
    rc = main(
        [
            "heartbeat",
            "--target",
            str(root),
            "--full",
            "--phase",
            "first real heartbeat",
            "--orders",
            "acked=001 done=001",
        ]
    )
    assert rc == 0
    text = (root / "control" / "status.md").read_text(encoding="utf-8")
    assert "phase: first real heartbeat\n" in text
    assert "orders: acked=001 done=001\n" in text
    assert "blockers: none\n" in text
    assert "⚑ needs-owner: none\n" in text
    assert parse_heartbeat(text) is not None


def test_cli_full_requires_phase(tmp_path, capsys):
    root = _control_host(tmp_path, status=None)
    rc = main(["heartbeat", "--target", str(root), "--full"])
    assert rc == 2
    assert "--phase" in capsys.readouterr().out


def test_cli_restamp_rejects_full_only_kit_flags(tmp_path, capsys):
    root = _control_host(tmp_path)
    rc = main(["heartbeat", "--target", str(root), "--kit-check", "green"])
    assert rc == 2
    assert "--full" in capsys.readouterr().out


def test_cli_status_file_flag_targets_a_lane_heartbeat(tmp_path):
    root = _control_host(tmp_path)
    lane = root / "control" / "status-mining.md"
    lane.write_text(_CONTRACT, encoding="utf-8")
    rc = main(
        [
            "heartbeat",
            "--target",
            str(root),
            "--status-file",
            "control/status-mining.md",
        ]
    )
    assert rc == 0
    stamped = parse_heartbeat(lane.read_text(encoding="utf-8"))
    assert stamped is not None
    assert stamped != parse_heartbeat(_CONTRACT)
    # The default heartbeat file was NOT touched.
    text = (root / "control" / "status.md").read_text(encoding="utf-8")
    assert text == _REALISTIC
