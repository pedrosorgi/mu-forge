# MU Forge

Structured JSON database of **MU Online** official game items — weapons, shields, classes, and rules normalized for programmatic use.

> **Project status:** Paused / archived as a portfolio dataset. No API or website is shipped in this repository.

## What is this?

MU Forge is a fan-made data project started in December 2025. The goal was to document official MU Online item and class data in a consistent, machine-readable format.

This repository contains:

- **Item databases** (`src/data/items/`) — weapons, shields, sets, accessories, and more
- **Class metadata** (`src/data/classes/`) — class info and evolution data
- **Game rules** (`src/data/rules/`) — shared rules for items and classes
- **Maintenance scripts** (`scripts/`) — validation, normalization, and scraping helpers

## Data coverage

### Populated

| Path | Description |
|------|-------------|
| `src/data/items/weapons/weapons.json` | Main weapon catalog |
| `src/data/items/weapons/ruud_weapons.json` | Ruud shop weapons |
| `src/data/items/weapons/socket_weapons.json` | Socket weapons |
| `src/data/items/weapons/divine_weapons.json` | Divine weapons |
| `src/data/items/shields/shields.json` | Standard shields |
| `src/data/items/shields/ruud_shields.json` | Ruud shields |
| `src/data/classes/class_info.json` | Playable classes |
| `src/data/classes/class_evolution.json` | Class evolution paths |
| `src/data/rules/items_rules.json` | Item-related rules |
| `src/data/rules/class_rules.json` | Class-related rules |

### Placeholders (empty, reserved for future work)

Categories such as ancient/socket/ruud set pieces, wings, pets, jewels, rings, earrings, pendants, skills, and socket shields have file stubs under `src/data/` but no data yet.

Run `python scripts/smoke_load_jsons.py` to see the full list.

## Item schema (example)

```json
{
  "id": 1,
  "img": "small_axe.png",
  "slug": "small-axe",
  "internal_id": "small_axe",
  "name": "Small Axe",
  "category": "axe",
  "subcategory": null,
  "equip_location": "primary_hand",
  "requirements": {
    "str": 21,
    "agi": null,
    "ene": null,
    "cmd": null,
    "char_level": null
  },
  "base_stats": {
    "min_atk_dmg": 2,
    "max_atk_dmg": 7,
    "atk_speed": 20
  },
  "classes": [{ "class_id": "all", "min_evo": 1 }],
  "rarity": "normal",
  "allowed_options": {
    "excellent": "atk_weapons",
    "luck": true,
    "joh": true,
    "jol": true,
    "socket": false,
    "ancient": false
  }
}
```

Excellent variants may include a `base_item` field pointing to the normal version.

## Project structure

```
mu-forge/
├── src/data/
│   ├── classes/
│   ├── items/
│   │   ├── weapons/
│   │   ├── shields/
│   │   ├── set_items/
│   │   └── other/
│   └── rules/
├── scripts/
├── docs/
├── LICENSE
└── requirements.txt
```

## Scripts

```bash
pip install -r requirements.txt
python scripts/smoke_load_jsons.py
```

Other scripts in `scripts/` were used during manual curation. Review each file before running — some modify data files or expect local backups.

## License

**All rights reserved.** See [LICENSE](LICENSE).

This repository is provided for **viewing, study, and evaluation** of structure and organization only. Redistribution, commercial use, and building derivative products from the database are **not permitted** without explicit written permission from the author.

## Disclaimer

This is an independent, fan-made project. **MU Online** and related trademarks are property of their respective owners. This project is not affiliated with, endorsed by, or sponsored by Webzen or any other rights holder.
