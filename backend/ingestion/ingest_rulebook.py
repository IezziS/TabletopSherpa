from pypdf import PdfReader
from pathlib import Path
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

import chromadb


embedding_fn = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434/api/embeddings"
)
ROOT = Path(__file__).parent.parent.parent
pdf_path_10thed = ROOT / "data"/ "rules" / "wh40kcorerules10th.pdf"

chroma_client = chromadb.PersistentClient(path = ROOT / "data"/"chroma_db")
collection = chroma_client.get_or_create_collection(name="wh40k_core_rules_10th", embedding_function= embedding_fn)

reader = PdfReader(pdf_path_10thed)
pages = []

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text: 
        pages.append({
            "id": f"page_{i+1}",
            "text": text,
            "metadata": {"page_number": i+1}
        })

collection.add(
    documents=[page["text"] for page in pages], 
    metadatas=[page["metadata"] for page in pages], 
    ids=[page["id"] for page in pages]
    )


print("Done, ingest completed!")
print(f"Ingested {len(pages)} pages from the core rule book into ChromaDB")