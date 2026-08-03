import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
chroma_client = chromadb.PersistentClient(path=str(ROOT / "data" / "chroma_db"))

embedding_fn = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434/api/embeddings"
)
COLLECTIONS = {
    "10th": [
        "wh40k_core_rules_10th",
        "wh40k_stratagems_10th",
        "wh40k_abilities_10th",
        'wh40k_datasheets_10th',
        'wh40k_detachments_10th'
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
    "advance", 'infantry', 'vehicle', 'character', 'monster',
    'fly', 'transport', 'battleline', 'epic hero', 'towering',
    'lead', 'attach', 'bodyguard', 'leader', 'embark', 'disembark',
    "sequence", 'phase'
    "allocate", "allocating", "wounds"
}
ABILITY_KEYWORDS = {
    # Direct ability name queries
    'ability', 'abilities', 'rule', 'special rule',
    # Common ability names that appear in the data
    'synapse', 'deep strike', 'feel no pain', 'deadly demise',
    'lone operative', 'stealth', 'infiltrate', 'scout',
    'leader', 'fights first', 'hover', 'reanimation',
    'oath of moment', 'dark pacts', 'acts of faith',
    'strands of fate', 'for the greater good',
    'battle focus', 'power from pain', 'harbingers',
    'blessings of khorne', 'waaagh', 'doctrina',
    'martial katah', 'voice of command', 'gate of infinity',
    # Mechanic keywords that imply ability lookups
    'aura', 'psychic', 'ritual', 'miracle dice', 'fate dice',
    'pain token', 'dread', 'bondsman', 'invulnerable save',
    'battle shock', 'objective control'
}
DATASHEETS_KEYWORDS = {
    'datasheet', 'statline', 'stats', 'profile', 'characteristic',
    'unit', 'model', 'squad', 'warband', 'army list',
    'toughness', 'movement', 'save', 'wounds', 'leadership', 
    'objective control', 'invulnerable', 'armour', 'oc',
    'strength', 'attacks', 'skill', 'ballistic', 'weapon skill', "bs", 'ws',
    'wargear', 'loadout', 'equipped', 'weapon', 'melee', 'ranged',
    'gun', 'sword', 'rifle', 'bolter', 'cannon', 'missile',
    'replace', 'swap', 'option', 'upgrade',
    'composition', 'how many models', 'squad size', 'minimum', 
    'maximum', 'points', 'pts',
    'keyword', 
    'how many', 'can i take',
    'what weapons', 'what abilities', 'how tough', 'how fast'

}
DETACHMENTS_KEYWORDS = {
    'Detachments', 'Detachment', 'Detachment ability'
    ,'Ability', 'sub faction', 'enhancements'
}

# Build this once when the module loads
NAME_CACHE = {}

def get_collection(name):
    return chroma_client.get_or_create_collection(name = name,embedding_function=embedding_fn)

def build_name_cache():
    for edition, collections in COLLECTIONS.items():
        NAME_CACHE[edition] = {}
        for collection_name in collections:
            try:
                collection = get_collection(name=collection_name)
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
    if any(keyword in q for keyword in ABILITY_KEYWORDS):
        collections.append(f"wh40k_abilities_{edition}")
    if any(keyword in q for keyword in DATASHEETS_KEYWORDS):
        collections.append(f"wh40k_datasheets_{edition}")
    if not collections:
        collections = COLLECTIONS.get(edition, [])
    
    return collections

def find_exact_matches(question, collection, collection_name, edition):
    names = NAME_CACHE.get(edition, {}).get(collection_name, {})
    question_upper = question.upper()
    question_words = set(question_upper.split())
    
    matches = []
    for upper_name, original_name in names.items():
        name_words = set(upper_name.split())
        # Check if all words in the unit name appear in the question
        # OR if all question content words appear in the unit name
        if name_words.issubset(question_words) or \
           any(word in question_upper for word in name_words if len(word) > 4):
            matches.append(original_name)
    
    
    if matches:
        all_results_docs = []
        all_results_metas = []
        all_results_ids = []
        
        for match in matches:
            results = collection.get(where={"name": match})
            if results['documents']:
                all_results_docs.extend(results['documents'])
                all_results_metas.extend(results['metadatas'])
                all_results_ids.extend(results['ids'])
        
        return all_results_docs, all_results_metas, all_results_ids
    
    return None, None, None

def query_collection(question, collection_name, edition, n_results):
    all_documents = []
    all_metadatas = []
    seen_ids = set()
    try:
        collection = get_collection(name=collection_name)
        docs, metas, ids = find_exact_matches(question, collection, collection_name, edition)
        if docs:
            for doc, meta, id in zip(docs, metas, ids):
                if id not in seen_ids: 
                    all_documents.append(doc)
                    all_metadatas.append(meta)
                    seen_ids.add(id)
            return all_documents, all_metadatas, list(seen_ids)

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


