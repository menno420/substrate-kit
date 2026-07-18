# 2026-07-18 · de-wall the skill layer + stray gen2 doc

> **Status:** `complete`

Run type: worker session (owner-directed cleanup).

- **📊 Model:** opus-4.8 · medium · docs-only

Residual from the dewall arc: prior sessions fixed the templates (#444) and the
rendered docs (#446), but the false "agents must NOT arm auto-merge / never
self-merge; leave it to the owner or a server-side workflow" doctrine still
lived in the kit-shipped SKILL layer (a skill body + a guard test that ENFORCED
the false phrase), so it would re-propagate to every adopter. Ground truth
(verified today): auto mode is OFF; agents merge their own/sibling green PRs
directly (MCP/REST) — a normal action, proven ~19× today. Merging / ready-flip
/ arming auto-merge are normal agent actions. Genuine walls kept: ref/branch
DELETION 403, tag-push/release 403, raw api.github.com blocked, repo
settings/secrets/external accounts = owner, direct-push-to-protected-main.

## What shipped (PR #<pending>)

- `src/engine/skills/skills.py` — `_SESSION_CLOSE_BODY`: the intro "two rails"
  line and step 3 no longer say "NEVER arm auto-merge on, or merge, your own PR
  — refused terminally"; step 3 now reads "Land your own green PR — merging is
  normal agent work … merge it directly (MCP/REST), or let the auto-merge-
  enabler land it … only a `do-not-automerge`-labelled PR waits". The born-red
  designed-hold reading is preserved. `_UPGRADE_DISTRIBUTION_BODY` and
  `_RELEASE_BODY`: "never self-arm/self-merge" → "land it on green (merge
  directly or via the enabler)". session-close skill `description`: "never
  self-merge" → "land on green".
- `tests/test_skills.py` — `test_session_close_is_the_landing_path_playbook`
  no longer asserts the false phrase `"NEVER arm auto-merge"`; it now asserts
  the accurate `"Land your own green PR"` + `"merging is normal agent work"`
  and adds `assert "NEVER arm auto-merge" not in body` so the guard defends
  truth against a regression instead of pinning the lie. The section comment
  updated too.
- `docs/gen2/next-boot.md` — the KNOWN-WALLS bullet "Owner-gated merges are
  refused on relayed consent" replaced with "Merging works agent-side — NOT a
  wall (corrected 2026-07-18)"; the genuinely-true ref/branch-DELETION and
  tag-push 403 walls are explicitly retained.
- `dist/bootstrap.py` — regenerated (`python3 src/build_bootstrap.py`); skills
  are baked into the single-file dist, so the edit must ride there too
  (`test_committed_bootstrap_is_current`).

Note: `docs/SKILLS.md` (task target 3) does not exist in this repo — the
skill-index text is the skill `description` in `skills.py`, which is fixed
above. The materialized `.substrate/skills/session-close/SKILL.md` was already
free of the false doctrine (older simpler body), so no change was needed there.

## How the test assertion was handled

The assertion `assert "NEVER arm auto-merge" in body` ENFORCED the false wall,
so it was replaced (not merely deleted) with positive assertions on the
corrected phrasing plus a negative `not in` guard, keeping the test load-bearing.

## Verify

- `python3 -m pytest` → `1726 passed, 1 skipped`.
- `grep -c "NEVER arm auto-merge\|never self-arm/self-merge" dist/bootstrap.py`
  → `0`.

## 💡 Session idea

Add a `check`-level content guard (the one #446 already proposed) that reds any
kit-shipped skill body or forward-binding doc containing a false-wall phrase
(`NEVER arm auto-merge`, `never self-merge`, `refused on relayed consent`),
scoped to exclude `.sessions/`, `docs/retro/`, `docs/planning/`. This session
is the third hand-fix of the same regression class across templates → rendered
docs → skill layer; enforce-don't-exhort says the fourth propagation should be
caught mechanically at build time, not by a future agent grepping.

## ⟲ Previous-session review

The 2026-07-18 dewall-docs session (PR #446) did the rendered docs cleanly and,
crucially, FLAGGED this exact residual on its decide-and-flag line ("Template
still carries the false wording … `docs/gen2/next-boot.md`'s relayed-consent
merge note is the same class"), which is precisely why this session existed and
found its targets fast — the self-auditing loop working as designed. What it
(and the whole arc) still leaves open is the mechanical guard: three sessions
have now hand-removed the same false doctrine from three layers, and each
flagged the next residual by prose rather than by a check. The system
improvement is to stop relying on the flag-and-next-session chain and land the
build-time content guard so the regression cannot re-enter any kit-shipped
surface — the previous-session review of this arc should be a red CI line, not a
paragraph.
