from pathlib import Path
from backend.ingestion.base_ingest import run_ingestion

ROOT = Path(__file__).parent.parent.parent
output_file = open(ROOT / "data"/ "core_rules_text.txt", "w", encoding = "utf-8")


def ingest_core_rules(edition, chroma_client):
    
    rules_path = ROOT / "data" / "rules" / f"wh40kcorerules{edition}.txt"
    
    with open(rules_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split on your separator
    chunks = [c.strip() for c in content.split("+" * 20) if c.strip()]
    
    documents = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        
        lines = chunk.split("\n")
        title = lines[0].strip()
        
        documents.append(chunk)
        metadatas.append({
            "source": "core_rules",
            "title": title,
            "name": title,
            "edition": edition
        })
        ids.append(f"core_rules_{edition}_{i}")
        output_file.write(chunk + "\n---\n")
        
    
    run_ingestion(f"wh40k_core_rules_{edition}",documents,metadatas,ids,chroma_client)
    output_file.close()
    print(f"Ingested {len(documents)} rule pages into ChromaDB")