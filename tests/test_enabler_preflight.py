"""Tests for the enabler INSTALL-time preflight (enabler-install-preflight,
online half — the check-time branch half is tests/test_check_automerge_preflight).

Covers the verdict legs (Allow-auto-merge ON/OFF/hidden; zero contexts /
match / name mismatch), every graceful-degradation path (no git checkout, no
origin, non-github origin, offline transport, HTTP errors, malformed JSON —
a preflight that hard-fails installs offline would be worse than none),
origin-URL parsing across remote shapes, the worktree ``.git``-file
indirection, token-header injection, and the adopt-report integration. All
HTTP goes through the injectable ``http_get`` seam — no test touches the
network.
"""

import json
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import AUTOMERGE_ENABLER_RELPATH, adopt
from engine.enabler_preflight import (
    PREFLIGHT_PREFIX,
    _github_slug,
    enabler_install_preflight,
)
from engine.lib.config import Config
from engine.lib.state import JsonStateBackend, default_state

API = "https://api.github.com"
REPO_URL = f"{API}/repos/menno420/example"
RULES_URL = f"{API}/repos/menno420/example/rules/branches/main"


def _repo_with_origin(tmp_path: Path, url: str) -> Path:
    root = tmp_path / "repo"
    (root / ".git").mkdir(parents=True)
    (root / ".git" / "config").write_text(
        "[core]\n\trepositoryformatversion = 0\n"
        f'[remote "origin"]\n\turl = {url}\n'
        "\tfetch = +refs/heads/*:refs/remotes/origin/*\n",
        encoding="utf-8",
    )
    return root


def _github_repo(tmp_path: Path) -> Path:
    return _repo_with_origin(tmp_path, "https://github.com/menno420/example.git")


def _fake_get(responses: dict, calls: list | None = None):
    """Build an http_get returning canned (status, json-bytes) per URL."""

    def get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
        if calls is not None:
            calls.append((url, dict(headers)))
        status, payload = responses[url]
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        return status, body

    return get


def _happy_responses(
    allow: object = True,
    contexts: list[str] | None = None,
    default_branch: str = "main",
) -> dict:
    repo: dict = {"default_branch": default_branch}
    if allow is not None:
        repo["allow_auto_merge"] = allow
    rules = [
        {
            "type": "required_status_checks",
            "parameters": {
                "required_status_checks": [
                    {"context": name}
                    for name in (
                        contexts if contexts is not None else ["substrate-gate"]
                    )
                ],
            },
        },
        {"type": "deletion"},  # non-status rule — must be ignored
    ]
    return {
        REPO_URL: (200, repo),
        f"{API}/repos/menno420/example/rules/branches/{default_branch}": (200, rules),
    }


# ── verdict legs ─────────────────────────────────────────────────────────


def test_happy_path_verifies_both_legs(tmp_path):
    root = _github_repo(tmp_path)
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(_happy_responses()),
        env={},
    )
    assert len(lines) == 2
    assert all(line.startswith(PREFLIGHT_PREFIX) for line in lines)
    assert '"Allow auto-merge" is ON' in lines[0]
    assert "checklist item 2 verified" in lines[1]
    assert "'substrate-gate'" in lines[1]
    assert not any("UNVERIFIED" in line for line in lines)


def test_allow_auto_merge_off_is_loud(tmp_path):
    root = _github_repo(tmp_path)
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(_happy_responses(allow=False)),
        env={},
    )
    assert '"Allow auto-merge" is OFF' in lines[0]
    assert "cannot arm ANY PR" in lines[0]
    assert '"Allow auto-merge" = ON' in lines[0]


def test_hidden_allow_field_reports_unverifiable_never_off(tmp_path):
    # Tokenless / read-only credentials: the API omits merge settings.
    root = _github_repo(tmp_path)
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(_happy_responses(allow=None)),
        env={},
    )
    assert '"Allow auto-merge" UNVERIFIED' in lines[0]
    assert "is OFF" not in lines[0]
    assert "GITHUB_TOKEN" in lines[0]
    # The rules leg still runs — a partial verdict beats none.
    assert "checklist item 2 verified" in lines[1]


def test_zero_required_contexts_flags_inert_install(tmp_path):
    root = _github_repo(tmp_path)
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(_happy_responses(contexts=[])),
        env={},
    )
    assert "ZERO status-check contexts" in lines[1]
    assert "INERT" in lines[1]
    assert "'substrate-gate'" in lines[1]


def test_required_context_name_mismatch_names_the_real_gates(tmp_path):
    root = _github_repo(tmp_path)
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(_happy_responses(contexts=["quality", "kit-quality"])),
        env={},
    )
    assert "'kit-quality', 'quality'" in lines[1]
    assert "not 'substrate-gate'" in lines[1]
    assert 'automerge."required_context"' in lines[1]


def test_rules_url_uses_the_reported_default_branch(tmp_path):
    root = _github_repo(tmp_path)
    calls: list = []
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(_happy_responses(default_branch="master"), calls),
        env={},
    )
    assert calls[1][0].endswith("/rules/branches/master")
    assert "'master'" in lines[1]


# ── graceful degradation (the preflight must never break an install) ─────


def test_no_git_checkout_degrades_without_http(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    calls: list = []
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get({}, calls),
        env={},
    )
    assert len(lines) == 1
    assert "UNVERIFIED" in lines[0]
    assert "checklist" in lines[0]
    assert calls == []


def test_no_origin_remote_degrades_without_http(tmp_path):
    root = tmp_path / "repo"
    (root / ".git").mkdir(parents=True)
    (root / ".git" / "config").write_text("[core]\n\tbare = false\n", encoding="utf-8")
    calls: list = []
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get({}, calls),
        env={},
    )
    assert len(lines) == 1
    assert "no origin remote" in lines[0]
    assert calls == []


def test_non_github_origin_degrades_without_http(tmp_path):
    # The agent-seat shape: a local git proxy remote.
    root = _repo_with_origin(tmp_path, "http://127.0.0.1:41729/git/menno420/example")
    calls: list = []
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get({}, calls),
        env={},
    )
    assert len(lines) == 1
    assert "not a github.com URL" in lines[0]
    assert calls == []


def test_offline_transport_failure_degrades_gracefully(tmp_path):
    root = _github_repo(tmp_path)

    def get(url, headers):
        raise OSError("Name or service not known")

    lines = enabler_install_preflight(
        root, "substrate-gate", http_get=get, env={}
    )
    assert len(lines) == 1
    assert "UNVERIFIED" in lines[0]
    assert "offline" in lines[0]


def test_repo_http_error_degrades_gracefully(tmp_path):
    root = _github_repo(tmp_path)
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get({REPO_URL: (404, {"message": "Not Found"})}),
        env={},
    )
    assert len(lines) == 1
    assert "HTTP 404" in lines[0]


def test_malformed_repo_json_degrades_gracefully(tmp_path):
    root = _github_repo(tmp_path)
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get({REPO_URL: (200, b"<!doctype html>")}),
        env={},
    )
    assert len(lines) == 1
    assert "UNVERIFIED" in lines[0]


def test_rules_leg_failure_keeps_the_allow_verdict(tmp_path):
    root = _github_repo(tmp_path)
    responses = _happy_responses()
    responses[RULES_URL] = (403, {"message": "Forbidden"})
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(responses),
        env={},
    )
    assert '"Allow auto-merge" is ON' in lines[0]
    assert "UNVERIFIED (HTTP 403)" in lines[1]


def test_rules_non_list_json_degrades_that_leg(tmp_path):
    root = _github_repo(tmp_path)
    responses = _happy_responses()
    responses[RULES_URL] = (200, {"unexpected": "shape"})
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(responses),
        env={},
    )
    assert "required status-check contexts on 'main' UNVERIFIED" in lines[1]


# ── origin parsing ───────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/menno420/example.git",
        "https://github.com/menno420/example",
        "ssh://git@github.com/menno420/example.git",
        "git@github.com:menno420/example.git",
        "git@github.com:menno420/example",
    ],
)
def test_github_slug_recognizes_remote_shapes(url):
    assert _github_slug(url) == ("menno420", "example")


@pytest.mark.parametrize(
    "url",
    [
        "https://gitlab.com/menno420/example.git",
        "http://127.0.0.1:41729/git/menno420/example",
        "/home/user/example",
        "git@github.com.evil.example:menno420/example.git",
    ],
)
def test_github_slug_rejects_non_github_remotes(url):
    assert _github_slug(url) is None


def test_worktree_git_file_resolves_the_shared_config(tmp_path):
    # A worktree checkout: .git is a FILE pointing at the shared gitdir.
    shared = tmp_path / "shared" / ".git"
    (shared / "worktrees" / "wt").mkdir(parents=True)
    (shared / "config").write_text(
        '[remote "origin"]\n\turl = https://github.com/menno420/example.git\n',
        encoding="utf-8",
    )
    (shared / "worktrees" / "wt" / "commondir").write_text(
        "../..\n", encoding="utf-8"
    )
    root = tmp_path / "wt"
    root.mkdir()
    (root / ".git").write_text(
        f"gitdir: {shared / 'worktrees' / 'wt'}\n", encoding="utf-8"
    )
    lines = enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(_happy_responses()),
        env={},
    )
    assert '"Allow auto-merge" is ON' in lines[0]


# ── credentials ──────────────────────────────────────────────────────────


def test_token_from_env_rides_the_authorization_header(tmp_path):
    root = _github_repo(tmp_path)
    calls: list = []
    enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(_happy_responses(), calls),
        env={"GITHUB_TOKEN": "tok-123"},
    )
    assert calls[0][1]["Authorization"] == "Bearer tok-123"


def test_no_token_sends_no_authorization_header(tmp_path):
    root = _github_repo(tmp_path)
    calls: list = []
    enabler_install_preflight(
        root,
        "substrate-gate",
        http_get=_fake_get(_happy_responses(), calls),
        env={},
    )
    assert "Authorization" not in calls[0][1]


# ── adopt integration ────────────────────────────────────────────────────


def _make_backend(root: Path, config: Config) -> JsonStateBackend:
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return backend


def test_wire_enforcement_adopt_runs_the_install_preflight(tmp_path):
    # A scratch adopt target has no .git → the preflight degrades to its
    # honest UNVERIFIED line in the adopt report (and never hits the
    # network — the same guarantee that keeps offline installs green).
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    lines = adopt(
        root, config, backend, kit_root=tmp_path / "kit", wire_enforcement=True
    )
    assert (root / AUTOMERGE_ENABLER_RELPATH).is_file()
    preflight = [line for line in lines if line.startswith(PREFLIGHT_PREFIX)]
    assert len(preflight) == 1
    assert "UNVERIFIED" in preflight[0]
    # It rides directly after the repo-settings checklist it deepens.
    checklist_at = next(
        index
        for index, line in enumerate(lines)
        if "repo-settings checklist" in line
    )
    assert lines.index(preflight[0]) > checklist_at


def test_default_adopt_without_enabler_skips_the_preflight(tmp_path):
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert not (root / AUTOMERGE_ENABLER_RELPATH).is_file()
    assert not any(line.startswith(PREFLIGHT_PREFIX) for line in lines)
