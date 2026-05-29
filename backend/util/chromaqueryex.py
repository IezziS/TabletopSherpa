import chromadb
import uuid

client = chromadb.PersistentClient(path = "data/chroma_db")
collection = client.get_or_create_collection(name="wh40k_core_rules_10th")

results = collection.query(
    query_texts=[
        "what is the shooting phase?",
        "What is the CP cost for command re roll?" 
        ],
    n_results=1
)

for i, query_reuslt in enumerate(results["documents"]):
    print(f"Query {i+1}:")
    print("\n".join(query_reuslt))
    print("\n---\n")