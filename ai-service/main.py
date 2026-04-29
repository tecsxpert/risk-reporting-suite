from fastapi import FastAPI
from pydantic import BaseModel
from services.groq_client import GroqClient
import json

app = FastAPI()
client = GroqClient()

class TextRequest(BaseModel):
    text: str

@app.post("/categorise")
def categorise(req: TextRequest):
    prompt = f"""
Classify the text into:
- Technology
- Finance
- Health
- Education
- Other

Return ONLY JSON:
{{
  "category": "",
  "confidence": 0.0,
  "reasoning": ""
}}

Text: {req.text}
"""

    result = client.generate_response(prompt)

    try:
        return json.loads(result["response"])
    except:
        return {
            "category": "Other",
            "confidence": 0.5,
            "reasoning": result["response"]
        }