import chromadb
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
chroma_client = chromadb.PersistentClient(path = ROOT / "data" / "chroma_db")

COLLECTIONS = {
    "10th": [
        "wh40k_core_rules_10th",
        "wh40k_stratagems_10th"
    ],
    "11th": []
}
STRATAGEM_KEYWORDS = {
    "stratagem",
    "stratagems",
    "command point",
    "cp",
    "command re-roll",
    "overwatch"
}
CORE_RULES_KEYWORDS = {
    "saving throw",
    "shooting phase",
    "charge phase",
    "psychic",
    "fight phase",
    "movement phase",
    "command phase",
    "movement",
    "shooting",
    "charge",
    "pile in",
    "fall back",
    "advance",
    "sequence",
    "allocate",
    "saves",
    "wounds",
    "damage"
}

# Build this once when the module loads
NAME_CACHE = {}

def build_name_cache():
    for edition, collections in COLLECTIONS.items():
        NAME_CACHE[edition] = {}
        for collection_name in collections:
            try:
                collection = chroma_client.get_collection(name=collection_name)
                all_meta = collection.get()['metadatas']
                NAME_CACHE[edition][collection_name] = {
                    m['name'].upper(): m["name"]
                    for m in all_meta if 'name' in m
                }
                
            except Exception as e:
                print(f"Error building name cache for collection {collection_name}: {e}")
                continue

def determine_collections(question, edition):
    q= question.lower()
    
    collections = []
    if any(keyword in q for keyword in STRATAGEM_KEYWORDS):
        collections.append(f"wh40k_stratagems_{edition}")
    if any(keyword in q for keyword in CORE_RULES_KEYWORDS):
        collections.append(f"wh40k_core_rules_{edition}")
    if not collections:
        collections = COLLECTIONS.get(edition, [])
    
    return collections

def find_exact_matches(question, collection, collection_name, edition):
    names = NAME_CACHE.get(edition, {}).get(collection_name, {})
    question_upper = question.upper()
    matches = [
        original_name
        for upper_name, original_name in names.items()
        if upper_name in question_upper
    ]
    
    if matches:
        best_match = max(matches, key=len)
        results = collection.get(where={"name": best_match})
        return results['documents'], results['metadatas'], results['ids']
    
    return None, None, None

def query_collection(question, collection_name, edition, n_results):
    all_documents = []
    all_metadatas = []
    seen_ids = set()
    try:
        collection = chroma_client.get_or_create_collection(name=collection_name)
        docs, metas, ids = find_exact_matches(question, collection, collection_name, edition)
        if docs:
            for doc, meta, id in zip(docs, metas, ids):
                if id not in seen_ids: 
                    all_documents.append(doc)
                    all_metadatas.append(meta)
                    seen_ids.add(id)
        #semantic search
        semantic_results = collection.query(
            query_texts=[question],
            n_results=n_results
        )
        for doc, meta, id, in zip(
            semantic_results["documents"][0], 
            semantic_results["metadatas"][0], 
            semantic_results["ids"][0]
        ):
            if id not in seen_ids:
                all_documents.append(doc)
                all_metadatas.append(meta)
                seen_ids.add(id)        
    except Exception as e:
        print(f"Error querying collection {collection_name}: {e}")
        
    return all_documents, all_metadatas, list(seen_ids)


def query_router(question, edition, n_results):
    collections_to_query = determine_collections(question, edition)
    all_documents = []
    all_metadatas = []
    for c in collections_to_query:
        print(f"Querying collection: {c}")
        docs, metadatas, ids = query_collection(question, c, edition, n_results)
        if docs:
            all_documents.extend(docs)
            all_metadatas.extend(metadatas)
    return all_documents, all_metadatas

        
        

build_name_cache()