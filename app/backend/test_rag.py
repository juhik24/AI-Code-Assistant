from app.backend.rag import retrieve_context

results = retrieve_context("Where is JWT generated?")

documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]

for i in range(len(documents)):
    print("=" * 60)
    print(f"Rank: {i + 1}")
    print(f"Distance: {distances[i]:.4f}")
    print(f"Source: {metadatas[i]['source']}")
    print()
    print(documents[i])