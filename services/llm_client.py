import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    api_key = "gsk_GZ91a0iHFY3czIDbM4uWGdyb3FYWxBrCJjxsuucMbYlOUnFn0Lt"

client = Groq(api_key=api_key)

def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
