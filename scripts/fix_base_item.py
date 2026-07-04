#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "src" / "data" / "items" / "weapons" / "weapons.json"
if not p.exists():
    print('File not found:', p)
    exit(1)

with p.open('r', encoding='utf-8') as f:
    data = json.load(f)

# Function to convert hyphen to underscore
def to_snake_case(s):
    return s.replace('-', '_')

# Update base_item in all items
for category, items in data.items():
    if isinstance(items, list):
        for item in items:
            if 'base_item' in item:
                item['base_item'] = to_snake_case(item['base_item'])

# Write back
with p.open('w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Updated base_item fields to snake_case.')