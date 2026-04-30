from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


class GroqClient:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_answer(self, question, context):

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

        return response.choices[0].message.content