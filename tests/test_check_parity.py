"""Local ``check --strict`` ↔ CI substrate-gate parity (ORDER 018).

Two local-green→CI-red round-trips in one night (idea-engine PR #274 — inbox
grammar gate, which only ran with ``--inbox-base``; PR #299 — the CI
``check_ideas`` preflight) proved the local ritual and the CI gate had
diverged into two check lists. These tests pin the convergence:

- **Inbox leg**: a plain local ``cmd_check`` (no ``--inbox-base``) derives
  the merge-base blob of ``control/inbox.md`` from ``origin/main`` and reds
  on the same non-append / grammar violations CI reds on; it self-skips
  (NOTE'd) without git context, silently on a bare non-git tree.
- **Preflight leg**: ``substrate.config.json::preflight_scripts`` is the ONE
  check list — a failing script reds plain local ``check --strict`` exactly
  as it reds the CI gate (whose full lane runs this same code); an absent
  script is a NOTE'd self-skip; a nested run is guard-skipped.

The two deliberate red fixtures
(`test_local_strict_reds_on_non_append_inbox_with_derivable_origin_main`,
`test_local_strict_reds_on_failing_preflight_script`) are the ORDER's
done-when proof: a tree failing either CI leg now fails plain local
``python3 bootstrap.py check --strict`` too.
"""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

pytest.importorskip("engine.cli")

from engine.cli import _PREFLIGHT_NESTED_ENV, cmd_check
from engine.lib.config import Config, save_config

# A minimal but real inbox: header + intro + one well-formed ORDER block
# (mirrors tests/test_check_inbox_append.py).
BASE_INBOX = (
    "# x · inbox\n"
    "> ORDERS to this Project. ONE writer: the manager. Never edit this file.\n"
    "\n"
    "## ORDER 001 · 2026-07-09T12:07Z · status: new\n"
    "priority: P1\n"
    "do: adopt the coordination protocol.\n"
    "why: the bus is live.\n"
    "done-when: status reports acked=001, done=001.\n"
)

ORDER_002 = (
    "\n"
    "## ORDER 002 · 2026-07-09T14:15Z · status: new\n"
    "priority: P2\n"
    "do: ship the visibility band.\n"
    "why: adopters need it.\n"
    "done-when: status reports done=002.\n"
)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _fresh_status(root: Path) -> None:
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _write(
        root,
        "control/status.md",
        f"# x · status\nupdated: {now_iso}\nphase: t\nhealth: green\n"
        "last-shipped: none\nblockers: none\norders: acked= done=\n"
        "⚑ needs-owner: none\nnotes: none\n",
    )


@pytest.fixture()
def git_repo(tmp_path):
    """A git checkout with a committed inbox and a resolvable origin/main.

    ``origin/main`` is a plain remote-tracking ref pointed at HEAD (no real
    remote needed): exactly the state a session's local clone is in after
    the CLAUDE.md preflight (`git fetch origin main`).
    """
    _fresh_status(tmp_path)
    _write(tmp_path, "control/inbox.md", BASE_INBOX)
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "base")
    _git(tmp_path, "update-ref", "refs/remotes/origin/main", "HEAD")
    return tmp_path


# ---------------------------------------------------------------------------
# Inbox leg — merge-base derived locally from origin/main (done-when red #1)
# ---------------------------------------------------------------------------


def test_local_strict_reds_on_non_append_inbox_with_derivable_origin_main(
    git_repo, capsys,
):
    # The PR #274 class, now caught locally: an edit to an existing ORDER
    # line reds plain `check --strict` with NO --inbox-base handed in.
    _write(
        git_repo,
        "control/inbox.md",
        BASE_INBOX.replace("priority: P1", "priority: P0"),
    )
    assert cmd_check(git_repo, strict=True) == 1
    assert "inbox-not-append" in capsys.readouterr().out


def test_local_strict_reds_on_malformed_appended_order(git_repo, capsys):
    # The grammar half of the same leg: a malformed appended block reds
    # locally exactly as CI's --inbox-base lane reds it.
    _write(
        git_repo,
        "control/inbox.md",
        BASE_INBOX + "\n## ORDER 002 broken header\nno fields here\n",
    )
    assert cmd_check(git_repo, strict=True) == 1
    assert "inbox-order-grammar" in capsys.readouterr().out


def test_local_strict_greens_on_pure_append(git_repo, capsys):
    # Control case: a legal pure-append of a well-formed ORDER stays green.
    _write(git_repo, "control/inbox.md", BASE_INBOX + ORDER_002)
    assert cmd_check(git_repo, strict=True) == 0
    out = capsys.readouterr().out
    assert "inbox-not-append" not in out
    assert "inbox-order-grammar" not in out


def test_status_only_lane_also_derives_locally(git_repo, capsys):
    # The conventional preflight wrapper runs `check --strict --status-only`
    # — that invocation must catch the violation too, without --inbox-base.
    _write(
        git_repo,
        "control/inbox.md",
        BASE_INBOX.replace("priority: P1", "priority: P0"),
    )
    assert cmd_check(git_repo, strict=True, status_only=True) == 1
    assert "inbox-not-append" in capsys.readouterr().out


def test_no_git_checkout_self_skips_silently(tmp_path, capsys):
    # A bare non-git tree stays quiet: no derivation, no NOTE, no red —
    # the pre-ORDER-018 fail-open posture for trees with no diff context.
    _fresh_status(tmp_path)
    _write(tmp_path, "control/inbox.md", BASE_INBOX)
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    assert "inbox merge-base leg skipped" not in capsys.readouterr().out


def test_no_origin_main_self_skips_with_note(tmp_path, capsys):
    # Git checkout but no origin/main remote-tracking ref → NOTE'd self-skip,
    # never a red (the ORDER's "self-skip when unavailable").
    _fresh_status(tmp_path)
    _write(tmp_path, "control/inbox.md", BASE_INBOX)
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "base")
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    assert "inbox merge-base leg skipped" in capsys.readouterr().out


def test_explicit_inbox_base_still_wins(git_repo, capsys):
    # CI's path is untouched: an explicit --inbox-base is used verbatim and
    # no derivation runs (the base here differs from origin/main's blob on
    # purpose — the explicit verdict must be the one reported).
    _write(git_repo, "control/inbox.md", BASE_INBOX + ORDER_002)
    base = git_repo / "explicit.base"
    base.write_text(BASE_INBOX + ORDER_002, encoding="utf-8")
    assert (
        cmd_check(git_repo, strict=True, status_only=True, inbox_base=base) == 0
    )


def test_inbox_created_since_base_is_graded_against_empty_base(git_repo, capsys):
    # A file absent at the merge-base grades its WHOLE body (empty base blob
    # — the generated gate's `|| : > basefile` posture): valid content passes.
    _git(git_repo, "rm", "-q", "--cached", "control/inbox.md")
    _git(git_repo, "commit", "-q", "-m", "drop inbox from index")
    _git(git_repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    _write(git_repo, "control/inbox.md", BASE_INBOX)
    assert cmd_check(git_repo, strict=True, status_only=True) == 0
    _write(git_repo, "control/inbox.md", "stray prose, not an ORDER block\n")
    assert cmd_check(git_repo, strict=True, status_only=True) == 1
    assert "inbox-order-grammar" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Preflight-scripts leg — the ONE config-declared check list (done-when red #2)
# ---------------------------------------------------------------------------


def _config_with_scripts(root: Path, scripts: list[str]) -> None:
    save_config(root, Config(preflight_scripts=scripts))


def test_local_strict_reds_on_failing_preflight_script(tmp_path, capsys):
    # The PR #299 class, now caught locally: the repo's own preflight checker
    # (e.g. scripts/check_ideas.py behind the conventional wrapper) failing
    # reds plain `check --strict` — the same leg CI's full lane runs.
    _fresh_status(tmp_path)
    _write(
        tmp_path,
        "scripts/fail.py",
        "import sys\nprint('idea grammar violation: bad frontmatter')\n"
        "sys.exit(1)\n",
    )
    _config_with_scripts(tmp_path, ["scripts/fail.py"])
    assert cmd_check(tmp_path, strict=True) == 1
    out = capsys.readouterr().out
    assert "preflight-script" in out
    assert "idea grammar violation" in out


def test_passing_preflight_script_stays_green(tmp_path, capsys):
    _fresh_status(tmp_path)
    _write(tmp_path, "scripts/ok.py", "print('all green')\n")
    _config_with_scripts(tmp_path, ["scripts/ok.py"])
    assert cmd_check(tmp_path, strict=True) == 0
    assert "preflight-script" not in capsys.readouterr().out


def test_absent_preflight_script_self_skips_with_note(tmp_path, capsys):
    # The default entry names a conventional path many adopters won't have:
    # absence is a NOTE'd self-skip, never a red.
    _fresh_status(tmp_path)
    _config_with_scripts(tmp_path, ["scripts/preflight.py"])
    assert cmd_check(tmp_path, strict=True) == 0
    assert "preflight script scripts/preflight.py not found" in (
        capsys.readouterr().out
    )


def test_preflight_scripts_skip_on_status_only_lane(tmp_path, capsys):
    # Control fast lane stays scoped: no preflight scripts run under
    # --status-only (also what makes the conventional wrapper's own
    # `check --strict --status-only` child non-recursive by construction).
    _fresh_status(tmp_path)
    _write(tmp_path, "scripts/fail.py", "import sys\nsys.exit(1)\n")
    _config_with_scripts(tmp_path, ["scripts/fail.py"])
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    assert "preflight-script" not in capsys.readouterr().out


def test_nested_run_guard_skips_preflight_scripts(tmp_path, capsys, monkeypatch):
    # A preflight wrapper that itself invokes `bootstrap.py check --strict`
    # must not recurse: the child env carries the guard and skips the leg.
    _fresh_status(tmp_path)
    _write(tmp_path, "scripts/fail.py", "import sys\nsys.exit(1)\n")
    _config_with_scripts(tmp_path, ["scripts/fail.py"])
    monkeypatch.setenv(_PREFLIGHT_NESTED_ENV, "1")
    assert cmd_check(tmp_path, strict=True) == 0
    assert "nested check run" in capsys.readouterr().out


def test_preflight_entries_support_arguments(tmp_path, capsys):
    # An entry is a shlex-split command line, so `script.py --flag` works —
    # the check_ideas `--outbox` shape from the ORDER.
    _fresh_status(tmp_path)
    _write(
        tmp_path,
        "scripts/mode.py",
        "import sys\nsys.exit(0 if '--outbox' in sys.argv else 3)\n",
    )
    _config_with_scripts(tmp_path, ["scripts/mode.py --outbox"])
    assert cmd_check(tmp_path, strict=True) == 0
    _config_with_scripts(tmp_path, ["scripts/mode.py"])
    assert cmd_check(tmp_path, strict=True) == 1
    assert "exit 3" in capsys.readouterr().out


def test_default_config_names_the_conventional_wrapper():
    # The done-when hinges on parity arriving on upgrade with no config
    # edit: the default preflight list names the conventional wrapper path.
    assert Config().preflight_scripts == ["scripts/preflight.py"]
