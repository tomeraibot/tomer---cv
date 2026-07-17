# ARCHITECTURE — Interactive CV

## System overview

```
Browser ──► index.html (static, no secrets)
              │  SITE_CONFIG.agent.mode
              │
    ┌─────────┴──────────┐
    ▼ demo               ▼ live
 canned answers    POST /api/interview
 (in CONTENT)            │
                         ▼
                  interview_proxy (FastAPI, Docker)
                   · API key from env only
                   · grounded system prompt
                   · CORS: cv domain only
                         │
                         ▼
                  Claude API  ◄── verified facts
                                   (file now → Qdrant cv:profile later)
```

## Frontend

Single-file architecture, deliberately:
- **`:root` + `[data-palette]` blocks** — every visual decision is a token.
- **`SITE_CONFIG`** — agent mode/endpoint/copy, active palette.
- **`CONTENT`** — 100% of page text. The DOM is rendered from this object;
  there is no content in markup.
- Behavior: chapter expanders, contextual chips → agent with chapter context,
  persistent in-session `history[]` sent to the backend (last 10 turns),
  bottom-sheet (mobile) / right-drawer (desktop) from one component via
  media queries — true parity, not two builds.
- A11y baseline: focus-visible styles, aria-expanded on expanders,
  dialog semantics on the sheet, `prefers-reduced-motion` respected.

## Agent modes

| Mode | Behavior | Use |
|---|---|---|
| `demo` | Chip questions return curated answers from `CONTENT`; free text returns an honest demo notice | Static hosting, previews, zero backend |
| `live` | All questions POST to the proxy with `{question, context, history}` | Production |

Failure handling in live mode: network/5xx → graceful in-chat fallback message;
the static CV remains fully usable.

## Backend (api/interview_proxy.py)

- FastAPI, one POST endpoint + health check.
- System prompt = hard rules + verified facts file. Rules: ground every claim,
  never invent, ≤120 words, bilingual (answers in visitor's language),
  decline off-topic.
- **v1.2 upgrade path:** swap file-stuffing for Qdrant retrieval against the
  existing `cv:profile` collection (Ollama embeddings) — top-k facts per
  question instead of full context. Interface to the frontend is unchanged.

## Security model

1. No secrets in the repo or the browser. `ANTHROPIC_API_KEY` via env,
   `.env` with `chmod 600`, same convention as the rest of the stack.
2. CORS locked to the production origin.
3. nginx rate-limiting on `/api/interview` (see DEPLOYMENT.md).
4. `max_tokens: 512` caps worst-case cost per request.
5. Prompt-injection posture: the system prompt scopes the agent to CV topics
   and forbids invention; the agent has **no tools** — worst case is a wrong
   sentence, not an action.

## Decision log

| # | Decision | Why |
|---|---|---|
| A1 | Single HTML file | One deploy artifact; trivially portable; matches existing cv repo pattern |
| A2 | Render-from-config | Separates edit surface from structure; enables future CMS/JSON source without refactor |
| A3 | Demo mode default | Site can ship before backend; safe for any static host |
| A4 | Proxy over direct API | Never expose keys client-side (lesson from v1 chat drawer) |
| A5 | History capped at 10 turns | Bounded context cost; enough for a visit-length conversation |
| A6 | Adaptive desktop composition in the same file — **not** a separate desktop site | Considered routing desktop traffic to a second site; rejected: two deploy artifacts, UA-sniff routing is brittle (tablets, resized windows), split SEO/link equity, double content maintenance. Instead, ≥1024px activates a different composition: sticky identity rail (name, lede, scrollspy chapter nav with hue swatches, contact, agent status), wider content column, depth blocks in a side-by-side grid, agent as right drawer. Mobile markup/behavior untouched. If a truly divergent desktop experience is ever needed, the config-driven content makes a split cheap later. |
| A7 | Visual tokens adopted from Claude Design exploration | Ocean palette selected; `riso-offset` dual-accent card shadow ported as a configurable `cardEffect` (`riso-offset` / `hard-edge` / `none`) |

## Responsive composition model (v1.1)

One codebase, two compositions sharing one CONTENT source:

| Surface | <1024px (mobile/tablet) | ≥1024px (desktop) |
|---|---|---|
| Identity | Hero block at top | Sticky left rail: title, lede, chapter nav (scrollspy), contact links, agent status |
| Chapters | Single column | Wider column; `.more-inner` depth blocks in `auto-fit` grid (side by side) |
| Agent | Bottom sheet | Right drawer (440px) |
| Footer | Full contact footer | Footer retained; rail duplicates key links |

Scrollspy: IntersectionObserver with `-30%/-55%` rootMargin highlights the
active chapter swatch in the rail.
