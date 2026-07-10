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
from engine.hooks.settings import full_settings_template, hooks_fill_table
from engine.lib.atomicio import atomic_write_text
from engine.lib.config import KIT_VERSION, Config, save_config
from engine.lib.guardrail import assert_safe_target
from engine.render import build_context, find_placeholders, load_templates, render
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
    """
    if not dist_file.is_file():
        return None
    text = dist_file.read_text(encoding="utf-8")
    version = dist_version(text) or "unknown"
    dest = root / config.state_dir / BACKUP_DIRNAME / f"bootstrap-{version}.py"
    rel = f"{config.state_dir}/{BACKUP_DIRNAME}/bootstrap-{version}.py"
    if dest.exists() and dest.read_text(encoding="utf-8") == text:
        # Never silent on the idempotent path: an upgrade whose OLD dist was
        # already banked (a prior adopt/check pass, or a re-run) must still
        # account for it explicitly, or the report's only `archived:` line
        # names the NEW version and readers conclude the old dist was never
        # banked — the exact doubt the archive-first covenant exists to remove
        # (field-reported three times, v1.6.0 rollout).
        report.append(f"archived: {rel} (already banked)")
        return dest
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
    return (
        "# Session logs\n\n"
        "Per-session logs live here as `<date>-<slug>.md`, newest first. "
        "Create the log as the session's FIRST commit with a born-red status "
        "(`> **Status:** `in-progress``) so in-flight work is visible to "
        "parallel sessions, then flip it to `complete` as the deliberate LAST "
        "step once the close-out is written — a half-done session never reads "
        "as finished. Before it counts as complete, a log must carry these "
        "markers, each written with its exact backticked byte-form: "
        f"{pairs}.\n\n"
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
        "#       - uses: actions/checkout@v4\n"
        "#       - name: substrate checks\n"
        "#         run: python3 bootstrap.py check --strict\n"
    )


LIVE_CI_RELPATH = ".github/workflows/substrate-gate.yml"


def live_ci_workflow(interpreter: str = "python3", sessions_dir: str = ".sessions") -> str:
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
    exactly this). The workflow instead derives the card from what the PR/push
    diff touches under ``sessions_dir`` and passes it via
    ``check --session-log``. When the diff names **no card** the step passes
    an explicitly named, nonexistent sentinel **without**
    ``--require-session-log`` — per the engine contract an explicitly named
    absent card is ADVISORY. (The previous behaviour — omitting the argument —
    was NOT fail-open in CI: the engine's newest-by-mtime fallback latched
    onto the mid-session in-progress card and redded every unrelated PR;
    adopter live-fire, gba-homebrew PR #3, 2026-07-10.) A card **ADDED** by
    the PR (a born-red heartbeat: first-commit-carries-an-in-progress-card
    conventions make in-progress the REQUIRED state at birth) also gates
    advisory via the absent sentinel, because under ``--strict`` the engine
    reds ANY existing-but-incomplete card — the locked door could never pass
    a heartbeat (adopter live-fire: gba-homebrew PR #2 merged red on exactly
    this). A card **MODIFIED** by the PR (every session close-out flips one)
    keeps the full ``--require-session-log`` locked door, so a close-out that
    forgot to flip ``complete`` still reds. Both fixes validated live across
    gba-homebrew PRs #3–#14.

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
    file.
    """
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
        "      - uses: actions/checkout@v4\n"
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
        "      - uses: actions/setup-python@v5\n"
        "        if: steps.lane.outputs.control_only != 'true'\n"
        "        with:\n"
        '          python-version: "3.x"\n'
        "      - name: substrate gate (docs + session-log required)\n"
        "        if: steps.lane.outputs.control_only != 'true'\n"
        "        # Gate on the session card THIS PR/push touches (CI flattens\n"
        "        # mtimes, so the engine's newest-by-mtime guess is unreliable\n"
        "        # here). No card in the diff -> pass an explicitly named,\n"
        "        # nonexistent sentinel WITHOUT --require-session-log: per the\n"
        "        # engine's contract an explicit absent card is ADVISORY,\n"
        "        # while the bare mtime fallback latches onto the mid-session\n"
        "        # in-progress card and reds every unrelated PR (adopter\n"
        "        # live-fire, gba-homebrew PR #3, 2026-07-10 — the omitted\n"
        "        # argument was never fail-open in CI). Second live-fire case:\n"
        "        # a heartbeat PR that ADDS the born-red card (first-commit\n"
        "        # conventions REQUIRE an in-progress card at birth) can never\n"
        "        # satisfy the locked door — gba-homebrew PR #2 merged red on\n"
        "        # exactly this. So: a card ADDED by the PR gates ADVISORY via\n"
        "        # the absent sentinel (under --strict the engine reds ANY\n"
        "        # existing-but-incomplete card, required or not — born-red is\n"
        "        # the REQUIRED state at birth, so a heartbeat must not be\n"
        "        # judged on completeness); a card MODIFIED by the PR (every\n"
        "        # session close-out flips one) keeps the full locked-door\n"
        "        # gate, so a close-out that forgot to flip `complete` still\n"
        "        # reds.\n"
        "        run: |\n"
        '          if [ -n "${{ github.base_ref }}" ]; then\n'
        '            range="origin/${{ github.base_ref }}...HEAD"\n'
        "          else\n"
        '            range="${{ github.event.before }}..${{ github.sha }}"\n'
        "          fi\n"
        '          card="$(git diff --name-only --diff-filter=d "$range" -- '
        f"'{sessions_dir}/*.md' ':!{sessions_dir}/README.md' 2>/dev/null "
        '| tail -1)"\n'
        '          added="$(git diff --name-only --diff-filter=A "$range" -- '
        f"'{sessions_dir}/*.md' ':!{sessions_dir}/README.md' 2>/dev/null "
        '| tail -1)"\n'
        '          echo "session gate card: ${card:-<none - advisory sentinel>}"\n'
        '          if [ -n "$card" ] && [ "$card" != "$added" ]; then\n'
        f"            {interpreter} bootstrap.py check --strict --require-session-log"
        ' --session-log "$card"\n'
        "          elif [ -n \"$card\" ]; then\n"
        '            echo "card $card is newly ADDED by this PR (born-red heartbeat)'
        ' — advisory sentinel gate"\n'
        f"            {interpreter} bootstrap.py check --strict --session-log "
        f"{sessions_dir}/__born-red-card-added__.md\n"
        "          else\n"
        f"            {interpreter} bootstrap.py check --strict --session-log "
        f"{sessions_dir}/__no-card-in-diff__.md\n"
        "          fi\n"
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

    # (0b) Adopt renders what it knows: seed derivable slots (provisional,
    # never overwriting an existing answer), then build the render context.
    report.extend(record_derived_slots(backend, derive_slots(root, config.docs_root)))
    bootstrap_path = _vendor_bootstrap(root, report)
    # (0c) Bank the running dist under <state_dir>/backup/ (§4.3): a future
    # upgrade's doc diff needs the OLD templates to still exist, so the
    # archive is written before anything could ever overwrite the file.
    dist_file = Path(bootstrap_path)
    if not dist_file.is_absolute():
        dist_file = root / bootstrap_path
    archive_dist(root, config, dist_file, report)
    context = build_context(backend.data)
    # The live integration mode is state, not a slot — render it truthfully.
    context.setdefault("integration_mode", str(backend.get("mode", "guided")))

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

    # (2) Session-log scaffolding.
    sessions_rel = f"{config.sessions_dir}/README.md"
    readme = _adopt_sessions_readme(config.session_markers)
    _adopt_plant(root / config.sessions_dir / "README.md", sessions_rel, readme, report)

    # (3) The context-pack index skeleton.
    project_name = context.get("project_name") or root.name
    skeleton = pack_index_skeleton(project_name)
    _adopt_plant(root / "project.index.json", "project.index.json", skeleton, report)

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
    gate_text = live_ci_workflow(
        config.interpreter_for_checks or "python3",
        sessions_dir=config.sessions_dir,
    )
    gate_rel = f"{config.state_dir}/ci/substrate-gate.yml"
    _adopt_stage(
        state_base / "ci" / "substrate-gate.yml",
        gate_rel,
        gate_text,
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
    live_gate = root / LIVE_CI_RELPATH
    if live_gate.is_file():
        if live_gate.read_text(encoding="utf-8") == gate_text:
            report.append(f"kept: {LIVE_CI_RELPATH} (kit-owned, already current)")
        else:
            atomic_write_text(live_gate, gate_text)
            report.append(
                f"regenerated: {LIVE_CI_RELPATH} (kit-owned — template@new; "
                "hand edits are overwritten, host carve-outs belong in a "
                "separate workflow)",
            )
    elif wire_enforcement:
        _adopt_plant(
            live_gate,
            LIVE_CI_RELPATH,
            gate_text,
            report,
        )

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
