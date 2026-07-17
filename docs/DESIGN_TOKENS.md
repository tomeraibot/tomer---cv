# DESIGN TOKENS — editing all visuals

All visual decisions live in the `<style>` block of `index.html`, in the
section marked `DESIGN TOKENS — EDIT VISUALS HERE`. No color or font is
defined anywhere else.

## Switching palettes

Three prebuilt palettes ship: `ocean` (default, selected via Claude Design
exploration), `chromatic`, `sunset`. Switch by editing one line in `SITE_CONFIG`:

```js
palette: "sunset"
```

## Card effect

A second visual knob, ported from the Claude Design "Ocean" export:

```js
cardEffect: "riso-offset"   // riso-offset | hard-edge | none
```

- `riso-offset` — dual offset shadow in `--accent` / `--accent-2`, a subtle
  misregistered-print feel. Inherits any palette automatically.
- `hard-edge` — solid `6px 6px 0 var(--ink)` neo-brutalist shadow.
- `none` — flat cards.

## Anatomy of a palette

```css
[data-palette="chromatic"]{
  --bg / --bg-2        /* page background, panels (Under the Hood) */
  --ink                /* dark text on colored cards & sheet */
  --paper              /* agent sheet background */
  --text / --text-dim  /* light text on dark background */
  --hairline           /* borders on dark background */
  --c1a --c1b          /* chapter 1 gradient (a = light stop, b = dark stop) */
  --c2a --c2b          /* chapter 2 */
  --c3a --c3b          /* chapter 3 */
  --c4a --c4b          /* chapter 4 */
  --accent --accent-2  /* agent identity: FAB gradient, labels, send button */
  --signal             /* the "alive" color: pulse dot, focus rings, hood headings */
}
```

## Creating a new palette

1. Copy any `[data-palette="..."]` block, rename it.
2. Set `SITE_CONFIG.palette` to the new name.
3. Contrast rules to keep:
   - `--ink` on every `--cNa/--cNb` gradient: aim WCAG AA (4.5:1) for the
     summary text.
   - `--text-dim` on `--bg`: keep readable, it carries the lede and Under
     the Hood body.
   - The four chapter hues must be distinguishable from each other at a
     glance — that's the concept.

## Porting palettes from Claude Design

The exploration prompt (`claude-design-prompt.md`) asks Claude Design to
return a token table per variation. Paste those hexes into a new palette
block — nothing else needs to change.

## Beyond color

- **Type:** the three roles are `--display`, `--body`, `--mono` in `:root`.
  Swap the Google Fonts `<link>` and these three lines together.
- **Shape language:** `--radius-card`, `--radius-pill`.
- **Flat instead of gradients:** set each `--cNa` equal to its `--cNb`.
- **Signature animation:** the Under the Hood button's spinning conic border
  uses the four chapter hues automatically — it inherits any palette.
