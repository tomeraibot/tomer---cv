# PRD — Interactive CV "Chromatic Chapters"

**Owner:** Tomer Sahar · **Status:** v1 approved · **Last updated:** 2026-07-15

## 1. Problem

A traditional CV is a static claim sheet. For a product leader whose thesis is
*governed, grounded AI agents*, a PDF is off-brand: it tells instead of shows.
Recruiters spend 30–60 seconds; senior stakeholders want depth on demand.
One artifact must serve both.

## 2. Concept

**"Don't read it. Interview it."** A scrollable CV where every career chapter
carries three layers: a summary (30-second read), an expandable deep-dive
(Role & Scope / Highlights / The Story), and contextual questions answered by
an AI agent grounded in verified facts. The agent runs on the same self-hosted
platform Tomer builds professionally — the site is proof of the thesis.

## 3. Audiences & jobs-to-be-done

| Audience | JTBD | Served by |
|---|---|---|
| Recruiter (30–60s) | Scan fit fast | Hero + chapter summaries |
| Hiring manager / CEO | Judge depth & thinking | +More blocks, agent Q&A |
| Tech lead / CTO | Verify he actually builds | ⚙ Under the Hood section |
| Consulting prospect | Understand the offering | Product Experts chapter + agent |

## 4. Scope — v1

**In:** 4 career chapters with 3-layer content · contextual question chips ·
persistent-history agent (demo mode) · Under the Hood technical explainer with
signature CTA button · 3 swappable palettes · full mobile/desktop parity ·
config-driven content and tokens (single edit surface each).

**Out (v1):** live LLM backend wiring (stub delivered, deploy is v1.1) ·
Qdrant retrieval (v1.2) · analytics · multilingual page copy (agent is
bilingual; page copy is English) · CMS.

### v1.1 (shipped) — visual lock + desktop composition

Trigger: Claude Design exploration selected the **Ocean** palette; field
feedback: mobile experience strong, desktop was a stretched single column.

- Ocean set as default palette; `riso-offset` card effect ported as a
  configurable token (`cardEffect`).
- Desktop (≥1024px) gets its own composition — sticky identity rail with
  scrollspy chapter navigation, wider content column, side-by-side depth
  blocks, right-drawer agent. Mobile untouched.
- Decision of record: adaptive composition in one file **instead of** a
  separate desktop site (see ARCHITECTURE.md, decision A6).

## 5. Design decisions of record

1. **No 3D/WebGL.** Rejected (Gemini-era concept): heavy, fails mobile parity,
   off-tone for the audience. Boldness comes from color + type.
2. **Color encodes structure.** 4 chapters = 4 hues. Palette is information
   architecture, not decoration.
3. **Agent is woven, not bolted on.** Questions live inside chapters and open
   the agent pre-contextualized; the drawer keeps history across the visit.
4. **Progressive depth.** Summary → +More → agent. Nothing forces the
   30-second reader to work.
5. **Demo-first agent.** Site ships static-safe; live mode is a config flip
   once the proxy is deployed. No API keys client-side, ever.

## 6. Success criteria

- Visitor can reach any chapter's full depth in ≤ 2 taps.
- Page interactive < 1.5s on mid-range mobile (single file, one font request).
- Agent answers stay within verified facts (spot-check 20 questions pre-launch).
- At least one interviewer mentions the site unprompted. (The real KPI.)

## 7. Risks

| Risk | Mitigation |
|---|---|
| Agent hallucinates beyond CV | Grounded system prompt + hard rules; later Qdrant retrieval |
| Unverified placeholder metrics ship | `[EDIT]` markers + launch checklist in DEPLOYMENT.md |
| Bold palette polarizes | 3 prebuilt palettes; Claude Design prompt for fast exploration |
| Proxy abuse / cost | Rate-limit at nginx; max_tokens capped; CORS locked |
