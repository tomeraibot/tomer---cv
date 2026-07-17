"""
interview_proxy.py — FastAPI proxy for the CV agent ("The Interview").

Purpose: keep the LLM API key server-side. The static site POSTs here;
this service builds a grounded prompt from verified CV facts and calls
the LLM. Designed to run as a small Docker service on the existing VPS
stack (ai_stack_git_edge network), fronted by nginx at /api/interview.

SECURITY NOTES
- ANTHROPIC_API_KEY comes from environment only (.env, chmod 600).
- CORS locked to the CV domain.
- Answers are grounded: the system prompt embeds verified facts and
  instructs the model to decline anything outside them.
- Optional next step: replace FACTS file with a Qdrant retrieval call
  (collection: cv:profile) for true RAG instead of full-context stuffing.
"""

import os
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]  # fail fast if missing
MODEL = os.environ.get("INTERVIEW_MODEL", "claude-sonnet-4-6")
ALLOWED_ORIGIN = os.environ.get("CV_ORIGIN", "https://cv.tomersahar.com")
FACTS_PATH = Path(os.environ.get("CV_FACTS_PATH", "/app/data/verified_facts.md"))

app = FastAPI(title="cv-interview-proxy")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class Turn(BaseModel):
    role: str
    content: str


class AskRequest(BaseModel):
    question: str
    context: str = "full-cv"          # chapter id or "full-cv"
    history: list[Turn] = []


def build_system_prompt() -> str:
    facts = FACTS_PATH.read_text(encoding="utf-8") if FACTS_PATH.exists() else ""
    return (
        "You are 'The Interview' — the CV agent on Tomer Sahar's interactive "
        "resume site. Answer questions about Tomer's career, skills and "
        "approach, in the language the visitor uses (Hebrew or English).\n\n"
        "HARD RULES:\n"
        "1. Ground every claim in the VERIFIED FACTS below. If asked something "
        "not covered, say so plainly and suggest contacting Tomer directly.\n"
        "2. Never invent metrics, employers, dates or claims.\n"
        "3. Keep answers under 120 words, confident and concrete.\n"
        "4. Politely decline off-topic requests (you only discuss Tomer's CV).\n\n"
        f"VERIFIED FACTS:\n{facts}"
    )


@app.post("/api/interview")
async def interview(req: AskRequest):
    messages = [t.model_dump() for t in req.history][-10:]
    messages.append(
        {"role": "user", "content": f"[visitor is viewing: {req.context}]\n{req.question}"}
    )
    payload = {
        "model": MODEL,
        "max_tokens": 512,
        "system": build_system_prompt(),
        "messages": messages,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=payload,
        )
    if r.status_code != 200:
        raise HTTPException(502, "Upstream LLM error")
    data = r.json()
    answer = "".join(b.get("text", "") for b in data.get("content", []))
    return {"answer": answer}


@app.get("/api/interview/health")
async def health():
    return {"status": "ok", "model": MODEL, "facts_loaded": FACTS_PATH.exists()}
