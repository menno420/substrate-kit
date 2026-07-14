"""Mechanical work-claim writer — the ``bootstrap claim`` verb's logic.

Why + provenance: the one-file-per-claim work-claim convention (EAP §6.4,
``control/claims/README.md``) only protects parallel sessions when the claim
bullet PARSES — an unparseable claim is invisible to ``check_claims``'
duplicate scan, which silently defeats the claim system during the exact
window it exists for. That failure is realized, not theoretical: the
2026-07-14 git-truth session (#358 card, 💡 ender) hand-wrote a bullet
without the backticked token and fired ``claims-format`` mid-session. This
module closes the gap the same way ``engine.heartbeat`` closed the
hand-stamped ``updated:`` line: a mechanical writer that renders from — and
round-trips through — the SAME ``engine.grammar`` constants the enforcer
consumes (``WORK_CLAIM_BULLET_RE`` / ``WORK_CLAIM_DATE_RE``, EAP §6.8), so
the verb can never emit a claim ``check_claims`` cannot parse.

Two lanes, both refuse-and-name (never a silent clobber):

- **Write lane** (:func:`render_claim` + the CLI's default) — renders the
  one-bullet claim file for branch ``claude/<slug>``: backticked branch
  token first (the duplicate scan's key), bold scope, optional files/area
  segment, and the current UTC date as the LAST ``YYYY-MM-DD`` on the line
  (the post-#353 rule: the claim's own date is the last date on the bullet,
  so a dated filename mentioned in the scope can never shadow it).
  Overwriting an existing file is allowed only when :func:`owner_token`
  proves it is this branch's own claim (a refresh).
- **Delete lane** (``--delete``) — removes YOUR OWN claim at session close;
  a foreign claim (different branch token, or a file the grammar cannot
  parse — ownership unprovable) is refused with the file left intact.

Ownership check shape (decided-and-flagged): the existing file's bullet
token must equal the branch this invocation derives from the slug — the
same token the duplicate scan keys on, so "who owns this file" and "who
holds this claim" can never disagree. Stdlib only; sits below ``cli.py``
(which owns file I/O via ``atomic_write_text``) and imports only grammar.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from engine.grammar import (
    WORK_CLAIM_BULLET_RE,
    WORK_CLAIM_DATE_RE,
    work_claim_order_ids,
)

# Work branches are claude/<slug> by fleet convention (the auto-merge-enabler
# allowlist + every session card in .sessions/); the claim FILE flattens the
# slash so the filename stays a single path segment: claude-<slug>.md.
BRANCH_PREFIX = "claude/"
FILENAME_PREFIX = "claude-"

# Filename-safe slug: starts alphanumeric, then alphanumerics, dot, dash,
# underscore. Everything else (slashes, spaces, backticks) is refused — the
# slug names both a git branch and a file.
_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

# The `--order` flag's accepted shapes: bare digits (`20` / `020`), with an
# optional case-insensitive `order ` prefix tolerated (`ORDER 020`) — the
# rendered segment is always the normalized `order NNN`.
_ORDER_FLAG_RE = re.compile(r"^(?:order\s+)?(\d{1,4})$", re.IGNORECASE)


class ClaimError(ValueError):
    """A claim write/delete that cannot proceed safely.

    Raised instead of guessing: a malformed slug, scope text that would
    break the bullet grammar, or a foreign claim at the target path each
    name their fix in the message — never a silent clobber.
    """


def branch_for(slug: str) -> str:
    """Return the claim's branch (``claude/<slug>``); refuse a bad slug."""
    if not _SLUG_RE.match(slug):
        msg = (
            f"slug {slug!r} is not filename-safe — use alphanumerics, dots, "
            "dashes, underscores (the slug names both the claude/<slug> "
            "branch and the claude-<slug>.md claim file)."
        )
        raise ClaimError(msg)
    return f"{BRANCH_PREFIX}{slug}"


def claim_filename(slug: str) -> str:
    """Return the claim file's name (``claude-<slug>.md``); refuse a bad slug."""
    branch_for(slug)  # same validation, one home
    return f"{FILENAME_PREFIX}{slug}.md"


def utc_date(now: datetime | None = None) -> str:
    """Render the claim date (UTC ``YYYY-MM-DD``) — computed at call time.

    Always the CURRENT UTC date, never a cached module-load value: a claim
    stamped with a stale date starts life closer to the ~72h staleness
    horizon than it should.
    """
    moment = now or datetime.now(timezone.utc)
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%d")


def _refuse_grammar_breakers(label: str, value: str) -> str:
    """Refuse text that would break the one-line bullet grammar."""
    if "\n" in value or "\r" in value:
        msg = f"{label} must be one line — the claim grammar is a single bullet."
        raise ClaimError(msg)
    if "`" in value:
        msg = (
            f"{label} must not contain backticks — the enforcer's bullet "
            "regex keys the duplicate scan on the LAST backticked token, so "
            f"a backtick in the {label} would shadow the branch token."
        )
        raise ClaimError(msg)
    stripped = value.strip()
    if not stripped:
        msg = f"{label} must be non-empty."
        raise ClaimError(msg)
    return stripped


def normalize_order(raw: str) -> str:
    """Return the 3-digit-normalized order id for an ``--order`` value.

    ``20`` / ``020`` / ``ORDER 020`` → ``020``. Anything else (ranges,
    comma lists, prose) is refused — a claim serves ONE order; a genuine
    multi-order session claims the primary one and names the rest in scope.
    """
    match = _ORDER_FLAG_RE.match(raw.strip())
    if not match:
        msg = (
            f"order {raw!r} is not a single order id — pass 1-4 digits "
            "(e.g. --order 020); the rendered segment is `order NNN`."
        )
        raise ClaimError(msg)
    return f"{int(match.group(1)):03d}"


def claim_order_ids(text: str) -> set[str]:
    """Return the order ids a claim FILE names on its bullet line.

    Empty when the file has no parseable bullet or the bullet names no
    order — order-less claims stay valid (the segment is optional) and are
    simply invisible to the cross-branch order-overlap scan.
    """
    bullet = WORK_CLAIM_BULLET_RE.search(text)
    if bullet is None:
        return set()
    line_end = text.find("\n", bullet.start())
    if line_end == -1:
        line_end = len(text)
    return work_claim_order_ids(text[bullet.start() : line_end])


def owner_token(text: str) -> str | None:
    """Return the claim file's bullet token (its owning branch), or None.

    None means the grammar cannot parse the file — ownership is unprovable,
    which the write/delete lanes treat as foreign (refuse, leave intact).
    """
    match = WORK_CLAIM_BULLET_RE.search(text)
    return match.group(1).strip() if match else None


def _verify_claim_roundtrip(
    text: str,
    branch: str,
    date: str,
    order: str | None = None,
) -> str:
    """Assert ``text`` parses back to ``(branch, date[, order])``; return it.

    The write → parse → equal recipe (same shape as
    ``engine.heartbeat._verify_roundtrip``), run on every render: the token
    the duplicate scan will key on must be exactly ``branch``, the LAST
    ``YYYY-MM-DD`` on the bullet line — the claim's own date under the
    post-#353 rule — must be exactly ``date``, and when an ``order`` was
    requested the cross-branch overlap scan must read it back.
    """
    parsed = owner_token(text)
    line = text.splitlines()[0] if text else ""
    dates = WORK_CLAIM_DATE_RE.findall(line)
    order_ok = order is None or order in claim_order_ids(text)
    if parsed != branch or not dates or dates[-1] != date or not order_ok:
        msg = (
            "internal round-trip failure: the rendered claim did not parse "
            f"back to token {branch!r} + date {date}"
            + (f" + order {order}" if order is not None else "")
            + " — refusing to emit a claim the enforcer cannot read."
        )
        raise ClaimError(msg)
    return text


def render_claim(
    slug: str,
    scope: str,
    *,
    area: str | None = None,
    order: str | None = None,
    now: datetime | None = None,
) -> str:
    """Render the one-bullet claim file for ``claude/<slug>``.

    Shape (``grammar.work_claim_bullet_example`` / control/claims/README.md):
    backticked branch token · bold scope [· files/area] [· order NNN] ·
    UTC date last. ``order`` is the optional inbox-ORDER reference the
    cross-branch overlap scan keys on (the #362/#363 collision fix).
    Raises :class:`ClaimError` on a slug/scope/area/order that would break
    the grammar; every render is round-trip verified before it leaves.
    """
    branch = branch_for(slug)
    scope = _refuse_grammar_breakers("scope", scope)
    norm_order = normalize_order(order) if order is not None else None
    date = utc_date(now)
    parts = [f"- `{branch}`", f"**{scope}**"]
    if area is not None:
        parts.append(_refuse_grammar_breakers("area", area))
    if norm_order is not None:
        parts.append(f"order {norm_order}")
    parts.append(date)
    return _verify_claim_roundtrip(
        " · ".join(parts) + "\n", branch, date, norm_order
    )
