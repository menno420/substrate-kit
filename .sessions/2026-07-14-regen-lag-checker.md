# 2026-07-14 — Staged-artifact regen-lag checker (ORDER 019 item 6)

> **Status:** `in-progress`

About to: build the staged-artifact regen-lag checker per
`docs/ideas/staged-artifact-regen-lag-checker-2026-07-12.md` — a `check`
finding that fires when `state.json` `slot_values` are filled but staged
`.substrate/` artifacts still carry live `${...}` placeholders (the
"looks staged, isn't rendered" class proven live on websites @ `992c045`),
reusing `find_placeholders_outside_code`, with unit + mutation-fixture
tests and a byte-stable dist regen.

📊 Model: Claude 5 family (Fable) · standard · engine-checker build

(Enders — 💡 session idea and ⟲ previous-session review — land at close-out.)
