import chromadb
from pathlib import Path
from backend.ingestion.ingest_stratagems import ingest_stratagems
from backend.ingestion.ingest_abilities import ingest_abilities
from backend.ingestion.ingest_datasheets import ingest_datasheets
from backend.ingestion.ingest_detachments import ingest_detachments
from backend.ingestion.ingest_rulebook import ingest_core_rules


ROOT = Path(__file__).parent.parent.parent
chroma_client = chromadb.PersistentClient(path = ROOT / "data"/"chroma_db")

if __name__ == "__main__":
    ingest_stratagems("stratagems.csv", "10th",chroma_client)
    ingest_abilities("abilities.csv", "10th",chroma_client)
    ingest_datasheets("10th", chroma_client)
    ingest_detachments("10th", chroma_client)
    ingest_core_rules("10th", chroma_client)