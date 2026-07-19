#!/usr/bin/env python3
"""measure_grounded_skills — the grounded-skills before/after measurement harness.

Why + provenance: the grounded-skills program wrap report
(``docs/reports/2026-07-12-grounded-skills-wrap.md`` §3d) names the
measurement gap — the program's effect on agent behavior is unmeasured — and
proposes a before/after measurement per the PR #247 methodology
(``docs/reports/2026-07-11-adopter-outcomes-measurement.md``): every number
carries its n and window; honest nulls where the data can't support a claim.
This harness pre-builds that run so the ~2026-07-19..26 window session is
turnkey (heartbeat baton item; pre-registration per #247 §7.1 — metric
definitions frozen BEFORE the window opens). Added 2026-07-15.
Reliability (PL-008): UNVERIFIED — confirm its numbers against ground truth
a few times before trusting them; **delete this if it proves unreliable over
multiple sessions.**

The four §3d metrics (definitions canonical in
``docs/operations/grounded-skills-measurement.md``):

- **M1 skill-grounding rate** — fraction of session cards referencing a
  shipped kit skill (``/name`` token, ``.claude/skills/<name>``, or the
  ``docs/SKILLS.md`` index). Skill names are read live from the engine's
  SKILLS list — one source, no drift copy.
- **M2 owner-ask field compliance** — fraction of field-formatted ``⚑`` ask
  blocks (``⚑``-at-line-start paragraph carrying a ``WHAT:`` label — see
  ``owner_action_blocks``) that carry all six required fields
  (``engine.grammar.OWNER_ACTION_FIELDS``) plus a risk-class token.
- **M3 capability-ledger activity** — dated append-log lines in
  ``docs/CAPABILITIES.md`` (``CAPABILITY_LOG_LINE_RE``), bucketed by their
  own date; venue-token compliance among lines that carry a venue-shaped
  field (old-format lines fail open, per the grammar's doctrine).
- **M4 merge-throughput proxy** — merged/squashed PRs per day on the default
  branch, counted from ``(#N)`` subject suffixes in ``git log``. Open→merge
  latency needs the GitHub API, so it is not in the default (local/git-only)
  path — it is available as the **opt-in ``--api-latency`` mode** (graduated
  from the GSW-4 pass), which reuses ``scripts/measure_pr_latency.py``'s pure
  logic and is cleanly SKIPPED (not errored) when no token is present or the
  network fails.

Read-only everywhere: the harness clones (or reads pre-cloned/local trees)
and never writes to any adopter repo (KF-2).

Usage (the turnkey window run)::

    python3 scripts/measure_grounded_skills.py --clone --workdir /tmp/gsm \
        --json gsm.json --out report-skeleton.md

``--json`` writes the machine-readable results to a (typically ephemeral) path;
``--commit-results PATH`` writes the same payload to a durable, committed-into-repo
path (parent dirs created) so a measure→verify→publish chain's raw ``results.json``
survives an ephemeral-container split — the chain does the ``git add`` step.
``--freeze`` (with either sink) also writes a ``<output>.freeze`` sidecar carrying
the sha256 of the exact output bytes plus a paste-ready reproduce command, so every
window run is self-citing and tamper-evident.

Tests: ``tests/test_measure_grounded_skills.py`` (fixture trees, no network).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT_REL = Path(__file__).resolve().relative_to(_REPO_ROOT)
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import _git_truth  # noqa: E402

from engine.grammar import (  # noqa: E402
    CAPABILITY_LOG_LINE_RE,
    CAPABILITY_VENUE_SHAPE_RE,
    CAPABILITY_VENUE_TOKENS,
    OWNER_ACTION_FIELDS,
    RISK_CLASS_TOKENS,
)

# ── frozen defaults (pre-registered; changing them after 2026-07-15 is a
#    protocol amendment, not a tweak — record it in the protocol doc) ────────

#: v1.15.0 fleet distribution completed 2026-07-12T18:31:47Z (wrap report §1,
#: adopters.md regen header at PR #298). Cards carry day resolution only, so
#: the boundary DAY is excluded from both buckets and reported separately.
DEFAULT_BOUNDARY = date(2026, 7, 12)
#: Before-window start — covers the whole fleet's session-card record (the
#: oldest adopter repo was created 2026-07-07; #247 §1).
DEFAULT_START = date(2026, 7, 1)

_CARD_DATE_RE = re.compile(r"^(20\d{2})-(\d{2})-(\d{2})-.+\.md$")
_MERGE_SUFFIX_RE = re.compile(r"\(#\d+\)\s*$")
_GIT_URL_TMPL = "https://github.com/{repo}.git"


def skill_names() -> tuple[str, ...]:
    """The shipped skill names, read live from the engine's SKILLS list."""
    from engine.skills.skills import SKILLS

    return tuple(s["name"] for s in SKILLS)


# ── roster ───────────────────────────────────────────────────────────────────


def parse_roster(text: str) -> list[str]:
    """``docs/fleet-repos.txt`` → ``owner/repo`` list (extra tokens are
    per-lane heartbeat files, not repos — dropped here)."""
    repos: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        repos.append(line.split()[0])
    return repos


# ── bucketing ────────────────────────────────────────────────────────────────


def card_date(filename: str) -> date | None:
    """Session-card filename date (``YYYY-MM-DD-<slug>.md``), else None."""
    m = _CARD_DATE_RE.match(filename)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def bucket(d: date, *, start: date, boundary: date, end: date) -> str | None:
    """``before`` / ``boundary-day`` / ``after``, or None outside the window."""
    if d < start or d > end:
        return None
    if d < boundary:
        return "before"
    if d == boundary:
        return "boundary-day"
    return "after"


# ── M1 — skill-grounding ─────────────────────────────────────────────────────


def card_references_skill(text: str, names: tuple[str, ...]) -> bool:
    """True when a card references any grounded-skill surface."""
    if "docs/SKILLS.md" in text:
        return True
    for name in names:
        if f"/{name}" in text or f".claude/skills/{name}" in text:
            return True
    return False


# ── M2 — OWNER-ACTION compliance ─────────────────────────────────────────────


#: The WHAT: label (canonical spelling of field 1) — an ask block is only
#: countable when field-formatted; see the detection rule below.
_WHAT_LABEL = OWNER_ACTION_FIELDS[0][0]


def owner_action_blocks(text: str) -> list[str]:
    """Field-formatted ``⚑`` ask blocks.

    Detection rule (frozen; spot-check-verified 2026-07-15 against the kit's
    own corpus): a block is a contiguous paragraph whose FIRST line starts
    with ``⚑`` (line start — the fleet writes both ``⚑ OWNER-ACTION`` and
    named asks like ``⚑ P10 required-check swap``) and which carries a
    ``WHAT:`` field label. Requiring line-start + WHAT: kills the dominant
    noise class — mid-line prose *mentions* ("will mark ⚑ OWNER-ACTION 13
    RESOLVED"), which outnumbered real blocks ~29:0 in the kit's own cards.
    Known limitation (stated in the protocol doc): a fully free-form ask
    with no WHAT: at all is invisible to M2, so M2 measures compliance
    *among field-formatted asks*, not ask-formatting adoption itself.
    """
    blocks: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        stripped = lines[i].lstrip()
        if stripped.startswith("⚑"):
            j = i + 1
            while j < len(lines) and lines[j].strip():
                if lines[j].lstrip().startswith("⚑"):
                    break
                j += 1
            block = "\n".join(lines[i:j])
            if _WHAT_LABEL in block:
                blocks.append(block)
            i = j
        else:
            i += 1
    return blocks


def block_compliant(block: str) -> bool:
    """All six fields (any accepted alternate) present + a risk-class token."""
    for alts in OWNER_ACTION_FIELDS:
        if not any(a in block for a in alts):
            return False
    return any(t in block for t in RISK_CLASS_TOKENS)


# ── M3 — capability-ledger activity ──────────────────────────────────────────


@dataclass
class CapabilityLine:
    day: date
    #: True/False = venue-shaped field 3 judged against the known tokens;
    #: None = old five-field format (fail open — never judged).
    venue_ok: bool | None


def capability_lines(text: str) -> list[CapabilityLine]:
    """Dated append-log lines with their venue verdicts (fail-open rule)."""
    out: list[CapabilityLine] = []
    for raw in text.splitlines():
        m = CAPABILITY_LOG_LINE_RE.match(raw.strip())
        if not m:
            continue
        try:
            day = date.fromisoformat(m.group(1))
        except ValueError:
            continue
        fields = [f.strip() for f in m.group(2).split("·")]
        venue_ok: bool | None = None
        if len(fields) >= 2:
            candidate = fields[1]
            if CAPABILITY_VENUE_SHAPE_RE.match(candidate):
                venue_ok = candidate in CAPABILITY_VENUE_TOKENS
        out.append(CapabilityLine(day=day, venue_ok=venue_ok))
    return out


# ── M4 — merge-throughput proxy ──────────────────────────────────────────────


def _is_shallow(repo_dir: Path) -> bool:
    """True if ``repo_dir`` is a shallow (grafted) clone — its git-log history
    is then truncated and the M4 merge counts unreliable.

    Thin adapter over the shared ``_git_truth.require_full_history`` rule (the
    single home of the shallow -> degrade decision that this harness used to
    re-implement with its own ``rev-parse --is-shallow-repository`` probe). An
    UNKNOWN verdict (git unavailable) is reported as not-shallow, preserving
    this guard's original fail-open-to-proceed behavior.
    """
    verdict = _git_truth.require_full_history(_git_truth.make_runner(repo_dir))
    return verdict.verdict == _git_truth.SHALLOW


def merged_counts(repo_dir: Path, *, start: date, boundary: date, end: date) -> dict | None:
    """Merged/squashed-PR subject counts per bucket from git log, or None
    when the tree is not a usable git repo (reported as an honest null).

    A shallow clone silently truncates history (verified 2026-07-15: the
    session container's kit clone reported 0 before-window merges against a
    real count in the hundreds), so the result carries a ``shallow`` flag
    and the renderer marks such rows unreliable instead of publishing them.
    """
    try:
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(repo_dir),
                "log",
                f"--since={start.isoformat()}T00:00:00",
                f"--until={end.isoformat()}T23:59:59",
                "--date=short",
                "--pretty=%ad %s",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    counts = {"before": 0, "boundary-day": 0, "after": 0}
    for line in proc.stdout.splitlines():
        parts = line.split(" ", 1)
        if len(parts) != 2 or not _MERGE_SUFFIX_RE.search(parts[1]):
            continue
        try:
            d = date.fromisoformat(parts[0])
        except ValueError:
            continue
        b = bucket(d, start=start, boundary=boundary, end=end)
        if b:
            counts[b] += 1
    counts["shallow"] = _is_shallow(repo_dir)
    return counts


# ── per-repo measurement ─────────────────────────────────────────────────────


@dataclass
class RepoResult:
    name: str
    ok: bool = True
    skip_reason: str = ""
    #: bucket → {cards, skill_cards, oa_blocks, oa_compliant}
    cards: dict = field(default_factory=dict)
    #: bucket → {lines, venue_judged, venue_ok}
    capability: dict = field(default_factory=dict)
    #: current-state (undated) OWNER-ACTION blocks in control/status*.md
    status_oa_blocks: int = 0
    status_oa_compliant: int = 0
    merged: dict | None = None


def _empty_card_bucket() -> dict:
    return {"cards": 0, "skill_cards": 0, "oa_blocks": 0, "oa_compliant": 0}


def _empty_cap_bucket() -> dict:
    return {"lines": 0, "venue_judged": 0, "venue_ok": 0}


def measure_repo(
    name: str,
    root: Path,
    *,
    start: date,
    boundary: date,
    end: date,
    names: tuple[str, ...],
) -> RepoResult:
    """All four metrics over one local tree (read-only)."""
    res = RepoResult(name=name)
    for b in ("before", "boundary-day", "after"):
        res.cards[b] = _empty_card_bucket()
        res.capability[b] = _empty_cap_bucket()

    sessions = root / ".sessions"
    if sessions.is_dir():
        for f in sorted(sessions.iterdir()):
            if not f.is_file() or f.suffix != ".md":
                continue
            d = card_date(f.name)
            if d is None:
                continue
            b = bucket(d, start=start, boundary=boundary, end=end)
            if b is None:
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            slot = res.cards[b]
            slot["cards"] += 1
            if card_references_skill(text, names):
                slot["skill_cards"] += 1
            for block in owner_action_blocks(text):
                slot["oa_blocks"] += 1
                if block_compliant(block):
                    slot["oa_compliant"] += 1

    ledger = root / "docs" / "CAPABILITIES.md"
    if ledger.is_file():
        try:
            for line in capability_lines(ledger.read_text(encoding="utf-8")):
                b = bucket(line.day, start=start, boundary=boundary, end=end)
                if b is None:
                    continue
                slot = res.capability[b]
                slot["lines"] += 1
                if line.venue_ok is not None:
                    slot["venue_judged"] += 1
                    if line.venue_ok:
                        slot["venue_ok"] += 1
        except (OSError, UnicodeDecodeError):
            pass

    control = root / "control"
    if control.is_dir():
        for f in sorted(control.glob("status*.md")):
            try:
                text = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for block in owner_action_blocks(text):
                res.status_oa_blocks += 1
                if block_compliant(block):
                    res.status_oa_compliant += 1

    res.merged = merged_counts(root, start=start, boundary=boundary, end=end)
    return res


# ── acquisition ──────────────────────────────────────────────────────────────


def clone_repo(repo: str, workdir: Path) -> tuple[Path | None, str]:
    """Clone ``owner/repo`` (reusing an existing clone); (path, error)."""
    dest = workdir / repo.split("/", 1)[1]
    if (dest / ".git").exists():
        return dest, ""
    try:
        proc = subprocess.run(
            ["git", "clone", "--quiet", _GIT_URL_TMPL.format(repo=repo), str(dest)],
            capture_output=True,
            text=True,
            timeout=600,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, f"clone failed: {exc}"
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout).strip().splitlines()
        return None, f"clone failed: {tail[-1] if tail else 'unknown error'}"
    return dest, ""


# ── rendering ────────────────────────────────────────────────────────────────


def _rate(num: int, den: int) -> str:
    if den == 0:
        return "null (n=0)"
    return f"{num}/{den} ({100.0 * num / den:.0f}%)"


def render_report(
    results: list[RepoResult], *, start: date, boundary: date, end: date
) -> str:
    """Markdown report skeleton — every number carries its n and window."""
    win = (
        f"before = {start} .. {boundary} (exclusive) · boundary-day = {boundary}"
        f" (excluded from both buckets) · after = {boundary} (exclusive) .. {end}"
    )
    lines = [
        "# Grounded-skills measurement — harness output",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"Window: {win}",
        "Method: docs/operations/grounded-skills-measurement.md (pre-registered);",
        "PR #247 precedent. Card dates are filename dates (day resolution).",
        "",
        "## Skipped repos (honest nulls)",
        "",
    ]
    skipped = [r for r in results if not r.ok]
    if skipped:
        for r in skipped:
            lines.append(f"- {r.name} — {r.skip_reason}")
    else:
        lines.append("- none")
    lines += [
        "",
        "## M1 — skill-grounding rate (cards referencing a shipped skill / cards)",
        "",
        "| repo | before | after |",
        "|---|---|---|",
    ]
    for r in results:
        if not r.ok:
            continue
        b, a = r.cards["before"], r.cards["after"]
        lines.append(
            f"| {r.name} | {_rate(b['skill_cards'], b['cards'])} "
            f"| {_rate(a['skill_cards'], a['cards'])} |"
        )
    lines += [
        "",
        "## M2 — OWNER-ACTION six-field + risk-class compliance (dated cards)",
        "",
        "| repo | before | after | status*.md now (undated) |",
        "|---|---|---|---|",
    ]
    for r in results:
        if not r.ok:
            continue
        b, a = r.cards["before"], r.cards["after"]
        lines.append(
            f"| {r.name} | {_rate(b['oa_compliant'], b['oa_blocks'])} "
            f"| {_rate(a['oa_compliant'], a['oa_blocks'])} "
            f"| {_rate(r.status_oa_compliant, r.status_oa_blocks)} |"
        )
    lines += [
        "",
        "## M3 — capability append-log lines (count · venue compliance)",
        "",
        "| repo | before | after |",
        "|---|---|---|",
    ]
    for r in results:
        if not r.ok:
            continue
        b, a = r.capability["before"], r.capability["after"]
        lines.append(
            f"| {r.name} | {b['lines']} · venue {_rate(b['venue_ok'], b['venue_judged'])} "
            f"| {a['lines']} · venue {_rate(a['venue_ok'], a['venue_judged'])} |"
        )
    lines += [
        "",
        "## M4 — merged-PR throughput proxy ((#N) subjects on the default branch)",
        "",
        "| repo | before | boundary-day | after |",
        "|---|---|---|---|",
    ]
    for r in results:
        if not r.ok:
            continue
        if r.merged is None:
            lines.append(f"| {r.name} | null (no git history) | — | — |")
        elif r.merged.get("shallow"):
            lines.append(
                f"| {r.name} | null (shallow clone — history truncated,"
                " re-clone full) | — | — |"
            )
        else:
            m = r.merged
            lines.append(
                f"| {r.name} | {m['before']} | {m['boundary-day']} | {m['after']} |"
            )
    lines += [
        "",
        "## Interpretation guardrails (fill in the run session — not the harness)",
        "",
        "- Expected M1 before ≈ 0: the skills did not exist in adopters before"
        f" {boundary}; the finding of interest is AFTER-window uptake, and a"
        " low after-rate is an honest negative headline, not a reporting"
        " problem.",
        "- Confounds carried from #247 §6 apply (born-with-kit design,"
        " model-mix, fleet-program launch, agent-under-owner-identity).",
        "- PR open→merge latency is NOT in this output — run the optional"
        " GitHub API pass per the protocol doc if latency claims are wanted.",
        "",
    ]
    return "\n".join(lines)


def results_json(
    results: list[RepoResult], *, start: date, boundary: date, end: date
) -> dict:
    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window": {
            "start": start.isoformat(),
            "boundary": boundary.isoformat(),
            "end": end.isoformat(),
        },
        "repos": [
            {
                "name": r.name,
                "ok": r.ok,
                "skip_reason": r.skip_reason,
                "cards": r.cards,
                "capability": r.capability,
                "status_oa_blocks": r.status_oa_blocks,
                "status_oa_compliant": r.status_oa_compliant,
                "merged": r.merged,
            }
            for r in results
        ],
    }


# ── opt-in API-latency mode (graduated from GSW-4) ───────────────────────────


def _load_latency_module():
    """Load ``scripts/measure_pr_latency.py`` as a module (sibling path).

    There is no package under ``scripts/`` — matching the importlib-load
    convention the tests already use — so this loads the standalone latency
    script by path and returns the executed module. Loading it does NOT touch
    the network or import ``requests`` (that stays lazy inside its network
    path), so the harness's default/offline path stays stdlib-only.
    """
    path = Path(__file__).with_name("measure_pr_latency.py")
    spec = importlib.util.spec_from_file_location("measure_pr_latency", path)
    if spec is None or spec.loader is None:  # pragma: no cover — path is fixed
        raise ImportError(f"cannot load latency module from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_api_latency(
    repos: list[str], *, start: date, boundary: date, end: date, verbose: bool = False
) -> dict:
    """Opt-in GitHub-API open→merge latency pass, reusing measure_pr_latency.

    Returns one of:
    - ``{"status": "skipped", "reason": ...}`` — no token (checked WITHOUT
      touching the network) or a network/rate-limit failure (honest null).
    - ``{"status": "ok", "payload": ...}`` — the measure_pr_latency payload.

    Never crashes the harness: a credential-less env or a network failure SKIPS.
    """
    mod = _load_latency_module()

    # Resolve the token WITHOUT touching the network. When absent, return the
    # same message text ``make_session`` would raise — but never open a session.
    if mod._resolve_token() is None:
        reason = (
            "no GitHub token in env (tried " + ", ".join(mod._TOKEN_ENV_VARS) + ")"
        )
        return {"status": "skipped", "reason": reason}

    # Network path — any failure (RuntimeError from make_session, requests
    # errors, unexpected exceptions) becomes an honest SKIP, not a crash.
    try:
        session = mod.make_session()
        repo_results: list[dict] = [
            mod.measure_repo(
                repo, session, start=start, boundary=boundary, end=end, verbose=verbose
            )
            for repo in repos
        ]
        payload = mod.build_payload(
            repo_results,
            start=start,
            boundary=boundary,
            end=end,
            generated=mod._now_iso(),
        )
    except Exception as exc:  # noqa: BLE001 — any failure is an honest null SKIP
        return {"status": "skipped", "reason": str(exc)}
    return {"status": "ok", "payload": payload}


def render_api_latency(result: dict) -> str:
    """A modest latency section mirroring the frozen report §7 shape.

    The authoritative latency report is the frozen doc (report §7); this is the
    harness's re-runnable readout, kept deliberately high-level.
    """
    lines = [
        "## Open→merge latency (--api-latency · GitHub-API pass)",
        "",
    ]
    if result.get("status") != "ok":
        lines.append(f"API latency: SKIPPED — {result.get('reason', 'unknown')}")
        lines.append("")
        return "\n".join(lines)

    payload = result["payload"]
    lines += [
        "Opt-in GitHub-API pass, reusing scripts/measure_pr_latency.py's pure",
        "logic (no duplication). latency = merged_at − created_at (minutes);",
        "numpy-style linear-interpolation percentiles; PRs bucketed by merged_at",
        "UTC date. The authoritative frozen run is report §7.",
        "",
        "### Per-repo latency (minutes) — before · after (n·median)",
        "",
        "| repo | before (n·med) | after (n·med) |",
        "|---|---|---|",
    ]
    for r in payload.get("repos", []):
        if not r.get("ok"):
            lines.append(f"| {r.get('name', '?')} | null ({r.get('skip_reason', 'error')}) | — |")
            continue
        al = r["api_latency"]
        b, a = al["before"], al["after"]
        lines.append(
            f"| {r['name']} | {b['latency_n']}·{b['median_min']} "
            f"| {a['latency_n']}·{a['median_min']} |"
        )
    agg = payload.get("fleet_aggregate", {})
    lines += [
        "",
        "### Fleet aggregate (pooled, minutes)",
        "",
        "| bucket | n | median | p90 | max |",
        "|---|---|---|---|---|",
    ]
    for b in ("before", "boundary-day", "after"):
        c = agg.get(b, {})
        lines.append(
            f"| {b} | {c.get('latency_n', 0)} | {c.get('median_min')} "
            f"| {c.get('p90_min')} | {c.get('max_min')} |"
        )
    lines.append("")
    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────────


def _render_freeze_block(record: dict, targets: list[Path]) -> str:
    """A paste-ready, human-facing citation block for a frozen run."""
    rule = "─" * 57
    lines = [
        rule,
        "frozen run — self-citing (sha256 of the exact output bytes)",
        rule,
        "sha256: " + record["sha256"],
        "targets: " + ", ".join(t.name for t in targets),
        "reproduce:",
        "  " + record["reproduce"],
        "verify:",
        *("  sha256sum " + str(t) + "   # == sha256 above" for t in targets),
        rule,
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--roster", type=Path, default=_REPO_ROOT / "docs" / "fleet-repos.txt")
    ap.add_argument("--clone", action="store_true", help="clone roster repos into --workdir")
    ap.add_argument("--workdir", type=Path, help="clone destination (required with --clone)")
    ap.add_argument(
        "--local",
        action="append",
        default=[],
        metavar="NAME=PATH",
        help="measure a pre-cloned/local tree instead of cloning (repeatable)",
    )
    ap.add_argument("--start", type=date.fromisoformat, default=DEFAULT_START)
    ap.add_argument("--boundary", type=date.fromisoformat, default=DEFAULT_BOUNDARY)
    ap.add_argument("--end", type=date.fromisoformat, default=datetime.now(timezone.utc).date())
    ap.add_argument("--json", type=Path, help="write machine-readable results here")
    ap.add_argument(
        "--commit-results",
        type=Path,
        metavar="PATH",
        help=(
            "persist the machine-readable results to a durable (committed-into-repo) "
            "PATH — the same JSON as --json, but its parent dirs are created and it "
            "is meant for a git-tracked location a later measure→verify→publish step "
            "re-reads, so a raw results.json survives ephemeral-container splits "
            "(the chain does the git step). Subject to the same shallow-clone "
            "refuse-to-publish guard as --json"
        ),
    )
    ap.add_argument("--out", type=Path, help="write the markdown report here (default: stdout)")
    ap.add_argument(
        "--api-latency",
        action="store_true",
        help=(
            "opt-in; also measures open→merge PR latency via the GitHub API; "
            "requires a token in GITHUB_PAT/GH_TOKEN/GITHUB_TOKEN; cleanly "
            "SKIPPED (not errored) when the token is absent or the network fails"
        ),
    )
    ap.add_argument(
        "--freeze",
        action="store_true",
        help=(
            "given --json/--commit-results, also emit a self-citing freeze "
            "record: the sha256 of the exact output bytes plus a ready-to-paste "
            "reproduce block (the exact command that produced it). Writes a "
            "<output>.freeze sidecar next to each JSON artifact and prints the "
            "paste block to stderr — every window run becomes tamper-evident "
            "and self-citing. Honors the same shallow-clone refuse guard as "
            "--json (a frozen artifact can't ship off a shallow clone)."
        ),
    )
    args = ap.parse_args(argv)
    if args.freeze and not (args.json or args.commit_results):
        ap.error("--freeze requires --json or --commit-results")

    targets: list[tuple[str, Path | None, str]] = []
    for spec in args.local:
        if "=" not in spec:
            ap.error(f"--local expects NAME=PATH, got {spec!r}")
        name, path = spec.split("=", 1)
        targets.append((name, Path(path), ""))
    if args.clone:
        if not args.workdir:
            ap.error("--clone requires --workdir")
        args.workdir.mkdir(parents=True, exist_ok=True)
        for repo in parse_roster(args.roster.read_text(encoding="utf-8")):
            dest, err = clone_repo(repo, args.workdir)
            targets.append((repo, dest, err))
    if not targets:
        ap.error("nothing to measure — pass --clone and/or --local NAME=PATH")

    names = skill_names()
    results: list[RepoResult] = []
    for name, path, err in targets:
        if path is None or not path.is_dir():
            results.append(
                RepoResult(name=name, ok=False, skip_reason=err or f"not a directory: {path}")
            )
            continue
        results.append(
            measure_repo(
                name,
                path,
                start=args.start,
                boundary=args.boundary,
                end=args.end,
                names=names,
            )
        )

    report = render_report(results, start=args.start, boundary=args.boundary, end=args.end)

    api_latency_result: dict | None = None
    if args.api_latency:
        repos = parse_roster(args.roster.read_text(encoding="utf-8"))
        api_latency_result = run_api_latency(
            repos, start=args.start, boundary=args.boundary, end=args.end
        )
        report = report + "\n" + render_api_latency(api_latency_result)

    if args.out:
        args.out.write_text(report, encoding="utf-8")
    else:
        print(report)
    # Both --json and --commit-results emit the same machine-readable payload;
    # --commit-results only differs in that it writes to a durable, committed
    # location (parent dirs created) so the raw results survive an ephemeral-
    # container split for a later measure→verify→publish step to re-read.
    if args.json or args.commit_results:
        # Refuse to publish machine-readable JSON off a shallow clone: its M4
        # git-history metrics are silently zeroed by the truncated history, so
        # a written-but-zeroed JSON reads clean while being wrong. The markdown
        # path above only soft-nulls the shallow rows; the JSON seam is promoted
        # to an enforced refuse-to-publish — and a durable, git-tracked
        # --commit-results artifact off a shallow clone is worse still. Reuse
        # the per-repo ``shallow`` flag already carried on ``RepoResult.merged``
        # (no recomputation).
        shallow_repos = [
            r.name for r in results if r.merged is not None and r.merged.get("shallow")
        ]
        if shallow_repos:
            print(
                "REFUSE: shallow clone detected for "
                + ", ".join(shallow_repos)
                + " — M4 git-history metrics would be zeroed. Re-clone with full"
                " history (git fetch --unshallow) before generating --json /"
                " --commit-results.",
                file=sys.stderr,
            )
            return 2
        payload = results_json(results, start=args.start, boundary=args.boundary, end=args.end)
        if api_latency_result is not None:
            payload["api_latency"] = api_latency_result
        blob = json.dumps(payload, indent=2) + "\n"
        if args.json:
            args.json.write_text(blob, encoding="utf-8")
        if args.commit_results:
            args.commit_results.parent.mkdir(parents=True, exist_ok=True)
            args.commit_results.write_text(blob, encoding="utf-8")
        if args.freeze:
            # Self-cite: pin the exact output bytes with a sha256 and emit the
            # exact command that produced them. The hash is over ``blob`` (the
            # bytes actually written), so a plain ``sha256sum <output>`` verifies
            # it — the freeze record lives in a sidecar, never inside the hashed
            # payload, so there is no self-referential hash. This runs INSIDE the
            # shallow-clone guard above, so a frozen artifact can never ship off a
            # shallow clone whose M4 metrics are zeroed.
            digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
            reproduce = "python3 " + " ".join(
                shlex.quote(a) for a in [str(_SCRIPT_REL), *effective_argv]
            )
            written = [p for p in (args.json, args.commit_results) if p is not None]
            record = {
                "tool": _SCRIPT_REL.name,
                "algo": "sha256",
                "sha256": digest,
                "bytes": len(blob.encode("utf-8")),
                "reproduce": reproduce,
                "note": (
                    "sha256 pins the exact output bytes for tamper-evidence; the "
                    "reproduce command regenerates the measurement (the payload's "
                    "'generated' timestamp differs run-to-run, the metrics do not)."
                ),
            }
            freeze_blob = json.dumps(record, indent=2) + "\n"
            for target in written:
                target.with_name(target.name + ".freeze").write_text(
                    freeze_blob, encoding="utf-8"
                )
            print(_render_freeze_block(record, written), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
