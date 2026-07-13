# 2026-07-13 — skill-body pointer guard (groom-forward of #334's 💡 idea)

> **Status:** `complete`

About to: extend the template-pointer guard (#334) to the pointer surfaces it
skipped — the kit-shipped skill bodies (`src/engine/skills/skills.py`), where
dot-led path pointers and markdown-link pointers are today unjudged by
`check_skill_grounds`, plus an existence pin on its `_KIT_SHIPPED_PATHS`
whitelist (the rot class). Staged CLAUDE.md verified already covered by #334.

Did: STEP-1 inventory first, code second. Findings at HEAD 7c736fa:
(1) staged CLAUDE.md — ALREADY covered by #334 (`load_templates()` globs
every `*.tmpl` incl. `CLAUDE.md.tmpl`; the guard iterates it) — honest
null, no duplicate check; (2) skill bodies — mostly covered by
`check_skill_grounds` + its enforcing kit-root/empty-target zero-findings
tests, EXCEPT three verified blind spots: dot-led paths never judged
(`_FIRST_TOKEN_RE`; live instance `.substrate/upgrade-report.md`),
markdown links never extracted (`_SPAN_RE`; zero live, future class), and
`_KIT_SHIPPED_PATHS` whitelist rot (no existence pin anywhere — a kit
rename would resolve dead pointers forever); (3) seat-digest/HANDOFF
emissions compute paths from live config/files — self-grounded, null.

Shipped `tests/test_skill_pointer_guard.py` (5 tests, a2107a0): #334's
extractor imported from `tests/test_template_pointer_guard.py` (one source
of truth) over every SKILLS body (18 distinct pointers), resolution via
ADOPT_PLAN dests / kit-generated artifacts / existence-asserted kit-self
refs / release-wave transients / an empty commented whitelist, loud
fix-path failures, vacuity floor pinning the dot-led class, stale-entry
hygiene, and the `_KIT_SHIPPED_PATHS` rot pin. Mutation-tested all three
classes (dot-led + md-link injections, runbook-file removal) — each reds
loud; reverted. Zero src/engine changes → no dist regen. guard-fires.jsonl
delta committed with the work (a2107a0).

Verify: pytest 1269 → 1274 passed; `python3 dist/bootstrap.py check
--strict` red only on this card's own designed born-red hold pre-flip.

⚑ Self-initiated: groom-forward of the 💡 idea on #334's session card
(pointer guard → skill surface), per the standing grooming ender + the
night-run ORDER 016 self-initiative program.

💡 Session idea: graduate the dot-led-path class into `check_skill_grounds`
itself (widen `_FIRST_TOKEN_RE` to accept a leading `.` plus a deliberate
state-dir classification) so ADOPTER-side rendered and host-added SKILL.md
files inherit the coverage too — this session's guard covers only the
kit-truth SKILLS list; a host-edited skill with a dead dot-led pointer
still fails open in the advisory scan (dedup-checked `docs/ideas/`: no
entry covers skill-ground extraction classes).

⟲ Previous-session review: #334's guard design proved genuinely reusable —
its extractor imported here unchanged, exactly as its card predicted. One
miss: the card's 💡 idea named "the staged CLAUDE.md" as a skipped surface
when the guard it had just shipped already covered `CLAUDE.md.tmpl` via
`load_templates()`; a one-line glob check before writing the idea would
have kept the groomed scope accurate. Improvement: when recording a
groom-forward idea, cite the evidence that the named surface is actually
uncovered — this session spent its inventory step re-deriving that.

📊 Model: Claude 5 family
