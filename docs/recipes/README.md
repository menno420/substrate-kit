# Recipes

> **Status:** `reference`
>
> Portable engineering patterns proven in the estate and graduated into kit
> doctrine. A recipe is a **pattern to copy by hand**, not a contract to import —
> apply it when your repo grows the shape it describes. Each recipe names its
> estate proof and its escalation boundary.

## Index

- [Pinned feed contract](pinned-feed-contract.md) — the discipline for a
  committed artifact one repo generates and another consumes over a raw URL: a
  versioned shape contract, producer-side fail-closed CI parity, consumer-side
  render-time verification. Kills the cross-repo feed-desync bug class.

## Recipe frontmatter — `applies-when:`

Every graduated recipe (every file here except this README) carries an
**`applies-when:`** badge in its header blockquote, under the `Status:` badge:

> **applies-when:** `content:raw.githubusercontent.com, path:*.json`

The value is a **cheap structural signature** — a comma-separated list of
tokens, each either `path:<glob>` (a file-path glob) or `content:<marker>`
(a content substring) — describing the *shape a repo grows* when this recipe
applies. It exists so a **future** discovery check can nudge an adopter whose
tree matches the signature toward the relevant recipe: **discovery, not
enforcement**. The nudge itself is deferred until >=2 recipes carry signatures
(a recipe's escalation rule — don't pre-build the check for a single instance).
The `check_recipe_applies_when` advisory keeps every graduation carrying a
well-formed tag in the meantime.
