import chromadb
from backend.util.chroma_utils import query_router


client = chromadb.PersistentClient(path = "data/chroma_db")
#collection = client.get_or_create_collection(name="wh40k_core_rules_10th")



collection = client.get_collection("wh40k_datasheets_10th")
all_meta = collection.get()['metadatas']
intercessor_units = [m['name'] for m in all_meta if 'INTERCESSOR' in m['name'].upper()]
print(intercessor_units)


question = "What is the wounds characteristic of a space marine intercessor?"
print(question)
print(query_router(question,'10th', 5))


