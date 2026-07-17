# Claude Design Prompt — CV "Chromatic Chapters" Visual Exploration

Copy everything below the line into Claude Design, and attach the file `index.html` (or `direction-c-chromatic.html`) as the starting point.

---

## PROMPT

I'm exploring visual directions for my interactive CV website. The attached HTML is the current design — concept name: **"Chromatic Chapters"**. I want you to generate visual variations while keeping the concept and structure completely intact.

### What this site is
An interactive CV for Tomer Sahar (product leader / AI strategy consultant, Tel Aviv). The core concept: **"Don't read it — interview it."** Each career chapter is a color-blocked card with a summary, an expandable "+More" section (Role & Scope / Highlights / The Story), and question chips that open an AI agent in a bottom sheet. The agent answers from verified CV facts.

### HARD CONSTRAINTS — do not change
1. **Layout & structure:** hero → 4 chapter cards → "Under the Hood" section → footer. Keep the card anatomy: title, years badge, role line, summary, +More expander, question chips.
2. **Interactions:** expandable +More, question chips, floating "Ask me" button, bottom-sheet chat (mobile) / side drawer (desktop). Do not remove or redesign the interaction model.
3. **Concept encoding:** each of the 4 chapters must own a distinct color world. The color IS the information architecture — 4 chapters, 4 hues. Never collapse them into one palette-wide accent.
4. **Mobile parity:** every variation must work identically at 390px width and at desktop width. No desktop-only effects.
5. **Typography roles:** keep 3 roles — a characterful display face, a readable body face, a mono face for labels/badges. You may swap the specific typefaces.
6. **No 3D, no WebGL, no particle effects.** Boldness comes from color and type, not from heavy tech.
7. **Content:** do not rewrite any copy. Text stays exactly as-is.

### WHAT TO VARY — generate 5 distinct variations
For each variation, change only: the full color system (background, 4 chapter hues, accent, agent-sheet palette), gradient treatment (or flat), the display/body/mono typeface pairing, corner radius + shadow language, and the hero type treatment.

Current tokens for reference:
- Background: deep plum `#1C0F2E` / `#120A1F`
- Chapter hues: tangerine `#FF7A1A`, pink `#FF3E8A`, cyan `#35DDE8`, lime `#C8F53B`
- Agent accent: violet `#8A5CFF`; sheet on warm paper `#FFF9F0`
- Type: Syne (display) / Manrope (body) / JetBrains Mono (labels)

Variation briefs to explore (feel free to propose better ones):
1. **Sunset Editorial** — warm dusk background, chapter hues from a sunset ramp (amber → coral → magenta → violet), softer gradients, higher elegance.
2. **Electric Daylight** — light/near-white background with hyper-saturated chapter blocks, hard contrast, energetic.
3. **Deep Ocean** — dark blue-black base, chapter hues in aquatic jewel tones (teal, ultramarine, coral, gold).
4. **Print Riso** — flat inks, no gradients, slightly off-registration feel, riso-print palette (fluorescent pink, blue, sunflower, green).
5. **Your wildcard** — one direction I haven't thought of, justified in one sentence.

### OUTPUT FORMAT
For each variation: (a) the modified HTML/CSS I can preview, (b) a token table (name → hex) so I can port the palette back into my codebase's `:root` block, (c) one sentence on who this direction speaks to (recruiter / CEO / tech lead).

My taste calibration: I like bold and colorful, with an aesthetic spine — not neon-on-black clichés, not corporate beige. Swiss discipline underneath, loud surface on top.
