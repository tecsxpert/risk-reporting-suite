from fastapi import FastAPI
from pydantic import BaseModel

from services.query_service import retrieve_context
from services.groq_client import GroqClient

app = FastAPI()

groq_client = GroqClient()


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "API running"}


@app.post("/query")
def query_docs(request: QueryRequest):

    context, sources = retrieve_context(
        request.question
    )

    answer, meta = groq_client.generate_answer(
        request.question,
        context
    )

    return {
        "answer": answer,
        "sources": sources,
        "meta": meta
    }