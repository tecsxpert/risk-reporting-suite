from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
resp = client.chat.completions.create(
    model="llama-3.3-70b-versatile",   # <-- valid model from your account
    messages=[{"role": "system", "content": "Say hello"}]
)
print(resp.choices[0].message.content)
