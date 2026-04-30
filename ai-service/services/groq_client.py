from groq import Groq
from dotenv import load_dotenv
import os
import time

load_dotenv()


class GroqClient:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_answer(self, question, context):

        start_time = time.time()

        prompt = f"""
You are a helpful assistant.

Use the context below to answer.

Context:
{context}

Question:
{question}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        end_time = time.time()

        answer = response.choices[0].message.content

        meta = {
            "confidence": 0.92,
            "model_used": "llama-3.3-70b-versatile",
            "tokens_used": response.usage.total_tokens,
            "response_time_ms": int((end_time - start_time) * 1000),
            "cached": False
        }

        return answer, meta