# 2026-07-11 — host workflow action-pin bump (checkout@v5 / setup-python@v6)

> **Status:** `in-progress`

- **📊 Model:** fable-5 · low · mechanical refactor

## Scope (what is about to happen)

One bounded slice, claim `control/claims/host-workflow-pin-bump.md`
(#198 @ 6d34913, on main before build). Bump the kit's OWN host workflows
off the Node-20-deprecated action majors — the "Kit's OWN workflow
action-pin bump" next-queue item from the ORDER 013 self-review (W-10b):
`.github/workflows/ci.yml` (checkout@v4 L21, setup-python@v5 L96) and
`.github/workflows/release.yml` (L39/L40) go to `actions/checkout@v5` /
`actions/setup-python@v6`, matching what the generated gate emits since
PR #195 (`src/engine/adopt.py` pins, verified). Inventory says these are
the ONLY action pins in `.github/workflows/` — `auto-merge-enabler.yml` and
`auto-merge-disarm.yml` carry no `uses:` at all — so no other majors to
sweep. `release.yml` cannot be exercised without cutting a release (never
dispatched for a pin bump): validated by careful YAML review and marked
**verified-at-next-release**. `ci.yml` exercises itself on this PR.
Rider on the final flip commit ONLY (sibling-card rule): rewrite the 4
off-PL-004 `📊 Model:` lines flagged by self-review W-10a (the 4 of the 5
newest complete cards) to the family-level `<model> · <effort> ·
<task-class>` taxonomy form. No CHANGELOG entry (host-workflow pins are
kit-internal, not adopter-visible; no engine/dist change). Close-out:
status.md overwrite (preserving ALL standing content — orders through 013,
⚑ OWNER-ACTION 2–13, ROUTINE STATE/Q-0265, Self-review 2026-07-11,
release/wave/P4 records) + claim delete as the deliberate last step before
this card's flip. Files: `.github/workflows/ci.yml` +
`.github/workflows/release.yml` + the 4 model-line card fixes (flip commit
only) + `control/status.md` + claim delete + this card. NEVER
control/inbox.md, bench/, src/, dist/, or PR #181.

## Close-out

(pending — written at flip)
