import pandas as pd
from backend.util.clean_html import clean_html_waha
from backend.ingestion.base_ingest import run_ingestion
from pathlib import Path


ROOT = Path(__file__).parent.parent.parent
output_file = open(ROOT / "data"/ "detachments_text.txt", "w", encoding = "utf-8")

def format_enhancements(detachment_id, enhancements):
    enhancement_info  = enhancements[enhancements['detachment_id'] == detachment_id]
    enhancement_list = []
    
    for _, row in enhancement_info.iterrows() :
        if pd.notna(row['name']):
            enhancement_list.append(f"\tName: {row['name']} Description: {row['description']}")
        
    return '\n'.join(enhancement_list)
    
def format_detachment_abilities(detachment_id, detachment_abilities):
    abilities_info =  detachment_abilities[detachment_abilities['detachment_id'] == detachment_id]
    abilities_list = []
    
    for _, row in abilities_info.iterrows():
        if pd.notna(row['name']):
            abilities_list.append(f"\tName: {row['name']} : {row['description']}")
    return '\n'.join(abilities_list)

def cleaner_helper(sheets):
    for col in sheets.columns:
        print(f"Checking column: {col} ({sheets[col].dtype})")
        if( sheets[col].dtype == 'str'):
            print(f"Cleaning {col}")
            sheets[col] = sheets[col].apply(clean_html_waha)
    return sheets

def ingest_detachments(edition, chroma_client):
    data_path = ROOT /'data'/ 'wahapedia'/ edition
    detachments = pd.read_csv(data_path / 'detachments.csv', sep= '|', encoding = 'utf-8-sig')
    detachments_abilities = pd.read_csv(data_path / 'detachment_abilities.csv' , sep='|' , encoding ='utf-8-sig')
    enhancements = pd.read_csv(data_path / 'enhancements.csv', sep= '|' , encoding = 'utf-8-sig')
    factions = pd.read_csv(data_path / 'factions.csv', sep='|', encoding = 'utf-8-sig')
    
    detachments = detachments.merge(
        factions[['id', 'name']].rename(columns = {'id': 'faction_id', 'name': 'faction_name'}),
        on = "faction_id",
        how = "left"
    )
    
    detachments = cleaner_helper(detachments)
    detachments_abilities = cleaner_helper(detachments_abilities)
    enhancements = cleaner_helper(enhancements)
    
    documents = []
    metadatas = []
    ids = []
    
    for _, row in detachments.iterrows():
        enhance_text = format_enhancements(row['id'] , enhancements)
        abilites_text = format_detachment_abilities(row['id'], detachments_abilities)
        det_type = ''
        if pd.notna(row['type']):
            det_type = row['type']
        else:
            det_type = "Normal"
        document = f"""DETACHMENT NAME: {row['name']}
FACTION: {row['faction_name']}
TYPE: {det_type}
ABILITY / ABILITIES:\n {abilites_text}
WARLORD ENHANCEMENTS:\n {enhance_text}
        """
        documents.append(document)
        metadatas.append({
            "source": "detachments",
            "name": row['name'],
            "faction": str(row['faction_name']),
        })
        ids.append(f"detachment{row['id']}")
        output_file.write(document + "\n---\n")

    run_ingestion(f"wh40k_detachments_{edition}", documents, metadatas, ids, chroma_client)
    output_file.close()
    print(f"Ingested {len(documents)} detachments into ChromaDB")
        
    
    
    
    