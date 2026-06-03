#This is going to be a doozy, Datasheet information is split across multiple files.
import pandas as pd
from backend.util.clean_html import clean_html_waha
from backend.ingestion.base_ingest import run_ingestion
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
output_file = open(ROOT / "data"/ "datasheets_text.txt", "w", encoding = "utf-8")

def format_abilities(datasheet_id, datasheets_abilities, abilities, faction_id):
    unit_abilities = datasheets_abilities[datasheets_abilities['datasheet_id'] == datasheet_id]
    
    core = [] 
    faction = []
    datasheet = []
    wargear = []
    special = []
    for _, row in unit_abilities.iterrows():
        a_type = row['type']
        
        if a_type =='Core':
            match  = abilities[abilities['id'] == row['ability_id']]
            if not match.empty:
                core.append(match.iloc[0]['name'])
                if pd.notna(row['parameter']):
                    core.append(f"({row['parameter']})")
        elif a_type == 'Faction':
            ability_match = abilities[abilities['id'] == row['ability_id']]
            if not ability_match.empty:
                faction_match = ability_match[ability_match['faction_id'] == faction_id]
                if not faction_match.empty:
                    faction.append(faction_match.iloc[0]['name'])
                else:
                    # Fall back to any entry if no faction specific one exists
                    faction.append(ability_match.iloc[0]['name'])
        elif a_type == 'Datasheet':
            name = row['name'] if pd.notna(row['name']) else 'Unknown'
            desc = row['description'] if pd.notna(row['description']) else 'Description Unavailable'
            datasheet.append(f"{name}: {desc}")
        elif a_type == 'Wargear':
            name = row['name'] if pd.notna(row['name']) else 'Unknown'
            desc = row['description'] if pd.notna(row['description']) else 'Description Unavailable'
            wargear.append(f"{name}: {desc}")
        elif 'Special' in a_type:
            name = row['name'] if pd.notna(row['name']) else 'Unknown'
            desc = row['description'] if pd.notna(row['description']) else 'Description Unavailable'
            special.append(f"{name}: {desc}")
            
    
    parts = []
    if core:
        parts.append(f"\tCore Abilities: {', '.join(core)}")
    if faction:
        parts.append(f"\tFaction Abilities: {', '.join(faction)}")
    if datasheet:
        parts.append("\tUnit Abilities:\n" + '\n'.join(f"  \t- {a}" for a in datasheet))
    if wargear:
        parts.append('\tWargear Abilities:\n' + '\n'.join(f" \t- {a}" for a in wargear))
    if special:
        parts.append('\tSpecial Abilities:\n' + '\n'.join(f" \t- {a}" for a in special))
    return '\n'.join(parts)
 

def format_keywords(datasheet_id, keywords):
    unit_keywords = keywords[(keywords['datasheet_id'] == datasheet_id) & (pd.notna(keywords['keyword']))]
    keyword_list = []
    for _, row in unit_keywords.iterrows():
        if pd.notna(row['model']) and str(row['model']).strip():
            keyword_list.append(f"\t{row['keyword']} ({row['model']})")
        else:
            keyword_list.append("\t"+row['keyword'])
    
    return '\n'.join(keyword_list)


def format_leader(datasheet_id, ds_leader, datasheets):
    leader_info = ds_leader[ds_leader['leader_id'] == datasheet_id]
    
    can_lead =[]
    if not leader_info.empty:
        for _, row in leader_info.iterrows():
            match = datasheets[datasheets['id'] == row['attached_id']]
            if not match.empty:
                unit_name = match.iloc[0]['name']
                can_lead.append(f"\t{unit_name}")
    if can_lead:
        return "This Model can be attached to / lead:\n" + '\n'.join(f"  - {u}" for u in can_lead)
    return ""

#WHY DOES MAKARI HAVE A SPECIAL RULE FOR HIS INVULVERABLE SAVE? WHO KNOWS! BUT IT MEANS WE HAVE TO CHECK THE MODELS FOR EACH DATASHEET 
# TO SEE IF THEY HAVE ANY SPECIAL RULES OR ABILITIES ATTACHED TO THEM. FUCK!    
def format_models(datasheet_id, statline):
    statline_info = statline[statline['datasheet_id'] == datasheet_id]  
    statlines = []
    for _, rows in statline_info.iterrows():
        invul = 'None' 
        invul_Cond = ''
        if pd.notna(rows['inv_sv']) and rows['inv_sv'] != '-':
            invul = rows['inv_sv']
            invul_Cond = rows['inv_sv_descr'] if pd.notna(rows['inv_sv_descr']) else ''
        model = (
            f"\t{rows['name']}: "
            f"Movement (M):{rows['M']} Toughness (T):{rows['T']} Armor Save (Sv):{rows['Sv']} "
            f"Wounds (W):{rows['W']} Invulnerable Save: {invul} {invul_Cond} "
            f"Leadership (Ld):{rows['Ld']} Objective Control (OC):{rows['OC']}"
            ).strip()
        statlines.append(model)
    return '\n'.join(statlines)
  
def format_cost(datasheet_id, model_cost):
    cost_info = model_cost[model_cost['datasheet_id'] == datasheet_id]
    costs = []
    for _, row in cost_info.iterrows():
        
        if pd.notna(row['cost']):
            costs.append(f"\t{row['description']}: {row['cost']} points")
                
    return '\n'.join(costs)
def format_options(datasheet_id, options):
    options_info = options[options['datasheet_id'] == datasheet_id]
    options_list = []
    for _, row in options_info.iterrows():
        if pd.notna(row['description']):
            options_list.append(f"\t{row['description']}")
    return '\n'.join(options_list)

def format_wargear(datasheet_id, wargear):
    wargear_info = wargear[wargear['datasheet_id']== datasheet_id]
    wargear_list = []
    dice = False
    
    for _, row in wargear_info.iterrows():
        if pd.notna(row['dice']) &  pd.notna(row['name']):
            if dice == False:
                wargear_list.append(f"Roll a dice to determine which statline is used for weapons contain Dice stat:")
                dice = True
            wargear_list.append(f"\t{row['name']} Dice: {row['dice']} Keywords: {row['description']} Range: {row['range']} "
                                f"Type: {row['type']} Attacks (A): {row['A']} BS or WS: {row['BS_WS']} Strength (S): {row['S']} "
                                f"AP: {row['AP']} Damage (D): {row['D']}")
        elif pd.notna(row['name']):
            wargear_list.append(f"\t{row['name']} Keywords: {row['description']} Range: {row['range']} "
                                f"Type: {row['type']} Attacks (A): {row['A']} BS or WS: {row['BS_WS']} Strength (S): {row['S']} "
                                f"AP: {row['AP']} Damage (D): {row['D']}")
    return '\n'.join(wargear_list)

def cleaner_helper(sheets):
    for col in sheets.columns:
        print(f"Checking column: {col} ({sheets[col].dtype})")
        if( sheets[col].dtype == 'str'):
            print(f"Cleaning {col}")
            sheets[col] = sheets[col].apply(clean_html_waha)
    return sheets

def ingest_datasheets(edition, chroma_client):
    output_file = open(ROOT / "data"/ "datasheets_text.txt", "w", encoding = "utf-8")
    
    data_path = ROOT / 'data' / 'wahapedia' / edition
    datasheets = pd.read_csv(data_path / 'datasheets.csv', sep='|', encoding = 'utf-8-sig')
    datasheets = datasheets.dropna(axis=1, how='all')
    
    datasheets_abilities = pd.read_csv(data_path / 'datasheets_abilities.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_keywords = pd.read_csv(data_path / 'datasheets_keywords.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_leader = pd.read_csv(data_path / 'datasheets_leader.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_models = pd.read_csv(data_path / 'datasheets_models.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_model_cost = pd.read_csv(data_path / 'datasheets_models_cost.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_options = pd.read_csv(data_path / 'datasheets_options.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_wargear = pd.read_csv(data_path / 'datasheets_wargear.csv', sep='|', encoding = 'utf-8-sig')
    
    abilities = pd.read_csv(data_path / 'abilities.csv', sep='|', encoding = 'utf-8-sig')
    factions = pd.read_csv(data_path / 'factions.csv', sep='|', encoding = 'utf-8-sig')
    
    datasheets = datasheets.merge(
        factions[['id', 'name']].rename(columns = {'id': 'faction_id', 'name': 'faction_name'}),
        on = "faction_id",
        how = "left"
    )
    
    datasheets = cleaner_helper(datasheets)
    datasheets_abilities = cleaner_helper(datasheets_abilities)
    datasheets_keywords = cleaner_helper(datasheets_keywords)
    datasheets_leader = cleaner_helper(datasheets_leader)
    datasheets_models = cleaner_helper(datasheets_models)
    datasheets_model_cost = cleaner_helper(datasheets_model_cost)
    datasheets_options = cleaner_helper(datasheets_options)
    datasheets_wargear = cleaner_helper(datasheets_wargear)
    abilities = cleaner_helper(abilities)
    
    
    
    documents = [] 
    metadatas = []
    ids = []
    
    
    for _, row in datasheets.iterrows():
        
        
        row_abilities = format_abilities(row['id'], datasheets_abilities, abilities, row['faction_id'])
        row_keywords = format_keywords(row['id'], datasheets_keywords)
        row_leader = format_leader(row['id'], datasheets_leader, datasheets)
        row_models = format_models(row['id'], datasheets_models)
        row_model_cost = format_cost(row['id'], datasheets_model_cost)
        row_options = format_options(row['id'], datasheets_options)
        row_wargear = format_wargear(row['id'], datasheets_wargear)
        
        document = f"""UNIT NAME: {row['name']}
ROLE: {row['role']}
FACTION: {row['faction_name']}
KEYWORDS: \n{row_keywords}
LOADOUT: {row['loadout']}
ABILITIES: \n {row_abilities}"""
        if row_leader:
            document += f"\nLEADER INFO:\n {row_leader}"
        document += f"""\nMODELS:\n{row_models}
MODEL COSTS: \n{row_model_cost}
WARGEAR OPTIONS: \n{row_options}
WARGEAR STATS: \n {row_wargear}
        """
            
        documents.append(document)
        metadatas.append({
            "source": "datasheets",
            "name": row['name'],
            "faction": str(row['faction_name']),
        })
        ids.append(f"datasheet_{row['id']}")
        output_file.write(document + "\n---\n")

    run_ingestion(f"wh40k_datasheets_{edition}", documents, metadatas, ids, chroma_client)
    output_file.close()
    print(f"Ingested {len(documents)} datasheets into ChromaDB")
    

    