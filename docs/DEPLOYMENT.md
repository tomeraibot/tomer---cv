# DEPLOYMENT — VPS runbook

Target: existing Contabo VPS stack, `tomer---cv` repo pattern, nginx front,
Docker services on `ai_stack_git_edge`.

## Pre-flight checklist (do not skip)

- [ ] `grep -rn "openclaw_default" .` returns **nothing** in any compose file
      you touch — that network is permanently dead (root cause of the last
      502 on cv.tomersahar.com).
- [ ] `grep -n "\[EDIT" index.html` — resolve every placeholder
      (SciPlay metrics, LinkedIn URL, email).
- [ ] `SITE_CONFIG.agent.mode` is `"demo"` unless the proxy is deployed
      and healthy.
- [ ] Changes flow via fork → PR → CI → human merge. Agent-authored changes
      come from `tomer-ai-agent`; merge from the personal account.

## Phase 1 — static site (demo mode)

1. PR `index.html` (+ docs) into the `tomer---cv` repo.
2. Ensure the site container/compose references `ai_stack_git_edge` (edge)
   only. Static serving via the existing nginx pattern.
3. Post-merge deploy per repo convention, then verify:
   ```bash
   curl -sI https://cv.tomersahar.com | head -3        # expect 200
   ```
4. Manual smoke test on a real phone: chips, +More, bottom sheet,
   Under the Hood button.

## Phase 2 — live agent (v1.1)

1. New service dir `services/cv-interview/` with `interview_proxy.py`,
   `requirements.txt` (`fastapi uvicorn httpx pydantic`), Dockerfile
   (uvicorn on :8091), and `data/verified_facts.md`.
2. Compose service on **internal** network + nginx location:
   ```nginx
   location /api/interview {
       proxy_pass http://cv_interview:8091;
       limit_req zone=interview burst=5 nodelay;   # define zone: 10r/m per IP
   }
   ```
3. Env (in `.env`, `chmod 600` — never committed):
   `ANTHROPIC_API_KEY`, `CV_ORIGIN=https://cv.tomersahar.com`,
   optional `INTERVIEW_MODEL`.
4. Health check, then flip the frontend:
   ```bash
   curl -s https://cv.tomersahar.com/api/interview/health
   # {"status":"ok",...}  → PR: SITE_CONFIG.agent.mode = "live"
   ```

## Phase 3 — Qdrant grounding (v1.2)

Replace facts-file stuffing in `build_system_prompt()` with top-k retrieval
from the existing `cv:profile` collection (Ollama embeddings, internal
network). Frontend contract unchanged.

## Rollback

- Frontend: revert the merge commit, redeploy (single file — trivial).
- Agent misbehaving: flip `mode` back to `"demo"` — one-line PR, site stays up.
- Proxy down: no action needed; frontend degrades gracefully in-chat.

## Launch checklist

- [ ] All `[EDIT]` resolved and fact-checked
- [ ] 20-question spot check of live agent (10 Hebrew / 10 English),
      including 3 off-topic probes → expect polite declines
- [ ] Lighthouse mobile: performance ≥ 90
- [ ] 429/timeout path tested (kill proxy, ask a question, verify fallback)
- [ ] Old CV version archived in repo history
