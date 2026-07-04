from pathlib import Path
import json

# pasta raiz do projeto (MU-FORGE)
ROOT_DIR = Path(__file__).resolve().parent.parent

# caminhos
WEAPONS_JSON_PATH = (
    ROOT_DIR
    / "src"
    / "data"
    / "items"
    / "weapons"
    / "ruud_weapons.json"
)

OUTPUT_FILE = (
    ROOT_DIR
    / "src"
    / "data"
    / "items"
    / "weapons"
    / "weapons_migrated.json"
)

print("Lendo:", WEAPONS_JSON_PATH)

with open(WEAPONS_JSON_PATH, encoding="utf-8") as f:
    weapons_data = json.load(f)

# ---- MIGRAÇÃO ----
for category, items in weapons_data.items():
    for item in items:

        # 1. Rarity
        item["rarity"] = "excellent" if item.get("excellent_option") else "normal"

        # 2. Allowed options
        item["allowed_options"] = {
            "excellent": True,
            "luck": item.get("luck_option", False),
            "joh": item.get("joh_option", False),
            "jol": item.get("jol_option", False),
        }

        # 3. Remover flags antigas
        item.pop("excellent_option", None)
        item.pop("luck_option", None)
        item.pop("joh_option", None)
        item.pop("jol_option", None)

        # 4. Limpar base_stats nulos
        base_stats = item.get("base_stats", {})
        item["base_stats"] = {
            k: v for k, v in base_stats.items() if v is not None
        }

        if item.get("one_handed") is True:
            item["equip_location"] = "primary_hand"
        elif item.get("one_handed") is False:
            item["equip_location"] = "both_hands"
        else:
            item["equip_location"] = "secondary_hand"

        item.pop("one_handed", None)

# Classes: name -> class_id
        for cls in item.get("classes", []):
            if "name" in cls:
                cls["class_id"] = cls.pop("name")

# ---- SALVAR UMA VEZ ----
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(weapons_data, f, indent=2, ensure_ascii=False)

print("Migração concluída com sucesso 🚀")
print("Arquivo gerado em:", OUTPUT_FILE)
