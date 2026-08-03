from backend.util.chroma_utils import get_collection


def run_ingestion(collection_name, documents, metadatas, ids, chroma_client):
    try: 
        collection = chroma_client.delete_collection(name=collection_name)
    except Exception as e:
        print(f"Error deleting collection {collection_name} : {e}")
        pass
    collection = get_collection(collection_name)
    
    existing = collection.get()
    if existing['ids']:
        collection.delete(ids=existing['ids'])
        
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i+batch_size]
        batch_metas = metadatas[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        
        collection.add(
            documents=batch_docs,
            metadatas=batch_metas,
            ids=batch_ids
        )
    print(f"Ingested {len(documents)} documents into collection {collection_name}")
    
    