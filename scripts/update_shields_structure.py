#!/usr/bin/env python3
import json
from pathlib import Path
from collections import OrderedDict
import re

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "src" / "data" / "items" / "shields" / "shields.json"
if not p.exists():
    print('File not found:', p)
    exit(1)

with p.open('r', encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)

def to_snake_case(s):
    # Convert PascalCase or camelCase to snake_case
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()

def to_hyphen_case(s):
    return s.replace('_', '-').replace(' ', '-')

for item in data['shields']:
    name = item['name']
    is_excellent = 'excellent' in name.lower()

    # base_name: remove "Excellent " if present
    base_name = name.replace('Excellent ', '') if is_excellent else name

    # img: from img_path if exists, else keep
    if 'img_path' in item:
        img_filename = item['img_path'].split('/')[-1]
        item['img'] = img_filename
        del item['img_path']

    # slug
    slug_base = base_name.lower().replace(' ', '-')
    item['slug'] = f"excellent-{slug_base}" if is_excellent else slug_base

    # base_item
    item['base_item'] = base_name.lower().replace(' ', '_')

    # internal_id
    item['internal_id'] = f"excellent_{item['base_item']}" if is_excellent else item['base_item']

    # classes
    for cls in item['classes']:
        cls['class_id'] = to_snake_case(cls['class_id'])

    # allowed_options
    item['allowed_options']['excellent'] = "shields"

    # Reorder keys to match weapons.json
    ordered_item = OrderedDict()
    key_order = ['id', 'img', 'slug', 'base_item', 'internal_id', 'name', 'category', 'equip_location', 'requirements', 'base_stats', 'classes', 'rarity', 'allowed_options']
    for key in key_order:
        if key in item:
            ordered_item[key] = item[key]
    # Add any extra keys not in the order
    for key, value in item.items():
        if key not in ordered_item:
            ordered_item[key] = value
    # Replace the item
    data['shields'][data['shields'].index(item)] = ordered_item

# Write back
with p.open('w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Updated all shield items to match the structure and key order of weapons.json.')