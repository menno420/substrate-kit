# 2026-07-12 — heartbeat-grammar map row: negative `**kit:**` example + adopters.md deference

> **Status:** `complete`

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

## Close-out

Shipped (PR #289):

- **`src/engine/grammar.py`** — `kit_line_negative_example()` renderer
  (the bold-label form `- **kit:** v1.2.3 · check: green · engaged: yes`)
  plus the leniency-edge note at `KIT_LINE_RE`: the optional bold group
  cannot contain the `kit:` token — the pokemon-mod-lab live incident
  (hardening report §a.4) stated where the regex lives.
- **`control-README.md.tmpl`** § "`status.md` format" — the
  "Exact grammar or invisible" block: the valid
  bold-label-before-plain-token shape stated as the contrast, the taught
  negative example in its own fenced block (verbatim from the grammar
  renderer), and the "Version truth defers to the generated registry"
  paragraph (self-reports lag 1–3 releases; generated `docs/adopters.md`
  + the committed tree are version truth; never hand-assert a spread).
- **`control-status.md.tmpl`** — the seeded notes now teach the
  plain-token rule (negative example verbatim, pointer to the README
  section for the valid bold-label shape) and the deference doctrine.
- **Tests:** suite **1198 → 1203** (+5 in `tests/test_grammar.py`):
  negative example REJECTED by both `KIT_LINE_RE` and `parse_kit_line`;
  the bold-label-before-plain-token contrast shape still parses; both
  templates carry the negative example verbatim (writer↔enforcer shared
  pin, the `CAPABILITY_LOG_TAUGHT_FORMAT` precedent); both templates
  carry the deference doctrine (`docs/adopters.md` + "version truth" +
  "self-report" pins); the rendered status seed still parses to the REAL
  seeded `kit:` line (the taught negative is inert in the seed).
- **CHANGELOG:** `[Unreleased]` entry prepended.
- **Dist:** rebuilt via `python3 src/build_bootstrap.py` — 828,825 B;
  byte-pin suite green.

Verify (verbatim tails): `python3 -m pytest tests/ -q` → `1203 passed in
17.91s` · `python3 -m ruff check src/engine/` → `All checks passed!` ·
`python3 dist/bootstrap.py check --strict` → the designed born-red hold
naming this card ("HOLD (by design) … nothing to investigate"), nothing
else — cleared by this flip commit.

**Decide-and-flag calls (map row silent on the detail):**

1. ⚑ PL-008 constant-sharing path TAKEN for the negative example: the
   templates and the enforcer (`KIT_LINE_RE`) now share the exact string,
   so it is grammar-homed (`kit_line_negative_example()`) with test-pinned
   agreement — the shared-pin precedent, not a duplicated literal. The
   deference doctrine stays TEMPLATE-DIRECT: no checker consumes that
   prose, so per the slice-2/3/4/5/8 rule it gets direct test pins, no
   grammar constant.
2. ⚑ Suite-count correction: the mission brief and #287-era records say
   1195; ground truth on main HEAD a025d6d is **1198** (verified by a
   clean stash run this session). CHANGELOG records 1198 → 1203.
3. ⚑ The status-seed notes carry only the NEGATIVE example inline (the
   valid bold-label shape is routed to the README section) — a
   line-wrapped positive example beginning a line in a heartbeat file
   would itself match `KIT_LINE_RE`; the negative is inert by
   construction (pinned by the seed no-shadow test).
4. ⚑ The kit's own live `control/README.md` / `control/status.md` are NOT
   retro-edited — consumer #0 picks template changes up at its own
   upgrade, the same no-adopter-retro-edits rule every wave follows
   (precedent: the slice-4 owner-assist section is likewise not in the
   live README).

**Graduation-map absorption after this PR:** map §(b) rows — capabilities
discovery ✅ (pre-existing) · owner-action fields ✅ (pre-existing) ·
propose-don't-apply ✅ (pre-existing) · friction→guard ✅ (pre-existing) ·
unattended question routing ✅ (pre-existing) · Evidence block ✅ (#287) ·
landing path ✅ (slice 2, absorbed via the `session-close` playbook per its
"new template OR playbook skill" home) · routines doctrine ✅ (#287) ·
**heartbeat grammar ✅ (THIS PR — the last open row)** · claims ✅
(pre-existing) · preflight reset ✅ (#287). The map is now fully absorbed
kit-side; out-of-lane remainders unchanged (slice 7 in websites #177,
fm-side slice-6 wiring on the fm lane).

## Session enders

💡 **Session idea:** `check` could carry an advisory `heartbeat-grammar`
finding that fires when a heartbeat file contains a bold-bolded
`**kit:**` token on a line where no plain `kit:` line parses — the
negative example is now taught in two templates, but an adopter who
already wrote the broken shape (pokemon-mod-lab item e) gets no in-repo
signal; the grammar module already owns both halves, so the checker is
one regex + one advisory line (enforce-don't-exhort). Dedup-checked
`docs/ideas/`: the #232-card grammar follow-up idea covers *parsing* the
bold form leniently; this is the complementary *warn-the-writer* lane.

⟲ **Previous-session review:** #287 (the §7 tail) did the completeness
accounting exactly right — its card named the heartbeat-grammar row as
the one unowned remainder and mirrored it onto the status ⚑ FOR MANAGER
line, which is the only reason this session's scope was derivable in
minutes. What it could have done better: it left the row's ownership as
"follow-on candidate" prose rather than filing a claim or queue item —
one more line (a `control/claims/` stub or a `next:` queue row) would
have made the handoff mechanical instead of narrative. The system
improvement this surfaces: when a session's completeness audit names an
unowned remainder, it should also name the handoff artifact (queue row /
claim / order), not just the fact.

**Documentation audit:** CHANGELOG entry present; the taught text is
self-indexing (it lives in the planted control docs adopters already
read); the writer↔enforcer pins live in `tests/test_grammar.py`; the
decide-and-flag list above is the complete set of unrecorded judgment
calls; claim file deleted this commit; status heartbeat overwritten
surgically (phase/health/last-shipped/⚑-row-resolution/notes only).
Capability delta: none — branch push, MCP PR open, checkers, and the
designed-hold gate all behaved as already recorded for this venue.
