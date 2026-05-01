import time
from fastapi import FastAPI
from pydantic import BaseModel

from services.query_service import retrieve_context
from services.groq_client import GroqClient

from services.health_service import (
    add_response_time,
    get_health_data
)

from services.cache_service import (
    get_cache,
    set_cache,
    should_skip_cache
)

app = FastAPI()

groq_client = GroqClient()


# -------------------------------------------------
# Middleware: Track API response time
# -------------------------------------------------
@app.middleware("http")
async def track_response_time(request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = (time.time() - start) * 1000

    add_response_time(duration)

    return response


# -------------------------------------------------
# Request model
# -------------------------------------------------
class QueryRequest(BaseModel):
    question: str


# -------------------------------------------------
# Home API
# -------------------------------------------------
@app.get("/")
def home():

    return {
        "message": "API running"
    }


# -------------------------------------------------
# Query API with Cache + Meta Object
# -------------------------------------------------
@app.post("/query")
def query_docs(request: QueryRequest):

    start = time.time()

    question = request.question

    # ---------------------------------------------
    # Skip cache for fresh requests
    # Example:
    # no-cache: What is AI?
    # ---------------------------------------------
    if should_skip_cache(question):

        context, sources = retrieve_context(question)

        answer, groq_meta = groq_client.generate_answer(
            question,
            context
        )

        response_time = round(
            (time.time() - start) * 1000,
            2
        )

        return {
            "answer": answer,
            "sources": sources,
            "meta": {
                "confidence": 0.95,
                "model_used": "llama3-8b-8192",
                "tokens_used": groq_meta.get("tokens_used", 0),
                "response_time_ms": response_time,
                "cached": False
            }
        }

    # ---------------------------------------------
    # Check cache
    # ---------------------------------------------
    cached_result = get_cache(question)

    if cached_result:

        cached_result["meta"]["cached"] = True

        return cached_result

    # ---------------------------------------------
    # Generate fresh response
    # ---------------------------------------------
    context, sources = retrieve_context(question)

    answer, groq_meta = groq_client.generate_answer(
        question,
        context
    )

    response_time = round(
        (time.time() - start) * 1000,
        2
    )

    result = {
        "answer": answer,
        "sources": sources,
        "meta": {
            "confidence": 0.95,
            "model_used": "llama3-8b-8192",
            "tokens_used": groq_meta.get("tokens_used", 0),
            "response_time_ms": response_time,
            "cached": False
        }
    }

    # ---------------------------------------------
    # Save in cache
    # ---------------------------------------------
    set_cache(question, result)

    return result


# -------------------------------------------------
# Health Monitoring API
# -------------------------------------------------
@app.get("/health")
def health():

    return get_health_data()