from services.chroma_client import ChromaClient

client = ChromaClient()

# Add sample data
client.add_text("1", "AI is used in healthcare")
client.add_text("2", "Stock market analysis and finance")
client.add_text("3", "Education systems are evolving")

# Query
result = client.query("healthcare technology")

print(result)