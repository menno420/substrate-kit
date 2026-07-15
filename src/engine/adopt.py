"""One-step adopt flow — plant the workflow docs, stage the packs (Lane B8).

``adopt`` turns a bare host repo into a substrate-governed one in a single
idempotent pass: it renders every content template with the currently filled
interview slots and *plants* the live docs (constitution, contracts, ledgers,
session scaffolding) — **skip-if-exists, never clobbering** a file the host
already owns — then *stages* the ``.claude`` material (working agreement,
skill pack, persona pack, hook wiring, CI example) under ``<state_dir>`` for
the host to install deliberately. Only an explicit ``include_claude=True``
writes a live ``.claude/`` tree, and even then only files that are absent
(the host opt-in stays non-destructive).

Adopt renders what it knows (the Phase-2.5 G2 fix): before rendering, every
deterministically-derivable slot (project name, language, verify command,
docs root — ``engine/derive.py``) is recorded as a provisional interview
answer, and any doc still carrying unfilled ``${slot}`` placeholders is
planted under a loud UNRENDERED banner instead of silently inert — a cold
session sees at a glance which prose is live and which is an unfilled slot.
The guardrail runs first: the kit refuses to adopt into its own tree. Pure
stdlib; every write goes through ``atomic_write_text``.
"""

from __future__ import annotations

import hashlib
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

from engine.agents.agents import AGENTS, agent_document, agent_relpath
from engine.contextpack import pack_index_skeleton
from engine.derive import derive_slots, record_derived_slots
from engine.enabler_preflight import enabler_install_preflight
from engine.hooks.settings import full_settings_template, hooks_fill_table
from engine.lib.atomicio import atomic_write_text
from engine.lib.config import KIT_VERSION, Config, save_config
from engine.lib.guardrail import assert_safe_target
from engine.loop.telemetry import MODEL_LINE_NEEDLE
from engine.render import (
    agreement_home,
    build_context,
    find_placeholders,
    load_templates,
    render,
)
from engine.seatdigest import seat_digest_relpath, seat_digest_text
from engine.skills.skills import SKILLS, skill_document, skill_relpath

# Template filename -> planted relpath. CLAUDE.md.tmpl is deliberately absent:
# it is STAGED under <state_dir>/claude/ (the kit never live-writes .claude/
# without the explicit include_claude opt-in).
ADOPT_PLAN: list[tuple[str, str]] = [
    ("CONSTITUTION.md.tmpl", "CONSTITUTION.md"),
    ("decisions.md.tmpl", "docs/decisions.md"),
    ("architecture.md.tmpl", "docs/architecture.md"),
    ("ownership.md.tmpl", "docs/ownership.md"),
    ("runtime_contracts.md.tmpl", "docs/runtime_contracts.md"),
    ("repo-navigation-map.md.tmpl", "docs/repo-navigation-map.md"),
    ("helper-policy.md.tmpl", "docs/helper-policy.md"),
    ("collaboration-model.md.tmpl", "docs/collaboration-model.md"),
    ("ai-project-workflow.md.tmpl", "docs/ai-project-workflow.md"),
    ("owner-profile.md.tmpl", "docs/owner-profile.md"),
    ("AGENT_ORIENTATION.md.tmpl", "docs/AGENT_ORIENTATION.md"),
    ("current-state.md.tmpl", "docs/current-state.md"),
    ("question-router.md.tmpl", "docs/question-router.md"),
    # Capability manifest (inbox ORDER 006): what sessions in this
    # environment can and cannot do — verified findings + the discovery
    # rule (check file → check env → attempt once + capture the exact
    # error → append same session). Sessions read it at start (orientation
    # wiring in CLAUDE.md/CONSTITUTION/AGENT_ORIENTATION templates) and
    # append discoveries at close (session-close skill nudge), so one
    # session's imagined-wall lesson never costs a second session.
    ("CAPABILITIES.md.tmpl", "docs/CAPABILITIES.md"),
    # The skill index (grounded-skills program slice 1 —
    # docs/planning/2026-07-12-grounded-skills-program.md §2/§7.1): one
    # table — skill → when to reach for it → capabilities — rendered FROM
    # the kit's SKILLS list via the engine-computed ``skills_index``
    # context key (engine.render.build_context), so the planted index can
    # never drift from the skills the kit actually emits. Boot-set wiring
    # lives in the CLAUDE / CONSTITUTION / AGENT_ORIENTATION templates
    # (the CAPABILITIES.md pattern); advisory only — no CI enforcement
    # of "you used the skill" (§8 Q2=B, graduation later).
    ("SKILLS-index.md.tmpl", "docs/SKILLS.md"),
    # Routine / wake-chain doctrine (grounded-skills program §7 tail —
    # docs/planning/2026-07-12-grounded-skills-program.md §6 "Routine/
    # wake-chain doctrine" row; map: docs/reports/
    # 2026-07-12-prompt-template-hardening-input.md §(b)): binding choice
    # by lifetime + verify-delivery, verbatim create-call records,
    # probe-not-record re-verification at every wake, the scheduler-health
    # wedge signature, sequential trigger-write pacing, and the failsafe
    # blind-window check — incident-backed (the 2026-07-12 trigger
    # forensics) and portably worded (no fleet/env ids: the env-id
    # mismatch is itself load-bearing, forensics H2). Routed from the
    # CLAUDE / AGENT_ORIENTATION templates like its CAPABILITIES/SKILLS
    # siblings so the plant never orphans an adopter's check --strict
    # (the orphan-doc reachability rule).
    ("routines.md.tmpl", "docs/ROUTINES.md"),
    # The multi-repo reading path (ORDER 016 seat-item 4 — provenance
    # superbot Q-0272, docs/fleet-reading-path.md's own kit-graduation
    # clause): the standing read-authorization, the one-command fleet
    # orient, the sibling/truth-file map, the tiered depth ladder, and the
    # truth rules — so no session burns turns re-discovering that its
    # fleet is readable (the 2026-07-12 incident: ~3 turns lost to
    # re-derivation). Slot-driven (fleet_dark_repos / fleet_status_command
    # / fleet_siblings — none critical, so the graduation gate is
    # unaffected); routed from the AGENT_ORIENTATION template like its
    # CAPABILITIES/SKILLS/ROUTINES siblings so the plant never orphans an
    # adopter's check --strict (the orphan-doc reachability rule), and
    # deliberately NOT in the K0 boot set — Q-0272 doctrine keeps the path
    # routed, not front-loaded.
    ("reading-path.md.tmpl", "docs/reading-path.md"),
    ("ideas-README.md.tmpl", "docs/ideas/README.md"),
    ("session-journal.md.tmpl", ".session-journal.md"),
    # The fleet coordination protocol (band KL-8, spec: superbot
    # docs/planning/fleet-coordination-protocol-2026-07-09.md §2): committed
    # git files are the only medium Projects share, so every adopted repo
    # gets the control/ bus — the manager-written inbox, the project-written
    # status heartbeat, and the local protocol contract. Root-level on
    # purpose (a bus, not documentation): _adopt_dest's docs_root remap
    # never applies.
    ("control-README.md.tmpl", "control/README.md"),
    ("control-inbox.md.tmpl", "control/inbox.md"),
    ("control-status.md.tmpl", "control/status.md"),
    # The kit-owned work-claim convention (EAP program review §6.4): one
    # file per claim under control/claims/ — the measured 0%-conflict
    # layout (vs ~98% for a shared-append ledger; superbot
    # tools/sim/claim_layout_sim.py). The planted README both documents the
    # convention and makes the directory exist; check_claims enforces it
    # (advisory-only) with a legacy-location compat window for pre-§6.4
    # homes (docs/owner/claims/, root claims/). Shared across lanes like
    # inbox.md/README.md — a --lane adopt never re-plants it.
    ("control-claims-README.md.tmpl", "control/claims/README.md"),
    # The setup-script contract hook (EAP program review §6.5): every fleet
    # environment's archetype setup shim prefers a repo's own
    # scripts/env-setup.sh (fleet-manager environments/templates/
    # setup-universal.sh), so the kit plants the contract-conformant hook —
    # always exit 0, defensive posture, no secret values, guarded installs.
    # Slot-free by design: a shell file must never carry the markdown
    # UNRENDERED banner, and shell `$var` syntax must never read as an
    # interview slot (tests pin both). Root-level on purpose (a hook the
    # environment shim executes, not documentation): _adopt_dest's docs_root
    # remap never applies. check_setup_script is the enforcer half
    # (advisory-only); skip-if-exists keeps every hand-rolled script.
    ("env-setup.sh.tmpl", "scripts/env-setup.sh"),
]

# State key holding {planted relpath: sha256 hex} for every doc the kit last
# wrote (planted by adopt, or re-rendered in place by `render --live`).
# "Consumer-untouched" is decided by comparing a doc's current hash to this
# record — never by re-rendering old templates, whose slot/banner/date
# substitution makes byte-matching impossible (founding plan §4.3). `upgrade`
# reads it to classify planted-doc drift; installs predating the record have
# no hashes and are honestly treated as consumer-diverged.
DOC_HASHES_STATE_KEY = "planted_doc_hashes"


def _sha256_text(text: str) -> str:
    """Return the sha256 hex digest of ``text`` (utf-8)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def record_doc_hash(backend: Any, relpath: str, text: str) -> None:
    """Record ``text``'s sha256 under ``relpath`` in the planted-doc hash map."""
    hashes = dict(backend.get(DOC_HASHES_STATE_KEY) or {})
    hashes[relpath] = _sha256_text(text)
    backend.set(DOC_HASHES_STATE_KEY, hashes)


def doc_is_untouched(backend: Any, relpath: str, current_text: str) -> bool:
    """True when ``current_text`` still matches the recorded kit-written hash."""
    hashes = backend.get(DOC_HASHES_STATE_KEY) or {}
    recorded = hashes.get(relpath)
    return recorded is not None and recorded == _sha256_text(current_text)


BACKUP_DIRNAME = "backup"

# Lane names become path components (`control/status-<lane>.md`) and config
# entries, so the charset is deliberately tight: no separators, no dots, no
# spaces — nothing that could escape control/ or read ambiguously in a list.
_LANE_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")

SINGLE_HEARTBEAT_RELPATH = "control/status.md"


def lane_status_relpath(lane: str) -> str:
    """Return the per-lane heartbeat relpath (`control/status-<lane>.md`)."""
    return f"control/status-{lane}.md"


def lane_drift_advisory(heartbeat_files: list[str]) -> str | None:
    """Return the plain-adopt lane-drift advisory line, or ``None``.

    The ``adopt --lane`` inverse gap (idea 2026-07-10, the #103 rider): a
    **plain** adopt (no ``--lane``) into a repo whose ``heartbeat_files``
    already names lane files plants the singular ``control/status.md`` seed
    *without declaring it* — the file exists on disk but no gate validates
    it, exactly the half-declared state the ORDER 004 empty-list fail-safe
    exists to prevent, recreated by the one hand-path left into the bus.

    Lane-shaped means: a non-empty list that differs from the untouched
    default ``[SINGLE_HEARTBEAT_RELPATH]``. An empty list is NOT lane-shaped
    — it falls back to the default at every consumer (the
    ``heartbeat_files`` doctrine), so the singular seed it receives is the
    declared one. Advisory only, never a refusal: a deliberate singular
    adopt into a lane-shaped repo may be intended (e.g. a consolidating
    Project), so the caller prints the nudge and plants anyway.
    """
    if not heartbeat_files or heartbeat_files == [SINGLE_HEARTBEAT_RELPATH]:
        return None
    return (
        f"ADVISORY — this repo is lane-shaped (heartbeat_files: "
        f"{heartbeat_files}) — did you mean `adopt --lane <name>`? "
        f"Continuing with the singular control/status.md (advisory, "
        f"not a refusal)."
    )


def validate_lane_name(lane: str) -> str:
    """Return ``lane`` unchanged, or raise ``ValueError`` for an unsafe name.

    Runs before any write: a lane name is interpolated into a planted path
    and into ``heartbeat_files``, so a bad one must refuse the whole adopt,
    never plant-then-apologize.
    """
    if not _LANE_NAME_RE.fullmatch(lane):
        raise ValueError(
            f"invalid lane name {lane!r} — use letters/digits/hyphen/underscore "
            "(it becomes control/status-<lane>.md)",
        )
    return lane


def _register_lane_heartbeat(
    root: Path,
    config: Config,
    lane: str,
    report: list[str],
) -> bool:
    """Register the lane's heartbeat in ``config.heartbeat_files`` (in place).

    Returns True when the config changed (the caller persists it). Rules,
    all idempotent:

    - already listed → nothing to do (re-adopt safe);
    - the list is still the untouched default (``control/status.md``) and the
      singular file does NOT exist on disk (a lane-shaped repo from the
      start — the ``--lane`` adopt never planted it) → the lane file
      *replaces* the default entry, because the status gate treats every
      listed heartbeat as mandatory and must not hold strict RED on a
      singular file no Project owns;
    - otherwise (a first Project already beats on ``control/status.md``, or
      a custom list names sibling lanes) → *append*, never dropping another
      lane's declared heartbeat (one-writer-per-file scales by splitting).

    An empty configured list means "the default" at every consumer
    (misconfiguration never silently disables the gate), so it is expanded
    to the default before the rules above apply.
    """
    lane_rel = lane_status_relpath(lane)
    files = list(config.heartbeat_files) or [SINGLE_HEARTBEAT_RELPATH]
    if lane_rel in files:
        report.append(f"lane: {lane} — heartbeat already declared ({lane_rel})")
        return False
    if files == [SINGLE_HEARTBEAT_RELPATH] and not (
        root / SINGLE_HEARTBEAT_RELPATH
    ).exists():
        files = [lane_rel]
    else:
        files.append(lane_rel)
    config.heartbeat_files = files
    report.append(
        f"lane: {lane} — heartbeat_files now {files} (substrate.config.json)",
    )
    return True

_DIST_VERSION_RE = re.compile(r"bootstrap v(\d[^\s]*)")


def dist_version(text: str) -> str | None:
    """Parse the version stamp out of a single-file bootstrap's header line."""
    first_line = text.split("\n", 1)[0]
    match = _DIST_VERSION_RE.search(first_line)
    return match.group(1) if match else None


def archive_dist(
    root: Path,
    config: Config,
    dist_file: Path,
    report: list[str],
) -> Path | None:
    """Bank ``dist_file`` under ``<state_dir>/backup/bootstrap-<version>.py``.

    The §4.3 ordering constraint: an upgrade's planted-doc diff needs the OLD
    dist's templates to still exist when it runs, so *both* ``adopt`` and
    ``upgrade`` archive the running dist before anything could overwrite it —
    the archive exists from v1.0.0 onward. Pre-stamp dists archive as
    ``bootstrap-unknown.py``. Idempotent: an identical existing archive is
    left alone; None when there is no single file to archive (source layout).

    **Never overwrite, never silently accept** (queued fix 2, wave B'
    verification): a pre-existing archive at the target name is
    hash-verified against the bytes about to be banked. Identical → the
    explicit ``(already banked)`` line. Different → the earlier bank is a
    rollback source someone may still need (two unstamped dists both name
    ``bootstrap-unknown.py``; a re-tagged dist can collide on a version
    name), so the new bytes bank under a content-hash-suffixed dedup name
    and the collision is reported — the pre-existing archive is left
    byte-untouched.
    """
    if not dist_file.is_file():
        return None
    text = dist_file.read_text(encoding="utf-8")
    version = dist_version(text) or "unknown"
    dest = root / config.state_dir / BACKUP_DIRNAME / f"bootstrap-{version}.py"
    rel = f"{config.state_dir}/{BACKUP_DIRNAME}/bootstrap-{version}.py"
    if dest.exists():
        if dest.read_text(encoding="utf-8") == text:
            # Never silent on the idempotent path: an upgrade whose OLD dist
            # was already banked (a prior adopt/check pass, or a re-run) must
            # still account for it explicitly, or the report's only
            # `archived:` line names the NEW version and readers conclude the
            # old dist was never banked — the exact doubt the archive-first
            # covenant exists to remove (field-reported three times, v1.6.0
            # rollout).
            report.append(f"archived: {rel} (already banked)")
            return dest
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]
        dedup_name = f"bootstrap-{version}.{digest}.py"
        dedup = dest.with_name(dedup_name)
        dedup_rel = f"{config.state_dir}/{BACKUP_DIRNAME}/{dedup_name}"
        if dedup.exists() and dedup.read_text(encoding="utf-8") == text:
            report.append(f"archived: {dedup_rel} (already banked)")
            return dedup
        atomic_write_text(dedup, text)
        report.append(
            f"archived: {dedup_rel} (name collision: {rel} already exists "
            "with DIFFERENT content — banked under a content-hash suffix; "
            "the pre-existing archive was NOT overwritten)",
        )
        return dedup
    atomic_write_text(dest, text)
    report.append(f"archived: {rel}")
    return dest


_ADOPT_NEXT_STEPS = (
    "next steps: run `bootstrap ask` to see the pending interview questions, "
    "answer them and fill the planted docs in place (`bootstrap render --live`), and set "
    "the integration mode with `bootstrap mode <observe|guided|active>`."
)

# First line doubles as the removal marker `strip_unrendered_banner` keys off.
UNRENDERED_BANNER_FIRST_LINE = (
    "> ⚠️ **UNRENDERED SLOTS BELOW — run `python3 bootstrap.py ask`.**"
)
_UNRENDERED_BANNER = (
    UNRENDERED_BANNER_FIRST_LINE + "\n"
    "> Every `${...}` token in this file is an unfilled interview slot, not\n"
    "> project truth. Fill: `bootstrap answer <slot> <value...>`, then\n"
    "> `bootstrap render --live` (fills in place and removes this banner).\n"
    "> Prose without `${...}` tokens is live guidance already.\n\n"
)


def with_unrendered_banner(text: str) -> str:
    """Prepend the loud UNRENDERED banner when ``text`` has unfilled slots.

    An inert-looking doc was the measured Phase-2.5 failure mode: raw
    ``${...}`` placeholders read as non-actionable scaffolding and only cost
    orientation. The banner names what the tokens are and the exact two
    commands that fill them; a fully-rendered doc gets no banner.
    """
    if not find_placeholders(text):
        return text
    return _UNRENDERED_BANNER + text


def strip_unrendered_banner(text: str) -> str:
    """Remove the adopt-time banner (used once a file has no placeholders)."""
    if not text.startswith(UNRENDERED_BANNER_FIRST_LINE):
        return text
    lines = text.split("\n")
    index = 0
    while index < len(lines) and lines[index].startswith(">"):
        index += 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    return "\n".join(lines[index:])


def _vendor_bootstrap(root: Path, report: list[str]) -> str:
    """Vendor the running single-file bootstrap into ``root``; return hook path.

    The staged hook commands run ``<interpreter> bootstrap.py hook <event>``
    relative to the host repo root — in the Phase-2.5 A/B the file was never
    there, so every staged hook pointed outside the target repo (the second
    G2 failure cause). When adopt runs *as* the single-file ``bootstrap.py``,
    copy it to the target root (skip-if-exists, like every plant) so those
    commands resolve. Running from the source/pip layout there is no single
    file to vendor: fall back to an existing root copy, else the absolute
    path of the running entry point, else the documented bare-name contract
    (the hooks README fill-table row covers relocation).
    """
    at_root = root / "bootstrap.py"
    entry = Path(sys.argv[0]).resolve() if sys.argv and sys.argv[0] else None
    is_bootstrap_entry = (
        entry is not None and entry.name == "bootstrap.py" and entry.is_file()
    )
    # A target that already contains the *generating* dist/bootstrap.py — the
    # kit repo itself, operating on itself as consumer #0 (§3.3) — must not
    # gain a vendored root duplicate: it would silently drift from the
    # CI-byte-pinned dist file (KL-0 friction guard, 2026-07-09). Hook
    # commands point at the dist copy instead.
    dist_copy = root / "dist" / "bootstrap.py"
    if (
        is_bootstrap_entry
        and not at_root.exists()
        and dist_copy.is_file()
        and entry == dist_copy.resolve()
    ):
        return "dist/bootstrap.py"
    if not at_root.exists() and is_bootstrap_entry and entry != at_root:
        _adopt_plant(
            at_root,
            "bootstrap.py",
            entry.read_text(encoding="utf-8"),
            report,
        )
    if at_root.exists():
        return "bootstrap.py"
    if is_bootstrap_entry:
        return str(entry)
    return "bootstrap.py"


def _adopt_dest(relpath: str, config: Config) -> str:
    """Remap the plan's ``docs/`` prefix onto the host's configured docs root."""
    prefix = "docs/"
    if relpath.startswith(prefix) and config.docs_root != "docs":
        return f"{config.docs_root}/{relpath[len(prefix) :]}"
    return relpath


def _adopt_plant(path: Path, relpath: str, text: str, report: list[str]) -> bool:
    """Write ``text`` at ``path`` unless it exists; report planted/kept.

    Returns True when the file was actually written (so callers can record
    provenance — e.g. the planted-doc hash — only for kit-written content).
    """
    if path.exists():
        report.append(f"kept: {relpath}")
        return False
    atomic_write_text(path, text)
    report.append(f"planted: {relpath}")
    return True


def _adopt_stage(path: Path, relpath: str, text: str, report: list[str]) -> None:
    """Write a staged (generated, regenerable) artifact and report it."""
    atomic_write_text(path, text)
    report.append(f"staged: {relpath}")


def _staged_previous_text(path: Path) -> str | None:
    """Return a staged artifact's pre-regen bytes, or None when absent.

    The three-way carve-out compare's old-template recovery source: read
    BEFORE :func:`_adopt_stage` overwrites the staged copy with the new
    render. Unreadable honestly equals absent — the consumer degrades to
    the two-way compare rather than crashing.
    """
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


# Provenance marker for the retroactively-merged model doctrine (the
# search-hygiene plant pattern): appended entries sit under one comment
# naming their origin, so a host reading its own README knows which
# paragraph the kit owns.
MODEL_DOCTRINE_MARKER = (
    "<!-- substrate-kit: model-attribution doctrine "
    "(family-level names — ORDER 012) -->"
)

# The doctrine's detection phrase — one distinctive substring shared by the
# fresh-plant render and the retroactive merge, so the two paths can never
# drift apart on "is it already there?".
_MODEL_DOCTRINE_PHRASE = "family-level model name your own harness/environment reports"


def _doctrine_phrase_present(text: str) -> bool:
    """Emphasis-blind presence test for :data:`_MODEL_DOCTRINE_PHRASE`.

    The v1.10.0 wave found the exact-substring test emphasis-blind
    (websites #105): a hand-merged doctrine carried Markdown emphasis
    INSIDE the phrase ("…model name **your own harness/environment reports
    this session**"), so the match missed it and the retroactive merge
    appended a harmless near-duplicate paragraph. Strip the Markdown
    emphasis characters (``*`` ``_`` and backticks) and collapse
    whitespace (a reflowed hand-merge is still the same doctrine) before
    the substring test. Stripping can only join characters ACROSS a
    removed run, never split words, so a false positive still requires
    the phrase's exact words in order.
    """
    normalized = re.sub(r"[*_`]", "", text)
    normalized = re.sub(r"\s+", " ", normalized)
    return _MODEL_DOCTRINE_PHRASE in normalized


def _model_doctrine_text() -> str:
    """The ORDER 012 family-level model-attribution doctrine, one paragraph.

    Composed in one place for both consumers: the fresh
    ``.sessions/README.md`` plant embeds it inline, and
    :func:`_merge_model_doctrine` appends it (under
    :data:`MODEL_DOCTRINE_MARKER`) to READMEs planted before the doctrine
    existed — the v1.9.0 wave found 4 adopters needing exactly that
    hand-merge because the PR #170 render was not retroactive.
    """
    return (
        f"The `{MODEL_LINE_NEEDLE}` model segment is the **{_MODEL_DOCTRINE_PHRASE} "
        "this session** "
        "(e.g. `fable-5`, `opus-4.8`, `sonnet-5`) — the committed card's "
        "self-report is the attribution ground truth. Never copy it from "
        "an external surface (schedule/Routines screens are evidenced to "
        "misattribute), and never record an exact model ID — family-level "
        "names only, never an exact model-ID token (dated or not)."
    )


def _merge_model_doctrine(
    root: Path,
    config: Config,
    report: list[str],
) -> None:
    """Append the model doctrine to a pre-existing ``.sessions/README.md``.

    The PR #170 doctrine render only reached FRESH plants — skip-if-exists
    left every already-planted README without it, and the v1.9.0
    distribution wave had to regen/hand-merge 4 adopters. Retroactive now,
    with the same append-only/provenance covenant as the search-hygiene
    plants: existing content is preserved byte-for-byte (host edits are
    host policy), the appended paragraph sits under
    :data:`MODEL_DOCTRINE_MARKER`, re-runs are idempotent (the
    detection phrase is shared with the fresh render, so a v1.9.0+ plant
    is already "present"), and an unreadable file is skipped + reported,
    never destroyed. No-op when the host's markers don't require the
    Model line — doctrine without the needle would be noise.
    """
    if not any(
        m.get("needle") == MODEL_LINE_NEEDLE for m in config.session_markers
    ):
        return
    relpath = f"{config.sessions_dir}/README.md"
    path = root / config.sessions_dir / "README.md"
    if not path.is_file():
        return
    try:
        existing = path.read_text(encoding="utf-8")
    except OSError:
        report.append(
            f"skipped: {relpath} (unreadable — model doctrine not merged)",
        )
        return
    if _doctrine_phrase_present(existing):
        return
    chunk = ""
    if not existing.endswith("\n"):
        chunk += "\n"
    chunk += "\n" + MODEL_DOCTRINE_MARKER + "\n" + _model_doctrine_text() + "\n"
    atomic_write_text(path, existing + chunk)
    report.append(
        f"merged: {relpath} (model-attribution doctrine appended; "
        "existing content preserved)",
    )


def _adopt_sessions_readme(markers: list[dict[str, str]]) -> str:
    """Compose the one-paragraph ``.sessions/README.md`` (born-red convention).

    Each marker renders as ``label (`needle`)`` — the exact byte-form the
    session-log checker scans for, not just its human name. Labels alone were
    the run-1 ON-arm false-red (idea model-line-checker-false-red-2026-07-09):
    a cold session that read this README learned "Model line" but had no way
    to learn the ``📊 Model:`` needle, wrote a reasonable ``> **Model:**``
    line, and stayed red against a card that visibly carried a Model line.
    """
    pairs = ", ".join(
        f"{m['label']} (`{m['needle']}`)" if m.get("needle") else m["label"]
        for m in markers
        if m.get("label")
    )
    pairs = pairs or "(no markers configured)"
    # Attribution ground truth (fleet standing rule, ORDER 012 / fm model
    # matrix 2026-07): the model segment is the FAMILY-LEVEL name the
    # session's own harness reports — self-report in the committed card is
    # the only reliable attribution surface. Rendered only when the host's
    # markers actually require the Model line.
    model_doctrine = ""
    if any(m.get("needle") == MODEL_LINE_NEEDLE for m in markers):
        model_doctrine = " " + _model_doctrine_text()
    return (
        "# Session logs\n\n"
        "Per-session logs live here as `<date>-<slug>.md`, newest first. "
        "Create the log as the session's FIRST commit with a born-red status "
        "(`> **Status:** `in-progress``) so in-flight work is visible to "
        "parallel sessions, then flip it to `complete` as the deliberate LAST "
        "step once the close-out is written — a half-done session never reads "
        "as finished. Before it counts as complete, a log must carry these "
        "markers, each written with its exact backticked byte-form: "
        f"{pairs}.{model_doctrine}\n\n"
        "If the card is missing at session end, the kit **auto-drafts** one "
        "from evidence (files touched, git HEAD movement, the verify "
        "command); an in-progress card missing its close-out gets the "
        "drafted section appended. A draft is a starting point, not a "
        "close-out: verify the evidence, resolve every `[[fill:]]` slot, "
        "then flip the Status badge — unresolved slots (and the `drafted` "
        "status) keep the card counting incomplete.\n\n"
        "**Guard recipes:** when a card records friction-to-guard material "
        "for a *later* session (a deferred fix, a flagged footgun), carry a "
        "one-line **guard recipe** naming the code anchors — function + file "
        "+ the test target — not just the symptom. A symptom-only entry "
        "costs the next session a re-derivation grep pass; a recipe lets it "
        "land the guard in minutes.\n"
    )


def ci_snippet() -> str:
    """Return the staged, fully-commented GitHub-Actions-style CI example.

    Everything is commented out: the host copies it into
    ``.github/workflows/`` and uncomments/adjusts deliberately — the kit never
    installs live CI.
    """
    return (
        "# Example GitHub-Actions-style quality gate for a substrate-kit host.\n"
        "# Copy into .github/workflows/, uncomment, and adjust the interpreter\n"
        "# and bootstrap path to match your repo.\n"
        "#\n"
        "# `bootstrap.py check --strict` runs every kit checker in one pass:\n"
        "# docs hygiene (badges / links / reachability), session-log markers,\n"
        "# namespace shadowing, seam authority, orientation budget, the\n"
        "# decision ledger, and the control/ status heartbeat.\n"
        "#\n"
        "# Coordination-only writes (control/** heartbeats) should skip heavy\n"
        "# suites — but if a check is REQUIRED, use an in-job short-circuit\n"
        "# (see the staged substrate-gate.yml's control lane), never\n"
        "# `paths-ignore`: a required context that never reports stays\n"
        "# pending and blocks auto-merge.\n"
        "#\n"
        "# NOTE: the INSTALLED .github/workflows/substrate-gate.yml is\n"
        "# KIT-OWNED — adopt/upgrade regenerates it in place and hand edits\n"
        "# are overwritten. Host-specific CI belongs in a separate workflow\n"
        "# (a copy of this example is a good home).\n"
        "#\n"
        "# name: substrate-quality\n"
        "# on:\n"
        "#   pull_request:\n"
        "#   push:\n"
        "#     branches: [main]\n"
        "# jobs:\n"
        "#   substrate-check:\n"
        "#     runs-on: ubuntu-latest\n"
        "#     steps:\n"
        "#       - uses: actions/checkout@v5\n"
        "#       - name: substrate checks\n"
        "#         run: python3 bootstrap.py check --strict\n"
    )


LIVE_CI_RELPATH = ".github/workflows/substrate-gate.yml"

# Characters a verify_command may carry and still be embedded verbatim in the
# generated gate's `run: |` block. A conservative allowlist on purpose: the
# slot is free prose routed into markdown (templates/CLAUDE.md), so values
# like websites' real one — a pytest line with "(all four service suites)"
# annotations — are documentation, not shell; embedding one would red every
# PR at that adopter with a syntax error, not a test failure. Rejected values
# fall back to the hardened pytest step (never a broken workflow), and adopt
# reports the fallback so the divergence stays visible. No newlines (YAML
# block integrity), no `$`/backticks/parens/redirects/globs — plain commands
# joined by spaces, `&&`, `|`, or `;` all pass.
_GATE_TEST_COMMAND_SAFE_RE = re.compile(r"^[A-Za-z0-9 ._/:=,;&|'\"-]+$")


def _is_default_pytest_command(command: str, interpreter: str) -> bool:
    """True when ``command`` adds nothing over the planted pytest step.

    The hardened fallback step already runs ``<interpreter> -m pytest tests/
    -q`` (with a tests/-absent self-skip and dependency installs), so a
    verify_command that is just pytest — bare, or ``-m pytest`` on the
    gate's/derive's interpreter, with at most ``tests/`` / ``-q`` arguments
    (the exact shapes ``derive.detect_verify_command`` seeds and the #403
    step runs) — keeps the fallback: it is strictly more robust than an
    inlined equivalent. Anything else (extra paths, flags, chained
    commands) is a real divergence worth honoring.
    """
    tokens = command.split()
    for prefix in (
        [interpreter, "-m", "pytest"],
        ["python3", "-m", "pytest"],
        ["pytest"],
    ):
        if tokens[: len(prefix)] == prefix:
            rest = tokens[len(prefix) :]
            return all(token in ("tests/", "tests", "-q") for token in rest)
    return False


def gate_test_command(
    state: dict[str, Any],
    interpreter: str = "python3",
) -> str | None:
    """Return the verify_command the gate's test step should run, or None.

    None means "plant the hardened pytest fallback" (#403's step, unchanged
    bytes). The interview's ``verify_command`` slot drives the step only when
    ALL of:

    - the slot is **filled** — user-confirmed. A ``provisional`` value is
      either derive's own pytest default (nothing to honor) or an
      unconfirmed self-answer (``ASSUMED: …`` is not shell), and the
      interview contract says provisional answers never count until
      confirmed;
    - the value is **gate-safe** — single line, no unfilled ``${...}``
      placeholder, and within :data:`_GATE_TEST_COMMAND_SAFE_RE` (the slot
      is free prose; only a value that is unambiguously a runnable command
      may be embedded in a workflow every PR executes);
    - the value is **non-default** — a plain pytest invocation keeps the
      fallback step, which is strictly more robust (tests/-absent
      self-skip, dependency installs) than inlining the same command.

    Called with the same state document by adopt's gate render and
    upgrade's read-only carve-out rescan, so the expected gate text can
    never disagree between the writer and the scanner.
    """
    slots = state.get("slots")
    if not isinstance(slots, dict) or slots.get("verify_command") != "filled":
        return None
    values = state.get("slot_values")
    entry = values.get("verify_command") if isinstance(values, dict) else None
    value = entry.get("value") if isinstance(entry, dict) else None
    if not isinstance(value, str):
        return None
    command = value.strip()
    if not command or "\n" in command or "${" in command:
        return None
    if not _GATE_TEST_COMMAND_SAFE_RE.match(command):
        return None
    if _is_default_pytest_command(command, interpreter):
        return None
    return command


def _strip_parenthetical(command: str) -> str:
    """Drop ``(...)`` annotation segments and collapse the whitespace.

    The observed gate-unsafe shape is a runnable command decorated with
    prose in parentheses (websites' real verify line carries ``(all four
    service suites)`` / ``(kit gate)`` annotations). Stripping them is the
    one mechanical rewrite that reliably recovers the runnable command;
    anything cleverer risks suggesting a command the owner never wrote.
    """
    stripped = command
    while True:
        reduced = re.sub(r"\s*\([^()]*\)", "", stripped)
        if reduced == stripped:
            break
        stripped = reduced
    return " ".join(stripped.split())


def gate_test_command_advisory(value: str, interpreter: str = "python3") -> str | None:
    """Return a gate-safety NOTE for a just-filled verify_command, or None.

    The answer-time half of the #405 honored-lane contract: a prose-y
    verify answer records silently, and its gate-unsafety otherwise
    surfaces only as the *absence* of the honored test step at the next
    adopt/upgrade — the owner never learns their verify line cannot drive
    CI. This runs :func:`gate_test_command`'s gate-safety legs (newline,
    unfilled ``${...}``, the :data:`_GATE_TEST_COMMAND_SAFE_RE` allowlist)
    at the moment the value is typed, when fixing it costs one retype
    instead of an adopt-cycle round-trip.

    None means nothing to say: the value is gate-safe — it either drives
    the gate's test step verbatim or is a default pytest invocation whose
    hardened fallback step is strictly more robust (nothing is lost either
    way). A returned NOTE names the offending shape and, when stripping
    parenthetical annotations recovers a gate-safe command, the runnable
    rewrite. Advisory prose only — the recorded answer and every exit code
    stay untouched (the slot is still a fine CLAUDE.md verify line).
    """
    command = value.strip()
    if not command:
        return None
    if "\n" in command:
        reason = "it spans multiple lines (the gate embeds a single command line)"
    elif "${" in command:
        reason = "it carries an unfilled `${...}` placeholder"
    elif not _GATE_TEST_COMMAND_SAFE_RE.match(command):
        offending = sorted(
            {ch for ch in command if not _GATE_TEST_COMMAND_SAFE_RE.match(ch)}
        )
        reason = (
            "it carries characters outside the gate-safe set: "
            + " ".join(offending)
        )
    else:
        return None
    note = (
        "NOTE gate-safety: this verify_command will NOT drive the "
        f"substrate-gate's test step — {reason}; the gate keeps the "
        "hardened pytest fallback."
    )
    # A rewrite is offered only for single-line values: the whitespace
    # collapse would join multi-line commands into one broken line, and a
    # wrong suggestion is worse than none.
    rewrite = "" if "\n" in command else _strip_parenthetical(command)
    if (
        rewrite
        and rewrite != command
        and "${" not in rewrite
        and _GATE_TEST_COMMAND_SAFE_RE.match(rewrite)
    ):
        if _is_default_pytest_command(rewrite, interpreter):
            note += (
                " Stripped of the annotations it is the default pytest "
                "invocation — the fallback already runs the equivalent, "
                "so nothing is lost (annotations belong in docs)."
            )
        else:
            note += (
                " Runnable rewrite that would drive it: "
                f'`answer verify_command "{rewrite}"` '
                "(annotations belong in docs, not the command)."
            )
    else:
        note += (
            " Re-record a plain runnable command to drive the gate "
            "(prose annotations are documentation, not shell)."
        )
    return note


def live_ci_workflow(
    interpreter: str = "python3",
    sessions_dir: str = ".sessions",
    test_command: str | None = None,
) -> str:
    """Return the LIVE (uncommented) CI gate workflow — the locked door.

    Unlike :func:`ci_snippet` (a commented example the host installs by hand),
    this is a working GitHub-Actions workflow ``adopt --wire-enforcement``
    writes into ``.github/workflows/``. It runs
    ``bootstrap.py check --strict --require-session-log`` on every pull request,
    so the merge is **held red** until the session's journal is written and the
    whole hygiene suite passes. This is the forcing function that makes the
    memory ritual non-optional: a nag can be ignored, a failing required check
    cannot. `fetch-depth: 0` gives the checkout the history the diff needs.
    A docs-only or bot PR that shouldn't need a session card is handled by the
    host adding a `paths-ignore:` or a label carve-out — kept strict by default
    on purpose (the discipline is the point).

    The gate step is **PR-diff-aware**: a fresh CI checkout flattens every file
    mtime to checkout time, so the engine's newest-by-mtime card guess is
    arbitrary in CI (the kit's own CI once carried a git-mtime-restore shim for
    exactly this). The workflow instead derives the cards from what the PR/push
    diff touches under ``sessions_dir`` — **every card in the diff, never a
    single picked one**: the old ``tail -1`` picker graded only the
    last-sorted card, so a PR that ADDED an in-progress card and MODIFIED a
    later-sorting sibling shipped the in-progress card GREEN (the multi-card
    shadowing loophole, venture-lab #33 head 798a3d0, run 29144734514 —
    partially reopening the superbot-games #40 class the v1.10.0 hold
    closed). When the diff names **no card** the step passes
    an explicitly named, nonexistent sentinel **without**
    ``--require-session-log`` — per the engine contract an explicitly named
    absent card is ADVISORY. (The previous behaviour — omitting the argument —
    was NOT fail-open in CI: the engine's newest-by-mtime fallback latched
    onto the mid-session in-progress card and redded every unrelated PR;
    adopter live-fire, gba-homebrew PR #3, 2026-07-10.) **Every** card
    **ADDED** by the PR (a born-red heartbeat:
    first-commit-carries-an-in-progress-card conventions make in-progress
    the REQUIRED state at birth) gates via the
    absent sentinel plus ``--added-card`` — the engine grades each card by
    what it DECLARES: an in-progress/drafted card is the born-red **HOLD**
    (red until it flips complete), a badge-less or complete-but-malformed
    card reds on grammar, and a complete well-formed card passes; ANY added
    card holding holds the whole step. The hold
    tier closed the v1.9.0 wave's card-only loophole: the then-current lane
    fully EXEMPTED an in-progress added card, so a card-only born-red PR
    with auto-merge pre-armed went green and merged 24 seconds after open —
    before the session built anything (superbot-games PR #40). Completeness
    is still never graded mid-flight (the gba-homebrew PR #2 lesson —
    born-red is the REQUIRED state at birth); the hold is a single
    designed-state finding with a HOLD-by-design banner, not a marker red.
    Sibling cards **MODIFIED** by a diff that also adds card(s) gate through
    the **same** ``--require-session-log`` locked door as a modified-only
    diff — the added card is still the gate's subject via its own
    ``--added-card`` lane, so a sibling verdict can only ADD red, never
    substitute for the added card's (grading siblings is strictly tighter
    than the earlier advisory-only logging and cannot reintroduce the
    tail-1 shadowing; supersedes the #187 advisory-sibling design —
    external review #226 finding G-1 showed a PR adding one good card
    could silently flip a sibling to in-progress, or strip its markers,
    and still merge). A diff that **only
    modifies** cards (every session close-out flips one) keeps the full
    ``--require-session-log`` locked door on EACH modified card, so a
    close-out that forgot to flip ``complete`` still reds. Session cards
    **DELETED** by the diff are a hard red on sight — session memory is
    append-only, and the card lists are built with ``--diff-filter=d``
    (deletions excluded), so before this guard a deletion-only PR fell to
    the no-card advisory path and could merge while erasing session
    memory (external review #226 finding G-2; same guard mirrored in the
    kit's own dogfood gate). The
    diff-selection fixes validated live across gba-homebrew PRs #3–#14.
    One deliberate exception
    (queued fix 3, venture-lab #14): a card ADDED by a PR that ALSO touches
    this gate workflow file itself gates through the full locked door —
    GitHub runs a ``pull_request`` workflow from the PR head, so the PR that
    regenerates the gate runs the NEW gate mid-PR, and without the exception
    the regen could silently loosen an added card's hold MID-PR. Hold
    semantics may only tighten, never loosen, within the PR that changes
    them; that branch also runs ``--simulate-added-card`` so the lane's
    would-be verdict stays observable on exactly the PRs that ship gate
    changes. The merge path is unchanged — flip the card ``complete``.

    **Control fast lane (KL-8):** a diff touching only ``control/**`` (a
    status heartbeat, a manager inbox append) short-circuits the job GREEN
    *in-job* — deliberately **not** a ``paths-ignore``, because when this
    check is REQUIRED a workflow that never runs leaves the context pending
    forever and auto-merge jams (the fleet-protocol heartbeat-lane lesson,
    2026-07-09). The required context always reports; coordination writes
    never pay the heavy suite and never need a session card. The lane is
    **not checker-free though**: it still runs the scoped
    ``check --strict --status-only`` heartbeat gate, because a control-only
    diff edits exactly the files ``check_status_current`` validates — the
    original lane skipped the one checker that could catch a broken/deleted
    heartbeat, deferring the red onto the next unrelated PR (the fleet
    adoption review finding, 2026-07-09). Stdlib-only on the system
    ``python3``, so the lane stays fast.

    **Kit-owned (EAP program review §6.1):** the installed copy at
    :data:`LIVE_CI_RELPATH` is a kit-owned artifact — once it exists, every
    adopt/upgrade pass regenerates it in place (see :func:`adopt` step 6b),
    so gate fixes like the two above reach installed gates on
    ``bootstrap.py upgrade`` instead of stranding as hand-forked patches
    (the gba-homebrew live-fire fix had to be hand-forked precisely because
    no such ownership existed). Hand edits are overwritten; the generated
    header says so and routes host customizations to a separate workflow
    file. Host additions the regen would drop are detected, banked, and
    reported as carve-outs (see :func:`gate_carveouts` — the
    superbot-games #16 hand-added-pytest-job class).

    **Inbox append-only gate (issue #36 report 2, wired v1.7.1):** the gate
    runs the ``check --strict --status-only --inbox-base`` pure-append +
    ORDER-grammar validation whenever a PR touches ``control/inbox.md`` — on
    BOTH lanes (an inbox append rides the fast lane; a mixed PR could smuggle
    an inbox edit through the full lane). git extracts the merge-base blob in
    bash because the engine never shells out (§3.2); the step self-skips when
    the inbox is untouched, so repos without the control protocol never pay
    it. Before v1.7.1 the generated gate never wired ``--inbox-base``, so
    inbox pure-append enforcement was LATENT on every adopter (the v1.7.0
    distribution-wave finding).

    **Pytest step (the tests-blind-gate class, superbot-games #16):** a host
    can live its whole life with a green gate while its test suite never runs
    in CI — superbot-games' 73 pure-domain tests were invisible to gen-1 CI
    because the gate ran only ``check --strict``, and both lanes ASSUMED CI
    ran them (fixed consumer-side in games#16; this plants the fix kit-side).
    A convention ships with its checker; a test suite ships with its CI
    runner. The step is **always planted** and self-skips in-job when no
    ``tests/`` directory exists — the idea's simpler variant: no adopt-time
    conditional to go stale, and the gate self-heals the moment tests arrive.
    It rides the full lane only (behind the same control-fast-lane
    short-circuit — heartbeat PRs never pay a test suite), installs pytest
    plus the host's ``requirements.txt`` when present, and runs the suite on
    the same interpreter as the gate step.

    **verify_command honored (the #403 follow-on):** when ``test_command``
    is provided — the caller passing :func:`gate_test_command`'s verdict on
    the interview's ``verify_command`` slot (filled + gate-safe +
    non-default; see its docstring for why each condition exists) — the
    test step runs THAT command verbatim instead of the hardcoded pytest
    line, so the CI runner and the verify line ``templates/CLAUDE.md``
    teaches every session stop diverging (websites' four-suite line and
    non-pytest stacks were invisible to the planted step). The command is
    an owner-confirmed runnable promise, so the ``tests/``-absent self-skip
    does not apply to it (a verify command need not touch ``tests/`` at
    all); ``requirements.txt`` still installs when present, and pytest
    installs only when the command mentions it. ``test_command=None``
    keeps #403's hardened fallback byte-identical — adopters whose slot
    does not qualify see zero gate churn.
    """
    if test_command is None:
        test_step = (
            "      - name: pytest suite (a test suite ships with its CI runner; "
            "self-skips when tests/ is absent)\n"
            "        if: steps.lane.outputs.control_only != 'true'\n"
            "        # A host can live its whole life with a green gate while its\n"
            "        # tests never run in CI (superbot-games' 73 tests were\n"
            "        # invisible to gen-1 CI until games#16 hand-added a runner).\n"
            "        # Always planted, self-skips when tests/ is absent — so the\n"
            "        # gate self-heals the moment tests arrive. Full lane only:\n"
            "        # control/** heartbeat PRs never pay the test suite.\n"
            "        run: |\n"
            "          if [ ! -d tests ]; then\n"
            '            echo "no tests/ directory — pytest step skipped'
            ' (self-heals when tests/ arrives)."\n'
            "            exit 0\n"
            "          fi\n"
            "          if [ -f requirements.txt ]; then\n"
            f"            {interpreter} -m pip install --quiet -r requirements.txt\n"
            "          fi\n"
            f"          {interpreter} -m pip install --quiet pytest\n"
            f"          {interpreter} -m pytest tests/ -q\n"
        )
    else:
        pytest_install = (
            f"          {interpreter} -m pip install --quiet pytest\n"
            if "pytest" in test_command
            else ""
        )
        test_step = (
            "      - name: verify suite (the interview's verify_command drives "
            "the gate's test step)\n"
            "        if: steps.lane.outputs.control_only != 'true'\n"
            "        # The command below is this repo's own CONFIRMED\n"
            "        # verify_command interview slot — the same line the planted\n"
            "        # CLAUDE.md/CONSTITUTION teach every session to run — so the\n"
            "        # CI runner can no longer diverge from the doctrine (the\n"
            "        # #403 step hardcoded pytest). An owner-confirmed command is\n"
            "        # a runnable promise, so there is no tests/-absent self-skip\n"
            "        # here (the command need not touch tests/ at all). Change it\n"
            "        # via `bootstrap.py answer verify_command \"...\"` and the\n"
            "        # next adopt/upgrade regen. Full lane only: control/**\n"
            "        # heartbeat PRs never pay the suite.\n"
            "        run: |\n"
            "          if [ -f requirements.txt ]; then\n"
            f"            {interpreter} -m pip install --quiet -r requirements.txt\n"
            "          fi\n"
            f"{pytest_install}"
            f"          {test_command}\n"
        )
    return (
        "# substrate-kit enforcement gate (LIVE — installed by "
        "`bootstrap.py adopt --wire-enforcement`).\n"
        "# KIT-OWNED: adopt/upgrade regenerates this file in place, so\n"
        "# upstream gate fixes land here on every `bootstrap.py upgrade` —\n"
        "# hand edits are OVERWRITTEN. Put host-specific customizations\n"
        "# (e.g. a label carve-out for PRs that legitimately need no session\n"
        "# card) in a SEPARATE workflow file, never in this one.\n"
        "# Holds the merge red until the session journal is written and every\n"
        "# hygiene check passes. If this check is REQUIRED, prefer an\n"
        "# in-job short-circuit (like the control lane below) over\n"
        "# `paths-ignore`: a required context that never reports stays\n"
        "# pending and blocks auto-merge forever.\n"
        "name: substrate-gate\n"
        "on:\n"
        "  pull_request:\n"
        "  push:\n"
        "    branches: [main]\n"
        "jobs:\n"
        "  substrate-gate:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v5\n"
        "        with:\n"
        "          fetch-depth: 0\n"
        "      - name: control fast lane (control/**-only diff short-circuits green)\n"
        "        # Heartbeat/inbox commits are coordination, not code: they\n"
        "        # skip the heavy gate but the job still REPORTS green so a\n"
        "        # required context never jams auto-merge. Empty/unreadable\n"
        "        # diffs fail safe onto the full suite.\n"
        "        id: lane\n"
        "        run: |\n"
        '          if [ -n "${{ github.base_ref }}" ]; then\n'
        '            range="origin/${{ github.base_ref }}...HEAD"\n'
        "          else\n"
        '            range="${{ github.event.before }}..${{ github.sha }}"\n'
        "          fi\n"
        '          files="$(git diff --name-only "$range" 2>/dev/null || true)"\n'
        "          control_only=false\n"
        '          if [ -n "$files" ] && [ -z "$(printf \'%s\\n\' "$files" '
        "| grep -v '^control/')\" ]; then\n"
        "            control_only=true\n"
        "          fi\n"
        '          echo "control_only=$control_only" >> "$GITHUB_OUTPUT"\n'
        '          echo "control-only diff: $control_only"\n'
        "      - name: control-status gate (fast lane — a control diff must "
        "still prove its heartbeat)\n"
        "        if: steps.lane.outputs.control_only == 'true'\n"
        "        # The lane skips the heavy gate, but a control-only PR edits\n"
        "        # exactly the files the status checker validates — without\n"
        "        # this step a heartbeat-deleting control PR merges GREEN and\n"
        "        # pre-reddens the NEXT unrelated PR (kit fleet review\n"
        "        # 2026-07-09). Scoped + stdlib-only on the system python3\n"
        "        # (no setup-python): the lane stays fast, and heartbeat PRs\n"
        "        # still need no session card.\n"
        "        run: python3 bootstrap.py check --strict --status-only\n"
        "      - name: inbox append-only gate (control/inbox.md pure-append + "
        "ORDER grammar)\n"
        "        # control/inbox.md is one-writer/append-only by protocol\n"
        "        # (control/README.md): without this step a green control-only\n"
        "        # PR could rewrite or erase orders. Holds the PR red unless\n"
        "        # the inbox diff is PURE-APPEND vs the merge-base and the\n"
        "        # appended text is well-formed ORDER blocks. Runs on BOTH\n"
        "        # lanes (no lane condition): an inbox append rides the fast\n"
        "        # lane, but a mixed PR could smuggle an inbox edit through\n"
        "        # the full lane too. Stdlib-only system python3; git extracts\n"
        "        # the base blob here in bash because the engine never shells\n"
        "        # out. Self-skips when control/inbox.md is untouched.\n"
        "        run: |\n"
        '          if [ -n "${{ github.base_ref }}" ]; then\n'
        '            base="$(git merge-base "origin/${{ github.base_ref }}" HEAD)"\n'
        '            range="origin/${{ github.base_ref }}...HEAD"\n'
        "          else\n"
        '            base="${{ github.event.before }}"\n'
        '            range="${{ github.event.before }}..${{ github.sha }}"\n'
        "          fi\n"
        '          changed="$(git diff --name-only "$range" 2>/dev/null '
        "| grep -Fx 'control/inbox.md' || true)\"\n"
        '          if [ -z "$changed" ]; then\n'
        '            echo "control/inbox.md not in diff — inbox append-only '
        'gate skipped."\n'
        "          else\n"
        '            basefile="$(mktemp)"\n'
        '            git show "$base:control/inbox.md" > "$basefile" '
        "2>/dev/null || : > \"$basefile\"\n"
        "            python3 bootstrap.py check --strict --status-only "
        '--inbox-base "$basefile"\n'
        "          fi\n"
        "      - uses: actions/setup-python@v6\n"
        "        if: steps.lane.outputs.control_only != 'true'\n"
        "        with:\n"
        '          python-version: "3.x"\n'
        "      - name: substrate gate (docs + session-log required)\n"
        "        if: steps.lane.outputs.control_only != 'true'\n"
        "        # Gate on the session cards THIS PR/push touches (CI flattens\n"
        "        # mtimes, so the engine's newest-by-mtime guess is unreliable\n"
        "        # here) — EVERY card in the diff, never a single picked one:\n"
        "        # the old `tail -1` picker graded only the last-sorted card,\n"
        "        # so a PR that ADDED an in-progress card and MODIFIED a\n"
        "        # later-sorting sibling shipped the in-progress card GREEN\n"
        "        # (the multi-card shadowing loophole, venture-lab #33 head\n"
        "        # 798a3d0 — partially reopening the superbot-games #40\n"
        "        # class). No card in the diff -> pass an explicitly named,\n"
        "        # nonexistent sentinel WITHOUT --require-session-log: per the\n"
        "        # engine's contract an explicit absent card is ADVISORY,\n"
        "        # while the bare mtime fallback latches onto the mid-session\n"
        "        # in-progress card and reds every unrelated PR (adopter\n"
        "        # live-fire, gba-homebrew PR #3, 2026-07-10 — the omitted\n"
        "        # argument was never fail-open in CI). EVERY card ADDED by\n"
        "        # the PR (first-commit conventions REQUIRE an in-progress\n"
        "        # card at birth) gates via the absent sentinel +\n"
        "        # --added-card: the engine grades each card by what it\n"
        "        # DECLARES — an in-progress/drafted card is the born-red\n"
        "        # HOLD (red until it flips complete; the superbot-games #40\n"
        "        # loophole fix, where a card-only born-red PR with\n"
        "        # auto-merge pre-armed went green and merged 24 s after\n"
        "        # open), a badge-less or complete-but-malformed card reds on\n"
        "        # grammar (the venture-lab #15 false-green class), and a\n"
        "        # complete well-formed card passes; ANY added card holding\n"
        "        # holds the whole step. Completeness is never graded\n"
        "        # mid-flight (the gba-homebrew #2 lesson — born-red is the\n"
        "        # REQUIRED state at birth); the hold is a single\n"
        "        # designed-state finding with a HOLD-by-design banner.\n"
        "        # Sibling cards MODIFIED by a diff that also adds card(s)\n"
        "        # gate through the SAME --require-session-log locked door\n"
        "        # as a modified-only diff: the added card still gates via\n"
        "        # its own --added-card lane, so a sibling verdict can only\n"
        "        # ADD red, never substitute — strictly tighter than the\n"
        "        # old advisory-only logging, which let a PR adding one\n"
        "        # good card silently break a modified sibling (review\n"
        "        # #226 finding G-1; supersedes the #187 advisory design).\n"
        "        # Session cards DELETED by the diff are a hard red —\n"
        "        # session memory is append-only; the card lists use\n"
        "        # --diff-filter=d (deletions excluded), so without this a\n"
        "        # deletion-only PR fell to the no-card advisory path and\n"
        "        # merged while erasing session memory (review #226\n"
        "        # finding G-2). A diff that ONLY modifies cards\n"
        "        # (every session close-out flips one) keeps the full\n"
        "        # locked-door gate on EACH modified card, so a close-out\n"
        "        # that forgot to flip `complete` still reds. EXCEPT: when\n"
        "        # this same PR also touches THIS gate workflow file (an\n"
        "        # upgrade PR regenerating the kit-owned gate), every ADDED\n"
        "        # card keeps the FULL locked door too — the PR runs the NEW\n"
        "        # gate the moment the regen commit lands, so without this\n"
        "        # the regen itself could loosen an added card's hold MID-PR\n"
        "        # (venture-lab #14). Hold semantics may only tighten, never\n"
        "        # loosen, inside the PR that changes them; that branch also\n"
        "        # runs --simulate-added-card so the added-card lane's\n"
        "        # would-be verdict stays observable on exactly the PRs that\n"
        "        # ship gate changes. The escape is the normal one — flip\n"
        "        # the card complete.\n"
        "        run: |\n"
        '          if [ -n "${{ github.base_ref }}" ]; then\n'
        '            range="origin/${{ github.base_ref }}...HEAD"\n'
        "          else\n"
        '            range="${{ github.event.before }}..${{ github.sha }}"\n'
        "          fi\n"
        '          cards="$(git diff --name-only --diff-filter=d "$range" -- '
        f"'{sessions_dir}/*.md' ':!{sessions_dir}/README.md' 2>/dev/null)\"\n"
        '          added="$(git diff --name-only --diff-filter=A "$range" -- '
        f"'{sessions_dir}/*.md' ':!{sessions_dir}/README.md' 2>/dev/null)\"\n"
        '          deleted="$(git diff --name-only --diff-filter=D "$range" -- '
        f"'{sessions_dir}/*.md' ':!{sessions_dir}/README.md' 2>/dev/null)\"\n"
        '          gate_regen="$(git diff --name-only "$range" -- '
        f"'{LIVE_CI_RELPATH}' 2>/dev/null | tail -1)\"\n"
        '          echo "session gate cards: ${cards:-<none - advisory sentinel>}"\n'
        "          fail=0\n"
        '          if [ -n "$deleted" ]; then\n'
        "            while IFS= read -r card; do\n"
        '              [ -z "$card" ] && continue\n'
        '              echo "session card DELETED by this PR (session memory is'
        ' append-only — hard red): $card"\n'
        '            done <<< "$deleted"\n'
        "            fail=1\n"
        "          fi\n"
        '          if [ -n "$added" ]; then\n'
        "            while IFS= read -r card; do\n"
        '              [ -z "$card" ] && continue\n'
        "              if printf '%s\\n' \"$added\" | grep -Fxq -- \"$card\";"
        " then continue; fi\n"
        '              echo "modified sibling card (locked-door gate — same'
        " door as a modified-only diff; supersedes the #187 advisory"
        ' semantics): $card"\n'
        f"              {interpreter} bootstrap.py check --strict"
        ' --require-session-log --session-log "$card" || fail=1\n'
        '            done <<< "$cards"\n'
        "            while IFS= read -r card; do\n"
        '              [ -z "$card" ] && continue\n'
        '              if [ -n "$gate_regen" ]; then\n'
        '                echo "card $card is ADDED but this PR also touches the'
        ' gate workflow itself — locked-door gate (mid-PR semantics may only'
        ' tighten; flip the card complete to merge)"\n'
        f"                {interpreter} bootstrap.py check --strict"
        ' --require-session-log --session-log "$card"'
        ' --simulate-added-card "$card" || fail=1\n'
        "              else\n"
        '                echo "card $card is newly ADDED by this PR (born-red heartbeat)'
        ' — added-card gate: in-progress HOLDs until the card flips complete;'
        ' grammar misses red"\n'
        f"                {interpreter} bootstrap.py check --strict --session-log "
        f"{sessions_dir}/__born-red-card-added__.md"
        ' --added-card "$card" || fail=1\n'
        "              fi\n"
        '            done <<< "$added"\n'
        '          elif [ -n "$cards" ]; then\n'
        "            while IFS= read -r card; do\n"
        '              [ -z "$card" ] && continue\n'
        '              echo "card $card is MODIFIED by this PR (close-out'
        ' flip) — locked-door gate"\n'
        f"              {interpreter} bootstrap.py check --strict"
        ' --require-session-log --session-log "$card" || fail=1\n'
        '            done <<< "$cards"\n'
        "          else\n"
        f"            {interpreter} bootstrap.py check --strict --session-log "
        f"{sessions_dir}/__no-card-in-diff__.md\n"
        "          fi\n"
        '          exit "$fail"\n'
        f"{test_step}"
    )


def _workflow_outline(text: str) -> dict[str, list[str]]:
    """Best-effort outline of a GitHub-Actions workflow: job id -> step labels.

    Line-based on purpose (the engine is stdlib-only — no YAML parser): job
    ids are the two-space-indented ``<id>:`` keys under a top-level ``jobs:``
    block; step labels are the ``- name:`` / ``- uses:`` list entries inside
    a job. Deeper-indented content (``run: |`` script bodies, ``with:``
    blocks) is ignored. Good enough to *detect* host additions — and the
    caller banks the full pre-regen file besides, so a parse miss can only
    under-report, never lose content.
    """
    jobs: dict[str, list[str]] = {}
    in_jobs = False
    current: str | None = None
    for raw in text.split("\n"):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            in_jobs = stripped == "jobs:"
            current = None
            continue
        if not in_jobs:
            continue
        if (
            indent == 2
            and stripped.endswith(":")
            and not stripped.startswith("-")
        ):
            current = stripped[:-1]
            jobs[current] = []
            continue
        if current is None:
            continue
        match = re.match(r"-\s+(name|uses):\s*(.+)$", stripped)
        if match is not None and indent <= 8:
            label = match.group(2).strip()
            if match.group(1) == "uses":
                label = f"uses: {label}"
            jobs[current].append(label)
    return jobs


def gate_carveouts(live_text: str, expected_text: str) -> list[str]:
    """Describe host additions in a live gate vs the kit-generated one.

    Returns one human-readable line per host-added job and per host-added
    step inside a kit job (superbot-games PR #16 hand-added its ONLY pytest
    CI job inside the kit-owned gate — a plain regen would have silently
    deleted the repo's whole test gate). Removals and edits of kit content
    are NOT reported here: the regen restores those by design; only content
    that exists in the live file and nowhere in the kit template is a
    carve-out. Empty list = nothing host-added detected.
    """
    live_jobs = _workflow_outline(live_text)
    expected_jobs = _workflow_outline(expected_text)
    expected_steps_all = {
        step for steps in expected_jobs.values() for step in steps
    }
    lines: list[str] = []
    for job, steps in live_jobs.items():
        if job not in expected_jobs:
            detail = "; ".join(steps) if steps else "no named steps"
            lines.append(f"host-added job '{job}' ({detail})")
            continue
        for step in steps:
            if step not in expected_steps_all:
                lines.append(f"host-added step '{step}' in job '{job}'")
    return lines


AUTOMERGE_ENABLER_RELPATH = ".github/workflows/auto-merge-enabler.yml"

# The advisory routing label the fleet's enabler/disarm pair honors: a PR
# carrying it is never armed (kit doctrine — see
# docs/operations/auto-merge-guards.md guards 1–2). A constant, not config
# (house-style D-7): the label is program-wide vocabulary, and a per-repo
# rename would silently split the fleet's shared review convention.
AUTOMERGE_CARVEOUT_LABEL = "do-not-automerge"

# claim/* rides alongside claude/*: control fast-lane claim PRs land on
# claim/* heads, and a claude/-only default left them green+clean but
# unarmed forever (kit PR #293, the live stall — ~2 h during the v1.15.0
# wave-A distribution until re-landed on claude/* as #297).
DEFAULT_AUTOMERGE_BRANCH_PATTERNS = ("claude/*", "claim/*")
DEFAULT_AUTOMERGE_REQUIRED_CONTEXT = "substrate-gate"


def _automerge_branch_expr(branch_patterns: list[str] | None) -> str:
    """Render the workflow-expression term matching the arming branches.

    A trailing ``*`` is a prefix match (``claude/*`` →
    ``startsWith(github.head_ref, 'claude/')``); anything else matches the
    head ref exactly. Empty/blank patterns fall back to the default —
    the ``heartbeat_files`` doctrine: a stray ``[]`` (or a pattern list of
    empty strings) must not silently widen arming to EVERY branch.
    """
    terms: list[str] = []
    for raw in branch_patterns or []:
        pattern = str(raw).strip().replace("'", "")
        if not pattern or pattern == "*":
            # A bare "*" would arm every PR on the repo — refuse the
            # footgun and let the fallback keep the agent-branch default.
            continue
        if pattern.endswith("*"):
            terms.append(f"startsWith(github.head_ref, '{pattern[:-1]}')")
        else:
            terms.append(f"github.head_ref == '{pattern}'")
    if not terms:
        return _automerge_branch_expr(list(DEFAULT_AUTOMERGE_BRANCH_PATTERNS))
    return " || ".join(terms)


def automerge_enabler_workflow(
    branch_patterns: list[str] | None = None,
    required_context: str = DEFAULT_AUTOMERGE_REQUIRED_CONTEXT,
) -> str:
    """Return the LIVE auto-merge-enabler workflow (EAP program review §6.10).

    The superbot Q-0123 pattern, generalized from this repo's own
    ``.github/workflows/auto-merge-enabler.yml``: arm GitHub-native
    auto-merge on agent PRs the moment they open, so a born-red session PR
    merges itself the instant the required check goes green — the session
    just flips its card; GitHub does the gated merge. Adopters previously
    hand-forked this workflow or lacked it; it now plants and regenerates
    exactly like :func:`live_ci_workflow` (staged always, installed live by
    ``adopt --wire-enforcement``, kit-owned once it exists — see
    :func:`adopt` step 6b).

    Safety shape carried from the origin workflow, in firing order:

    - **Same-repo guard** — never runs for fork PRs (a fork's token could
      not arm anyway; the guard keeps the failure silent instead of noisy).
    - **Branch patterns** (``branch_patterns``, config
      ``automerge.branch_patterns``) — only agent branches arm.
    - **Refuse-to-arm guard** (the KL-0/KL-1 footgun): with NO required
      status-check CONTEXTS on the base branch, arming merges the PR
      INSTANTLY — the workflow counts the base branch's required contexts
      via the rules API and refuses to arm on zero. Contexts, not rules:
      a rule with an empty context list armed-and-merged kit PR #7.
    - **Label carve-out** (:data:`AUTOMERGE_CARVEOUT_LABEL`): a labelled PR
      is never armed — checked at the job level AND re-read FRESH from the
      API after a grace beat (the kit #22 stale-payload label race; the
      label is advisory routing, the required check is the enforcement —
      docs/operations/auto-merge-guards.md).

    ``required_context`` (config ``automerge.required_context``) is
    informational — it names the gate in the log lines so an adopter reading
    the run knows WHICH check must go green / become required; the guard
    itself counts contexts generically.
    """
    branch_expr = _automerge_branch_expr(
        list(branch_patterns) if branch_patterns is not None else None,
    )
    context = (required_context or DEFAULT_AUTOMERGE_REQUIRED_CONTEXT).replace("'", "")
    return (
        "# substrate-kit auto-merge enabler (LIVE — installed by\n"
        "# `bootstrap.py adopt --wire-enforcement`).\n"
        "# KIT-OWNED: adopt/upgrade regenerates this file in place, so\n"
        "# upstream enabler fixes land here on every `bootstrap.py upgrade` —\n"
        "# hand edits are OVERWRITTEN. Put host-specific customizations in a\n"
        "# SEPARATE workflow file, never in this one.\n"
        "#\n"
        "# Arms GitHub-native auto-merge on agent PRs at open, so a born-red\n"
        "# session PR merges itself the moment the required check goes green.\n"
        "# INERT until two one-time repo settings exist (owner UI — see the\n"
        "# adopt report's repo-settings checklist):\n"
        '#   1. Settings → General → Pull Requests → "Allow auto-merge" = ON.\n'
        f"#   2. A ruleset on the default branch REQUIRING the '{context}'\n"
        "#      status check.\n"
        "# With NO required check, arming merges a PR INSTANTLY — the\n"
        "# refuse-to-arm guard below counts required contexts and refuses on\n"
        "# zero rather than inverting the gate.\n"
        "#\n"
        f"# CARVE-OUT: label `{AUTOMERGE_CARVEOUT_LABEL}` = never armed\n"
        "# (job-level check + a fresh API re-read to defeat the stale-payload\n"
        "# label race). The label is advisory routing; the required check\n"
        "# going red is the enforcement.\n"
        "name: auto-merge-enabler\n"
        "on:\n"
        "  pull_request:\n"
        "    # `synchronize` (every push to the PR head) re-arms: arming is\n"
        "    # idempotent and never merges anything itself — the merge stays\n"
        "    # gated by the required check. This narrows the green-behind\n"
        "    # stall: a fix-push or `git merge origin/<base>` re-arms on the\n"
        "    # up-to-date head.\n"
        "    types: [opened, reopened, ready_for_review, synchronize]\n"
        "permissions:\n"
        "  contents: write\n"
        "  pull-requests: write\n"
        "concurrency:\n"
        "  group: auto-merge-enabler-${{ github.event.pull_request.number }}\n"
        "  cancel-in-progress: false\n"
        "jobs:\n"
        "  enable-auto-merge:\n"
        "    if: >-\n"
        "      github.event.pull_request.head.repo.full_name == github.repository &&\n"
        "      github.event.pull_request.draft == false &&\n"
        f"      ({branch_expr}) &&\n"
        "      !contains(github.event.pull_request.labels.*.name, "
        f"'{AUTOMERGE_CARVEOUT_LABEL}')\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: Refuse to arm unless the base branch requires status "
        "CONTEXTS\n"
        "        id: rules\n"
        "        env:\n"
        "          GH_TOKEN: ${{ secrets.ROUTINE_PAT || secrets.GITHUB_TOKEN }}\n"
        "        run: |\n"
        "          # Count required check CONTEXTS, not rules: a\n"
        "          # required_status_checks RULE with an empty context list\n"
        "          # still lets an armed PR merge with nothing to wait for.\n"
        "          contexts=\"$(gh api "
        '"repos/$GITHUB_REPOSITORY/rules/branches/${{ github.base_ref }}" \\\n'
        "            --jq '[.[] | select(.type == \"required_status_checks\")\n"
        "                   | .parameters.required_status_checks // [] | "
        ".[].context]')\"\n"
        "          count=\"$(printf '%s' \"$contexts\" | python3 -c "
        "'import json,sys; print(len(json.load(sys.stdin)))')\"\n"
        '          echo "required contexts ($count): $contexts"\n'
        '          echo "required=$count" >> "$GITHUB_OUTPUT"\n'
        '          if [ "$count" = "0" ]; then\n'
        '            echo "::warning::the base branch requires no status-check '
        "CONTEXTS — arming would merge instantly. Refusing to arm; make "
        f"'{context}' a required check first (see the adopt repo-settings "
        'checklist)."\n'
        "          fi\n"
        f"      - name: Re-check the {AUTOMERGE_CARVEOUT_LABEL} label FRESH "
        "(stale-payload race guard)\n"
        "        id: label\n"
        "        if: steps.rules.outputs.required != '0'\n"
        "        env:\n"
        "          GH_TOKEN: ${{ secrets.ROUTINE_PAT || secrets.GITHUB_TOKEN }}\n"
        "          PR: ${{ github.event.pull_request.number }}\n"
        "        run: |\n"
        "          # The event payload snapshots labels at PR-open time; an\n"
        "          # MCP-created PR gets its label in a SECOND call right\n"
        "          # after create. Wait a grace beat, then re-read labels\n"
        "          # from the API and refuse to arm if the label is present\n"
        "          # NOW (the kit #22 incident class).\n"
        "          sleep 15\n"
        "          labels=\"$(gh api "
        '"repos/$GITHUB_REPOSITORY/issues/$PR/labels" '
        "--jq '[.[].name] | join(\",\")')\"\n"
        '          echo "labels on re-read: $labels"\n'
        '          case ",$labels," in\n'
        f"            *,{AUTOMERGE_CARVEOUT_LABEL},*)\n"
        f'              echo "{AUTOMERGE_CARVEOUT_LABEL} present on re-read '
        '— refusing to arm."\n'
        '              echo "skip=1" >> "$GITHUB_OUTPUT" ;;\n'
        "            *)\n"
        '              echo "skip=0" >> "$GITHUB_OUTPUT" ;;\n'
        "          esac\n"
        "      - name: Enable native auto-merge (squash)\n"
        "        if: steps.rules.outputs.required != '0' && "
        "steps.label.outputs.skip == '0'\n"
        "        env:\n"
        "          # Prefer a PAT so the eventual merge attributes to a real\n"
        "          # user; GITHUB_TOKEN is the fallback.\n"
        "          GH_TOKEN: ${{ secrets.ROUTINE_PAT || secrets.GITHUB_TOKEN }}\n"
        "          PR: ${{ github.event.pull_request.number }}\n"
        "        run: |\n"
        '          if gh pr merge --auto --squash "$PR" --repo '
        '"$GITHUB_REPOSITORY"; then\n'
        f'            echo "Auto-merge enabled for PR #$PR — it merges when '
        f"'{context}' is green.\"\n"
        "          else\n"
        '            echo "::warning::Could not enable auto-merge for PR #$PR. '
        "Confirm: (1) 'Allow auto-merge' is ON, (2) the base branch requires "
        f"the '{context}' check, (3) the token has Pull requests + Contents "
        'write. On a repo shape where GitHub structurally refuses the arm '
        "(born-red required checks with no pending window, or PR-required-"
        "but-no-CI), REST merge-on-green is the landing path instead — see "
        'docs/operations/auto-merge-guards.md."\n'
        "          fi\n"
    )


BRANCH_SWEEP_RELPATH = ".github/workflows/branch-sweep.yml"

# The sweep's blast radius is DELETION, so its default pattern list is its
# own, not the automerge list: the fleet's agent-branch actors (claude/*
# sessions, codex/* and bot/* sibling conventions — inbox ORDER 023's named
# set). claim/* fast-lane refs are deliberately absent until the convention
# earns deletion evidence.
DEFAULT_SWEEP_BRANCH_PATTERNS = ("claude/*", "codex/*", "bot/*")
# Daily, off the top of the hour (GitHub sheds on-the-hour scheduled load).
DEFAULT_SWEEP_CRON = "17 3 * * *"


def _sweep_pattern_terms(
    branch_patterns: list[str] | None,
) -> tuple[list[str], list[str]]:
    """Return ``(patterns, query_prefixes)`` for the sweep workflow.

    ``patterns`` are the sanitized shell ``case`` terms (trailing ``*`` is a
    prefix match, mirroring :func:`_automerge_branch_expr`; the charset is
    clamped to path-safe characters so a pattern can never smuggle shell
    syntax into the generated script). ``query_prefixes`` are the
    matching-refs API query strings — the pattern minus its trailing ``*``.
    Empty/blank/bare-``*`` input falls back to the default (the
    ``heartbeat_files`` doctrine: a stray ``[]`` — or a bare ``*`` — must
    not silently put EVERY branch in deletion scope).
    """
    cleaned: list[str] = []
    for raw in branch_patterns or []:
        pattern = re.sub(r"[^A-Za-z0-9_./*-]", "", str(raw)).strip()
        if not pattern or pattern.replace("*", "") in ("", "/", "."):
            # A bare "*" (or a degenerate "*/*"-style glob with no literal
            # stem) would sweep every branch on the repo — refuse the
            # footgun and let the fallback keep the agent-branch default.
            continue
        if pattern not in cleaned:
            cleaned.append(pattern)
    if not cleaned:
        cleaned = list(DEFAULT_SWEEP_BRANCH_PATTERNS)
    queries: list[str] = []
    for pattern in cleaned:
        query = pattern[:-1] if pattern.endswith("*") else pattern
        if query not in queries:
            queries.append(query)
    return cleaned, queries


def _sweep_cron(cron: str | None) -> str:
    """Return a safe 5-field cron string, falling back to the default.

    Charset-clamped (digits, ``* , / -`` and spaces) and shape-checked
    (exactly five fields) — a malformed ``branch_sweep.cron`` knob must
    yield a workflow GitHub can parse, never a silently-dead schedule.
    """
    cleaned = re.sub(r"[^0-9*,/ -]", "", str(cron or "")).strip()
    if len(cleaned.split()) != 5:
        return DEFAULT_SWEEP_CRON
    return cleaned


def branch_sweep_workflow(
    branch_patterns: list[str] | None = None,
    cron: str = DEFAULT_SWEEP_CRON,
) -> str:
    """Return the LIVE scheduled branch-sweep workflow (inbox ORDER 023).

    GitHub's "Automatically delete head branches" silently skips merges
    performed by app/bot actors (community discussion 63409 · cli/cli#9073)
    — which is every fleet auto-merge — so spent agent branches accumulate
    by the hundreds (fm census 2026-07-14: 460/491 surviving ``claude/*``
    heads across four repos sit at exactly their merged PR's head SHA).
    This workflow is the settled remedy: a SCHEDULED sweep that deletes the
    head refs of merged+closed same-repo PRs matching the agent-branch
    patterns, with hard skip rules for open-PR heads, the default branch,
    fork heads, and refs that moved on after their PR closed.

    Deliberately scheduled, never ``pull_request: closed``: the fleet's
    merges are performed with GITHUB_TOKEN / app tokens, and events
    performed with GITHUB_TOKEN do not trigger workflows (the docs'
    "Automatic token authentication" recursion guard) — a closed-event
    cleanup would never fire for exactly the merges that need it.

    Plants and regenerates exactly like :func:`automerge_enabler_workflow`
    (staged always, installed live by ``adopt --wire-enforcement``,
    kit-owned once it exists — see :func:`adopt` step 6b).
    """
    patterns, queries = _sweep_pattern_terms(
        list(branch_patterns) if branch_patterns is not None else None,
    )
    case_expr = "|".join(patterns)
    patterns_note = " · ".join(patterns)
    query_words = " ".join(f"'{query}'" for query in queries)
    schedule = _sweep_cron(cron)
    return (
        "# substrate-kit branch sweep (LIVE — installed by\n"
        "# `bootstrap.py adopt --wire-enforcement`).\n"
        "# KIT-OWNED: adopt/upgrade regenerates this file in place, so\n"
        "# upstream sweep fixes land here on every `bootstrap.py upgrade` —\n"
        "# hand edits are OVERWRITTEN. Put host-specific customizations in a\n"
        "# SEPARATE workflow file, never in this one.\n"
        "#\n"
        "# WHY THIS EXISTS (inbox ORDER 023): GitHub's \"Automatically\n"
        "# delete head branches\" silently skips merges performed by app/bot\n"
        "# actors (github.com/orgs/community/discussions/63409 ·\n"
        "# cli/cli#9073) — which is every fleet auto-merge (armed via\n"
        "# GITHUB_TOKEN / MCP app tokens) — so spent agent branches\n"
        "# accumulate by the hundreds (fleet census 2026-07-14: 460/491\n"
        "# surviving claude/* heads across four repos sat at exactly their\n"
        "# merged PR's head SHA).\n"
        "#\n"
        "# WHY A SCHEDULE, NOT `pull_request: closed`: events performed with\n"
        "# GITHUB_TOKEN do not trigger workflows (the docs' \"Automatic\n"
        "# token authentication\" recursion guard), so a closed-event\n"
        "# cleanup would never fire for exactly the merges that need it.\n"
        "#\n"
        "# WHY A WORKFLOW, NOT THE AGENT: agent-side branch deletion is\n"
        "# historically 403-walled in fleet sessions (capability ledger\n"
        "# OA-10 — classifier + proxy deny every delete path). This\n"
        "# workflow, running with the repo's own GITHUB_TOKEN, is the\n"
        "# sanctioned path around that wall.\n"
        "#\n"
        "# WHAT IT DELETES — a ref must pass EVERY rule, in order:\n"
        f"#   1. matches a sweep pattern ({patterns_note});\n"
        "#   2. is the head of a MERGED or CLOSED same-repo PR (fork heads\n"
        "#      are excluded by construction: a closed fork PR must never\n"
        "#      delete a same-named local branch);\n"
        "#   3. its tip SHA equals that spent PR head's SHA (a ref that\n"
        "#      moved on after its PR closed may carry unmerged work —\n"
        "#      skipped, logged);\n"
        "#   4. is NOT the head of any OPEN pull request;\n"
        "#   5. is NOT the repository's default branch.\n"
        "# Every deletion and every skip is logged with its reason. Manual\n"
        "# runs (workflow_dispatch) take a `dry_run` input: log what WOULD\n"
        "# be deleted, delete nothing.\n"
        "name: branch-sweep\n"
        "on:\n"
        "  schedule:\n"
        f"    - cron: '{schedule}'\n"
        "  workflow_dispatch:\n"
        "    inputs:\n"
        "      dry_run:\n"
        "        description: 'Log what WOULD be deleted; delete nothing.'\n"
        "        type: boolean\n"
        "        default: false\n"
        "# Least-privilege: ref deletion needs `contents: write`; PR\n"
        "# enumeration needs `pull-requests: read`. Nothing else.\n"
        "permissions:\n"
        "  contents: write\n"
        "  pull-requests: read\n"
        "concurrency:\n"
        "  group: branch-sweep\n"
        "  cancel-in-progress: false\n"
        "jobs:\n"
        "  branch-sweep:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: Sweep spent agent branches (heads of merged/closed "
        "PRs)\n"
        "        env:\n"
        "          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}\n"
        "          DRY_RUN: ${{ inputs.dry_run == true && 'true' || 'false' "
        "}}\n"
        "        run: |\n"
        "          set -euo pipefail\n"
        "          default_branch=\"$(gh api \"repos/$GITHUB_REPOSITORY\" "
        "--jq .default_branch)\"\n"
        '          echo "default branch: $default_branch (never touched)"\n'
        '          echo "dry run: $DRY_RUN"\n'
        "          # Existing refs (+ tip SHAs) under each swept pattern's\n"
        "          # prefix, via the matching-refs API.\n"
        "          : > existing-raw.txt\n"
        f"          for query in {query_words}; do\n"
        '            gh api "repos/$GITHUB_REPOSITORY/git/matching-refs/'
        'heads/$query" \\\n'
        "              --paginate --jq '.[] | .ref + \" \" + .object.sha' "
        ">> existing-raw.txt\n"
        "          done\n"
        "          sed 's|^refs/heads/||' existing-raw.txt | sort -u > "
        "existing.txt\n"
        "          # Heads of OPEN PRs — never swept, whatever their PR\n"
        "          # history (a reused branch with a fresh PR stays).\n"
        '          gh api "repos/$GITHUB_REPOSITORY/pulls?state=open&'
        'per_page=100" \\\n'
        "            --paginate --jq '.[].head.ref' | sort -u > "
        "open-heads.txt\n"
        "          # Same-repo heads (+ head SHAs) of MERGED and CLOSED PRs\n"
        "          # (state=closed covers both; the repo filter drops fork\n"
        "          # heads).\n"
        '          gh api "repos/$GITHUB_REPOSITORY/pulls?state=closed&'
        'per_page=100" \\\n'
        "            --paginate \\\n"
        "            --jq '.[] | select(.head.repo != null) | "
        '.head.repo.full_name + " " + .head.ref + " " + .head.sha\' \\\n'
        "            > spent-raw.txt\n"
        "          awk -v repo=\"$GITHUB_REPOSITORY\" '$1 == repo "
        "{ print $2 \" \" $3 }' \\\n"
        "            spent-raw.txt | sort -u > spent-pairs.txt\n"
        "          cut -d' ' -f1 spent-pairs.txt | sort -u > spent-refs.txt\n"
        "          # The plan: every existing pattern-matched ref that fails\n"
        "          # a skip rule is logged with the reason; survivors are\n"
        "          # deleted (or dry-run-logged) below.\n"
        "          : > sweep-plan.txt\n"
        "          while read -r ref sha; do\n"
        '            case "$ref" in\n'
        f"              {case_expr}) ;;\n"
        '              *) echo "skip: $ref — matched a query prefix but no '
        'sweep pattern"; continue ;;\n'
        "            esac\n"
        '            if [ "$ref" = "$default_branch" ]; then\n'
        '              echo "skip: $ref — the default branch is never '
        'touched"\n'
        "              continue\n"
        "            fi\n"
        '            if grep -qxF "$ref" open-heads.txt; then\n'
        '              echo "skip: $ref — head of an OPEN pull request"\n'
        "              continue\n"
        "            fi\n"
        '            if ! grep -qxF "$ref" spent-refs.txt; then\n'
        '              echo "skip: $ref — no merged/closed PR has this head '
        '(live branch)"\n'
        "              continue\n"
        "            fi\n"
        '            if ! grep -qxF "$ref $sha" spent-pairs.txt; then\n'
        '              echo "skip: $ref — moved on since its PR closed (tip '
        'is not a spent PR head)"\n'
        "              continue\n"
        "            fi\n"
        "            printf '%s\\n' \"$ref\" >> sweep-plan.txt\n"
        "          done < existing.txt\n"
        '          echo "sweep plan: $(wc -l < sweep-plan.txt) of '
        '$(wc -l < existing.txt) candidate ref(s)"\n'
        "          while IFS= read -r ref; do\n"
        '            if [ "$DRY_RUN" = "true" ]; then\n'
        '              echo "DRY-RUN: would delete $ref"\n'
        "            elif gh api -X DELETE "
        '"repos/$GITHUB_REPOSITORY/git/refs/heads/$ref"; then\n'
        '              echo "deleted: $ref"\n'
        "            else\n"
        '              echo "::warning::could not delete $ref (already gone, '
        'protected, or a permissions gap)"\n'
        "            fi\n"
        "          done < sweep-plan.txt\n"
    )


def _branch_sweep_params(config: Config) -> tuple[list[str], str]:
    """Return the sweep's ``(branch_patterns, cron)`` from config.

    Fallback-on-empty at the consumer (the ``heartbeat_files`` doctrine): a
    stray ``{}``/``[]``/``""`` in ``substrate.config.json`` →
    ``branch_sweep`` must not silently widen the deletion scope or blank
    the schedule.
    """
    knobs = config.branch_sweep if isinstance(config.branch_sweep, dict) else {}
    patterns = knobs.get("branch_patterns") or list(
        DEFAULT_SWEEP_BRANCH_PATTERNS,
    )
    cron = str(knobs.get("cron") or DEFAULT_SWEEP_CRON)
    return [str(p) for p in patterns], cron


def _regen_kit_owned_workflow(
    root: Path,
    config: Config,
    relpath: str,
    expected_text: str,
    report: list[str],
    *,
    noun: str,
    install_when_absent: bool,
    old_text: str | None = None,
) -> None:
    """Plant/regenerate one kit-owned live workflow (adopt step 6b shape).

    The shared mechanism behind :data:`LIVE_CI_RELPATH` and
    :data:`AUTOMERGE_ENABLER_RELPATH` (EAP program review §6.1 + §6.10):
    an absent file is planted only when ``install_when_absent`` (the
    ``--wire-enforcement`` opt-in — the kit never installs live CI
    silently); once the file EXISTS it is kit-owned — regenerated in place
    on every adopt/upgrade pass, with the #137 carve-out protection: host
    additions are detected (:func:`gate_carveouts`), the full pre-regen copy
    is banked content-hash-named under ``<state_dir>/backup/``, and each
    carve-out is reported (upgrade surfaces them in ``upgrade-report.md``).

    **Three-way compare (v1.11.0-wave phantom-carve-out fix):** when a kit
    release changes the kit's OWN generated workflow content (the #199/#195
    checkout@v5 / setup-python@v6 pin bumps), a two-way live-vs-new compare
    misreads the kit's outgoing template content as "host-added" (6 live-gate
    adopters flagged phantom carve-outs on the v1.11.0 wave) and banks a
    pre-regen copy byte-identical to the OLD template. ``old_text`` — what
    the kit LAST shipped, recovered by the caller from the staged copy under
    ``<state_dir>/ci/`` BEFORE the staging pass overwrites it (the banked
    dist cannot supply it: these workflows are code-generated, not
    ``_TEMPLATES`` entries, so an old dist would have to be *executed* to
    re-render them) — makes the compare three-way: a detection counts as a
    host carve-out ONLY when the content is present in live and explained by
    NEITHER template. Kit-side evolution is a one-line informational note;
    a live file byte-identical to the old template yields zero flags and NO
    bank (the bank preserves host customization — identical content has
    none). ``old_text=None`` (first adopt, staged copy missing) degrades to
    the two-way compare with an explicit warning when it detects anything.
    """
    live_path = root / relpath
    if live_path.is_file():
        live_text = live_path.read_text(encoding="utf-8")
        if live_text == expected_text:
            # Byte-identity IS a clean scan result — say so explicitly
            # (queued fix 1): a report with no carve-out language at all is
            # indistinguishable from "the detector never ran".
            report.append(f"carve-out scan: {relpath} — ran, 0 found")
            report.append(f"kept: {relpath} (kit-owned, already current)")
            return
        if old_text is not None and live_text == old_text:
            # Three-way fast path: the live file is byte-identical to what
            # the kit last shipped — the whole live-vs-new delta is kit-side
            # template evolution. Nothing is host-added, nothing is banked;
            # the regen just moves the file to template@new.
            report.append(
                f"carve-out scan: {relpath} — ran, 0 found (live matched "
                "the previous kit template byte-for-byte; the delta is "
                "kit-side template evolution)",
            )
            atomic_write_text(live_path, expected_text)
            report.append(
                f"regenerated: {relpath} (kit-owned — template@new; "
                "hand edits are overwritten, host carve-outs belong in a "
                "separate workflow)",
            )
            return
        carveouts = gate_carveouts(live_text, expected_text)
        kit_side = 0
        if old_text is not None:
            # Three-way compare: a detection vs the NEW template that does
            # NOT also fire vs the OLD template is explained by what the
            # kit last shipped — kit-side evolution, never a host addition.
            # Only content present in live and in NEITHER template survives
            # as a carve-out (the intersection of both detections).
            vs_old = set(gate_carveouts(live_text, old_text))
            kept = [line for line in carveouts if line in vs_old]
            kit_side = len(carveouts) - len(kept)
            carveouts = kept
        elif carveouts:
            # No recoverable old template: degrade to the two-way compare
            # and say so — kit-side template evolution may over-report as
            # host additions in this mode (the v1.11.0-wave class).
            report.append(
                f"carve-out scan: {relpath} — previous kit template "
                "unavailable (no staged copy to recover it from); two-way "
                "compare vs the new template may report kit-side template "
                "changes as host additions",
            )
        if kit_side:
            report.append(
                f"carve-out scan: {relpath} — kit-updated {kit_side} "
                "step(s)/job(s) (template evolution; not host additions, "
                "not banked)",
            )
        if not carveouts:
            # Explicit-when-clean (queued fix 1, fleet-manager #40 finding):
            # the scan ran and found no host additions — name that, so the
            # upgrade report can prove the detector ran instead of leaving
            # silence that also matches "never ran".
            report.append(f"carve-out scan: {relpath} — ran, 0 found")
        if carveouts:
            digest = hashlib.sha256(live_text.encode("utf-8")).hexdigest()[:8]
            stem = relpath.rsplit("/", 1)[-1]
            stem = stem[: -len(".yml")] if stem.endswith(".yml") else stem
            bank_rel = (
                f"{config.state_dir}/{BACKUP_DIRNAME}/"
                f"{stem}.pre-regen-{digest}.yml"
            )
            atomic_write_text(root / bank_rel, live_text)
            for line in carveouts:
                report.append(f"carve-out: {relpath} — {line}")
            report.append(
                f"carve-out: full pre-regen {noun} banked at {bank_rel} — "
                "host additions were NOT carried into the regenerated "
                f"kit-owned {noun}; move them into a separate workflow file "
                "(e.g. .github/workflows/host-ci.yml) and commit that "
                "before shipping this upgrade/adopt PR.",
            )
        atomic_write_text(live_path, expected_text)
        report.append(
            f"regenerated: {relpath} (kit-owned — template@new; "
            "hand edits are overwritten, host carve-outs belong in a "
            "separate workflow)",
        )
    elif install_when_absent:
        _adopt_plant(live_path, relpath, expected_text, report)


def _automerge_params(config: Config) -> tuple[list[str], str]:
    """Return the enabler's (branch_patterns, required_context) from config.

    Fallback-on-empty at the consumer (the ``heartbeat_files`` doctrine): a
    stray ``{}``/``[]``/``""`` in ``substrate.config.json`` → ``automerge``
    must not silently widen arming or blank the context name.
    """
    knobs = config.automerge if isinstance(config.automerge, dict) else {}
    patterns = knobs.get("branch_patterns") or list(
        DEFAULT_AUTOMERGE_BRANCH_PATTERNS,
    )
    context = str(
        knobs.get("required_context") or DEFAULT_AUTOMERGE_REQUIRED_CONTEXT,
    )
    return [str(p) for p in patterns], context


def _workflow_context_names(root: Path) -> set[str]:
    """Collect plausible required-check context names from live workflows.

    A workflow job's status-check context is its display ``name:`` when set,
    else its job id — so both are collected, from every workflow under
    ``.github/workflows/``. Line-based like :func:`_workflow_outline`
    (stdlib-only, no YAML parser) and best-effort by design: the result only
    ever decides whether to *emit an advisory report line*, never a gate.
    Empty set = nothing judgeable (no workflows dir / no parseable jobs).
    """
    names: set[str] = set()
    wf_dir = root / ".github" / "workflows"
    if not wf_dir.is_dir():
        return names
    for wf_path in sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml")):
        try:
            text = wf_path.read_text(encoding="utf-8")
        except OSError:
            continue
        in_jobs = False
        current: str | None = None
        for raw in text.split("\n"):
            line = raw.rstrip()
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            indent = len(line) - len(line.lstrip(" "))
            if indent == 0:
                in_jobs = stripped == "jobs:"
                current = None
                continue
            if not in_jobs:
                continue
            if (
                indent == 2
                and stripped.endswith(":")
                and not stripped.startswith("-")
            ):
                current = stripped[:-1]
                names.add(current)
                continue
            if current is not None and indent == 4:
                match = re.match(r"name:\s*(.+)$", stripped)
                if match is not None:
                    names.add(match.group(1).strip().strip("'\""))
    return names


def _required_context_advisory(root: Path, required_context: str) -> str | None:
    """One advisory line when ``automerge.required_context`` looks wrong.

    The websites class (queued kit fix 3): the planted config defaulted
    ``required_context`` to ``substrate-gate`` while that repo's actual
    required check is ``quality`` — a value the kit cannot *derive* at plant
    time (which check is REQUIRED lives in the branch ruleset, owner-UI,
    invisible in-tree), but can *validate* against what is visible: the job
    names the repo's own workflows produce. Mismatch → one report line
    naming the exact config override; nothing judgeable → silence (a fresh
    adopt with no CI must not nag about a gate that isn't installed yet).
    The knob stays informational-only either way — the enabler's
    refuse-to-arm guard counts required contexts generically.
    """
    names = _workflow_context_names(root)
    if not names or required_context in names:
        return None
    listed = ", ".join(f"'{name}'" for name in sorted(names))
    return (
        f"automerge.required_context '{required_context}' matches no job in "
        f".github/workflows/ (contexts found: {listed}) — if this repo's "
        "REQUIRED check has a different name, set substrate.config.json -> "
        'automerge."required_context" to that exact context. The value '
        "labels the repo-settings checklist + enabler log lines "
        "(informational; the refuse-to-arm guard counts required contexts "
        "generically)."
    )


def _repo_settings_checklist(required_context: str) -> list[str]:
    """Return the one-time repo-settings checklist (EAP §6.10, second half).

    Adopt prints it whenever the live enabler is present: these are the
    owner-UI toggles a planted workflow CANNOT set for itself — verified
    live on the fleet (trading-strategy's "Allow auto-merge" is OFF, so its
    enabler cannot arm anything until the owner flips it; a workflow has no
    path to repo settings).
    """
    return [
        "repo-settings checklist (one-time, owner UI — the planted "
        "workflows are inert until these are set):",
        '  1. Settings → General → Pull Requests → "Allow auto-merge" = ON '
        "(a workflow cannot flip repo settings).",
        f"  2. Require the '{required_context}' status check on the default "
        "branch (Settings → Rules) — with NO required check, arming "
        "auto-merge merges a PR instantly. (If this repo's required check "
        "has a different name, pin it via substrate.config.json -> "
        'automerge."required_context" so this checklist and the enabler '
        "logs name the right context.)",
        '  3. Optional: "Automatically delete head branches" + auto-update '
        "of PR branches (closes the merged-branch clutter and the "
        "green-behind stall classes).",
    ]


# Search-hygiene plant (queued kit fix 5 — bench run-5 judge limitation 5):
# the ~12k-line vendored bootstrap.py + the <state_dir>/backup/ dist copies
# dominate repo-wide search in adopter repos (a code grep surfaces hundreds
# of engine hits before the repo's own sources). The guidance half shipped
# with the planted CLAUDE.md search-hygiene note (#165); this is the
# mechanical half: `.ignore` removes both from ripgrep-family tools by
# default (`rg -u`/`--no-ignore` still reaches them deliberately; plain
# `grep -r` has no ignore protocol and stays guidance-only), and
# `.gitattributes` linguist-generated hints collapse them in GitHub diffs
# and language stats. Both surfaces are MERGED, never clobbered: the kit
# only ever appends entries that are missing, under one marker comment.
SEARCH_HYGIENE_MARKER = (
    "# substrate-kit search hygiene (planted by adopt/upgrade; the kit only "
    "ever APPENDS missing entries — existing content above is host-owned)"
)


def _search_hygiene_surfaces(
    config: Config,
    vendored_relpath: str,
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Return the (file, entries) plan for the search-hygiene plant.

    Entries are root-anchored (leading ``/``) so only the vendored file and
    the state-dir backup bank match — never a same-named file deeper in the
    host tree. An absolute ``vendored_relpath`` (the no-vendored-copy
    fallback shapes) contributes no bootstrap entry: there is nothing
    in-repo to hide.
    """
    state_dir = config.state_dir.strip("/")
    bootstrap_entry = None
    if vendored_relpath and not Path(vendored_relpath).is_absolute():
        bootstrap_entry = "/" + vendored_relpath.lstrip("/")
    ignore_entries = tuple(
        entry
        for entry in (bootstrap_entry, f"/{state_dir}/backup/")
        if entry is not None
    )
    attr_entries = tuple(
        f"{pattern} linguist-generated=true"
        for pattern in (bootstrap_entry, f"/{state_dir}/backup/**")
        if pattern is not None
    )
    return ((".ignore", ignore_entries), (".gitattributes", attr_entries))


def _plant_search_hygiene(
    root: Path,
    config: Config,
    vendored_relpath: str,
    report: list[str],
) -> None:
    """Merge the search-hygiene entries into ``.ignore``/``.gitattributes``.

    Append-only merge (the clobber hazard is real: a host `.gitattributes`
    or `.ignore` carries host policy): existing lines are preserved
    byte-for-byte, already-present entries are never duplicated (idempotent
    across adopt/upgrade passes), and appended entries sit under one marker
    comment naming their provenance. Unreadable file → skip + report,
    never destroy.
    """
    for relpath, entries in _search_hygiene_surfaces(config, vendored_relpath):
        if not entries:
            continue
        path = root / relpath
        existing = ""
        if path.is_file():
            try:
                existing = path.read_text(encoding="utf-8")
            except OSError:
                report.append(
                    f"skipped: {relpath} (unreadable — left untouched; "
                    "search-hygiene entries not merged)",
                )
                continue
        present = {line.strip() for line in existing.splitlines()}
        missing = [entry for entry in entries if entry not in present]
        if not missing:
            report.append(
                f"kept: {relpath} (search-hygiene entries already present)",
            )
            continue
        chunk = ""
        if existing:
            if not existing.endswith("\n"):
                chunk += "\n"
            chunk += "\n"
        if SEARCH_HYGIENE_MARKER not in present:
            chunk += SEARCH_HYGIENE_MARKER + "\n"
        chunk += "\n".join(missing) + "\n"
        atomic_write_text(path, existing + chunk)
        noun = "entry" if len(missing) == 1 else "entries"
        if existing:
            report.append(
                f"merged: {relpath} ({len(missing)} search-hygiene {noun} "
                "appended; existing content preserved)",
            )
        else:
            report.append(
                f"planted: {relpath} ({len(missing)} search-hygiene {noun})",
            )


def adopt(
    root: Path,
    config: Config,
    backend: Any,
    *,
    kit_root: Path,
    include_claude: bool = False,
    wire_enforcement: bool = False,
    lane: str | None = None,
    archive_running: bool = True,
) -> list[str]:
    """Adopt the substrate workflow into ``root``; return the report lines.

    Steps (all idempotent): (0) guardrail — refuse the kit's own tree; then
    derive what the tree can tell us (provisional slots) and vendor the
    single-file bootstrap so hook commands resolve in-repo;
    (1) plant every ``ADOPT_PLAN`` doc rendered from the current slots —
    skip-if-exists, unrendered docs bannered; (2) plant
    ``<sessions_dir>/README.md``; (3) plant the ``project.index.json``
    skeleton; (4) stage the ``.claude`` material (CLAUDE.md, skills,
    personas, hook settings + fill-table README) under ``<state_dir>``;
    (5) stage the CI example; (6) with ``include_claude``, additionally
    write ``.claude/CLAUDE.md`` + ``.claude/settings.json`` if absent;
    (7) close with the next-steps line.

    ``wire_enforcement`` turns on the two **forcing functions** that make the
    memory ritual actually get used (the Phase-2.5 re-run showed docs alone get
    read but not written back): it implies ``include_claude`` (the live Stop-hook
    **nag**) **and** plants a live CI workflow (:data:`LIVE_CI_RELPATH`) running
    the ``--require-session-log`` gate — the **locked door** that holds a merge
    red until the journal is written. Kept opt-in: the kit still never installs
    executable CI/hooks silently (the deliberate safety default), but a host —
    or the rebuild's K0 session — flips this on to reproduce the enforcement
    this repo's discipline actually runs on. Once installed, the live gate is
    **kit-owned** (EAP program review §6.1): every subsequent adopt/upgrade
    pass regenerates it in place, hand edits included — see step 6b and
    :func:`live_ci_workflow`.

    ``lane`` makes the adopt **lane-aware** (the self-review G1 fix for
    double-adoption in SHARED repos): the seeded heartbeat plants as
    ``control/status-<lane>.md`` instead of the singular ``control/status.md``
    and is declared in ``config.heartbeat_files`` (see
    :func:`_register_lane_heartbeat` for the replace-vs-append rules), while
    ``control/inbox.md`` and ``control/README.md`` stay single — the
    manager-owned bus is shared, the heartbeat never is. A second Project
    adopting into an already-adopted repo passes ``--lane`` and joins
    (every shared file skip-if-exists kept, only its own heartbeat added)
    instead of re-planting the first Project's files by hand.
    """
    include_claude = include_claude or wire_enforcement
    assert_safe_target(root, kit_root)
    if lane is not None:
        validate_lane_name(lane)
    templates = load_templates()
    report: list[str] = []

    # (0a) Lane-drift advisory (the #103 inverse gap): a plain adopt into a
    # lane-shaped repo gets the `--lane` nudge as the FIRST report line —
    # advisory only, planting continues (see lane_drift_advisory).
    if lane is None:
        advisory = lane_drift_advisory(list(config.heartbeat_files))
        if advisory is not None:
            report.append(advisory)

    # (0b) Adopt renders what it knows: seed derivable slots (provisional,
    # never overwriting an existing answer), then build the render context.
    report.extend(record_derived_slots(backend, derive_slots(root, config.docs_root)))
    bootstrap_path = _vendor_bootstrap(root, report)
    # (0c) Bank the running dist under <state_dir>/backup/ (§4.3): a future
    # upgrade's doc diff needs the OLD templates to still exist, so the
    # archive is written before anything could ever overwrite the file.
    # ``archive_running=False`` is the upgrade path's carve-out: by the time
    # upgrade re-runs adopt (its step 6) the vendored file has already been
    # replaced with the NEW dist, so archiving here banked a spurious
    # ``bootstrap-<new>.py`` next to the correct old-dist archive (field-
    # reproduced on fleet-manager #35, superbot-games #22, trading-strategy
    # #38 — harmless, ``last-upgrade.json`` named the right one, but wrong).
    # Upgrade archives the OLD dist itself, archive-first, before the replace.
    if archive_running:
        dist_file = Path(bootstrap_path)
        if not dist_file.is_absolute():
            dist_file = root / bootstrap_path
        archive_dist(root, config, dist_file, report)
    context = build_context(backend.data)
    # The live integration mode is state, not a slot — render it truthfully.
    context.setdefault("integration_mode", str(backend.get("mode", "guided")))
    # The boot pointer is state too: only this run knows whether
    # .claude/CLAUDE.md is (or is about to be) live in the target — the
    # ORDER 015 dead-pointer fix (logic: engine.render.agreement_home).
    context.setdefault(
        "agreement_home",
        agreement_home(root, include_claude=include_claude),
    )

    # (1) Plant the live docs — never clobber; a doc with unfilled ${slots}
    # is planted under the loud UNRENDERED banner (visible, never inert).
    for template_name, plan_rel in ADOPT_PLAN:
        rel = _adopt_dest(plan_rel, config)
        if lane is not None and template_name == "control-status.md.tmpl":
            # Lane-aware adopt: the heartbeat is the ONE per-Project file on
            # the bus — parametrize its dest; a --lane adopt never creates
            # (nor touches) the singular control/status.md.
            rel = lane_status_relpath(lane)
        text = render(templates[template_name], context)
        if template_name == "decisions.md.tmpl":
            # The example D-0001 records THIS adoption — stamp the real date so
            # the planted ledger is check_ledger-clean from its first commit.
            text = text.replace("- date:\n", f"- date: {date.today().isoformat()}\n")
        final = with_unrendered_banner(text)
        if _adopt_plant(root / rel, rel, final, report):
            # Provenance for the upgrade diff (§4.3): hash what the kit wrote.
            record_doc_hash(backend, rel, final)

    # (1b) The seat-digest render surface (grounded-skills slice 6, §8
    # Q3=A): one GENERATED planted doc — both fence-marked digest blocks
    # (skills index + venue-filtered walls), rendered AFTER the plan loop so
    # a fresh adopt reads the just-planted capability ledger. Deliberately
    # outside ADOPT_PLAN: it is a derived render of live tree content, so
    # template hash-classification would misread every ledger append as doc
    # drift — upgrade refreshes it via refresh_seat_digest (kit-written
    # copies only) and `bootstrap.py seat-digest` regenerates on demand;
    # check_seat_digest (advisory) byte-compares it against a fresh render.
    digest_rel = seat_digest_relpath(config)
    digest_text = seat_digest_text(root, config, context)
    if _adopt_plant(root / digest_rel, digest_rel, digest_text, report):
        record_doc_hash(backend, digest_rel, digest_text)

    # (2) Session-log scaffolding. A pre-existing README (skip-if-exists
    # keeps it) still receives the model-attribution doctrine append-only
    # under a provenance marker — the PR #170 render was fresh-plant-only,
    # and the v1.9.0 wave hand-merged 4 adopters for exactly this gap.
    sessions_rel = f"{config.sessions_dir}/README.md"
    readme = _adopt_sessions_readme(config.session_markers)
    _adopt_plant(root / config.sessions_dir / "README.md", sessions_rel, readme, report)
    _merge_model_doctrine(root, config, report)

    # (3) The context-pack index skeleton.
    project_name = context.get("project_name") or root.name
    skeleton = pack_index_skeleton(project_name)
    _adopt_plant(root / "project.index.json", "project.index.json", skeleton, report)

    # (3b) Search hygiene (queued kit fix 5): keep the vendored dist + the
    # backup bank out of repo-wide search — merged, never clobbered.
    _plant_search_hygiene(root, config, bootstrap_path, report)

    # (4) Stage the .claude material under <state_dir> (regenerated each run).
    state_base = root / config.state_dir
    claude_doc = with_unrendered_banner(render(templates["CLAUDE.md.tmpl"], context))
    claude_rel = f"{config.state_dir}/claude/CLAUDE.md"
    _adopt_stage(state_base / "claude" / "CLAUDE.md", claude_rel, claude_doc, report)
    for skill in SKILLS:
        rel = skill_relpath(skill)
        body = render(skill["body"], context)
        document = skill_document(skill, body)
        _adopt_stage(state_base / rel, f"{config.state_dir}/{rel}", document, report)
    for agent in AGENTS:
        rel = agent_relpath(agent)
        body = render(agent["body"], context)
        document = agent_document(agent, body)
        _adopt_stage(state_base / rel, f"{config.state_dir}/{rel}", document, report)
    settings_text = full_settings_template(config, bootstrap_path=bootstrap_path)
    settings_rel = f"{config.state_dir}/hooks/settings.template.json"
    settings_path = state_base / "hooks" / "settings.template.json"
    _adopt_stage(settings_path, settings_rel, settings_text, report)
    hooks_readme_rel = f"{config.state_dir}/hooks/README.md"
    hooks_readme = hooks_fill_table()
    _adopt_stage(
        state_base / "hooks" / "README.md",
        hooks_readme_rel,
        hooks_readme,
        report,
    )

    # (5) Stage the CI example — and the LIVE gate workflow (KL-7): a default
    # adopt still never installs CI, but the engagement gate's
    # `enforcement-unwired` checklist line must be a one-copy fix, so the
    # ready-to-install substrate-gate.yml is always staged next to the
    # commented example. Kit stages, host installs — doctrine unchanged.
    ci_rel = f"{config.state_dir}/ci/quality.yml.example"
    _adopt_stage(
        state_base / "ci" / "quality.yml.example",
        ci_rel,
        ci_snippet(),
        report,
    )
    # The gate's test step honors the interview's verify_command (#403
    # follow-on): filled + gate-safe + non-default → the confirmed command
    # drives the step; anything else keeps the hardened pytest fallback.
    # Computed from the SAME state document upgrade's read-only carve-out
    # rescan reads, so writer and scanner can never expect different bytes.
    gate_interpreter = config.interpreter_for_checks or "python3"
    gate_test = gate_test_command(backend.data, gate_interpreter)
    if gate_test is not None:
        report.append(
            "gate test step: runs the interview's confirmed verify_command "
            f"({gate_test!r}) — pytest fallback not planted.",
        )
    gate_text = live_ci_workflow(
        gate_interpreter,
        sessions_dir=config.sessions_dir,
        test_command=gate_test,
    )
    gate_rel = f"{config.state_dir}/ci/substrate-gate.yml"
    # Three-way compare inputs (v1.11.0-wave phantom-carve-out fix): until
    # the _adopt_stage calls below overwrite them, the staged copies under
    # <state_dir>/ci/ hold what the kit LAST shipped — capture those bytes
    # FIRST so the kit-owned regen (step 6b) can tell kit-side template
    # evolution from host additions. Absent staged copy (first adopt) →
    # None → the regen honestly degrades to its two-way compare.
    old_staged_gate = _staged_previous_text(
        state_base / "ci" / "substrate-gate.yml",
    )
    old_staged_enabler = _staged_previous_text(
        state_base / "ci" / "auto-merge-enabler.yml",
    )
    old_staged_sweep = _staged_previous_text(
        state_base / "ci" / "branch-sweep.yml",
    )
    _adopt_stage(
        state_base / "ci" / "substrate-gate.yml",
        gate_rel,
        gate_text,
        report,
    )
    # The auto-merge enabler stages right next to the gate (EAP §6.10): the
    # two are halves of one pattern — the gate holds a born-red PR red, the
    # enabler arms the merge that fires when the card flips green.
    enabler_patterns, enabler_context = _automerge_params(config)
    enabler_text = automerge_enabler_workflow(enabler_patterns, enabler_context)
    enabler_rel = f"{config.state_dir}/ci/auto-merge-enabler.yml"
    _adopt_stage(
        state_base / "ci" / "auto-merge-enabler.yml",
        enabler_rel,
        enabler_text,
        report,
    )
    # The scheduled branch sweep (inbox ORDER 023) stages next to the
    # enabler — the litter the enabler's app-token merges leave behind
    # (delete-branch-on-merge skips bot merges) is what the sweep cleans.
    sweep_patterns, sweep_cron = _branch_sweep_params(config)
    sweep_text = branch_sweep_workflow(sweep_patterns, cron=sweep_cron)
    sweep_rel = f"{config.state_dir}/ci/branch-sweep.yml"
    _adopt_stage(
        state_base / "ci" / "branch-sweep.yml",
        sweep_rel,
        sweep_text,
        report,
    )

    # (6) Explicit host opt-in: live .claude/ (still never overwrites).
    if include_claude:
        claude_dir = root / ".claude"
        if _adopt_plant(
            claude_dir / "CLAUDE.md",
            ".claude/CLAUDE.md",
            claude_doc,
            report,
        ):
            record_doc_hash(backend, ".claude/CLAUDE.md", claude_doc)
        _adopt_plant(
            claude_dir / "settings.json",
            ".claude/settings.json",
            settings_text,
            report,
        )

    # (6b) Enforcement opt-in + kit-owned regeneration (EAP program review
    # §6.1). `--wire-enforcement` installs the LIVE CI gate (the locked door
    # that pairs with include_claude's live nag). Once the gate EXISTS it is
    # KIT-OWNED: every adopt/upgrade pass regenerates it in place — the
    # staged-artifacts-always-regenerate mechanism extended to the one live
    # workflow the kit installs — so template fixes (e.g. the #108 born-red
    # sentinel fixes, live-fired on gba-homebrew) reach installed gates on
    # `bootstrap.py upgrade` instead of stranding as hand-forked patches.
    # A default adopt still never CREATES live CI (the safety doctrine is
    # unchanged): only --wire-enforcement installs it; existence is the
    # opt-in signal after the first install. Hand edits are overwritten by
    # design — the generated header declares it and routes host carve-outs
    # to a separate workflow file.
    # Carve-out protection (superbot-games PR #16 class, shipped PR #137):
    # a host that hand-added jobs/steps INSIDE a kit-owned workflow — e.g.
    # its only pytest job — must never lose them to a silent regen. The
    # shared helper detects the additions, banks the full pre-regen copy
    # under <state_dir>/backup/ (content-hash-named, so successive regens
    # never clobber an earlier bank), and reports each carve-out explicitly
    # (upgrade surfaces them in upgrade-report.md). The regen itself still
    # happens — the workflow stays kit-owned; the host relocates the banked
    # additions into a separate workflow file.
    _regen_kit_owned_workflow(
        root,
        config,
        LIVE_CI_RELPATH,
        gate_text,
        report,
        noun="gate",
        install_when_absent=wire_enforcement,
        old_text=old_staged_gate,
    )
    # The auto-merge enabler (EAP §6.10) follows the gate's exact lifecycle:
    # created only by --wire-enforcement, kit-owned once it exists (a
    # hand-forked copy at the same path falls under kit ownership on the
    # next adopt/upgrade pass — the point of the shared basename).
    _regen_kit_owned_workflow(
        root,
        config,
        AUTOMERGE_ENABLER_RELPATH,
        enabler_text,
        report,
        noun="enabler",
        install_when_absent=wire_enforcement,
        old_text=old_staged_enabler,
    )
    # The branch sweep (ORDER 023) follows the enabler's exact lifecycle:
    # created only by --wire-enforcement, kit-owned once it exists.
    _regen_kit_owned_workflow(
        root,
        config,
        BRANCH_SWEEP_RELPATH,
        sweep_text,
        report,
        noun="sweep",
        install_when_absent=wire_enforcement,
        old_text=old_staged_sweep,
    )
    if (root / AUTOMERGE_ENABLER_RELPATH).is_file():
        # The §6.10 second half: the enabler is inert until two owner-UI
        # repo settings exist — say so in the adopt output itself, every
        # pass (the checklist is idempotent guidance, not a nag).
        report.extend(_repo_settings_checklist(enabler_context))
        # Install-time preflight (the online half of enabler-install-
        # preflight-2026-07-13; the check-time branch half is #321): verify
        # the two settings the checklist can only describe — "Allow
        # auto-merge" + required contexts — against the live GitHub API.
        # Advisory + fail-open by contract: offline / tokenless / non-GitHub
        # remotes collapse to one UNVERIFIED line, never a failed adopt.
        report.extend(enabler_install_preflight(root, enabler_context))
    # required_context sanity (queued kit fix 3, the websites class): after
    # the gate/enabler regens above so a just-installed live gate counts as
    # a matching context. Advisory line only — see the helper's docstring.
    context_advisory = _required_context_advisory(root, enabler_context)
    if context_advisory is not None:
        report.append(context_advisory)

    # (6b2) Lane-aware adopt: declare the just-planted lane heartbeat so the
    # status gate validates it (config mutated in place — cmd_adopt's
    # engagement checklist reads the same object).
    config_dirty = False
    if lane is not None:
        config_dirty = _register_lane_heartbeat(root, config, lane, report)

    # (6c) The install self-identifies (§4.1): record the kit version in the
    # config file (a declared dataclass field — survives load→save) and state.
    if config.kit_version != KIT_VERSION:
        config.kit_version = KIT_VERSION
        config_dirty = True
    if config_dirty:
        save_config(root, config)
    backend.set("kit_version", KIT_VERSION)
    report.append(f"recorded: kit_version {KIT_VERSION}")

    # (7) Point the adopter at the interview loop.
    report.append(_ADOPT_NEXT_STEPS)
    return report
