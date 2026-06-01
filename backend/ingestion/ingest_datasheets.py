#This is going to be a doozy, Datasheet information is split across multiple files.
import pandas as pd
from backend.util.clean_html import clean_html_waha
from backend.ingestion.base_ingest import run_ingestion
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
output_file = open(ROOT / "data"/ "datasheets_text.txt", "w", encoding = "utf-8")

def format_abilities(datasheet_id, datasheets_abilities, abilities):
    unit_abilities = datasheets_abilities[datasheets_abilities['datasheet_id'] == datasheet_id]
    
    core = [] 
    faction = []
    datasheet = []
    
    for _, row in unit_abilities.iterrows():
        a_type = row['type']
        
        if a_type =='Core':
            match  = abilities[abilities['id'] == row['ability_id']]
            if not match.empty:
                core.append(match.iloc[0]['name'])
        elif a_type == 'Faction':
            match = abilities[abilities['id'] == row['ability_id']] & (abilities['faction_id'] == row['faction_id'])
            if not match.empty:
                faction.append(match.iloc[0]['name'])
        elif a_type == 'Datasheet':
            name = row['name'] if pd.notna(row['name']) else 'Unknown'
            desc = row['description'] if pd.notna(row['description']) else 'Description Unavailable'
            datasheet.append(f"{name}: {desc}")
    
    
    parts = []
    if core:
        parts.append(f"Core Abilities: {', '.join(core)}")
    if faction:
        parts.append(f"Faction Abilities: {', '.join(faction)}")
    if datasheet:
        parts.append("Unit Abilities:\n" + '\n'.join(f"  - {a}" for a in datasheet))
    
    return '\n'.join(parts)
 

def format_keywords(datasheet_id, keywords):
    unit_keywords = keywords[keywords['datasheet_id']== datasheet_id & (pd.notna(keywords['keyword']))]
    keyword_list = []
    for _, row in unit_keywords.iterrows():
        if pd.notna(row['model']) and str(row['model']).strip():
            keyword_list.append(f"{row['keyword']} ({row['model']})")
        else:
            keyword_list.append(row['keyword'])
    
    return '\n'.join(keyword_list)


def format_leader(datasheet_id, ds_leader, datasheets):
    leader_info = ds_leader[ds_leader['leader_id'] == datasheet_id]
    
    can_lead =[]
    if not leader_info.empty:
        for _, row in leader_info.iterrows():
            match = datasheets[datasheets['id'] == row['attached_id']]
            if not match.empty:
                unit_name = match.iloc[0]['name']
                can_lead.append(unit_name)
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
            f"{rows['name']}: "
            f"Movement (M):{rows['M']} Toughness (T):{rows['T']} Armor Save (Sv):{rows['Sv']} "
            f"Wounds (W):{rows['W']} Invulnerable Save: {invul} {invul_Cond} "
            f"Leadership (Ld):{rows['Ld']} Objective Control (OC):{rows['OC']}"
            ).strip()
        statlines.append(model)
    return '\n'.join(statlines)
  
    
    
    
def ingest_datasheets(edition, chroma_client):
    data_path = ROOT / 'data' / 'wahapedia' / edition
    datasheets = pd.read_csv(data_path / 'datasheets.csv', sep='|', encoding = 'utf-8-sig')
    datasheets = datasheets.dropna(axis=1, how='all')
    
    datasheets_abilities = pd.read_csv(data_path / 'datasheets_abilities.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_enhancements = pd.read_csv(data_path / 'datasheets_enchantments.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_keywords = pd.read_csv(data_path / 'datasheets_keywords.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_leader = pd.read_csv(data_path / 'datasheets_leader.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_models = pd.read_csv(data_path / 'datasheets_models.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_model_cost = pd.read_csv(data_path / 'datasheets_model_cost.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_options = pd.read_csv(data_path / 'datasheets_options.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_unit_composition = pd.read_csv(data_path / 'datasheets_unit_composition.csv', sep='|', encoding = 'utf-8-sig')
    datasheets_wargear = pd.read_csv(data_path / 'datasheets_wargear.csv', sep='|', encoding = 'utf-8-sig')
    
    abilities = pd.read_csv(data_path / 'abilities.csv', sep='|', encoding = 'utf-8-sig')
    enhancements = pd.read_csv(data_path / 'enhancements.csv', sep='|', encoding = 'utf-8-sig')
    factions = pd.read_csv(data_path / 'factions.csv', sep='|', encoding = 'utf-8-sig')
    
    datasheets = datasheets.merge(
        factions[['id', 'name']].rename(columns = {'id': 'faction_id', 'name': 'faction_name'}),
        on = "faction_id",
        how = "left"
    )
    
    for _, row in datasheets.iterrows():
        row_abilities = format_abilities(row['id'], datasheets_abilities, abilities)
        row_keywords = format_keywords(row['id'], datasheets_keywords)
        row_leader = format_leader(row['id'], datasheets_leader, datasheets)
        row_models = format_models(row['id'], datasheets_models)
        
    
        
        
    