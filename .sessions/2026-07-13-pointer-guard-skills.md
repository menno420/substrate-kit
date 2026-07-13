# 2026-07-13 — skill-body pointer guard (groom-forward of #334's 💡 idea)

> **Status:** `in-progress`

About to: extend the template-pointer guard (#334) to the pointer surfaces it
skipped — the kit-shipped skill bodies (`src/engine/skills/skills.py`), where
dot-led path pointers and markdown-link pointers are today unjudged by
`check_skill_grounds`, plus an existence pin on its `_KIT_SHIPPED_PATHS`
whitelist (the rot class). Staged CLAUDE.md verified already covered by #334.
