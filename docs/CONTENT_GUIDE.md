# CONTENT GUIDE — editing all CV text

Every word on the page lives in the `CONTENT` object in `index.html`
(section marked `CONTENT — EDIT ALL CV TEXT HERE`). Nothing is hardcoded
in markup. This doc is the map.

## Hero

```js
hero: {
  eyebrow: "Tomer Sahar / Curriculum Vitae",
  title: 'One career.<br><span class="w1">Four</span> ...',  // w1/w2/w3 = chapter colors
  lede: "Each chapter has its own color..."
}
```

## Chapters — the core structure

Each chapter object:

```js
{
  id: "sciplay",          // unique, used for agent context — don't duplicate
  hue: 3,                 // 1–4 → maps to --c1..--c4 palette slots
  title: "SciPlay",
  years: "2018—22",
  role: "Product Leadership · Live-Ops Gaming",
  summary: "...",         // the 30-second layer. Target: ≤ 2 sentences
  more: {
    scope: "...",         // what the job actually was
    highlights: [ ... ],  // achievement bullets. Metrics > adjectives
    story: "..."          // optional: the narrative thread to today. Omit to hide block
  },
  questions: [            // the agent layer
    { q: "Chip label — phrase it as a real recruiter question",
      a: "Curated answer (used verbatim in demo mode; in live mode this is
          reference material — the model answers from verified facts)" }
  ]
}
```

**Adding a chapter:** copy a block, set a new `id`, assign a `hue`. More than
4 chapters? Hues repeat (1–4 cycle) or add `--c5a/--c5b` tokens + a
`.chapter[data-hue="5"]` rule.

**Reordering:** array order = page order. That's it.

## Writing rules (house style)

1. **Verified facts only.** Anything you can't defend in an interview doesn't
   ship. Placeholders are marked `[EDIT: ...]` — grep for `[EDIT` before launch.
2. **Summaries are for the 30-second reader.** No jargon walls.
3. **Highlights carry numbers** where they exist; where they don't, carry
   concrete nouns (what was built), not adjectives.
4. **Story blocks connect past → present thesis.** Each ends by touching the
   AI/agents throughline. This is the differentiator — protect it.
5. **Questions sound like humans.** "Hardest challenge?" not "Elaborate on
   key learnings."
6. Page copy is English. The live agent answers in the visitor's language.

## Under the Hood & footer

Same pattern: `CONTENT.underHood.sections[]` supports `p` (paragraph),
`list` (bullets), `diagram` (preformatted, `<b>` allowed), `tags` (pills).
`CONTENT.footer.links[]` — replace the two `[EDIT]` hrefs before launch.

## Agent copy

Greeting and demo-mode fallback live in `SITE_CONFIG.agent`
(`greeting`, `demoFreeTextReply`).
