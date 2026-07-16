"""Archive-ready note drafting — the ``archive-prep`` verb's engine half (S2).

Slice S2 of the archive-ready close-out plan
(``docs/planning/2026-07-15-archive-ready-close-out-plan.md`` §5), on top of
S1's template + doctrine (``src/engine/templates/archive-ready.md.tmpl`` ·
``docs/operations/archive-ready-close-out.md``). This module is the KL-5
evidence-draft pattern (``loop/handoff.py::ensure_draft``) pointed at the
archive seam: when a long-running chat is about to be archived, the session
runs ``archive-prep`` and *edits a drafted note* instead of hand-deriving the
fixed-shape checklist under time pressure — which is exactly where chat-only
knowledge leaks (plan §1: a pointed-at lessons file that did not exist; a
"disarmed" failsafe found still armed by the live probe).

Contract (plan §2):

1. **Drafts** ``docs/retro/archive-ready-<date>.md`` from the embedded S1
   template when no unresolved note exists — evidence fills what the tree can
   prove; everything else stays a named ``[[fill:]]`` slot.
2. **Reports** unresolved slots on re-run (the ``cmd_draft`` idiom); a note
   with zero remaining slots *and no guarded-slot residue* is complete and is
   **never touched**.
3. **REQUIRES-PROBE resolve semantics (S3):** the doctrine-guarded slots
   (routine state, the chat-only confirmation) resolve ONLY by wholesale
   replacement. Stripping the ``[[fill:`` / ``]]`` markers while keeping the
   templated instruction text is the sham-resolution the guard exists for — a
   record-shaped default that *looks* done. ``probe_slot_residue`` fingerprints
   the guarded slot bodies from the shipped template (whitespace-normalized
   word shingles) and reports any surviving run of default text; a note with
   residue is never reported complete and never blocks on silence.
4. The ``check --strict`` advisory half is slice S4, not here.

Evidence sources (plan §3 — tree-local, pure stdlib, no subprocess):

- ``control/claims/`` entries (``config.claims_dir``) — the live work claims;
- heartbeat ``⚑`` lines (``config.heartbeat_files``) — the open owner-action
  set, names only (full paste-ready blocks stay in the heartbeat);
- ``CHANGELOG.md`` ``[Unreleased]`` — the unreleased-payload park.

What is **never** auto-filled (plan §4.2 + the S1 doctrine): REQUIRES-PROBE
slots (routine state — a record-shaped default trusted at archive time is the
realized failure this surface exists to prevent) and the "nothing remains
chat-only" confirmation (writing it IS the final check). The engine cannot
reach GitHub or the trigger API, so live PR/check state stays a session slot.

Fail-open by contract: drafting never raises — a failure returns an advisory
naming the hand-copy fallback instead of crashing the verb.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from engine.checks.check_session_log import DRAFT_FILL_TOKEN
from engine.checks.check_status_current import heartbeat_relpaths
from engine.lib.atomicio import atomic_write_text
from engine.lib.config import Config
from engine.lib.residue import probe_residue
from engine.loop.handoff import DRAFT_MARKER
from engine.render import load_templates

# The S1 note skeleton, embedded in the dist / packaged with the wheel.
ARCHIVE_TEMPLATE_NAME = "archive-ready.md.tmpl"
# Where notes live + how instances are named (S1 doctrine: instantiate as
# docs/retro/archive-ready-<date>.md).
_RETRO_DIR = "retro"
_NOTE_GLOB = "archive-ready-*.md"
# Slots carrying this token resolve ONLY by wholesale replacement with live
# probe output — the drafter must never pre-fill them (plan §4.2).
REQUIRES_PROBE_TOKEN = "REQUIRES-PROBE"
# The confirmation slot's own never-draft rule, quoted from the template so
# the guard keys on the doctrine text itself.
_NEVER_DRAFT_TOKEN = "never drafted as complete"
# One [[fill:]] slot spans lines; no slot nests another (same grammar the
# session-log checker counts by token).
_ARCHIVE_SLOT_RE = re.compile(r"\[\[fill:.*?\]\]", re.DOTALL)
# Rendering caps — a giant heartbeat/CHANGELOG lists a head + "+N more"
# tail instead of flooding the note (the handoff _EVIDENCE_RENDER_CAP idiom).
_FLAG_RENDER_CAP = 20
_FLAG_LINE_CAP = 120
_PAYLOAD_RENDER_CAP = 30


def _judgment_slot(hint: str) -> str:
    """Return one unresolved judgment slot for the drafted text."""
    return f"{DRAFT_FILL_TOKEN} {hint}]]"


def archive_note_path(root: Path, config: Config, day: str | None = None) -> Path:
    """Return the archive-ready note path for ``day`` (default: today)."""
    day = day or date.today().isoformat()
    return root / config.docs_root / _RETRO_DIR / f"archive-ready-{day}.md"


# ---------------------------------------------------------------------------
# Evidence — what the tree can prove (plan §3)
# ---------------------------------------------------------------------------


def _claims_replacement(root: Path, config: Config) -> str:
    """Render the claims-directory evidence for the Claims slot."""
    claims_dir = root / config.claims_dir
    if not claims_dir.is_dir():
        return f"none at draft time (evidence: no `{config.claims_dir}/` directory)"
    entries = sorted(
        p.name for p in claims_dir.glob("*.md") if p.name != "README.md"
    )
    if not entries:
        return f"none at draft time (evidence: `{config.claims_dir}/` holds no claims)"
    names = ", ".join(f"`{name}`" for name in entries)
    return (
        f"{names} (evidence: `{config.claims_dir}/` at draft time) — "
        f"{_judgment_slot('kept-or-pruned disposition per claim, with a reason')}"
    )


def _flag_lines(root: Path, config: Config) -> list[str]:
    """Extract the ``⚑`` item lines from the heartbeat file(s), capped."""
    lines: list[str] = []
    for rel in heartbeat_relpaths(config.heartbeat_files):
        path = root / rel
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = raw.lstrip("#->*• \t")
            if not stripped.startswith("\N{BLACK FLAG}"):
                continue
            if len(stripped) > _FLAG_LINE_CAP:
                stripped = stripped[: _FLAG_LINE_CAP - 1].rstrip() + "\N{HORIZONTAL ELLIPSIS}"
            lines.append(stripped)
    return lines


def _flags_replacement(root: Path, config: Config) -> str:
    """Render the open owner-action evidence for the ⚑ slot."""
    heartbeats = ", ".join(f"`{n}`" for n in heartbeat_relpaths(config.heartbeat_files))
    flags = _flag_lines(root, config)
    if not flags:
        return f"none open (evidence: no \N{BLACK FLAG} lines in {heartbeats} at draft time)"
    shown = flags[:_FLAG_RENDER_CAP]
    tail = len(flags) - len(shown)
    bullets = "\n".join(f"- {line} (evidence)" for line in shown)
    more = f"\n- \N{HORIZONTAL ELLIPSIS} +{tail} more \N{BLACK FLAG} line(s) in the heartbeat" if tail > 0 else ""
    slot = _judgment_slot(
        "verify against the live heartbeat — one line + where each unblocks, prune what is stale",
    )
    return f"extracted from {heartbeats} at draft time:\n\n{bullets}{more}\n\n{slot}"


def _changelog_unreleased(root: Path) -> list[str]:
    """Return the CHANGELOG ``[Unreleased]`` section's content lines."""
    changelog = root / "CHANGELOG.md"
    if not changelog.is_file():
        return []
    lines = changelog.read_text(encoding="utf-8", errors="replace").splitlines()
    collected: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            if inside:
                break
            inside = "[unreleased]" in line.lower()
            continue
        if inside:
            collected.append(line.rstrip())
    while collected and not collected[0]:
        collected.pop(0)
    while collected and not collected[-1]:
        collected.pop()
    return collected


def _payload_replacement(root: Path) -> str:
    """Render the unreleased-payload evidence for the park slot."""
    slot = _judgment_slot(
        "unshipped slices / pinned PRs beyond the CHANGELOG, and what the next "
        'session cuts/ships from the park — or "nothing further parked"',
    )
    content = _changelog_unreleased(root)
    if not content:
        return (
            "CHANGELOG `[Unreleased]`: nothing parked at draft time "
            f"(evidence: no populated section found). {slot}"
        )
    shown = content[:_PAYLOAD_RENDER_CAP]
    tail = len(content) - len(shown)
    more = f"\n\N{HORIZONTAL ELLIPSIS} +{tail} more line(s) in CHANGELOG.md" if tail > 0 else ""
    body = "\n".join(shown)
    return (
        "CHANGELOG `[Unreleased]` at draft time (evidence):\n\n"
        f"```\n{body}{more}\n```\n\n{slot}"
    )


# ---------------------------------------------------------------------------
# Draft composition — the template with evidence substituted into its slots
# ---------------------------------------------------------------------------


def _fill_evidence(template: str, root: Path, config: Config, day: str) -> str:
    """Substitute tree evidence into the template's fillable slots.

    Slot-by-slot, keyed on the template's own hint text; anything unmatched —
    and anything the doctrine forbids drafting (REQUIRES-PROBE, the
    confirmation) — passes through untouched. Replacement text may itself
    carry fresh ``[[fill:]]`` judgment slots; ``re.sub`` never rescans
    replacements, so evidence can safely hand the judgment half back to the
    session.
    """

    def substitute(match: re.Match[str]) -> str:
        slot = match.group(0)
        if REQUIRES_PROBE_TOKEN in slot or _NEVER_DRAFT_TOKEN in slot:
            return slot  # never auto-filled, by doctrine
        if "YYYY-MM-DD" in slot:
            return f"{day} \N{MIDDLE DOT} {_judgment_slot('which chat/session is being archived')}"
        if "contents of the claims directory" in slot:
            return _claims_replacement(root, config)
        if "what is parked and where it survives" in slot:
            return _payload_replacement(root)
        if "every \N{BLACK FLAG} item open at archive time" in slot:
            return _flags_replacement(root, config)
        return slot

    return _ARCHIVE_SLOT_RE.sub(substitute, template)


def draft_archive_note(root: Path, config: Config, day: str | None = None) -> str:
    """Compose the drafted archive-ready note text (template + evidence)."""
    day = day or date.today().isoformat()
    template = load_templates()[ARCHIVE_TEMPLATE_NAME]
    text = _fill_evidence(template, root, config, day)
    # Provenance marker after the H1, same stamp the KL-5 card draft carries.
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines.insert(1, "")
        lines.insert(2, DRAFT_MARKER)
        text = "\n".join(lines)
        if not text.endswith("\n"):
            text += "\n"
    return text


# ---------------------------------------------------------------------------
# Resolve-time semantics (S3) — guarded slots resolve only by wholesale
# replacement; a templated default surviving marker-stripping is residue
# ---------------------------------------------------------------------------


def _archive_guarded_bodies(template: str) -> list[tuple[str, str]]:
    """Return ``(name, inner body)`` for each doctrine-guarded template slot.

    Guarded = the slots the drafter never auto-fills (plan §4.2): the
    REQUIRES-PROBE routine-state slot and the never-drafted-as-complete
    confirmation slot. Bodies come from the shipped template itself, so the
    fingerprints track the doctrine text without a second copy to drift.
    """
    guarded: list[tuple[str, str]] = []
    for match in _ARCHIVE_SLOT_RE.finditer(template):
        slot = match.group(0)
        if REQUIRES_PROBE_TOKEN in slot:
            name = f"routine-state ({REQUIRES_PROBE_TOKEN})"
        elif _NEVER_DRAFT_TOKEN in slot:
            name = "chat-only confirmation"
        else:
            continue
        body = slot[len(DRAFT_FILL_TOKEN) : -len("]]")]
        guarded.append((name, body))
    return guarded


def probe_slot_residue(text: str, template: str | None = None) -> list[str]:
    """Return residue findings — guarded default text surviving in ``text``.

    Empty list = every guarded slot was wholesale-replaced (or still carries
    its ``[[fill:]]`` markers, which the slot count already reports). One
    finding per guarded slot whose templated instruction text survives with
    the markers stripped — the sham-resolution a record-shaped default
    produces. S4's ``check --strict`` advisory reuses this seam.

    The fingerprint core lives in ``engine.lib.residue`` since the KL-5
    generalization (shingle window, whitespace normalization, intact-slot
    skip — behavior identical to the original S3 in-module implementation);
    this function keeps the archive surface's guarded-body extraction and
    finding wording.
    """
    if template is None:
        template = load_templates()[ARCHIVE_TEMPLATE_NAME]
    guilty = probe_residue(text, _archive_guarded_bodies(template))
    return [
        f"{name}: templated default text survives — this slot "
        "resolves ONLY by wholesale replacement with freshly probed "
        "output; stripping the [[fill:]] markers around the "
        "template's instruction text is not a resolution."
        for name in guilty
    ]


# ---------------------------------------------------------------------------
# The verb's engine seam (cmd_archive_prep calls this)
# ---------------------------------------------------------------------------


def ensure_archive_draft(root: Path, config: Config) -> list[str]:
    """Draft / report the archive-ready note; return advisory lines.

    The ``ensure_draft`` contract at the archive seam: no note (or only
    completed ones from earlier archives) → draft today's from evidence; the
    newest note still carrying ``[[fill:]]`` slots → report the count and
    touch nothing; a zero-slot note with guarded-slot residue (S3) → report
    the sham resolution and touch nothing — it is never "complete" and never
    silently superseded; a genuinely completed note is never touched.
    Fail-open: any failure returns the hand-copy fallback advisory instead of
    raising.
    """
    try:
        retro = root / config.docs_root / _RETRO_DIR
        existing = sorted(retro.glob(_NOTE_GLOB)) if retro.is_dir() else []
        newest = existing[-1] if existing else None
        if newest is not None:
            text = newest.read_text(encoding="utf-8", errors="replace")
            slots = text.count(DRAFT_FILL_TOKEN)
            rel = newest.relative_to(root) if newest.is_relative_to(root) else newest
            if slots:
                return [
                    f"{rel}: {slots} [[fill:]] slot(s) still unresolved — resolve "
                    "each with live facts (REQUIRES-PROBE slots by wholesale "
                    "replacement with probe output), write the confirmation "
                    "LAST, then land the note on main before the chat closes.",
                ]
            residue = probe_slot_residue(text)
            if residue:
                return [
                    f"{rel}: zero [[fill:]] slots remain, but templated "
                    "default text survives in guarded slot(s) — the note is "
                    "NOT complete (S3 resolve semantics):",
                    *[f"  - {finding}" for finding in residue],
                    "replace the surviving instruction text wholesale with "
                    "live probe output, then land the note on main.",
                ]
            if newest == archive_note_path(root, config):
                return [
                    f"{rel} is complete (zero unresolved slots) — nothing to "
                    "draft; a completed note is never touched.",
                ]
        path = archive_note_path(root, config)
        atomic_write_text(path, draft_archive_note(root, config))
        rel = path.relative_to(root) if path.is_relative_to(root) else path
        return [
            f"drafted {rel} from tree evidence — verify the evidence fills, "
            "resolve every [[fill:]] slot with live facts (the live PR table "
            "and routine state need YOUR tools; the engine cannot reach "
            "GitHub), write the confirmation last, land the note on main.",
            "checklist doctrine: docs/operations/archive-ready-close-out.md "
            "(in the kit repo).",
        ]
    except Exception as exc:  # fail open — the verb must never crash (plan §2)
        return [
            f"archive-prep failed open ({exc.__class__.__name__}: {exc}) — copy "
            "src/engine/templates/archive-ready.md.tmpl to "
            "docs/retro/archive-ready-<date>.md by hand and resolve its slots "
            "(docs/operations/archive-ready-close-out.md).",
        ]
