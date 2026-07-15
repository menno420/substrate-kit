"""Fleet kit-currency scanner — tree truth vs self-report, per adopter repo.

Why + provenance: the EAP program review (menno420/superbot
``docs/eap/eap-program-review-2026-07-10.md`` §6 item 3) found that nothing
owns the fleet's kit-version spread: ``docs/adopters.md`` was a hand-written
ledger fed by relayed heartbeats, so a stale or wrong row could sit
indefinitely and a repo's *claim* about its kit version was never checked
against what its tree actually vendors. This module makes the registry a
GENERATED artifact fed by evidence, with two evidence classes kept
deliberately distinct:

- **Tree truth** — what the adopter repo's committed tree actually contains:
  the vendored single-file bootstrap's stamped header (``bootstrap vX.Y.Z``
  on line 1 — the dist the repo *runs*, adopt's plant at ``bootstrap.py``,
  consumer #0's at ``dist/bootstrap.py``) and the ``kit_version`` pin that
  ``adopt``/``upgrade`` record in ``substrate.config.json``.
- **Self-report** — the ``kit: v<X.Y.Z> · check: green|red · engaged:
  yes|no`` heartbeat line each adopter maintains in its own
  ``control/status.md`` (planted by adopt since v1.3.0, inbox ORDER 003).

A self-report alone is a claim; the tree is truth. Where the two disagree
the row is a **DRIFT** row, surfaced loudly in the generated file and in the
run report — never silently resolved to either side.

Execution-home split (the constraint that shapes this module): kit CI cannot
authenticate to sibling repos, so the *fetching* run (``bootstrap
currency``) is agent-side only, while CI validates just the committed
output's format + staleness (``checks/check_adopters_current.py``, no
network). All parse / drift / render logic here is pure and unit-testable:
the network sits behind an injectable fetcher (``fetch(repo, path) -> str |
None``); the default fetcher is stdlib ``urllib`` (honours the
environment's proxy settings), layered so PRIVATE repos read as tree
truth, not as transport failure:

1. ``raw.githubusercontent.com`` — primary; correct for public repos.
2. The authenticated GitHub API contents endpoint (``GITHUB_TOKEN`` /
   ``GH_TOKEN``) — a raw 404 is AMBIGUOUS (absent file, or a private repo
   that 404s every unauthenticated path — the pokemon-mod-lab blindness,
   kit #230), so a 404 only ever becomes ``None`` ("truly absent") once
   the repo itself is proven readable.
3. A ``codeload.github.com`` tarball of the branch — the whole committed
   tree in one stdlib request; membership in it is definitive. This is
   also the transport that works in proxy-mediated agent seats where
   ``api.github.com`` REST is policy-blocked but GitHub credentials are
   injected at the proxy.

A repo readable by NO transport raises ``RepoUnreadableError``; the scan
records the row as *unreadable* — loudly distinct from "not adopted",
which is now always a statement about a tree we actually read.

Read-only by law: the scanner only ever *reads* sibling repos (KF-2 — the
lab never writes to consumers); the one file it writes is this repo's
``docs/adopters.md``.
"""

from __future__ import annotations

import io
import json
import os
import re
import tarfile
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

from engine.adopt import dist_version

# The `kit:` self-report line grammar is kit-owned with ONE home —
# engine.grammar (EAP §6.8): the writer templates and this parser consume
# the same constants, so they cannot drift apart. Shape notes live there.
from engine.grammar import (
    KIT_CHECK_FIELD_RE,
    KIT_ENGAGED_FIELD_RE,
    KIT_LINE_RE,
    KIT_VERSION_TOKEN_RE,
)

ADOPTERS_RELPATH = "docs/adopters.md"
ROSTER_RELPATH = "docs/fleet-repos.txt"
RAW_HOST = "https://raw.githubusercontent.com"
API_HOST = "https://api.github.com"
CODELOAD_HOST = "https://codeload.github.com"
DEFAULT_BRANCH = "main"
FETCH_TIMEOUT_S = 30
# Env vars consulted (in order) for the authenticated API fallback. Optional:
# without a token the API step still serves public repos and the codeload
# step still serves proxy-credentialed agent seats.
TOKEN_ENV_VARS = ("GITHUB_TOKEN", "GH_TOKEN")

# The machine-readable proof that the file is generated output. The CI-side
# format gate keys off this exact string; keep the two in lockstep (the
# checker imports this constant).
GENERATED_MARKER = "GENERATED — do not hand-edit"
REGEN_COMMAND = "python3 dist/bootstrap.py currency"
# The timestamp line the staleness advisory parses back out.
GENERATED_STAMP_PREFIX = "> Generated:"

# Vendored-dist candidates, in trust order: adopt plants ``bootstrap.py`` at
# the repo root; the kit repo itself (consumer #0) keeps ``dist/bootstrap.py``
# (same pair as ``upgrade.find_vendored_bootstrap``).
VENDORED_RELPATHS = ("bootstrap.py", "dist/bootstrap.py")
CONFIG_RELPATH = "substrate.config.json"
DEFAULT_HEARTBEAT = "control/status.md"

_NUMERIC_RE = re.compile(r"\d+")

Fetcher = Callable[[str, str], "str | None"]
# The HTTP seam the layered default fetcher (and its tests) stand on:
# ``(url, headers) -> (status, body_bytes)``. HTTP error statuses come back
# as data; only genuine transport failures (connection refused, DNS) raise.
HttpGet = Callable[[str, "dict[str, str]"], "tuple[int, bytes]"]


class CurrencyFetchError(RuntimeError):
    """Hard transport failure — aborts the run rather than faking evidence."""


class RepoUnreadableError(RuntimeError):
    """One repo is readable by NO transport — its evidence is UNKNOWN.

    Raised per-repo (never aborts the whole scan): ``scan_repo`` catches it
    and records the row as *unreadable*, which renders loudly distinct from
    "not adopted" — a 404 from an unauthenticated transport must never
    masquerade as "there is no tree" (the pokemon-mod-lab blindness,
    kit #230).
    """

    def __init__(self, repo: str, reason: str) -> None:
        self.repo = repo
        self.reason = reason
        super().__init__(f"{repo}: {reason}")


@dataclass
class SelfReport:
    """One heartbeat file's ``kit:`` line, parsed."""

    heartbeat: str
    version: str | None
    check: str | None
    engaged: str | None
    found: bool  # the heartbeat file exists (even if it carries no kit: line)


@dataclass
class RepoCurrency:
    """Everything the scan learned about one repo's kit state."""

    repo: str
    tree_version: str | None = None  # vendored bootstrap header (primary truth)
    tree_source: str | None = None  # which vendored path carried it
    config_pin: str | None = None  # substrate.config.json kit_version
    reports: list[SelfReport] = field(default_factory=list)
    # Transport verdict, not tree evidence: set when no transport could read
    # the repo (RepoUnreadableError reason). An unreadable row must never
    # render "not adopted" — we could not see the tree to say so.
    unreadable: str | None = None

    @property
    def adopted(self) -> bool:
        """Any kit artifact at all? No artifact = not adopted, not an error.

        Only meaningful for a repo the scan could actually read — verdict()
        checks ``unreadable`` first, so transport failure never renders as
        "not adopted".
        """
        return bool(
            self.tree_version
            or self.config_pin
            or any(r.version for r in self.reports),
        )

    @property
    def effective_tree(self) -> str | None:
        """The tree-truth version: vendored dist first, config pin second."""
        return self.tree_version or self.config_pin

    def drifts(self) -> list[str]:
        """Human-readable drift lines (empty = tree and reports agree)."""
        out: list[str] = []
        if (
            self.tree_version
            and self.config_pin
            and self.tree_version != self.config_pin
        ):
            out.append(
                f"tree-internal: vendored dist says v{self.tree_version} but "
                f"substrate.config.json pins v{self.config_pin}",
            )
        for report in self.reports:
            if not report.version or not self.effective_tree:
                continue
            if report.version != self.effective_tree:
                out.append(
                    f"self-report vs tree: {report.heartbeat} claims "
                    f"v{report.version} but the tree says "
                    f"v{self.effective_tree}",
                )
        return out

    def verdict(self, kit_version: str) -> str:
        """One cell: current / stale / DRIFT / pin-only / not adopted /
        unreadable."""
        if self.unreadable and not self.adopted:
            # No transport could read the repo and nothing was seen before
            # the failure: adoption is UNKNOWN, never "not adopted".
            return f"⚠️ unreadable — {self.unreadable}"
        if not self.adopted:
            return "not adopted / unknown"
        parts: list[str] = []
        if self.unreadable:
            # Partial evidence landed before the transport failed.
            parts.append(f"⚠️ partially unreadable — {self.unreadable}")
        if self.drifts():
            parts.append("⚠️ DRIFT")
        tree = self.effective_tree
        if tree is None:
            parts.append("no tree artifact (self-report only)")
        elif _version_key(tree) < _version_key(kit_version):
            parts.append(f"stale (v{tree} < v{kit_version})")
        elif tree == kit_version:
            parts.append("current")
        else:
            parts.append(f"ahead? (v{tree} vs kit v{kit_version})")
        if self.tree_version is None and self.config_pin is not None:
            parts.append("pin-only (no vendored dist found)")
        return " · ".join(parts)


def _version_key(version: str) -> tuple[int, ...]:
    """Sortable key for a semver-ish string (non-numeric parts ignored)."""
    return tuple(int(m) for m in _NUMERIC_RE.findall(version)) or (0,)


def parse_kit_line(text: str) -> tuple[str | None, str | None, str | None]:
    """Parse ``(version, check, engaged)`` from a heartbeat's ``kit:`` line.

    Returns ``(None, None, None)`` when the file carries no ``kit:`` line at
    all. Lenient by design: fields are scanned anywhere on the line, so a
    decorated heartbeat (extra prose between fields) still parses.
    """
    match = KIT_LINE_RE.search(text)
    if match is None:
        return (None, None, None)
    line = match.group(1)
    version = KIT_VERSION_TOKEN_RE.search(line)
    check = KIT_CHECK_FIELD_RE.search(line)
    engaged = KIT_ENGAGED_FIELD_RE.search(line)
    return (
        version.group(1) if version else None,
        check.group(1) if check else None,
        engaged.group(1) if engaged else None,
    )


def parse_roster(text: str) -> list[tuple[str, list[str]]]:
    """Parse the fleet roster: ``owner/repo [extra heartbeat paths...]``.

    One repo per line; ``#`` starts a comment; extra whitespace-separated
    tokens after the repo name are *additional* heartbeat files to read (the
    multi-lane pattern — superbot-games keeps ``control/status-<lane>.md``
    per lane; raw fetches cannot list directories, so lanes are declared
    here as data instead of guessed).
    """
    out: list[tuple[str, list[str]]] = []
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        tokens = line.split()
        out.append((tokens[0], tokens[1:]))
    return out


def _env_token() -> str:
    """The GitHub token for the authenticated API fallback ('' = none)."""
    for var in TOKEN_ENV_VARS:
        value = os.environ.get(var)
        if value:
            return value
    return ""


def _urllib_get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
    """Default ``HttpGet``: HTTP statuses are data, transport failures raise."""
    request = urllib.request.Request(url, headers=headers)  # noqa: S310
    try:
        with urllib.request.urlopen(  # noqa: S310
            request,
            timeout=FETCH_TIMEOUT_S,
        ) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read() or b""


class _TarTree:
    """A branch tarball held in memory — the committed tree, definitively.

    Membership answers the absent-vs-unreadable question with the strongest
    possible evidence: the whole tree is in hand, so a missing path IS a
    missing file, not a transport artifact.
    """

    def __init__(self, data: bytes) -> None:
        self._tar = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
        names = self._tar.getnames()
        # codeload prefixes every member with `<repo>-<ref>/`.
        self._root = names[0].split("/", 1)[0] if names else ""
        self._names = set(names)

    def read(self, path: str) -> str | None:
        """File content at ``path``, or None when absent from the tree."""
        member = f"{self._root}/{path}"
        if member not in self._names:
            return None
        handle = self._tar.extractfile(member)
        if handle is None:  # directory / link — no regular file at this path
            return None
        return handle.read().decode("utf-8", errors="replace")


def default_fetcher(
    host: str = RAW_HOST,
    branch: str = DEFAULT_BRANCH,
    api_host: str = API_HOST,
    codeload_host: str = CODELOAD_HOST,
    token: str | None = None,
    http_get: HttpGet | None = None,
) -> Fetcher:
    """Return the layered fetcher: raw -> authenticated API -> tarball.

    The asymmetry is deliberate: a missing file is evidence ("not adopted"),
    but a network/auth failure must never masquerade as one — a proxy outage
    silently generating a "nobody adopted" registry would be worse than no
    run at all. Layering (per fetched path):

    1. Raw content (unauthenticated). 200 is the answer; a non-404 failure
       still raises (transport outage = abort). A 404 is AMBIGUOUS — absent
       file, or a private repo that 404s every unauthenticated path — and
       falls through.
    2. GitHub API contents endpoint, ``Authorization`` from ``token`` (env
       ``GITHUB_TOKEN``/``GH_TOKEN`` when None; works unauthenticated for
       public repos). Used only once ``GET /repos/<repo>`` has proven the
       repo readable — only then does a contents 404 mean "truly absent".
    3. A ``codeload`` tarball of the branch (cached per repo): the whole
       committed tree in one request; membership in it is definitive. Also
       the transport that survives agent seats whose egress proxy blocks
       ``api.github.com`` REST but injects GitHub credentials.

    A repo no transport can read raises :class:`RepoUnreadableError` — the
    scan records the row as *unreadable*, never as "not adopted".
    """
    get = http_get or _urllib_get
    auth = token if token is not None else _env_token()
    api_headers = {"Accept": "application/vnd.github.raw+json"}
    if auth:
        api_headers["Authorization"] = f"Bearer {auth}"
    # Per-repo resolution cache: "api" | _TarTree | RepoUnreadableError.
    resolved: dict[str, object] = {}

    def _resolve(repo: str, api_status: int) -> object:
        """Prove the repo readable via API or tarball, else mark unreadable."""
        reasons = [
            f"raw 404 on every probe; API contents HTTP {api_status}"
            + ("" if auth else " (unauthenticated — no GITHUB_TOKEN/GH_TOKEN)"),
        ]
        status, _body = get(f"{api_host}/repos/{repo}", api_headers)
        if status == 200:
            return "api"
        reasons.append(f"API repo probe HTTP {status}")
        status, body = get(
            f"{codeload_host}/{repo}/tar.gz/refs/heads/{branch}",
            api_headers,
        )
        if status == 200:
            try:
                return _TarTree(body)
            except (tarfile.TarError, OSError) as exc:
                reasons.append(f"codeload tarball unreadable: {exc}")
        else:
            reasons.append(f"codeload tarball HTTP {status}")
        return RepoUnreadableError(repo, "; ".join(reasons))

    def fetch(repo: str, path: str) -> str | None:
        url = f"{host}/{repo}/{branch}/{path}"
        status, body = get(url, {})
        if status == 200:
            return body.decode("utf-8", errors="replace")
        if status != 404:
            raise CurrencyFetchError(f"GET {url} -> HTTP {status}")
        # Raw 404: ambiguous. A previously-resolved repo answers instantly.
        verdict = resolved.get(repo)
        if isinstance(verdict, _TarTree):
            return verdict.read(path)
        if isinstance(verdict, RepoUnreadableError):
            raise verdict
        # Ask the API; trust its 404 only from a repo proven readable.
        api_url = f"{api_host}/repos/{repo}/contents/{path}?ref={branch}"
        api_status, api_body = get(api_url, api_headers)
        if api_status == 200:
            return api_body.decode("utf-8", errors="replace")
        if verdict is None:
            verdict = _resolve(repo, api_status)
            resolved[repo] = verdict
            if isinstance(verdict, _TarTree):
                return verdict.read(path)
            if isinstance(verdict, RepoUnreadableError):
                raise verdict
        # verdict == "api": the repo is API-readable, so its 404 is truth.
        if api_status == 404:
            return None  # truly absent from a readable repo's tree
        raise CurrencyFetchError(f"GET {api_url} -> HTTP {api_status}")

    return fetch


def scan_repo(
    repo: str,
    fetch: Fetcher,
    extra_heartbeats: list[str] | None = None,
) -> RepoCurrency:
    """Scan one repo's committed tree for kit artifacts + self-reports.

    A :class:`RepoUnreadableError` from the fetcher marks the row
    *unreadable* (keeping any evidence gathered before the failure) instead
    of aborting the fleet scan — one dark repo must not black out the
    registry, and its row must say "unreadable", never "not adopted".
    """
    result = RepoCurrency(repo=repo)
    try:
        _scan_repo_evidence(result, fetch, extra_heartbeats)
    except RepoUnreadableError as exc:
        result.unreadable = exc.reason
    return result


def _scan_repo_evidence(
    result: RepoCurrency,
    fetch: Fetcher,
    extra_heartbeats: list[str] | None,
) -> None:
    """Gather one repo's evidence, mutating ``result`` in place."""
    repo = result.repo
    heartbeats = [DEFAULT_HEARTBEAT]
    config_text = fetch(repo, CONFIG_RELPATH)
    if config_text is not None:
        try:
            config = json.loads(config_text)
        except ValueError:
            config = {}
        pin = config.get("kit_version")
        result.config_pin = str(pin) if pin else None
        declared = config.get("heartbeat_files") or []
        if isinstance(declared, list) and declared:
            heartbeats = [str(h) for h in declared]
    for rel in VENDORED_RELPATHS:
        dist_text = fetch(repo, rel)
        if dist_text is not None:
            result.tree_version = dist_version(dist_text)
            result.tree_source = rel
            break
    for rel in extra_heartbeats or []:
        if rel not in heartbeats:
            heartbeats.append(rel)
    for rel in heartbeats:
        status_text = fetch(repo, rel)
        if status_text is None:
            result.reports.append(SelfReport(rel, None, None, None, found=False))
            continue
        version, check, engaged = parse_kit_line(status_text)
        result.reports.append(SelfReport(rel, version, check, engaged, found=True))


def scan_fleet(
    roster: list[tuple[str, list[str]]],
    fetch: Fetcher,
) -> list[RepoCurrency]:
    """Scan every rostered repo, in roster order."""
    return [scan_repo(repo, fetch, extras) for repo, extras in roster]


def _report_cell(scan: RepoCurrency) -> str:
    """Render the self-report column (per-lane when there are many)."""
    cells: list[str] = []
    for report in scan.reports:
        if not report.found:
            label = "no heartbeat file"
        elif report.version is None:
            label = "no `kit:` line"
        else:
            label = f"v{report.version}"
        if len(scan.reports) > 1:
            lane = report.heartbeat.rsplit("/", 1)[-1]
            label = f"{lane}: {label}"
        cells.append(label)
    return " · ".join(cells) if cells else "—"


def _engaged_cell(scan: RepoCurrency) -> str:
    values = [r.engaged for r in scan.reports if r.engaged]
    if not values:
        return "—"
    return " · ".join(values)


def render_adopters(
    scans: list[RepoCurrency],
    kit_version: str,
    now: datetime | None = None,
) -> str:
    """Render the generated ``docs/adopters.md`` text.

    Keeps the ledger's provenance preamble (ORDER 003, KF-2) and its
    ``living-ledger`` badge; adds the GENERATED marker + timestamp the
    CI-side format gate validates.
    """
    stamp = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: list[str] = [
        "# Fleet adopter registry",
        "",
        "> **Status:** `living-ledger` · **Sole writer: kit-lab** (this repo)",
        ">",
        f"> **{GENERATED_MARKER}** — regenerate with `{REGEN_COMMAND}`",
        "> (agent-side: kit CI cannot auth to sibling repos, so CI validates",
        "> only this file's format + staleness, never refetches).",
        f"{GENERATED_STAMP_PREFIX} {stamp} · kit release: v{kit_version}",
        ">",
        "> Who runs which kit version — the substrate-coordinator's",
        "> visibility surface (inbox ORDER 003; manager research 2026-07-09).",
        "> kit-lab is the fleet's substrate coordinator but has **zero write",
        "> access to adopter repos** (KF-2: the lab never writes to",
        "> consumers); this registry is generated from **read-only evidence**:",
        "> each repo's committed tree (the vendored `bootstrap.py` header —",
        "> the dist the repo *runs* — plus the `substrate.config.json`",
        "> `kit_version` pin) and its own heartbeat self-report (the `kit:",
        "> v<X.Y.Z> · check: green|red · engaged: yes|no` line planted by",
        "> adopt since v1.3.0). A self-report alone is a claim; the tree is",
        "> truth — disagreement is surfaced as a DRIFT row below, never",
        "> silently resolved.",
        "",
        "## Registry",
        "",
        "| repo | tree (vendored dist) | config pin | self-report (`kit:` line)"
        " | engaged | verdict vs kit v" + kit_version + " |",
        "|---|---|---|---|---|---|",
    ]
    for scan in scans:
        tree = (
            f"v{scan.tree_version} ({scan.tree_source})"
            if scan.tree_version
            else "—"
        )
        pin = f"v{scan.config_pin}" if scan.config_pin else "—"
        lines.append(
            f"| {scan.repo} | {tree} | {pin} | {_report_cell(scan)} "
            f"| {_engaged_cell(scan)} | {scan.verdict(kit_version)} |",
        )
    lines += ["", "## Drift report", ""]
    drift_lines = [
        f"- **{scan.repo}** — {drift}" for scan in scans for drift in scan.drifts()
    ]
    if drift_lines:
        lines.append(
            "Tree and self-report disagree below — reconcile at the SOURCE "
            "(the adopter's own heartbeat / pin), never by hand-editing "
            "this file:",
        )
        lines.append("")
        lines += drift_lines
    else:
        lines.append("No drift: every self-report matches its repo's tree.")
    lines += [
        "",
        "## Row protocol",
        "",
        "- **Columns:** `repo` (owner/name) · `tree` (the vendored dist the",
        "  repo *runs*, parsed from its stamped header — primary truth) ·",
        "  `config pin` (`substrate.config.json` `kit_version`, recorded by",
        "  adopt/upgrade — secondary) · `self-report` (the heartbeat `kit:`",
        "  line; per-lane on multi-Project repos) · `engaged` (the KL-7",
        "  post-adopt gate, as self-reported) · `verdict` (vs the kit's",
        "  current release; DRIFT when evidence disagrees).",
        "- **One writer:** only kit-lab sessions regenerate this file (same",
        "  one-writer rule as the `control/` bus). Adopters never write here",
        "  — their channel is their own `control/status.md` `kit:` line.",
        "- **Staleness reads as dark**, not as wrong: the `Generated:` stamp",
        "  above is the evidence date; rerun the scan to refresh.",
        "- **`unreadable` reads as dark too**: no transport (raw content,",
        "  authenticated API, branch tarball) could see that repo's tree",
        "  this run — adoption is UNKNOWN, deliberately never rendered as",
        '  "not adopted" (private-repo 404s are transport, not evidence).',
        "- **Roster:** `docs/fleet-repos.txt` (one `owner/repo` per line;",
        "  extra tokens name per-lane heartbeat files).",
        "- **Releases point back here:** every release's notes carry the",
        "  adopter upgrade checklist (`src/build_release_json.py` appends it",
        "  to `notes.md`), whose last step is updating the adopter's own",
        "  `kit:` status line — the loop that keeps the self-report column",
        "  honest.",
        "",
    ]
    return "\n".join(lines)


def _registry_rows(text: str) -> dict[str, str]:
    """Parse a registry's DATA rows, keyed by the repo cell.

    Works on any text :func:`render_adopters` produced (the committed file
    is generated output, format-gated by ``check_adopters_current``): a data
    row is a ``|``-led table line whose first cell is neither the ``repo``
    header nor a ``---`` separator. Everything outside the table — the
    ``Generated:`` stamp, the drift bullets, the protocol prose — is
    deliberately invisible to this parser: the rows are the evidence; the
    rest is rendering.
    """
    rows: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        first = cells[0]
        if first == "repo" or set(first) <= {"-", ":"}:
            continue  # header / separator, not evidence
        rows[first] = " | ".join(cells)
    return rows


def registry_delta(
    committed: str,
    scans: list[RepoCurrency],
    kit_version: str,
) -> list[str]:
    """Rows-only delta between the committed registry and a fresh scan.

    The ``currency --check`` preflight's core (idea
    ``docs/ideas/currency-check-registry-delta-preflight-2026-07-15.md``):
    render the would-be registry in memory, compare **data rows only**
    against ``committed``, and return the changed rows as ``-``/``+`` lines
    (empty list = a regen would change nothing but the ``Generated:``
    stamp). Two deliberate exclusions:

    - **The timestamp never counts** — the stamp line is outside the table,
      so a stamp-only delta cannot false-positive every run.
    - **Dark never counts** — a repo whose fresh scan hit transport failure
      (``unreadable`` set, fully dark or partial) is excluded from the
      compare in BOTH directions: network darkness is a statement about
      *this run's transport*, not about the fleet, and must never read as
      registry drift (the same not-adopted/unreadable asymmetry the fetcher
      enforces).
    """
    fresh = _registry_rows(render_adopters(scans, kit_version))
    old = _registry_rows(committed)
    dark = {scan.repo for scan in scans if scan.unreadable}
    out: list[str] = []
    for repo, row in fresh.items():
        if repo in dark:
            continue
        if repo not in old:
            out.append(f"+ {row}")
        elif old[repo] != row:
            out.append(f"- {old[repo]}")
            out.append(f"+ {row}")
    for repo, row in old.items():
        if repo not in fresh and repo not in dark:
            out.append(f"- {row}")
    return out


def drift_report_lines(scans: list[RepoCurrency], kit_version: str) -> list[str]:
    """The run report the subcommand prints: spread + drifts + stale rows."""
    out: list[str] = []
    for scan in scans:
        out.append(
            f"{scan.repo}: tree={scan.effective_tree or '—'} "
            f"pin={scan.config_pin or '—'} "
            f"report={_report_cell(scan)} -> {scan.verdict(kit_version)}",
        )
        out.extend(f"  DRIFT: {drift}" for drift in scan.drifts())
    return out
