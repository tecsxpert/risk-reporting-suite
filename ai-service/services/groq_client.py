import os
import time

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model_name = "llama3-8b-8192"

    # -------------------------------------------------
    # Generate answer
    # -------------------------------------------------
    def generate_answer(self, question, context):

        start = time.time()

        try:

            prompt = f"""
            Answer the question using the context below.

            Context:
            {context}

            Question:
            {question}
            """

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response.choices[0].message.content

            response_time = round(
                (time.time() - start) * 1000,
                2
            )

            meta = {
                "tokens_used": response.usage.total_tokens,
                "response_time_ms": response_time,
                "is_fallback": False
            }

            return answer, meta

        # -------------------------------------------------
        # FALLBACK SYSTEM
        # -------------------------------------------------
        except Exception as e:

            fallback_answer = """
            AI service is temporarily unavailable.

            Please try again later.
            """

            response_time = round(
                (time.time() - start) * 1000,
                2
            )

            meta = {
                "tokens_used": 0,
                "response_time_ms": response_time,
                "is_fallback": True,
                "error": str(e)
            }

            return fallback_answer, meta