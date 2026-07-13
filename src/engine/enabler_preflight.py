"""Auto-merge-enabler INSTALL-time preflight — the online-verifiable half of
the enabler install preflight (docs/ideas/enabler-install-preflight-
2026-07-13.md).

Why + provenance: the enabler installs cleanly into repos where it cannot
function, and the INERT state stays silent until the first parked PR. Three
seats hit it on the 2026-07-12→13 night run
(docs/reports/2026-07-13-night-run-adopter-outcomes.md §a). The check-time
branch-drift half shipped as ``checks/check_automerge_preflight.py`` (kit PR
#321); this module is the remaining half: at adopt/upgrade time — the moment
the live enabler is planted or regenerated — verify the two owner-UI
preconditions the printed repo-settings checklist can only *describe*, and
report what is actually configured:

- ``"Allow auto-merge"`` (repo setting) — OFF means the enabler cannot arm
  ANY PR (the trading-strategy class). Read from ``GET /repos/{owner}/{repo}``
  → ``allow_auto_merge``.
- Required status-check CONTEXTS on the default branch — zero means the
  enabler's refuse-to-arm guard keeps it INERT forever (the superbot-idle /
  gba-homebrew class). Read from ``GET /repos/{owner}/{repo}/rules/branches/
  {branch}`` — deliberately the SAME rules endpoint the enabler's own guard
  counts, so the preflight and the workflow can never disagree on semantics.
  A non-empty set that lacks the configured ``automerge.required_context``
  additionally flags the name mismatch (the websites class — the checklist
  and enabler logs would tell the owner to require a context nothing
  publishes).

The branch-allowlist condition is NOT verified here on purpose: at install
time the workflow is regenerated from ``automerge.branch_patterns``, so
workflow == config by construction; later drift is exactly what the #321
check-time advisory catches. Duplicating it here would double-report every
finding.

Posture is **advisory-only and fail-open** (the idea file's routing note:
"the preflight output may need to route to the owner queue rather than
assert"). The kit installs in varied environments — offline containers,
tokenless CI, non-GitHub remotes — and a preflight that hard-fails installs
offline would be worse than none. Every degradation collapses to one honest
``UNVERIFIED`` report line pointing back at the manual checklist:

- no ``.git`` / no origin remote / origin not a ``github.com`` URL
- no network, DNS failure, timeout (5 s per request)
- HTTP errors (404 on a private repo without a token, 403 rate limit, …)
- tokenless visibility: ``allow_auto_merge`` is only present in the API
  response for credentials with push scope — absence is reported as
  unverifiable, never as OFF
- malformed / unexpected JSON

Pure stdlib (``urllib``, honouring the environment's proxy settings — the
``currency.py`` transport precedent); no ``subprocess`` (§3.2): the origin
remote is read from ``.git/config`` directly (worktree ``.git`` files and
``commondir`` indirection followed best-effort). The HTTP transport is
injectable (``http_get(url, headers) -> (status, body)``) so tests never
touch the network; ``GITHUB_TOKEN`` / ``GH_TOKEN`` are honoured when present.
No ``engine.adopt`` imports (adopt imports *this* module — a reverse import
would cycle); callers pass the configured required-context name in.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Mapping

# One greppable prefix for every line this preflight emits into the adopt
# report (and the report file adopt writes), so a session — or the owner —
# can pull the verdict out of a long adopt/upgrade transcript in one grep.
PREFLIGHT_PREFIX = "enabler preflight:"

_API_ROOT = "https://api.github.com"
_TIMEOUT_SECONDS = 5

# The two github.com remote shapes worth recognizing: URL-style
# (https://github.com/o/r[.git], ssh://git@github.com/o/r[.git]) and
# scp-style (git@github.com:o/r[.git]). Anything else — local paths, proxy
# remotes, other hosts — degrades to UNVERIFIED rather than guessing.
_URL_SLUG_RE = re.compile(
    r"^(?:https?|ssh|git)://(?:[^/@]+@)?github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
)
_SCP_SLUG_RE = re.compile(
    r"^(?:[^@]+@)?github\.com:([^/]+?)/([^/]+?)(?:\.git)?/?$",
)


def _git_config_text(root: Path) -> str | None:
    """Return the repo's git config text, or ``None`` when unreachable.

    Handles the three checkout shapes best-effort: a normal ``.git/``
    directory, a worktree/submodule ``.git`` FILE (``gitdir: <path>``), and
    a worktree gitdir whose ``commondir`` file points at the shared
    ``.git``. Any read failure fails open (``None`` — not a verdict).
    """
    git_path = root / ".git"
    try:
        if git_path.is_dir():
            cfg = git_path / "config"
            return cfg.read_text(encoding="utf-8") if cfg.is_file() else None
        if git_path.is_file():
            match = re.search(
                r"^gitdir:\s*(.+)\s*$",
                git_path.read_text(encoding="utf-8"),
                re.MULTILINE,
            )
            if match is None:
                return None
            gitdir = Path(match.group(1).strip())
            if not gitdir.is_absolute():
                gitdir = (root / gitdir).resolve()
            common = gitdir / "commondir"
            if common.is_file():
                rel = common.read_text(encoding="utf-8").strip()
                base = Path(rel)
                if not base.is_absolute():
                    base = (gitdir / rel).resolve()
            else:
                base = gitdir
            cfg = base / "config"
            return cfg.read_text(encoding="utf-8") if cfg.is_file() else None
    except (OSError, UnicodeDecodeError):
        return None
    return None


def _origin_url(config_text: str) -> str | None:
    """Return the ``[remote "origin"]`` url from git-config text, or None.

    A deliberately small INI walk (git config is ini-shaped): track the
    current section header, take the first ``url =`` under the origin
    remote. No ``git`` subprocess (§3.2).
    """
    in_origin = False
    for raw in config_text.split("\n"):
        line = raw.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("["):
            in_origin = re.match(
                r'^\[remote\s+"origin"\]$',
                line,
            ) is not None
            continue
        if in_origin:
            match = re.match(r"url\s*=\s*(.+)$", line)
            if match is not None:
                return match.group(1).strip()
    return None


def _github_slug(url: str) -> tuple[str, str] | None:
    """Return ``(owner, repo)`` for a github.com remote URL, else ``None``."""
    for pattern in (_URL_SLUG_RE, _SCP_SLUG_RE):
        match = pattern.match(url.strip())
        if match is not None:
            return match.group(1), match.group(2)
    return None


def _preflight_urllib_get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
    """Default HTTP transport: stdlib urllib, short timeout, status+body.

    An HTTP error status is a *result* (returned), not an exception —
    transport-level failures (DNS, refused, timeout) propagate ``OSError``
    for the caller's fail-open handling.
    """
    request = urllib.request.Request(url, headers=headers)  # noqa: S310
    try:
        with urllib.request.urlopen(  # noqa: S310
            request,
            timeout=_TIMEOUT_SECONDS,
        ) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read() if exc.fp is not None else b""
        return exc.code, body


def _fetch_json(
    get: Callable[[str, dict[str, str]], tuple[int, bytes]],
    url: str,
    headers: dict[str, str],
) -> tuple[int | None, object]:
    """Return ``(status, parsed_json)`` — ``(None, None)`` on transport failure.

    ``status`` is ``None`` only when the request never completed (offline /
    DNS / timeout); a completed request with unparseable JSON keeps its
    status and parses to ``None``. Fail-open by contract: this helper never
    raises.
    """
    try:
        status, body = get(url, headers)
    except (OSError, ValueError):
        # OSError covers URLError / timeouts / refused sockets; ValueError
        # covers a malformed URL. Either way: not a verdict.
        return None, None
    try:
        return status, json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return status, None


def _required_contexts(rules: list) -> list[str]:
    """Collect required status-check context names from a rules-API response.

    Mirrors the enabler workflow's own jq
    (``.[] | select(.type == "required_status_checks") |
    .parameters.required_status_checks // [] | .[].context``) so the
    preflight counts exactly what the refuse-to-arm guard will count.
    """
    contexts: list[str] = []
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        if rule.get("type") != "required_status_checks":
            continue
        parameters = rule.get("parameters")
        checks = (
            parameters.get("required_status_checks")
            if isinstance(parameters, dict)
            else None
        )
        for check in checks or []:
            if isinstance(check, dict) and check.get("context"):
                contexts.append(str(check["context"]))
    return contexts


def _unverified(reason: str) -> list[str]:
    """One honest degradation line — the manual checklist is the fallback."""
    return [
        f"{PREFLIGHT_PREFIX} UNVERIFIED ({reason}) — verify the two repo "
        "settings by hand via the repo-settings checklist above.",
    ]


def enabler_install_preflight(
    root: Path,
    required_context: str,
    *,
    http_get: Callable[[str, dict[str, str]], tuple[int, bytes]] | None = None,
    env: Mapping[str, str] | None = None,
) -> list[str]:
    """Return advisory report lines verifying the enabler's repo settings.

    Called by ``adopt`` (and therefore ``upgrade``) whenever the live
    enabler workflow exists — right after the repo-settings checklist, which
    it deepens with what is *actually* configured. Advisory by contract:
    lines only, never an exception, never exit-affecting. ``http_get`` /
    ``env`` are test seams (default: stdlib urllib + ``os.environ``).
    """
    get = http_get if http_get is not None else _preflight_urllib_get
    environ: Mapping[str, str] = os.environ if env is None else env

    config_text = _git_config_text(root)
    if config_text is None:
        return _unverified("no readable git checkout at the target")
    origin = _origin_url(config_text)
    if origin is None:
        return _unverified("no origin remote in .git/config")
    slug = _github_slug(origin)
    if slug is None:
        return _unverified(
            "origin remote is not a github.com URL, so repo settings are "
            "not reachable from here",
        )
    owner, repo = slug

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "substrate-kit-enabler-preflight",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = environ.get("GITHUB_TOKEN") or environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    status, repo_data = _fetch_json(
        get,
        f"{_API_ROOT}/repos/{owner}/{repo}",
        headers,
    )
    if status is None:
        return _unverified(
            f"could not reach the GitHub API for {owner}/{repo} — offline "
            "or blocked network",
        )
    if status != 200 or not isinstance(repo_data, dict):
        return _unverified(
            f"GET /repos/{owner}/{repo} returned HTTP {status} — a private "
            "repo without a token, a rate limit, or a moved repo",
        )

    lines: list[str] = []
    allow = repo_data.get("allow_auto_merge")
    if allow is True:
        lines.append(
            f'{PREFLIGHT_PREFIX} "Allow auto-merge" is ON — checklist '
            "item 1 verified.",
        )
    elif allow is False:
        lines.append(
            f'{PREFLIGHT_PREFIX} "Allow auto-merge" is OFF — the installed '
            "enabler cannot arm ANY PR until the owner flips Settings → "
            'General → Pull Requests → "Allow auto-merge" = ON (checklist '
            "item 1).",
        )
    else:
        # The API only includes the merge-settings fields for credentials
        # with push scope; absence means "cannot see", never "off".
        lines.append(
            f'{PREFLIGHT_PREFIX} "Allow auto-merge" UNVERIFIED — the API '
            "hides merge settings without push-scope credentials (set "
            "GITHUB_TOKEN/GH_TOKEN to verify); checklist item 1 is the "
            "manual path.",
        )

    branch = str(repo_data.get("default_branch") or "main")
    rules_status, rules = _fetch_json(
        get,
        f"{_API_ROOT}/repos/{owner}/{repo}/rules/branches/{branch}",
        headers,
    )
    if rules_status != 200 or not isinstance(rules, list):
        why = (
            "offline or blocked network"
            if rules_status is None
            else f"HTTP {rules_status}"
        )
        lines.append(
            f"{PREFLIGHT_PREFIX} required status-check contexts on "
            f"'{branch}' UNVERIFIED ({why}); checklist item 2 is the "
            "manual path.",
        )
        return lines

    contexts = _required_contexts(rules)
    if not contexts:
        lines.append(
            f"{PREFLIGHT_PREFIX} '{branch}' requires ZERO status-check "
            "contexts — the enabler's refuse-to-arm guard keeps the install "
            "INERT (arming would merge PRs instantly) until the owner makes "
            f"'{required_context}' a required check (checklist item 2).",
        )
    elif required_context in contexts:
        lines.append(
            f"{PREFLIGHT_PREFIX} '{branch}' requires "
            f"{len(contexts)} status-check context(s) including "
            f"'{required_context}' — checklist item 2 verified.",
        )
    else:
        listed = ", ".join(f"'{name}'" for name in sorted(set(contexts)))
        lines.append(
            f"{PREFLIGHT_PREFIX} '{branch}' requires {listed} but not "
            f"'{required_context}' — the enabler still arms (its guard "
            "counts contexts generically), but the config knob names a "
            "context that is not required: set substrate.config.json -> "
            'automerge."required_context" to the real gate so the '
            "checklist + enabler logs name the right check.",
        )
    return lines
