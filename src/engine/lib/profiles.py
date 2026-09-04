"""Adoption profiles — the declared *shape* one install was born in.

Every knob an adopter can turn already lives in ``substrate.config.json``
(:mod:`engine.lib.config`) and every doc the kit plants already lives in one
data table (:data:`engine.adopt.ADOPT_PLAN`). What the kit had no name for was
**which shape a tree was adopted into** — so every consumer that walks the
plant table (``check_engagement``, ``check_template_sync``,
``check_skill_grounds``) assumed the one historical shape, and a host that
wanted a different one had to hand-delete files adoption would replant on its
next ``upgrade``.

A profile is that name. It is:

- **declarative** — a frozen record of which plant destinations a shape omits
  and which config defaults it is born with, never imperative planting code;
- **persisted** — ``Config.adoption_profile`` records it, so ``upgrade`` and
  ``render`` re-read the same shape rather than re-planting what ``adopt``
  deliberately left out (they already re-run ``adopt`` with the loaded config,
  so honoring the profile costs no second orchestration path);
- **closed** — an unknown name is refused loudly at ``init``/``adopt``, never
  silently defaulted, because a typo'd profile would otherwise plant the wrong
  tree and only be visible weeks later.

Two profiles ship. :data:`DEFAULT_PROFILE` (``"default"``) omits nothing and
overrides nothing: it reproduces every pre-profile adoption byte for byte, and
is what every existing install resolves to (an install whose config predates
this field loads the dataclass default). :data:`HUB_PROFILE` (``"hub"``) is the
**router-repository** shape — a repo whose job is to point at other repos and
hold estate-level records rather than to carry a product — which needs a tree
that is *intentionally sparse* at birth.

Why "hub" and not a repository name: a profile is a shape, and shapes are
portable. The kit ships no knowledge of which repository adopts which shape,
and nothing here may ever branch on one.

Pure stdlib; imports nothing from the engine (``config`` imports *this*, so the
dependency runs one way only).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

# The kit's historical shape, and the name an install carries when it never
# declared one. Changing what this profile does is a breaking change to every
# adopter, which is exactly why it is a named record rather than "the else
# branch": a diff that touches it is visible.
DEFAULT_PROFILE_NAME = "default"

# The router/records shape. Named for the ROLE, never for a repository.
HUB_PROFILE_NAME = "hub"


@dataclass(frozen=True)
class AdoptionProfile:
    """One declared adoption shape.

    ``omit_plan_dests`` names :data:`engine.adopt.ADOPT_PLAN` destinations —
    the *plan-relative* path, before ``_adopt_dest``'s ``docs_root`` remap, so
    a profile is stated once and stays correct for a host that also moved its
    docs root.

    ``plant_seat_digest`` covers the one generated doc that lives outside the
    plan (``docs/seat-digest.md``, a derived render of the planted skills index
    + capability ledger): a shape that plants neither of its inputs must not
    plant the render of them.

    ``config_defaults`` are :class:`engine.lib.config.Config` field names mapped
    to the value this shape is born with. They are applied **once**, when the
    install's config is created, and written to ``substrate.config.json`` — so
    the file an adopter reads states its own truth rather than implying it, and
    a host may then override any of them like any other key. Nothing re-applies
    them later; the config file is the truth after birth.
    """

    name: str
    summary: str
    omit_plan_dests: frozenset[str] = frozenset()
    plant_seat_digest: bool = True
    config_defaults: Mapping[str, Any] = field(default_factory=dict)

    def omits(self, plan_relpath: str) -> bool:
        """True when this shape does not plant ``plan_relpath``."""
        return plan_relpath in self.omit_plan_dests


DEFAULT_PROFILE = AdoptionProfile(
    name=DEFAULT_PROFILE_NAME,
    summary=(
        "the kit's historical shape — every planted doc, the control/ bus, "
        "a hidden .sessions/ dir, and a tracked unbounded guard-fire ledger"
    ),
)


# --- the hub shape -------------------------------------------------------
#
# K1 (no dead control/ room): the seat-era coordination bus — inbox, status
# heartbeat, claims — was designed for several autonomous Projects sharing one
# repository. A router repository has no lanes to coordinate, so planting the
# bus gives it a directory with a live name and no traffic on day one. Every
# checker that reads the bus (`check_status_current`, `check_inbox_append`,
# `check_claims`, `check_baton_resolves`, `check_baton_freshness`) is
# input-gated on those files existing and self-quiets when they do not — that
# is the kit's own documented contract ("a host that never adopted the bus adds
# nothing here", check_status_current's module docstring), so omitting the bus
# turns the bus checks off by construction rather than by suppression.
_CONTROL_DESTS = frozenset(
    {
        "control/README.md",
        "control/inbox.md",
        "control/status.md",
        "control/claims/README.md",
    },
)

# K2 (no generic docs pile): the seventeen docs/ plants are a general-purpose
# product-repository reading set. A hub's documentation IS its structure — it
# files by role, not into a flat docs/ directory — so planting the generic set
# recreates on day one exactly the pile a fresh hub exists to escape. The hub
# shape therefore plants NOTHING generic under docs/ and lets the adopter
# declare its own folders; the kit deliberately ships no opinion about what
# those folders are called (that belongs to the adopter's own migration, not to
# a portable kit).
_GENERIC_DOC_DESTS = frozenset(
    {
        "docs/AGENT_ORIENTATION.md",
        "docs/CAPABILITIES.md",
        "docs/SKILLS.md",
        "docs/ROUTINES.md",
        "docs/ai-project-workflow.md",
        "docs/architecture.md",
        "docs/collaboration-model.md",
        "docs/current-state.md",
        "docs/decisions.md",
        "docs/helper-policy.md",
        "docs/ideas/README.md",
        "docs/owner-profile.md",
        "docs/ownership.md",
        "docs/question-router.md",
        "docs/reading-path.md",
        "docs/repo-navigation-map.md",
        "docs/runtime_contracts.md",
    },
)

HUB_PROFILE = AdoptionProfile(
    name=HUB_PROFILE_NAME,
    summary=(
        "a router/records repository — no control/ bus, no generic docs/ set, "
        "a visible sessions/ dir, and an untracked size-capped guard-fire "
        "ledger"
    ),
    omit_plan_dests=_CONTROL_DESTS | _GENERIC_DOC_DESTS,
    # docs/seat-digest.md renders the planted skills index and capability
    # ledger; the hub plants neither, so the render would be a doc about two
    # absent docs.
    plant_seat_digest=False,
    config_defaults={
        # The boot set a shape that plants no docs is born with. The kit's
        # shipped default names two documents this shape guarantees it will
        # never plant, and leaving it alone was wrong: a bare hub is clean only
        # while it stays EMPTY. The moment it writes its own state document —
        # which is exactly what "declare your own folders" tells it to do —
        # `check_orientation_budget` engages on the doc that exists and reds,
        # EXIT-AFFECTING, on the one that never will (MEASURED: 3 findings
        # bare, 4 with an `orientation-missing` for docs/AGENT_ORIENTATION.md
        # once docs/current-state.md is created).
        #
        # Empty is NOT the fix: with no read-path roots the hub's own state
        # document becomes an orphan under `check_reachable` instead — one
        # false red traded for another (measured both ways). Naming the one
        # entry a hub plausibly writes keeps the boot-set gate real, keeps
        # orphan detection working, and is a config key the adopter re-points
        # if it files its state document elsewhere. That is configuration, not
        # a rename.
        "readpath_docs": ["current-state.md"],
        # K3: visible, not hidden. `sessions_dir` was already the seam — this
        # only changes which value the shape is born with, so a hub never needs
        # the rename that made this a birth-time requirement.
        "sessions_dir": "sessions",
        # K5: telemetry stays ON and useful; what changes is that it is not a
        # tracked artifact and cannot grow without bound. See
        # `engine.lib.config._default_telemetry` for each axis.
        "telemetry": {
            "guard_fires": {
                "enabled": True,
                "path": "",
                "tracked": False,
                "max_records": 2000,
            },
        },
    },
)


PROFILES: dict[str, AdoptionProfile] = {
    DEFAULT_PROFILE.name: DEFAULT_PROFILE,
    HUB_PROFILE.name: HUB_PROFILE,
}

PROFILE_NAMES: tuple[str, ...] = tuple(sorted(PROFILES))


class UnknownProfileError(ValueError):
    """Raised for a profile name the kit does not ship."""


def resolve_profile(name: str | None) -> AdoptionProfile:
    """Return the profile called ``name``; ``None``/empty means the default.

    Raises :class:`UnknownProfileError` for anything else. Refusing loudly is
    the point: a silent fallback would plant the historical tree under a
    misspelled hub profile and the divergence would only surface once the
    unwanted directories were already committed.
    """
    if not name:
        return DEFAULT_PROFILE
    try:
        return PROFILES[str(name)]
    except KeyError:
        known = ", ".join(PROFILE_NAMES)
        raise UnknownProfileError(
            f"unknown adoption profile {name!r} — known profiles: {known}",
        ) from None


def profile_for_config(config: Any) -> AdoptionProfile:
    """Return the profile an install's ``config`` declares.

    Fail-safe on a config that declares something unknown: a checker walking a
    foreign tree must not crash on it, so the *readers* degrade to the default
    shape while ``init``/``adopt`` — the writers, where a typo is still
    correctable — refuse via :func:`resolve_profile`.
    """
    try:
        return resolve_profile(getattr(config, "adoption_profile", None))
    except UnknownProfileError:
        return DEFAULT_PROFILE
