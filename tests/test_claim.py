"""The ``bootstrap claim`` verb (the #358 card's 💡 ender).

Pins the mechanical work-claim writer's contract: a verb-written claim
passes ``check_claims`` with ZERO findings — including the post-#353 case
where the scope mentions a dated filename (the claim's own date is the LAST
``YYYY-MM-DD`` on the bullet); ``--delete`` removes the session's own claim;
a FOREIGN claim at the same path (different branch token, or unparseable so
ownership is unprovable) is refused intact by both the delete and the
write-over lane; ``--dry-run`` touches nothing; grammar-breaking inputs
(backticks, newlines, unsafe slugs) are refused with the reason named.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from engine.checks.check_claims import check_claims
from engine.claim import (
    ClaimError,
    branch_for,
    claim_filename,
    owner_token,
    render_claim,
    utc_date,
)
from engine.cli import main
from engine.grammar import WORK_CLAIM_BULLET_RE, WORK_CLAIM_DATE_RE

_NOW = datetime(2026, 7, 14, 3, 30, 45, tzinfo=timezone.utc)


# ── the pure render lane ─────────────────────────────────────────────────────


def test_render_claim_matches_the_taught_grammar():
    text = render_claim(
        "widget-fix",
        "fix the widget",
        area="src/ + tests/",
        now=_NOW,
    )
    assert text == (
        "- `claude/widget-fix` · **fix the widget** · src/ + tests/ · 2026-07-14\n"
    )
    match = WORK_CLAIM_BULLET_RE.search(text)
    assert match is not None
    assert match.group(1) == "claude/widget-fix"


def test_render_claim_area_is_optional():
    text = render_claim("widget-fix", "fix the widget", now=_NOW)
    assert text == "- `claude/widget-fix` · **fix the widget** · 2026-07-14\n"


def test_render_claim_scope_with_dated_filename_keeps_claim_date_last():
    # The #353 case: a dated filename in the scope must not shadow the
    # claim's own date — the verb appends the real date LAST on the bullet.
    text = render_claim(
        "widget-fix",
        "build the idea in 2026-07-01-foo.md",
        now=_NOW,
    )
    dates = WORK_CLAIM_DATE_RE.findall(text)
    assert dates == ["2026-07-01", "2026-07-14"]
    assert dates[-1] == utc_date(_NOW)


def test_render_claim_refuses_backticks_and_newlines_in_scope():
    with pytest.raises(ClaimError, match="backtick"):
        render_claim("s", "scope with a `token` inside", now=_NOW)
    with pytest.raises(ClaimError, match="one line"):
        render_claim("s", "two\nlines", now=_NOW)
    with pytest.raises(ClaimError, match="backtick"):
        render_claim("s", "scope", area="`area`", now=_NOW)


def test_branch_and_filename_derivation_refuse_unsafe_slugs():
    assert branch_for("claim-verb") == "claude/claim-verb"
    assert claim_filename("claim-verb") == "claude-claim-verb.md"
    for bad in ("", "a/b", "a b", "a`b", "-lead", "../x"):
        with pytest.raises(ClaimError, match="filename-safe"):
            branch_for(bad)


def test_owner_token_reads_the_bullet_and_none_on_unparseable():
    assert owner_token("- `claude/x` · **s** · 2026-07-14\n") == "claude/x"
    assert owner_token("no bullet here\n") is None


def test_utc_date_is_computed_at_call_time():
    assert utc_date(_NOW) == "2026-07-14"
    # A no-arg call renders TODAY's UTC date, never a cached value.
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    assert utc_date() == today


# ── the CLI verb ─────────────────────────────────────────────────────────────


def _control_host(tmp_path: Path) -> Path:
    root = tmp_path / "host"
    (root / "control").mkdir(parents=True)
    (root / "control" / "inbox.md").write_text("# inbox\n", encoding="utf-8")
    return root


def _claim_path(root: Path, slug: str) -> Path:
    return root / "control" / "claims" / f"claude-{slug}.md"


def test_cli_written_claim_passes_check_claims_with_zero_findings(tmp_path, capsys):
    root = _control_host(tmp_path)
    rc = main(
        [
            "claim",
            "widget-fix",
            "--target",
            str(root),
            "--scope",
            "build the idea in 2026-07-01-foo.md",  # the #353 round-trip case
            "--area",
            "src/ + tests/",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "claim: wrote control/claims/claude-widget-fix.md" in out
    text = _claim_path(root, "widget-fix").read_text(encoding="utf-8")
    assert owner_token(text) == "claude/widget-fix"
    findings = check_claims(root, now=_NOW)
    assert findings == []


def test_cli_dry_run_writes_nothing(tmp_path, capsys):
    root = _control_host(tmp_path)
    rc = main(
        ["claim", "widget-fix", "--target", str(root), "--scope", "s", "--dry-run"]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "DRY RUN" in out
    assert "- `claude/widget-fix` · **s** ·" in out
    assert not _claim_path(root, "widget-fix").exists()
    assert not (root / "control" / "claims").exists()


def test_cli_delete_removes_own_claim(tmp_path, capsys):
    root = _control_host(tmp_path)
    assert main(["claim", "widget-fix", "--target", str(root), "--scope", "s"]) == 0
    assert _claim_path(root, "widget-fix").is_file()
    rc = main(["claim", "widget-fix", "--target", str(root), "--delete"])
    assert rc == 0
    assert "claim: deleted control/claims/claude-widget-fix.md" in (
        capsys.readouterr().out
    )
    assert not _claim_path(root, "widget-fix").exists()


def test_cli_delete_dry_run_leaves_the_file(tmp_path, capsys):
    root = _control_host(tmp_path)
    assert main(["claim", "widget-fix", "--target", str(root), "--scope", "s"]) == 0
    rc = main(["claim", "widget-fix", "--target", str(root), "--delete", "--dry-run"])
    assert rc == 0
    assert "DRY RUN" in capsys.readouterr().out
    assert _claim_path(root, "widget-fix").is_file()


def test_cli_delete_refuses_a_foreign_claim_and_leaves_it_intact(tmp_path, capsys):
    root = _control_host(tmp_path)
    path = _claim_path(root, "widget-fix")
    path.parent.mkdir(parents=True)
    foreign = "- `claude/other-branch` · **someone else's lane** · 2026-07-14\n"
    path.write_text(foreign, encoding="utf-8")
    rc = main(["claim", "widget-fix", "--target", str(root), "--delete"])
    assert rc == 2
    out = capsys.readouterr().out
    assert "belongs to `claude/other-branch`" in out
    assert "File left intact" in out
    assert path.read_text(encoding="utf-8") == foreign


def test_cli_write_refuses_to_overwrite_a_foreign_claim(tmp_path, capsys):
    root = _control_host(tmp_path)
    path = _claim_path(root, "widget-fix")
    path.parent.mkdir(parents=True)
    foreign = "- `claude/other-branch` · **someone else's lane** · 2026-07-14\n"
    path.write_text(foreign, encoding="utf-8")
    rc = main(["claim", "widget-fix", "--target", str(root), "--scope", "mine"])
    assert rc == 2
    assert "belongs to `claude/other-branch`" in capsys.readouterr().out
    assert path.read_text(encoding="utf-8") == foreign


def test_cli_refuses_an_unparseable_existing_file_as_foreign(tmp_path, capsys):
    root = _control_host(tmp_path)
    path = _claim_path(root, "widget-fix")
    path.parent.mkdir(parents=True)
    unparseable = "widget-fix — no bullet, no token\n"
    path.write_text(unparseable, encoding="utf-8")
    rc = main(["claim", "widget-fix", "--target", str(root), "--delete"])
    assert rc == 2
    assert "ownership unprovable" in capsys.readouterr().out
    assert path.read_text(encoding="utf-8") == unparseable


def test_cli_overwrites_its_own_claim_as_a_refresh(tmp_path, capsys):
    root = _control_host(tmp_path)
    assert main(["claim", "widget-fix", "--target", str(root), "--scope", "v1"]) == 0
    rc = main(["claim", "widget-fix", "--target", str(root), "--scope", "v2"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "refreshed own claim" in out
    text = _claim_path(root, "widget-fix").read_text(encoding="utf-8")
    assert "**v2**" in text
    assert check_claims(root, now=_NOW) == []


def test_cli_requires_scope_to_write(tmp_path, capsys):
    root = _control_host(tmp_path)
    rc = main(["claim", "widget-fix", "--target", str(root)])
    assert rc == 2
    assert "--scope is required" in capsys.readouterr().out


def test_cli_refuses_outside_a_control_carrying_host(tmp_path, capsys):
    root = tmp_path / "bare"
    root.mkdir()
    rc = main(["claim", "widget-fix", "--target", str(root), "--scope", "s"])
    assert rc == 2
    assert "no control/ bus" in capsys.readouterr().out


def test_cli_delete_of_a_missing_claim_names_it(tmp_path, capsys):
    root = _control_host(tmp_path)
    rc = main(["claim", "widget-fix", "--target", str(root), "--delete"])
    assert rc == 2
    assert "nothing to delete" in capsys.readouterr().out
