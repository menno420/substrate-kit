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
KIT_VERSION = "1.1.0"


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
    unconditional boot-read set the budget counts.
    """
    return {"budget_words": 7000, "boot_docs": []}


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
