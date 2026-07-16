# Session · 2026-07-16 · status-badge-value-parse

> **Status:** `in-progress`

Intent: bugs-first fix of the status-badge substring bug (the #420 card's 💡 idea): `status_in_progress` substring-matches hold tokens anywhere on the badge LINE, so prose like "*(auto-drafted by substrate-kit …)*" false-holds a card whose Status VALUE is `complete` ("auto-drafted" contains "drafted") — a latent false-hold class on the MERGE-BLOCKING session gate. Fix at root by parsing the badge VALUE (the `_STATUS_VALUE_RE` mechanism `_status_value_drafted` already uses) and judging tokens against the value only; regression test pinning the auto-drafted false-hold case; old-vs-new sweep over every existing `.sessions/*.md` card; dist regen.
