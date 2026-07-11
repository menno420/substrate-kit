"""Auto-drafted session handoff (band KL-5, founding plan §10 — the ruled B1 prerequisite).

The Phase-2.5 A/B measured the same failure twice: write-back that depends on
agent discipline does not happen in task-focused sessions (the ON arm read the
planted docs and wrote **nothing** back). This module stops asking the agent to
remember: ``session-close`` and the Stop hook **draft** the session card's
close-out from evidence the engine can already see, so the agent *edits a
draft* instead of authoring from scratch — the same trick that makes the
born-red card work (the card exists before the work; closing it is editing,
not remembering).

Evidence sources (all pure stdlib — no subprocess, per the engine lint bans):

- a **session-start anchor** (``state["session_anchor"]``) recorded by the
  SessionStart hook: timestamp + git HEAD/branch, read from ``.git`` by file
  parsing (loose refs, ``packed-refs``, worktree ``gitdir:`` files);
- an **mtime scan** of the working tree against the anchor — the stdlib
  analog of ``git diff --stat`` — classified code / tests / docs / sessions;
- git **HEAD movement** since the anchor (commits happened / nothing
  committed yet);
- the **derived verify command** (the adopt-time ``verify_command`` slot) —
  the engine cannot execute it, so the draft carries it as a run-and-record
  slot rather than fake results (the console's no-fake-data rule).

The drafted text marks every judgment-only field with a ``[[fill: …]]`` slot
and the card with ``<!-- substrate:auto-draft -->``; the session-log checker
counts unresolved slots, so a **drafted-but-unedited card is distinguishable
from a completed one** and the born-red gate keeps holding until the slots
resolve. Everything here is fail-open by contract: drafting can never crash a
hook or ``session-close``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from engine.checks.check_session_log import (
    DRAFT_FILL_TOKEN,
    _marker_miss,
    check_log,
    latest_session_log,
    status_in_progress,
)
from engine.lib.atomicio import atomic_write_text
from engine.lib.config import Config
from engine.loop.handoff_pointer import write_handoff_pointer

# State key for the session-start evidence anchor.
SESSION_ANCHOR_KEY = "session_anchor"
# Provenance marker stamped into every auto-drafted card/section.
DRAFT_MARKER = "<!-- substrate:auto-draft -->"

# Directories the evidence scan never descends into (vendored/derived trees;
# ``.git`` and the configured state_dir are excluded separately).
_SKIP_DIR_NAMES = frozenset(
    {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".eggs",
    },
)
_CODE_SUFFIXES = frozenset(
    {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".go",
        ".rs",
        ".java",
        ".rb",
        ".c",
        ".h",
        ".cpp",
        ".sh",
    },
)
# Rendering cap per evidence category — a giant session lists the head + a
# "+N more" tail instead of flooding the card.
_EVIDENCE_RENDER_CAP = 15
_SHA_LEN = 9


def _fill(hint: str) -> str:
    """Return one unresolved judgment slot for the drafted text."""
    return f"{DRAFT_FILL_TOKEN} {hint}]]"


# ---------------------------------------------------------------------------
# Git evidence — pure file parsing (subprocess is banned in engine code)
# ---------------------------------------------------------------------------


def _git_dir(root: Path) -> Path | None:
    """Resolve ``root``'s git directory (handles worktree ``gitdir:`` files)."""
    dot = root / ".git"
    if dot.is_dir():
        return dot
    if dot.is_file():
        text = dot.read_text(encoding="utf-8", errors="replace").strip()
        if text.startswith("gitdir:"):
            gitdir = Path(text.split(":", 1)[1].strip())
            if not gitdir.is_absolute():
                gitdir = (root / gitdir).resolve()
            if gitdir.is_dir():
                return gitdir
    return None


def _git_common_dir(git_dir: Path) -> Path:
    """Return the shared git dir (worktrees keep refs in ``commondir``)."""
    pointer = git_dir / "commondir"
    if pointer.is_file():
        common = Path(pointer.read_text(encoding="utf-8", errors="replace").strip())
        if not common.is_absolute():
            common = (git_dir / common).resolve()
        if common.is_dir():
            return common
    return git_dir


def _resolve_ref(git_dir: Path, ref: str) -> str | None:
    """Resolve a symbolic ref to a sha via loose refs, then ``packed-refs``."""
    common = _git_common_dir(git_dir)
    for base in (git_dir, common):
        loose = base / ref
        if loose.is_file():
            sha = loose.read_text(encoding="utf-8", errors="replace").strip()
            return sha or None
    packed = common / "packed-refs"
    if packed.is_file():
        for line in packed.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith(("#", "^")):
                continue
            parts = line.split(" ", 1)
            if len(parts) == 2 and parts[1].strip() == ref:
                return parts[0].strip() or None
    return None


def read_git_head(root: Path) -> tuple[str | None, str | None]:
    """Return ``(branch, sha)`` for ``root``'s HEAD — ``(None, None)`` on any failure.

    Pure file parsing (``HEAD`` → loose ref → ``packed-refs``), worktree-aware.
    Fail-open by contract: evidence gathering must never raise into a hook.
    """
    try:
        git_dir = _git_dir(root)
        if git_dir is None:
            return (None, None)
        head = (git_dir / "HEAD").read_text(encoding="utf-8", errors="replace").strip()
        if head.startswith("ref:"):
            ref = head.split(":", 1)[1].strip()
            branch = ref[len("refs/heads/") :] if ref.startswith("refs/heads/") else ref
            return (branch, _resolve_ref(git_dir, ref))
        # Detached HEAD: the file holds the sha itself.
        if len(head) >= 40 and all(c in "0123456789abcdef" for c in head.lower()):
            return (None, head)
        return (None, None)
    except Exception:  # fail open — git evidence is best-effort by contract
        return (None, None)


# ---------------------------------------------------------------------------
# The session-start anchor
# ---------------------------------------------------------------------------


def record_session_anchor(root: Path, config: Config, backend: Any) -> None:
    """Record this session's evidence anchor into state (fail-open).

    Stores ``{ts, epoch, head, branch}`` under ``state["session_anchor"]``.
    A same-day re-fire (SessionStart runs again on resume/clear) keeps the
    original anchor so mid-session resumes don't hide earlier changes; a
    stale anchor from a previous day is overwritten.
    """
    try:
        now = datetime.now(timezone.utc)
        existing = backend.data.get(SESSION_ANCHOR_KEY) if backend.data else None
        if isinstance(existing, dict):
            ts = existing.get("ts")
            if isinstance(ts, str) and ts[:10] == now.date().isoformat():
                return
        branch, sha = read_git_head(root)
        backend.set(
            SESSION_ANCHOR_KEY,
            {
                "ts": now.isoformat(timespec="seconds"),
                "epoch": now.timestamp(),
                "head": sha,
                "branch": branch,
            },
        )
    except Exception:  # fail open — anchoring must never crash a session start
        return


# ---------------------------------------------------------------------------
# Evidence gathering
# ---------------------------------------------------------------------------


@dataclass
class SessionEvidence:
    """What the engine can see about this session without being told."""

    anchor_ts: str | None = None
    anchor_epoch: float | None = None
    branch: str | None = None
    head_start: str | None = None
    head_now: str | None = None
    verify_command: str | None = None
    # category -> sorted relative paths; categories: code/tests/docs/sessions/other
    changed: dict[str, list[str]] = field(default_factory=dict)


def _classify(rel: str, config: Config) -> str:
    """Classify one changed path into an evidence category."""
    parts = Path(rel).parts
    if parts and parts[0] == config.sessions_dir:
        return "sessions"
    if parts and parts[0] == config.docs_root:
        return "docs"
    name = Path(rel).name
    if any(p in ("tests", "test") for p in parts[:-1]) or name.startswith("test_"):
        return "tests"
    if Path(rel).suffix.lower() in _CODE_SUFFIXES:
        return "code"
    return "other"


def _changed_since(root: Path, config: Config, epoch: float) -> dict[str, list[str]]:
    """Return files modified after ``epoch``, classified — the mtime diff scan."""
    changed: dict[str, list[str]] = {}
    skip = set(_SKIP_DIR_NAMES) | {config.state_dir}
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = list(current.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.is_dir():
                if entry.name not in skip and not entry.is_symlink():
                    stack.append(entry)
                continue
            try:
                if entry.stat().st_mtime <= epoch:
                    continue
            except OSError:
                continue
            rel = str(entry.relative_to(root))
            changed.setdefault(_classify(rel, config), []).append(rel)
    return {category: sorted(paths) for category, paths in sorted(changed.items())}


def gather_evidence(root: Path, config: Config, state: dict[str, Any]) -> SessionEvidence:
    """Collect the drafting evidence (fail-open — a partial view beats none)."""
    evidence = SessionEvidence()
    try:
        anchor = state.get(SESSION_ANCHOR_KEY)
        if isinstance(anchor, dict):
            ts, epoch = anchor.get("ts"), anchor.get("epoch")
            evidence.anchor_ts = ts if isinstance(ts, str) else None
            evidence.anchor_epoch = float(epoch) if isinstance(epoch, (int, float)) else None
            head = anchor.get("head")
            evidence.head_start = head if isinstance(head, str) else None
        evidence.branch, evidence.head_now = read_git_head(root)
        values = state.get("slot_values")
        if isinstance(values, dict):
            entry = values.get("verify_command")
            if isinstance(entry, dict) and isinstance(entry.get("value"), str):
                evidence.verify_command = entry["value"]
        if evidence.anchor_epoch is not None:
            evidence.changed = _changed_since(root, config, evidence.anchor_epoch)
    except Exception:  # fail open — return whatever was gathered so far
        return evidence
    return evidence


# ---------------------------------------------------------------------------
# Draft composition
# ---------------------------------------------------------------------------


def _evidence_lines(evidence: SessionEvidence) -> list[str]:
    """Render the auto-collected evidence as card bullet lines."""
    lines: list[str] = []
    if evidence.anchor_epoch is None:
        lines.append(
            "- files touched: unknown — no session-start anchor recorded "
            "(the SessionStart hook / `session-start` records it at boot).",
        )
    elif not evidence.changed:
        lines.append(
            f"- no files changed since session start ({evidence.anchor_ts}).",
        )
    else:
        for category, paths in evidence.changed.items():
            head = ", ".join(f"`{p}`" for p in paths[:_EVIDENCE_RENDER_CAP])
            tail = len(paths) - _EVIDENCE_RENDER_CAP
            more = f" (+{tail} more)" if tail > 0 else ""
            lines.append(f"- {category} touched ({len(paths)}): {head}{more}")
    if evidence.branch or evidence.head_now:
        branch = f"branch `{evidence.branch}`" if evidence.branch else "detached HEAD"
        start, now = evidence.head_start, evidence.head_now
        if start and now and start != now:
            movement = f"HEAD {start[:_SHA_LEN]} → {now[:_SHA_LEN]} (commits made this session)"
        elif start and now:
            movement = f"HEAD unchanged at {now[:_SHA_LEN]} (nothing committed yet)"
        elif now:
            movement = f"HEAD {now[:_SHA_LEN]}"
        else:
            movement = "HEAD unresolved"
        lines.append(f"- git: {branch}, {movement}.")
    if evidence.verify_command:
        lines.append(
            f"- verify: run `{evidence.verify_command}` and record the result "
            f"→ {_fill('verify result — the engine cannot execute commands')}",
        )
    else:
        lines.append(f"- verify: {_fill('how this session was verified (command + result)')}")
    return lines


# Label -> drafted stand-in line for the default session markers. Unknown
# host-configured markers get a generic needle-carrying line so resolving the
# slot satisfies the marker too.
def _marker_line(marker: dict[str, str]) -> str | None:
    """Return the drafted stand-in for one missing session marker."""
    label = marker.get("label", "")
    needle = marker.get("needle", "")
    if not needle or needle == "**Status:**":
        return None
    if label == "Session idea":
        return f"## 💡 Session idea\n\n{_fill('one idea you genuinely believe in — never filler')}"
    if label == "Previous-session review":
        return (
            "## ⟲ Previous-session review\n\n"
            f"{_fill('one genuine remark on the previous session + one workflow improvement')}"
        )
    if label == "Model line":
        return (
            f"- **\N{BAR CHART} Model:** {_fill('model')} \N{MIDDLE DOT} "
            f"{_fill('effort')} \N{MIDDLE DOT} {_fill('task-class (Q-0248 taxonomy)')}"
        )
    return f"- {needle} {_fill(label or 'resolve this marker')}"


def draft_close_out(
    evidence: SessionEvidence,
    markers: list[dict[str, str]] | None = None,
) -> str:
    """Compose the drafted close-out section (evidence + judgment slots).

    ``markers`` — the session markers still missing from the card, each drafted
    as a needle-carrying stand-in so one edit pass resolves everything.
    """
    parts = [
        f"## Close-out (auto-drafted {date.today().isoformat()} — edit, don't author)",
        "",
        DRAFT_MARKER,
        "",
        "**Evidence (auto-collected — verify, then keep or correct):**",
        "",
        *_evidence_lines(evidence),
        "",
        "**Judgment (the half only the session knows — resolve every slot):**",
        "",
        f"- Decisions made: {_fill('decisions taken this session, or none')}",
        f"- Next session should know: {_fill('the handoff pointer — where to pick up')}",
    ]
    for marker in markers or []:
        line = _marker_line(marker)
        if line:
            parts += ["", line]
    return "\n".join(parts) + "\n"


def draft_card(slug: str, evidence: SessionEvidence, config: Config) -> str:
    """Compose a full drafted skeleton card (the missing-card path)."""
    body = draft_close_out(evidence, list(config.session_markers))
    return (
        f"# Session {slug}\n\n"
        "> **Status:** `drafted` *(auto-drafted by substrate-kit — edit the\n"
        "> close-out, resolve every `[[fill:]]` slot, then flip this badge to\n"
        "> `complete`.)*\n\n"
        f"{body}"
    )


# ---------------------------------------------------------------------------
# The drafting orchestrator (both write-back surfaces call this)
# ---------------------------------------------------------------------------


def _unique_card_path(sessions_dir: Path, day: str) -> Path:
    """Return a non-colliding path for a drafted skeleton card."""
    path = sessions_dir / f"{day}-session.md"
    serial = 2
    while path.exists():
        path = sessions_dir / f"{day}-session-{serial}.md"
        serial += 1
    return path


def ensure_draft(root: Path, config: Config, backend: Any) -> list[str]:
    """Draft the session card / close-out from evidence; return advisory lines.

    The mechanized write-back seam (`session-close` and the Stop hook both run
    it): a missing card gets a drafted skeleton; an in-progress card missing
    close-out markers gets the drafted section appended; a card already
    drafted is only counted (unresolved slots); a completed card is never
    touched. Fail-open by contract — any failure returns ``[]`` rather than
    raising into a hook.

    After drafting, the repo-root ``HANDOFF.md`` pointer is refreshed —
    silently — so it names the just-drafted card (the B1 run-6 delivery-gap
    fix: the pointer rides the working-tree surfaces delegated workers
    actually touch). Silent by design: the refresh is bookkeeping, not an
    advisory, and it must not change this seam's advisory contract.
    """
    lines = _draft_advisories(root, config, backend)
    write_handoff_pointer(root, config)
    return lines


def _draft_advisories(root: Path, config: Config, backend: Any) -> list[str]:
    """The drafting body of ``ensure_draft`` (see its contract above)."""
    try:
        try:
            state = dict(backend.data) if backend.data else {}
        except Exception:
            state = {}
        evidence = gather_evidence(root, config, state)
        sessions_dir = root / config.sessions_dir
        card = latest_session_log(sessions_dir)
        if (
            card is not None
            and evidence.anchor_epoch is not None
            and card.stat().st_mtime <= evidence.anchor_epoch
        ):
            card = None  # newest card predates this session — not ours
        if card is None:
            day = date.today().isoformat()
            path = _unique_card_path(sessions_dir, day)
            atomic_write_text(path, draft_card(f"{day} — {path.stem}", evidence, config))
            rel = path.relative_to(root) if path.is_relative_to(root) else path
            return [
                f"session card was missing — auto-drafted {rel}: verify the "
                "evidence, resolve the [[fill:]] slots, flip Status to complete",
            ]
        text = card.read_text(encoding="utf-8")
        if DRAFT_MARKER in text or DRAFT_FILL_TOKEN in text:
            slots = text.count(DRAFT_FILL_TOKEN)
            if slots:
                return [
                    f"auto-draft in {card.name}: {slots} [[fill:]] slot(s) still "
                    "unresolved — the card counts drafted, not completed",
                ]
            return []
        if not status_in_progress(text):
            return []  # completed card — consumer-owned, never touched
        missing = check_log(card, config.session_markers)
        missing_misses = {m for m in missing if not m.startswith("a completed Status")}
        if not missing_misses:
            return []  # close-out already written; only the status flip remains
        # check_log reports each miss as "label (expected `needle`)" — map it
        # back to the configured marker via the same formatter so the drafted
        # stand-ins can never drift from what the checker said was missing.
        markers = [m for m in config.session_markers if _marker_miss(m) in missing_misses]
        section = draft_close_out(evidence, markers)
        atomic_write_text(card, text.rstrip("\n") + "\n\n" + section)
        return [
            f"auto-drafted close-out appended to {card.name} — verify the "
            "evidence, resolve the [[fill:]] slots, flip the Status badge",
        ]
    except Exception:  # fail open — drafting must never crash a hook
        return []
