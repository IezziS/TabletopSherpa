import pandas as pd
from backend.util.clean_html import clean_html_waha
from backend.ingestion.base_ingest import run_ingestion
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
output_file = open(ROOT / "data"/ "abilities_text.txt", "w", encoding = "utf-8")

CANONICAL_ABILITY_OWNERS = {
    'Synapse': 'TYR',
    'Oath of Moment': 'SM',
    'Dark Pacts': 'CSM',
    'Shadow in the Warp': 'TYR',
    'Doctrina Imperatives': 'AdM',
    'Nurgle\'s Gift (Aura)': 'DG',
    'Cabal of Sorcerers': 'TS',
    'Blessings of Khorne': 'WE',
    'Assigned Agents': 'AoI',
    'Kill Team': 'AoI',
    'Battle Focus': 'AE',
    'Disparate Paths': 'AE',
    'Thrill Seekers': 'EC'
}

#some duplicates exist in the dataset, where the same ability is listed under multiple factions. 
#this function will check the list of canonical owners for those duplicates. 
#I tried modifying the dataset... EVERYTHING BROKE. so now we have to do this weird check at ingestion time. fun!
def check_owner(ability_name, faction_id):
    canonical_owner = CANONICAL_ABILITY_OWNERS.get(ability_name)
    if canonical_owner is None:
        print(f"No duplicates for {ability_name}, including by default")
        return True  # No duplicates, must be cananonical order. include,
    print(f"Checking {ability_name} against canonical owner {canonical_owner} with faction ID {faction_id}")
    return str(faction_id) == canonical_owner


#This file is very similar to ingest_stratagems.py, but with some differences:
# - different metadata fields (no cp cost, phase, etc)
def ingest_abilities(filename , edition, chroma_client):
    data_path = ROOT / "data"/ "wahapedia" / edition
    abilities = pd.read_csv(data_path / filename, sep="|", encoding = "utf-8-sig")   
    abilities = abilities.dropna(axis = 1, how = "all")
    factions = pd.read_csv(data_path / "factions.csv", sep="|", encoding = "utf-8-sig")

    #Joining the the abilities with the factions. useful for chromaDB
    abilities = abilities.merge(
        factions[['id', 'name']].rename(columns = {'id': 'faction_id', 'name': 'faction_name'}),
        on = "faction_id",
        how = "left"
    )

    #text cleanup time
    for col in abilities.columns:
        print(f"Checking column: {col} ({abilities[col].dtype})")
        if( abilities[col].dtype == 'str'):
            print(f"Cleaning {col}")
            abilities[col] = abilities[col].apply(clean_html_waha)



    documents = []
    metadatas = []
    ids = []
    seen_ids = set()

    #spaghetti! bascically just fixing univerals, and duplicates.
    for _, row in abilities.iterrows():
        if(row.get('faction_name') == 'nan'):
            fac_name = 'Universal'
        else:
            fac_name = row.get('faction_name', 'Universal')
            
        document = f"""ABILITY: {row['name']}
    FACTION: {fac_name}
    EFFECT: {row['description']}
    """
        if row['id'] not in seen_ids:
            if check_owner(row['name'], row['faction_id']):
                documents.append(document)
                metadatas.append({
                    "source": "ability",
                    "name": row['name'],
                    "faction": str(fac_name),
                })
                ids.append(f"ability_{row['id']}")
                
                output_file.write(document + "\n---\n")
                seen_ids.add(row['id'])
            
    #calls the base ingestion function to actually put the data in chromaDB
    run_ingestion(f"wh40k_abilities_{edition}", documents, metadatas, ids, chroma_client)

    #these output files are just for debugging. 
    output_file.close()
    print(f"Ingested {len(documents)} abilities into ChromaDB")