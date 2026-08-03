import pandas as pd
from backend.util.clean_html import clean_html_waha
from backend.ingestion.base_ingest import run_ingestion
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
output_file = open(ROOT / "data"/ "stratagems_text.txt", "w", encoding = "utf-8")

#This file is responsible for ingesting the stratagems data from the Wahapedia CSVs into ChromaDB. 
# It reads the CSV, cleans the text, and then formats it into a consistent structure before ingestion.
#Could split it up, dont want to. 
def ingest_stratagems(filename , edition, chroma_client):
    data_path = ROOT / "data"/ "wahapedia" / edition
    stratagems = pd.read_csv(data_path / filename, sep="|", encoding = "utf-8-sig")   
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



    documents = []
    metadatas = []
    ids = []

    #spaghetti! bascically just fixing univerals.And checkign for duplicates, there shouldnt be any but who knows. 
    for _, row in stratagems.iterrows():
        
        if(row.get('faction_name') == 'nan'):
            fac_name = 'Universal'
        else:
            fac_name = row.get('faction_name', 'Universal')
            
        document = f"""STRATAGEM: {row['name']}
    FACTION: {fac_name}
    TYPE: {row['type']}
    CP COST: {row['cp_cost']}
    WHEN: {row['turn']} - {row['phase']}
    DETACHMENT: {row['detachment']}
    EFFECT: {row['description']}
    """
        documents.append(document)
        metadatas.append({
            "source": "stratagem",
            "name": row['name'],
            "faction": str(fac_name),
            "cp_cost": int(row['cp_cost']) if pd.notna(row['cp_cost']) else 0,
            "phase": str(row['phase']),
            "detachment": str(row['detachment'])
        })
        ids.append(f"stratagem_{row['id']}")
        
        output_file.write(document + "\n---\n")

    #generic ingestion to ChromaDB
    run_ingestion(f"wh40k_stratagems_{edition}", documents, metadatas, ids, chroma_client)

    #Debugging output file. 
    output_file.close()
    print(f"Ingested {len(documents)} stratagems into ChromaDB")