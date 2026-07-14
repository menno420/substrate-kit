"""Host-project configuration for one substrate-kit install.

Reads and writes ``substrate.config.json`` — the single file that absorbs every
host-specific knob so the engine code never hardcodes a project value. Two
interpreters are kept explicitly separate (Hermes-final): ``interpreter`` is the
kit's own runtime, ``interpreter_for_checks`` is the host project's verification
runtime (e.g. ``python3.10`` for a repo whose CI pins 3.10).
"""

from __future__ import annotations

import json
import sys
import uuid
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

from engine.lib.atomicio import atomic_write_text

CONFIG_FILENAME = "substrate.config.json"
DEFAULT_STATE_DIR = ".substrate"

# THE kit version (founding plan §4.1). Semver keyed to the planted-doc
# contract, state schema, config schema, and CLI surface: MAJOR = breaking
# change to any of those; MINOR = new capability; PATCH = fixes. Exposed as
# `bootstrap.py --version`, stamped into the dist header by
# `src/build_bootstrap.py`, and recorded into `substrate.config.json`
# (`kit_version`) + state by `adopt`/`upgrade`. Bump together with
# `pyproject.toml` `[project] version` (a test pins them equal) and a new
# CHANGELOG.md section (the release workflow refuses to publish without one).
KIT_VERSION = "1.17.0"


def _new_project_id() -> str:
    """Return a short, stable identifier for one install."""
    return uuid.uuid4().hex[:12]


def _default_cadence() -> dict[str, int]:
    """Return the default cadence knobs (every hardcoded cadence lives here)."""
    return {
        # 30, not 20: the source repo's live cadence (superbot Q-0134 — at burst
        # velocity a 20-band fired the docs pass several times a day); the 20
        # default was stale drift the founding plan §3.4 rules fixed.
        "reconciliation_prs": 30,
        "reconciliation_sessions": 20,
        "compaction_sessions": 20,
        "critical_slot_grace_sessions": 3,
        "staleness_days": 14,
        "guided_practice_sessions": 3,
    }


def _default_reflection() -> dict:
    """Return the reflection-buffer knobs (size cap is a hard context guard)."""
    return {"enabled": True, "buffer_size": 5}


def _default_orientation() -> dict:
    """Return the orientation-budget knobs (the K0 ≤7,000-word gate).

    ``boot_docs`` empty means "fall back to ``readpath_docs``" — the
    unconditional boot-read set the budget counts. ``headroom_warn_ratio``
    arms the advisory-only headroom gauge (PR #308): warn at >= this
    fraction of ``budget_words`` (never exit-affecting); >= 1 disables it.
    """
    return {"budget_words": 7000, "boot_docs": [], "headroom_warn_ratio": 0.95}


def _default_economy() -> dict:
    """Return the context-economy knobs (taxonomy/gauges are host policy).

    ``maturity`` gates the actuator: ``shadow`` (report only, the first-prune
    safety protocol) -> ``gated`` (apply with review) -> ``normal``. Classes and
    gauges ship empty — the engine supplies a documented generic default when
    unset; each adopting repo declares its own table (the kit ships the search,
    not our constants).
    """
    return {
        "maturity": "shadow",
        "pass_records_dir": "planning",
        "reference_roots": [],
        "id_patterns": [r"Q-\d{3,}", r"D-\d{3,}", r"R-\d{3,}"],
        "classes": [],
        "gauges": [],
        "debt_threshold": 10,
    }


def _default_namespace() -> dict:
    """Return the namespace-guard knobs (roots to scan + reserved-name map)."""
    return {"roots": [], "reserved": {}}


def _default_review_seam() -> dict:
    """Return the review-seam knobs (provisioned, not wired — no live reviewer)."""
    return {"reviewer": None}


def _default_heartbeat_files() -> list[str]:
    """Return the control-heartbeat file(s) the status checker validates.

    One entry — ``control/status.md`` — for the normal one-Project-per-repo
    shape. A SHARED repo hosting several Projects lists one file per lane
    (the superbot-games pattern, inbox ORDER 004: e.g.
    ``control/status-mining.md`` + ``control/status-exploration.md``): the
    one-writer-per-file rule is preserved *per lane*, and every listed
    heartbeat must beat. An empty list falls back to the default at every
    consumer (a misconfiguration must not silently disable the gate).
    """
    return ["control/status.md"]


"""Default work-claim directory (EAP program review §6.4).

The ONE kit-owned claims convention has two surfaces: ORDER claims are the
``claimed-by:`` annotation on a lane's own heartbeat orders line (one writer
per file — see ``control/README.md`` § "Claiming an order"), and WORK/lane
claims are one-file-per-claim markdown files under this directory (superbot's
measured evidence: a shared-append claim ledger merge-conflicts at ~98% under
concurrent sessions vs 0% for per-file — ``tools/sim/claim_layout_sim.py`` in
menno420/superbot; see the planted ``control/claims/README.md``). Lives under
``control/`` on purpose: claims are coordination traffic, so they ride the
control fast lane and land on main fast. Legacy locations
(``docs/owner/claims/``, root ``claims/``) are auto-detected by
``check_claims`` with an advisory migration nudge.
"""
DEFAULT_CLAIMS_DIR = "control/claims"


def _default_automerge() -> dict:
    """Return the auto-merge-enabler knobs (EAP program review §6.10).

    Parameterizes the kit-owned planted ``.github/workflows/
    auto-merge-enabler.yml`` (see ``adopt.automerge_enabler_workflow``):

    - ``branch_patterns`` — head-branch patterns the enabler arms on. A
      trailing ``*`` is a prefix match (``claude/*`` → every ``claude/…``
      head); anything else matches exactly. An empty list falls back to the
      default at the consumer (the ``heartbeat_files`` doctrine: a
      misconfiguration must not silently disable — or widen — the arming).
      Default covers ``claude/*`` (session branches) AND ``claim/*``
      (control fast-lane claim PRs): a claude/-only list left claim PRs
      green+clean but unarmed forever (kit PR #293, the live stall class).
    - ``required_context`` — the required status-check context the arming
      message names (default ``substrate-gate``, the planted gate's job).
      Informational only: the workflow's refuse-to-arm guard counts the
      base branch's required contexts generically via the rules API, so a
      wrong name here mislabels a log line, never the guard.
    """
    return {
        "branch_patterns": ["claude/*", "claim/*"],
        "required_context": "substrate-gate",
    }


def _default_branch_sweep() -> dict:
    """Return the scheduled branch-sweep knobs (inbox ORDER 023).

    Parameterizes the kit-owned planted ``.github/workflows/
    branch-sweep.yml`` (see ``adopt.branch_sweep_workflow``):

    - ``branch_patterns`` — head-branch patterns the sweep may delete. A
      trailing ``*`` is a prefix match (``claude/*`` → every ``claude/…``
      head); anything else matches exactly. An empty list falls back to
      the default at the consumer (the ``heartbeat_files`` doctrine: a
      misconfiguration must not silently widen the sweep — a bare ``*``
      would put EVERY branch in scope). Default covers the fleet's agent
      actors: ``claude/*`` (session branches), ``codex/*`` and ``bot/*``
      (sibling agent conventions). Deliberately NOT the automerge list:
      ``claim/*`` fast-lane refs are excluded until the convention earns
      its own evidence, and the sweep's blast radius is deletion, not
      arming.
    - ``cron`` — the 5-field schedule (default daily at 03:17 UTC —
      off the top of the hour, where GitHub sheds scheduled load).
      Blank falls back to the default at the consumer.
    """
    return {
        "branch_patterns": ["claude/*", "codex/*", "bot/*"],
        "cron": "17 3 * * *",
    }


def _default_preflight_scripts() -> list[str]:
    """Return the repo-local preflight scripts ``check`` runs on the full lane.

    Local-ritual ↔ CI-gate parity (ORDER 018 / idea-engine ASK 002): each
    entry is a repo-relative command line (``shlex``-split; a leading
    ``*.py`` token runs under the interpreter already running ``check``)
    executed by ``cmd_check`` on the full — non ``--status-only`` — lane,
    with any non-zero exit riding the strict finding loop. Because the
    generated substrate-gate's full lane itself invokes ``bootstrap.py
    check --strict``, this ONE list is what both the local ritual and CI
    run — a checker added to the repo's preflight wrapper is enforced in
    both venues with zero workflow edits. The default names the
    conventional wrapper path (idea-engine's ``scripts/preflight.py``
    convergence pattern) so parity arrives on upgrade without a config
    edit; an absent script self-skips with a NOTE, never a red.
    """
    return ["scripts/preflight.py"]


def _default_badge_tokens() -> list[str]:
    """Return the default Status-badge taxonomy the doc checker accepts."""
    return [
        "binding",
        "living-ledger",
        "reference",
        "plan",
        "historical",
        "audit",
        "owner-guidance",
        "ideas",
        "archive",
    ]


def _default_readpath_docs() -> list[str]:
    """Return the read-path doc names that seed the reachability roots."""
    return ["AGENT_ORIENTATION.md", "current-state.md"]


def _default_session_markers() -> list[dict[str, str]]:
    """Return the markers every session log must carry (label + substring).

    The Model line (``📊 Model: <model> · <effort> · <task-class>``) is the
    PL-004 telemetry feed (KL-3): ``session-close`` harvests it into
    ``telemetry/model-usage.jsonl``. New adopts require it from birth;
    existing installs gain it at ``upgrade`` (a consumer's gate only tightens
    when it upgrades — founding plan §5.2).
    """
    return [
        {"label": "Status badge", "needle": "**Status:**"},
        {"label": "Session idea", "needle": "💡"},
        {"label": "Previous-session review", "needle": "previous-session review"},
        {"label": "Model line", "needle": "\N{BAR CHART} Model:"},
    ]


@dataclass
class Config:
    """Host-project configuration for one substrate-kit install."""

    project_id: str = field(default_factory=_new_project_id)
    # The kit version this install last adopted/upgraded from — "" until an
    # `adopt`/`upgrade` records it (a pre-release install honestly reports
    # unrecorded rather than guessing). A DECLARED dataclass field on purpose:
    # `from_dict` drops unknown keys and `save_config` serialises only
    # dataclass fields, so a bare JSON key would be stripped on the next
    # load→save round-trip (founding plan §4.1).
    kit_version: str = ""
    interpreter: str = field(default_factory=lambda: sys.executable)
    interpreter_for_checks: str | None = None
    state_dir: str = DEFAULT_STATE_DIR
    docs_root: str = "docs"
    sessions_dir: str = ".sessions"
    paths: dict[str, str] = field(default_factory=dict)
    cadence: dict[str, int] = field(default_factory=_default_cadence)
    scopes: dict[str, str] = field(default_factory=dict)
    badge_tokens: list[str] = field(default_factory=_default_badge_tokens)
    readpath_docs: list[str] = field(default_factory=_default_readpath_docs)
    session_markers: list[dict[str, str]] = field(
        default_factory=_default_session_markers,
    )
    reflection: dict = field(default_factory=_default_reflection)
    orientation: dict = field(default_factory=_default_orientation)
    economy: dict = field(default_factory=_default_economy)
    namespace: dict = field(default_factory=_default_namespace)
    seams: list[dict] = field(default_factory=list)
    review_seam: dict = field(default_factory=_default_review_seam)
    heartbeat_files: list[str] = field(default_factory=_default_heartbeat_files)
    # Work-claim home (EAP §6.4 — see DEFAULT_CLAIMS_DIR above). A host that
    # deliberately keeps its claims elsewhere (e.g. superbot's
    # docs/owner/claims/) pins that path here; the pinned dir is then
    # canonical for that host and the legacy-location nudge never fires on it.
    claims_dir: str = DEFAULT_CLAIMS_DIR
    # Auto-merge-enabler knobs (EAP §6.10 — see _default_automerge above).
    automerge: dict = field(default_factory=_default_automerge)
    # Scheduled branch-sweep knobs (ORDER 023 — see _default_branch_sweep
    # above).
    branch_sweep: dict = field(default_factory=_default_branch_sweep)
    # Local preflight scripts (ORDER 018 — see _default_preflight_scripts
    # above): the ONE check list both the local ritual and the CI gate run.
    preflight_scripts: list[str] = field(
        default_factory=_default_preflight_scripts,
    )

    def to_json(self) -> str:
        """Serialise the config to indented, key-sorted JSON."""
        return json.dumps(asdict(self), indent=2, sort_keys=True)

    @classmethod
    def from_dict(cls, data: dict) -> Config:
        """Build a Config from a parsed dict, ignoring unknown keys."""
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


def config_path(root: Path) -> Path:
    """Return the config-file path for a project ``root``."""
    return root / CONFIG_FILENAME


def load_config(root: Path) -> Config:
    """Load the config from ``root``; return defaults if none exists."""
    path = config_path(root)
    if not path.exists():
        return Config()
    data = json.loads(path.read_text(encoding="utf-8"))
    return Config.from_dict(data)


def save_config(root: Path, config: Config) -> None:
    """Write ``config`` to ``root`` atomically."""
    atomic_write_text(config_path(root), config.to_json() + "\n")
