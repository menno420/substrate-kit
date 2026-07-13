# 2026-07-13 — template pointer guard (dead-pointer class → enforcing test)

> **Status:** `in-progress`

⚑ Self-initiated: converting the verified CI coverage gap behind ORDER 015's
dead-boot-pointer fix into an ENFORCING kit test (Q-0194 friction → guard) —
about to add `tests/test_template_pointer_guard.py` asserting every
template-emitted repo-local path pointer (backtick + markdown-link forms)
resolves to an ADOPT_PLAN destination, an adopt-generated artifact, a
kit-repo self-ref, or an explicitly documented whitelist entry.
