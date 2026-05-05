from services.rag_pipeline import search_docs

query = "cybersecurity threats in trading"
results = search_docs(query)

print("Query:", query)
for doc, score in zip(results["documents"][0], results["distances"][0]):
    print(f"- {doc[:80]}... (score={score:.4f})")
