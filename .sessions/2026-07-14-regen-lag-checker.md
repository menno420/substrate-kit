# 2026-07-14 — Staged-artifact regen-lag checker (ORDER 019 item 6)

> **Status:** `complete`

Intent: build the staged-artifact regen-lag checker per
`docs/ideas/staged-artifact-regen-lag-checker-2026-07-12.md` — a `check`
finding that fires when `state.json` `slot_values` are filled but staged
`.substrate/` artifacts still carry live `${...}` placeholders (the
"looks staged, isn't rendered" class proven live on websites @ `992c045`),
reusing `find_placeholders_outside_code`, with unit + mutation-fixture
tests and a byte-stable dist regen.

📊 Model: Claude 5 family (Fable) · standard · engine-checker build

## Did (PR #345)

- `src/engine/checks/check_staged_regen.py` — new advisory checker: scans
  the staged subtrees adopt writes (`agents/`, `claude/`, `ci/`, `hooks/`,
  `skills/` under `<state_dir>/`; never `backup/` or state-root files) and
  fires one `staged-regen-lag` finding per artifact whose live placeholders
  **outside code spans** (`find_placeholders_outside_code`, per the idea
  file) intersect the **filled** slot set from `state.json` — the
  intersection is both the lag definition and the false-positive firewall
  (shell `${VAR}` / GitHub `${{ }}` can never fire). Message names the
  regen commands (`upgrade`, `skills --build` / `agents --build`).
- Wired into `cmd_check`'s full lane as a never-exit-affecting advisory
  (same emit + guard-fire telemetry contract as the sibling advisories);
  registered in `src/build_bootstrap.py` MODULE_ORDER; dist rebuilt,
  byte-stable across two runs (sha256
  `7279347c68632e43892c158b1b91cc4290d44f3b43681013c0ca71a5874ececd`).
- `tests/test_check_staged_regen.py` — 12 tests: the idea file's fixture
  pair (filled `${project_name}` in a staged artifact fires; same slot in
  a code span / fenced block doesn't), the filled-intersection firewall,
  scan-surface boundaries (backup/, state-root, unreadable fail-open),
  the adopt→answer→lag→regen mutation arc, and cmd_check advisory /
  status-only-lane integration. Suite 1294 → 1306.
- Mutation test re-proved LIVE on the built dist in a scratch adopter:
  adopt → `answer architecture_layers …` → check fires 3 verbatim
  `staged-regen-lag` advisories → `bootstrap.py upgrade` → 0 findings.
- Adopter safety (read-only survey): superbot-next / websites /
  superbot-mineverse all scan **0 findings** (13 filled slots each, staged
  trees current), and the advisory posture is never exit-affecting anyway
  — the checker cannot red a currently-green adopter. Trees untouched
  (git status clean ×3).

## Decide-and-flag

- **Posture: advisory-first** — the idea file names it ("advisory-first
  per the adopt-freely posture"); a strict red would also bomb any adopter
  whose staged tree predates its answers the moment it upgrades.
- **Kit's own staged tree fires 3 TRUE advisories at HEAD**
  (`.substrate/agents/architect.md`, `reviewer.md`, `claude/CLAUDE.md` lag
  `architecture_layers` / `ownership_model` / `mutation_seam` /
  `owner_profile`) — left in place deliberately: the full remedy is
  `upgrade`, which also rewrites the live enabler workflow + config
  (cross-cutting, out of item-6 scope, and workflow edits reroute the PR
  through the locked-door lane). The pending release-wave upgrade (heartbeat
  Next-2 item 1) cleans it; meanwhile the firing advisories are live PL-008
  verification data. Guard-fire telemetry deltas committed per contract.
- **Idea-file frontmatter left `captured/open`** — the index checker's
  outcome rules require ship fields null until a merge exists; the body
  State line now points at PR #345 and the review-merge session flips the
  frontmatter.
- **parked green — owner disarm respected, landing path: owner-click.**
  The enabler armed auto-merge on #345 at open; it was disarmed before the
  card flip per the review-merge order for this lane, and — because the
  live enabler re-arms on every `synchronize` push (its own header says so)
  — the PR carries the kit-convention park, the `do-not-automerge` label
  (the enabler's designed carve-out, fresh-re-read each run; precedent:
  the #317 owner-ratification park), applied BEFORE the flip push so no
  later push can re-arm. Verified on a fresh PR fetch:
  `"labels":["do-not-automerge"]`. Never re-armed, never merged from this
  session; the review-merge session removes the label when it lands the PR.

## 💡 Session idea

Staged `claude/CLAUDE.md` has no single-pack regen verb: skills and agents
have `--build`, but the staged working agreement re-renders only inside a
full `upgrade` (which also rewrites live workflows/config — exactly why the
kit's own 3-artifact lag stays parked this session). A `bootstrap.py claude
--build` (or `render --staged`) pack verb would make the regen-lag
advisory's remedy targeted for every staged artifact class and let a repo
clear lag without a whole upgrade. Dedup: no `docs/ideas/` hit for a staged
CLAUDE.md pack verb (grep `render --staged` / `claude --build` = 0).

## ⟲ Previous-session review

Reviewed `.sessions/2026-07-13-session-gate-false-green.md` (PR #342,
ORDER 019 item 1). Genuinely strong: the fail-closed grading choice
(any-red-cards-red, diff-derived selection) closed a reproduced false-green
with regression pins both directions, and the card's honest rail note
(briefly self-armed auto-merge via MCP, disarmed ~2 min later) is exactly
the self-reporting the fleet needs. Concrete workflow improvement it
surfaces: that slip and this session's disarm dance are the same class —
the enabler auto-arms every `claude/*` PR even when the lane's orders say
park-for-review, so every such session must remember a manual disarm.
Worth an enabler-side convention (e.g. the enabler skipping PRs whose
branch/claim declares a review-merge lane), so parking is structural, not
per-session vigilance.
