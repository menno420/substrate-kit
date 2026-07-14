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
    claim_order_ids,
    normalize_order,
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


# ── the --order lane (the #362/#363 cross-branch collision guard) ────────────


def test_render_claim_with_order_appends_the_segment_before_the_date():
    text = render_claim("order-020-d", "sub-items (d)+(e)", order="20", now=_NOW)
    assert text == (
        "- `claude/order-020-d` · **sub-items (d)+(e)** · order 020 · 2026-07-14\n"
    )
    assert claim_order_ids(text) == {"020"}


def test_normalize_order_accepts_the_taught_shapes():
    assert normalize_order("20") == "020"
    assert normalize_order("020") == "020"
    assert normalize_order("ORDER 020") == "020"
    assert normalize_order(" order 7 ") == "007"


@pytest.mark.parametrize("bad", ["", "abc", "1,2", "001-006", "order", "20a"])
def test_normalize_order_refuses_non_single_ids(bad):
    with pytest.raises(ClaimError, match="not a single order id"):
        normalize_order(bad)


def test_claim_order_ids_reads_only_the_bullet_line():
    text = (
        "- `claude/lane-a` · **scope** · order 020 · 2026-07-14\n"
        "\nprose mentioning ORDER 019 below the bullet\n"
    )
    assert claim_order_ids(text) == {"020"}


def test_cli_order_writes_the_segment_and_check_claims_stays_clean(tmp_path):
    root = _control_host(tmp_path)
    rc = main(
        [
            "claim",
            "lane-a",
            "--target",
            str(root),
            "--scope",
            "serve the order",
            "--order",
            "020",
        ]
    )
    assert rc == 0
    text = _claim_path(root, "lane-a").read_text(encoding="utf-8")
    assert "· order 020 ·" in text
    assert check_claims(root) == []


def test_cli_refuses_a_second_branch_claiming_the_same_order(tmp_path, capsys):
    # The verb-side half of the guard: lane-b reaching for ORDER 020 while
    # lane-a's live claim names it is refused with the holder named.
    root = _control_host(tmp_path)
    assert (
        main(
            ["claim", "lane-a", "--target", str(root), "--scope", "first", "--order", "020"]
        )
        == 0
    )
    capsys.readouterr()
    rc = main(
        ["claim", "lane-b", "--target", str(root), "--scope", "second", "--order", "020"]
    )
    assert rc == 2
    out = capsys.readouterr().out
    assert "order 020 already has a live claim on a different branch" in out
    assert "claude-lane-a.md" in out
    assert "--force" in out
    assert not _claim_path(root, "lane-b").exists()


def test_cli_force_overrides_the_order_collision_refusal(tmp_path, capsys):
    root = _control_host(tmp_path)
    assert (
        main(
            ["claim", "lane-a", "--target", str(root), "--scope", "first", "--order", "020"]
        )
        == 0
    )
    capsys.readouterr()
    rc = main(
        [
            "claim",
            "lane-b",
            "--target",
            str(root),
            "--scope",
            "deliberate split",
            "--order",
            "020",
            "--force",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "--force override" in out
    assert _claim_path(root, "lane-b").exists()
    # The checker keeps flagging the (now deliberate) overlap — advisory.
    kinds = [f.kind for f in check_claims(root)]
    assert kinds == ["claims-order-collision", "claims-order-collision"]


def test_cli_distinct_orders_do_not_refuse(tmp_path):
    root = _control_host(tmp_path)
    assert (
        main(
            ["claim", "lane-a", "--target", str(root), "--scope", "first", "--order", "019"]
        )
        == 0
    )
    assert (
        main(
            ["claim", "lane-b", "--target", str(root), "--scope", "second", "--order", "020"]
        )
        == 0
    )
    assert check_claims(root) == []


def test_cli_own_claim_refresh_with_same_order_is_not_a_collision(tmp_path, capsys):
    root = _control_host(tmp_path)
    assert (
        main(
            ["claim", "lane-a", "--target", str(root), "--scope", "v1", "--order", "020"]
        )
        == 0
    )
    rc = main(
        ["claim", "lane-a", "--target", str(root), "--scope", "v2", "--order", "020"]
    )
    assert rc == 0
    assert "refreshed own claim" in capsys.readouterr().out


def test_cli_order_less_write_ignores_order_holders(tmp_path):
    # No --order → no collision scan; an order-carrying sibling never blocks
    # an order-less claim (backward compatibility).
    root = _control_host(tmp_path)
    assert (
        main(
            ["claim", "lane-a", "--target", str(root), "--scope", "first", "--order", "020"]
        )
        == 0
    )
    assert (
        main(["claim", "lane-b", "--target", str(root), "--scope", "unrelated"]) == 0
    )


def test_cli_refuses_a_malformed_order_value(tmp_path, capsys):
    root = _control_host(tmp_path)
    rc = main(
        ["claim", "lane-a", "--target", str(root), "--scope", "s", "--order", "1-3"]
    )
    assert rc == 2
    assert "not a single order id" in capsys.readouterr().out
