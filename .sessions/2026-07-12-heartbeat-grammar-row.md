# 2026-07-12 — heartbeat-grammar map row: negative `**kit:**` example + adopters.md deference

> **Status:** `in-progress`

- **📊 Model:** fable-5 · seat-worker · heartbeat-grammar graduation-map row

## Scope (what is about to happen)

Closing the LAST open graduation-map row of the grounded-skills program —
the heartbeat-grammar ◐ row
(`docs/reports/2026-07-12-prompt-template-hardening-input.md` map §(b) row
8: "add the negative example (`**kit:**` doesn't parse) and the adopters.md
deference line"; named the one remaining unowned row by the #287 card's
completeness section and the status ⚑ FOR MANAGER follow-on-candidate
line): (1) a NEGATIVE `kit:` line example — the bold-label form
`KIT_LINE_RE` rejects (`src/engine/grammar.py:120` — the optional bold
group cannot contain the `kit:` token; the pokemon-mod-lab live incident,
report §a.4) — homed as a grammar renderer (`kit_line_negative_example`)
and carried verbatim by `control-README.md.tmpl` +
`control-status.md.tmpl` (the writer↔enforcer shared-pin path: the
template and the checker now share the exact string, so it lives in
grammar with test-pinned agreement); (2) the adopters.md deference
doctrine (heartbeat `kit:` self-reports chronically lag 1–3 releases; the
generated `docs/adopters.md` / the committed tree is version truth) in the
same two templates — doctrine prose, no enforcer consumes it, so it stays
template-direct with test pins. Tests in `tests/test_grammar.py`
(negative example pinned REJECTED by `KIT_LINE_RE` + `parse_kit_line`;
bold-label-before-plain-token contrast pin; template↔grammar verbatim
pins; deference pins). CHANGELOG `[Unreleased]` entry; dist rebuild. No
new checker, no new template, no release, nothing outside the row.

Lane claim: `control/claims/claude-heartbeat-grammar-row.md` (deleted at
close, in-lane per the slice-4/5/8 + #287 precedent).
