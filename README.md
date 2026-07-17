# cv-interactive — "Chromatic Chapters"

The interactive CV of Tomer Sahar. Concept: **"Don't read it. Interview it."**
A single-file static site where each career chapter is a color-blocked card with
expandable depth and contextual questions answered by an AI agent grounded in
verified CV facts.

## Repo layout

```
cv-interactive/
├── index.html                 # The entire site (tokens + content + behavior)
├── claude-design-prompt.md    # Prompt for visual exploration in Claude Design
├── api/
│   └── interview_proxy.py     # FastAPI proxy for live agent mode
└── docs/
    ├── PRD.md                 # Product requirements & scope
    ├── ARCHITECTURE.md        # System design, agent flow, security
    ├── CONTENT_GUIDE.md       # How to edit all CV text
    ├── DESIGN_TOKENS.md       # How to change all visuals
    └── DEPLOYMENT.md          # VPS deployment runbook
```

## Quickstart (local preview)

```bash
cd cv-interactive
python3 -m http.server 8080
# open http://localhost:8080 — agent runs in demo mode, no backend needed
```

## The two edit surfaces

| What you want to change | Where | Doc |
|---|---|---|
| Any text on the page | `CONTENT` object in `index.html` | docs/CONTENT_GUIDE.md |
| Colors, fonts, radii | `:root` / `[data-palette=...]` blocks in `index.html` | docs/DESIGN_TOKENS.md |
| Agent behavior (demo/live, endpoint, greeting) | `SITE_CONFIG` object in `index.html` | docs/ARCHITECTURE.md |

## Development workflow

Same rules as the rest of the stack:
- All changes via **fork → PR → CI → human merge**. No direct pushes to main.
- Agent-authored changes come from the `tomer-ai-agent` machine account.
- Secrets live in `.env` (`chmod 600`), never in this repo.
- Search for `[EDIT` in `index.html` before going live — these are
  placeholders (metrics to verify, LinkedIn URL, email).

## Status

- [x] Concept validated via 3 interaction mockups + 3 visual directions
- [x] Direction C ("Chromatic Chapters") selected and built
- [x] Demo-mode agent (canned answers, static-hosting safe)
- [x] **v1.1:** Ocean palette adopted as default (via Claude Design exploration)
- [x] **v1.1:** `riso-offset` card effect ported from the Claude Design export
- [x] **v1.1:** Dedicated desktop composition — sticky identity rail, scrollspy
      chapter nav, side-by-side depth blocks. Mobile layout untouched.
- [ ] Live agent: deploy `api/interview_proxy.py`, flip `SITE_CONFIG.agent.mode`
- [ ] Replace facts-file grounding with Qdrant retrieval (`cv:profile`)
- [ ] Verify `[EDIT]` placeholders (SciPlay metrics, contact links)
- [ ] Desktop QA pass at 1280/1440/1920 + tablet check at 768–1023px
