from services.groq_client import GroqClient

client = GroqClient()

result = client.generate_response("Hello")

print(result)