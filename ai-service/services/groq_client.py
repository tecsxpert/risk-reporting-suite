from dotenv import load_dotenv
import os
import time
import logging
from groq import Groq

load_dotenv()

logging.basicConfig(level=logging.ERROR)

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found")

        self.client = Groq(api_key=self.api_key)

    def generate_response(self, prompt, retries=3):
        backoff = 2

        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )

                return {
                    "status": "success",
                    "response": response.choices[0].message.content
                }

            except Exception as e:
                logging.error(f"Attempt {attempt+1} failed: {e}")

                if attempt < retries - 1:
                    time.sleep(backoff)
                    backoff *= 2
                else:
                    return {
                        "status": "error",
                        "message": str(e)
                    }