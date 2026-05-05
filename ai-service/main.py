import time
import uuid
import threading

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
# In-memory job store
# -------------------------------------------------
jobs = {}


# -------------------------------------------------
# Middleware: Track response time
# -------------------------------------------------
@app.middleware("http")
async def track_response_time(request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = (time.time() - start) * 1000

    add_response_time(duration)

    return response


# -------------------------------------------------
# Request models
# -------------------------------------------------
class QueryRequest(BaseModel):
    question: str


class ReportRequest(BaseModel):
    topic: str


# -------------------------------------------------
# Home API
# -------------------------------------------------
@app.get("/")
def home():

    return {
        "message": "API running"
    }


# -------------------------------------------------
# Query API
# -------------------------------------------------
@app.post("/query")
def query_docs(request: QueryRequest):

    start = time.time()

    question = request.question

    # -------------------------------------------------
    # Skip cache logic
    # -------------------------------------------------
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
                "cached": False,
                "is_fallback": groq_meta.get(
                    "is_fallback",
                    False
                )
            }
        }

    # -------------------------------------------------
    # Check cache
    # -------------------------------------------------
    cached_result = get_cache(question)

    if cached_result:

        cached_result["meta"]["cached"] = True

        return cached_result

    # -------------------------------------------------
    # Generate fresh response
    # -------------------------------------------------
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
            "cached": False,
            "is_fallback": groq_meta.get(
                "is_fallback",
                False
            )
        }
    }

    # -------------------------------------------------
    # Save cache
    # -------------------------------------------------
    set_cache(question, result)

    return result


# -------------------------------------------------
# Background report processing
# -------------------------------------------------
def process_report(job_id, topic):

    jobs[job_id]["status"] = "processing"

    time.sleep(5)

    report = f"""
AI Generated Report

Topic: {topic}

Summary:
This report contains AI-generated insights about {topic}.
"""

    jobs[job_id]["status"] = "completed"

    jobs[job_id]["report"] = report

    # Simulated webhook
    print(f"Webhook triggered for job {job_id}")


# -------------------------------------------------
# Generate report API
# -------------------------------------------------
@app.post("/generate-report")
def generate_report(request: ReportRequest):

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "report": None
    }

    thread = threading.Thread(
        target=process_report,
        args=(job_id, request.topic)
    )

    thread.start()

    return {
        "message": "Report generation started",
        "job_id": job_id,
        "status": "queued"
    }


# -------------------------------------------------
# Job status API
# -------------------------------------------------
@app.get("/job/{job_id}")
def get_job_status(job_id: str):

    if job_id not in jobs:

        return {
            "error": "Job not found"
        }

    return jobs[job_id]


# -------------------------------------------------
# Health API
# -------------------------------------------------
@app.get("/health")
def health():

    return get_health_data()