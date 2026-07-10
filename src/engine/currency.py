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
None``); the default fetcher is stdlib ``urllib`` against
``raw.githubusercontent.com`` (honours the environment's proxy settings).

Read-only by law: the scanner only ever *reads* sibling repos (KF-2 — the
lab never writes to consumers); the one file it writes is this repo's
``docs/adopters.md``.
"""

from __future__ import annotations

import json
import re
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
DEFAULT_BRANCH = "main"
FETCH_TIMEOUT_S = 30

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

    @property
    def adopted(self) -> bool:
        """Any kit artifact at all? No artifact = not adopted, not an error."""
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
        """One cell: current / stale / DRIFT / pin-only / not adopted."""
        if not self.adopted:
            return "not adopted / unknown"
        parts: list[str] = []
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


def default_fetcher(
    host: str = RAW_HOST,
    branch: str = DEFAULT_BRANCH,
) -> Fetcher:
    """Return a raw-content fetcher: 404 -> None, other failures raise.

    The asymmetry is deliberate: a missing file is evidence ("not adopted"),
    but a network/auth failure must never masquerade as one — a proxy outage
    silently generating a "nobody adopted" registry would be worse than no
    run at all.
    """

    def fetch(repo: str, path: str) -> str | None:
        url = f"{host}/{repo}/{branch}/{path}"
        try:
            with urllib.request.urlopen(url, timeout=FETCH_TIMEOUT_S) as resp:  # noqa: S310
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            raise

    return fetch


def scan_repo(
    repo: str,
    fetch: Fetcher,
    extra_heartbeats: list[str] | None = None,
) -> RepoCurrency:
    """Scan one repo's committed tree for kit artifacts + self-reports."""
    result = RepoCurrency(repo=repo)
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
    return result


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
