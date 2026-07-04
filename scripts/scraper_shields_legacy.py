import requests
from bs4 import BeautifulSoup
import json
import time
import urllib.parse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Lista de shields socket
shields = [
    "Salamander Shield",
    "Guardian Shield",
    "Frost Barrier",
    "Grace Shield",
    "Crimson Glory",
    "Constant Shield",
    "Dark Devil Shield",
    "Light Lord Shield",
    "Ambition Shield",
    "Magic Knight Shield",
    "Lazy Wind Shield"
]

BASE_URL = "https://muonlinefanz.com/tools/items/data/itemdb/"

# Mapeamento de classes
CLASS_MAP = {
    "Dark Knight": "dark_knight",
    "Dark Wizard": "dark_wizard",
    "Fairy Elf": "fairy_elf",
    "Rune Mage": "rune_wizard",
    "Magic Gladiator": "magic_gladiator",
    "Dark Lord": "dark_lord",
    "Grow Lancer": "grow_lancer",
    "Lemuria": "lemuria",
    "Summoner": "summoner",
    "Rage Fighter": "rage_fighter",
    "Slayer": "slayer",
    "Gun Crusher": "gun_crusher",
    "White Wizard": "white_wizard",
    "Mage": "white_wizard",
    "BM": "blade_master",
    "FM": "fist_master",
    "DM": "dark_master",
    "SM": "soul_master",
    "MG": "magic_gladiator",
    "GL": "grow_lancer",
}

def extract_shield_data(name):
    """Extrai dados de um shield socket"""
    
    url_name = urllib.parse.quote(name)
    url = f"{BASE_URL}{url_name}.php"
    
    print(f"Acessando: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Verifica se é socket (span class="soc")
        soc_span = soup.find('span', class_='soc')
        if not soc_span:
            print(f"  ⚠ {name} NÃO é socket - pulando")
            return None
        
        # Extrai o nome do <text-subtitle>
        title = soup.find('text-subtitle')
        exact_name = title.text.strip() if title else name
        
        # Encontra a seção de detalhes (div com "Item details...")
        item_details_div = None
        for div in soup.find_all('div', id='col3'):
            if div.find('em') and 'Item details...' in div.find('em').text:
                item_details_div = div
                break
        
        if not item_details_div:
            print(f"  ❌ Não encontrou seção 'Item details...'")
            return None
        
        # Pega o texto completo da seção
        details_text = item_details_div.get_text(separator='\n')
        print(f"  DEBUG - Primeiros 300 caracteres: {details_text[:300]}")
        
        # Extrai DEF
        def_match = re.search(r'DEF:\s*\+?(\d+)', details_text)
        defense = int(def_match.group(1)) if def_match else None
        
        # Extrai DEF Rate
        def_rate_match = re.search(r'DEF Rate:\s*\+?(\d+)', details_text)
        def_rate = int(def_rate_match.group(1)) if def_rate_match else None
        
        # Extrai requisitos
        str_match = re.search(r'Strength:\s*(\d+)', details_text)
        str_req = int(str_match.group(1)) if str_match else None
        
        agi_match = re.search(r'Agility:\s*(\d+)', details_text)
        agi_req = int(agi_match.group(1)) if agi_match else None
        
        # Extrai level requirement
        level_match = re.search(r'Character Level\s*(\d+)', details_text)
        char_level = int(level_match.group(1)) if level_match else None
        
        # Extrai classes - procura por "Can be equipped by"
        classes = []
        equip_match = re.search(r'Can be equipped by\s*(.*?)$', details_text, re.MULTILINE)
        if equip_match:
            classes_text = equip_match.group(1)
            # Remove colchetes e separa por vírgula
            classes_text = classes_text.replace('[', '').replace(']', '')
            # Divide por vírgula
            class_names = [c.strip() for c in classes_text.split(',')]
            
            for class_name in class_names:
                if class_name in CLASS_MAP:
                    classes.append({
                        "class_id": CLASS_MAP[class_name],
                        "min_evo": 1
                    })
        
        # Se não encontrou classes, usa as classes conhecidas do HTML
        if not classes:
            # Procura no HTML por links ou texto de classes
            for class_display, class_id in CLASS_MAP.items():
                if class_display in details_text:
                    classes.append({
                        "class_id": class_id,
                        "min_evo": 1
                    })
        
        # Extrai número máximo de sockets
        soc_section = soup.find('span', class_='soc')
        max_sockets = 3  # default
        if soc_section and soc_section.parent:
            soc_text = soc_section.parent.get_text()
            soc_match = re.search(r'x(\d+)\s*max', soc_text)
            if soc_match:
                max_sockets = int(soc_match.group(1))
        
        # Verifica options adicionais
        options_section = soup.find('div', id='full_col', class_='textcenter')
        options_text = options_section.get_text() if options_section else ""
        
        has_luck = 'Luck option' in options_text
        has_jol = 'Jewel of Life' in options_text
        has_joh = 'Jewel of Harmony' in options_text
        
        # Monta o JSON
        item_data = {
            "id": None,
            "img": f"{exact_name.lower().replace(' ', '_')}.png",
            "slug": exact_name.lower().replace(' ', '-'),
            "internal_id": exact_name.lower().replace(' ', '_'),
            "name": exact_name,
            "category": "shield",
            "subcategory": "socket_shield",
            "equip_location": "secondary_hand",
            "requirements": {
                "str": str_req,
                "agi": agi_req,
                "ene": None,
                "cmd": None,
                "char_level": char_level
            },
            "base_stats": {
                "def": defense,
                "def_rate": def_rate,
                "max_sockets": max_sockets
            },
            "classes": classes,
            "rarity": "socket",
            "allowed_options": {
                "excellent": False,
                "luck": has_luck,
                "joh": has_joh,
                "jol": has_jol,
                "socket": True,
                "ancient": False
            }
        }
        
        print(f"  ✅ {exact_name}: DEF={defense}, DEF Rate={def_rate}, STR={str_req}, AGI={agi_req}, Level={char_level}")
        return item_data
        
    except Exception as e:
        print(f"  ❌ Erro ao acessar {name}: {e}")
        import traceback
        traceback.print_exc()
        return None

# Executar scraping
results = []
for i, shield_name in enumerate(shields, 1):
    print(f"\n[{i}/{len(shields)}] Processando: {shield_name}")
    data = extract_shield_data(shield_name)
    if data:
        results.append(data)
    time.sleep(1.5)  # Respeitar o servidor

# Adicionar IDs
for idx, item in enumerate(results, 1):
    item['id'] = idx

# Salvar JSON
output_file = ROOT / "src" / "data" / "items" / "shields" / "socket_shields.json"
payload = {"socket_shields": results}
with output_file.open("w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

print(f"\n✅ {len(results)} shields socket salvos em {output_file}")