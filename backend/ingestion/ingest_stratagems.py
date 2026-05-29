import pandas as pd
import chromadb
from backend.util.clean_html import clean_html_waha
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
output_file = open(ROOT / "data"/ "stratagems_text.txt", "w", encoding = "utf-8")

data_path = ROOT / "data"/ "wahapedia" / "10th" 

stratagems = pd.read_csv(data_path / "stratagems.csv", sep="|", encoding = "utf-8-sig")
stratagems = stratagems.dropna(axis = 1, how = "all")
factions = pd.read_csv(data_path / "factions.csv", sep="|", encoding = "utf-8-sig")

#Joining the the stratagems with the factions. useful for chromaDB
stratagems = stratagems.merge(
    factions[['id', 'name']].rename(columns = {'id': 'faction_id', 'name': 'faction_name'}),
    on = "faction_id",
    how = "left"
)

#text cleanup time
for col in stratagems.columns:
    print(f"Checking column: {col} ({stratagems[col].dtype})")
    if( stratagems[col].dtype == 'str'):
        print(f"Cleaning {col}")
        stratagems[col] = stratagems[col].apply(clean_html_waha)


chroma_client = chromadb.PersistentClient(path = ROOT / "data"/"chroma_db")
chroma_client.delete_collection("wh40k_stratagems_10th") 
collection = chroma_client.get_or_create_collection(name="wh40k_stratagems_10th")

documents = []
metadatas = []
ids = []

for _, row in stratagems.iterrows():
    document = f"""STRATAGEM: {row['name']}
FACTION: {row.get('faction_name', 'Universal')}
TYPE: {row['type']}
CP COST: {row['cp_cost']}
WHEN: {row['turn']} - {row['phase']}
DETACHMENT: {row['detachment']}
FLAVOUR: {row['legend']}
EFFECT: {row['description']}
"""
    documents.append(document)
    metadatas.append({
        "source": "stratagem",
        "name": row['name'],
        "faction": str(row.get('faction_name', 'Universal')),
        "cp_cost": int(row['cp_cost']) if pd.notna(row['cp_cost']) else 0,
        "phase": str(row['phase']),
        "detachment": str(row['detachment'])
    })
    ids.append(f"stratagem_{row['id']}")
    
    output_file.write(document + "\n---\n")

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
output_file.close()
print(f"Ingested {len(documents)} stratagems into ChromaDB")