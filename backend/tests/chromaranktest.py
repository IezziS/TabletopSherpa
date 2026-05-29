from backend.util.chroma_utils import chroma_client, query_router
import sys

sys.stdout.reconfigure(encoding='utf-8-sig')
collection = chroma_client.get_collection("wh40k_stratagems_10th")

documents, metadatas = query_router(
    "COUNTER-OFFENSIVE",
    edition="10th",
    n_results=10
)

for doc in documents:
    print(doc)
    print("=" * 80)