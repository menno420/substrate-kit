"""Tests for the shared wholesale-replacement residue core (KL-5 generalization).

The lib seam (``engine.lib.residue``) is the S3 archive fingerprint lifted to
surface-agnostic form plus the canonical session-card judgment-slot hints.
Pins here are the drift contracts named in the module docstring: the fill
token and code-stripping regexes mirror ``checks.check_session_log`` (lib/
must not import checks/), and every guarded card hint must appear verbatim
inside a real ``draft_card`` render (handoff draws its hints from the same
constants — a drift either way is a test failure, not a silent miss).
"""

from __future__ import annotations

import re

from engine.checks.check_session_log import (
    _CODE_SPAN_RE,
    _FENCE_RE,
    DRAFT_FILL_TOKEN,
)
from engine.lib.config import Config
from engine.lib.residue import (
    _RESIDUE_CODE_SPAN_RE,
    _RESIDUE_FENCE_RE,
    CARD_GUARDED_HINTS,
    CARD_HINT_VERIFY_RESULT,
    RESIDUE_FILL_TOKEN,
    RESIDUE_SHINGLE_WORDS,
    probe_card_residue,
    probe_residue,
    residue_shingles,
    strip_code_regions,
)
from engine.loop.handoff import SessionEvidence, draft_card

_SLOT_STRIP_RE = re.compile(r"\[\[fill:\s*(.*?)\]\]", re.DOTALL)


def _draft(verify_command: str | None = None) -> str:
    evidence = SessionEvidence(verify_command=verify_command)
    return draft_card("2026-07-16 — test", evidence, Config())


def _sham(text: str) -> str:
    """Strip every [[fill:]] marker pair, keep the hint text, claim done."""
    stripped = _SLOT_STRIP_RE.sub(r"\1", text)
    return stripped.replace("`drafted`", "`complete`")


# ---------------------------------------------------------------------------
# Mirror pins (lib/ cannot import checks/ — equality is enforced here)
# ---------------------------------------------------------------------------


def test_fill_token_pinned_to_session_log_constant():
    assert RESIDUE_FILL_TOKEN == DRAFT_FILL_TOKEN


def test_code_stripping_regexes_pinned_to_session_log():
    assert _RESIDUE_CODE_SPAN_RE.pattern == _CODE_SPAN_RE.pattern
    assert _RESIDUE_FENCE_RE.pattern == _FENCE_RE.pattern
    assert _RESIDUE_FENCE_RE.flags == _FENCE_RE.flags


def test_every_guarded_hint_appears_in_a_real_draft():
    """Drift pin: each canonical hint renders as an intact slot in a draft
    (the verify-result hint needs a recorded verify command to render)."""
    plain = _draft()
    with_command = _draft(verify_command="python3 -m pytest")
    for name, hint in CARD_GUARDED_HINTS:
        source = with_command if hint == CARD_HINT_VERIFY_RESULT else plain
        assert f"[[fill: {hint}]]" in source, name


# ---------------------------------------------------------------------------
# The generic core
# ---------------------------------------------------------------------------


def test_shingles_empty_body_matches_nothing():
    assert residue_shingles("") == set()
    assert residue_shingles("   \n\t ") == set()


def test_shingles_short_body_is_one_whole_shingle():
    assert residue_shingles("two words") == {"two words"}


def test_shingles_long_body_windows_and_normalizes():
    body = "one two three four five six seven eight nine"
    shingles = residue_shingles(body)
    assert len(shingles) == 2  # 9 words, window RESIDUE_SHINGLE_WORDS = 8
    rewrapped = "one two\n  three   four\tfive six\nseven eight nine"
    assert residue_shingles(rewrapped) == shingles
    assert RESIDUE_SHINGLE_WORDS == 8


def test_probe_residue_detects_stripped_body_and_names_it():
    guarded = [("alpha", "resolve this with a live probe result")]
    text = "# note\n\nresolve this with a live probe result\n"
    assert probe_residue(text, guarded) == ["alpha"]


def test_probe_residue_skips_intact_slot_both_spacings():
    guarded = [("alpha", "resolve this with a live probe result")]
    for slot in (
        "[[fill:resolve this with a live probe result]]",
        "[[fill: resolve this with a live probe result]]",
    ):
        assert probe_residue(f"# note\n\n{slot}\n", guarded) == []


def test_probe_residue_silent_on_wholesale_replacement():
    guarded = [("alpha", "resolve this with a live probe result")]
    text = "# note\n\nprobed live at 12:00Z: trigger disabled, zero claims.\n"
    assert probe_residue(text, guarded) == []


def test_probe_residue_detects_rewrapped_residue():
    guarded = [("alpha", "resolve this with a live probe result and more words")]
    text = "# note\n\nresolve this with a live\nprobe result and more words\n"
    assert probe_residue(text, guarded) == ["alpha"]


# ---------------------------------------------------------------------------
# The session-card surface
# ---------------------------------------------------------------------------


def test_card_sham_resolution_fires_and_names_slots():
    guilty = probe_card_residue(_sham(_draft(verify_command="python3 -m pytest")))
    assert "session idea" in guilty
    assert "previous-session review" in guilty
    assert "model line" in guilty
    assert "verify result" in guilty


def test_card_intact_draft_is_not_residue():
    """An unedited draft is *unresolved* (the fill count's report), never residue."""
    assert probe_card_residue(_draft()) == []
    assert probe_card_residue(_draft(verify_command="python3 -m pytest")) == []


def test_card_genuine_close_out_is_silent():
    text = (
        "# Session 2026-07-16 — test\n\n> **Status:** `complete`\n\n"
        "- **📊 Model:** fable-5 · medium · feature build\n"
        "- verify: ran python3 -m pytest, 1679 passed.\n"
        "- Decisions made: advisory-first over gate-red.\n"
        "- Next session should know: graduate the advisory once proven.\n\n"
        "## 💡 Session idea\n\nA real idea with real words.\n\n"
        "## ⟲ Previous-session review\n\nA real remark and a real improvement.\n"
    )
    assert probe_card_residue(text) == []


def test_card_hints_quoted_in_code_are_not_residue():
    """Cards that DISCUSS the draft mechanism quote hints in backticks/fences."""
    _, idea_hint = next(p for p in CARD_GUARDED_HINTS if p[0] == "session idea")
    backticked = (
        "# Session\n\n> **Status:** `complete`\n\n"
        f"The draft writes `{idea_hint}` as its idea hint.\n"
    )
    fenced = (
        "# Session\n\n> **Status:** `complete`\n\n"
        f"```\n{idea_hint}\n```\n"
    )
    assert probe_card_residue(backticked) == []
    assert probe_card_residue(fenced) == []
    assert strip_code_regions(backticked).count(idea_hint) == 0
