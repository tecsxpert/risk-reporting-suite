import time
from fastapi import FastAPI
from pydantic import BaseModel

from services.query_service import retrieve_context
from services.groq_client import GroqClient
from services.health_service import (
    add_response_time,
    get_health_data,
    cache_hit,
    cache_miss
)

app = FastAPI()

groq_client = GroqClient()


# -----------------------------
# Middleware: track response time
# -----------------------------
@app.middleware("http")
async def track_response_time(request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = (time.time() - start) * 1000
    add_response_time(duration)

    return response


# -----------------------------
# Request model
# -----------------------------
class QueryRequest(BaseModel):
    question: str


# -----------------------------
# Home API
# -----------------------------
@app.get("/")
def home():
    return {"message": "API running"}


# -----------------------------
# Query API
# -----------------------------
@app.post("/query")
def query_docs(request: QueryRequest):

    context, sources = retrieve_context(request.question)

    # Cache tracking logic
    if context:
        cache_hit()
    else:
        cache_miss()

    answer, meta = groq_client.generate_answer(
        request.question,
        context
    )

    return {
        "answer": answer,
        "sources": sources,
        "meta": meta
    }


# -----------------------------
# Health API
# -----------------------------
@app.get("/health")
def health():
    return get_health_data()