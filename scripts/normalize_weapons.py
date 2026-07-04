#!/usr/bin/env python3
from collections import OrderedDict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "src" / "data" / "items" / "weapons" / "weapons.json"
if not p.exists():
    print('File not found:', p)
    sys.exit(1)
# load preserving order
with p.open('r', encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)
if 'swords' not in data or not data['swords']:
    print('No swords entries found to extract schema')
    sys.exit(1)
# canonical keys from first sword
canonical_keys = list(data['swords'][0].keys())
print('Canonical keys:', canonical_keys)
# backup
bak = p.with_suffix('.json.bak')
with bak.open('w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
# normalize
new_data = OrderedDict()
new_id = 1
for category, items in data.items():
    if not isinstance(items, list):
        new_data[category] = items
        continue
    new_items = []
    for item in items:
        new_item = OrderedDict()
        for k in canonical_keys:
            if k == 'id':
                new_item['id'] = new_id
                new_id += 1
            else:
                if k in item:
                    new_item[k] = item[k]
                else:
                    if k == 'requirements':
                        new_item[k] = OrderedDict([('str',None),('agi',None),('ene',None),('cmd',None),('char_level',None)])
                    elif k == 'base_stats':
                        new_item[k] = OrderedDict([('min_atk_dmg',None),('max_atk_dmg',None),('wiz_dmg_percent',None),('atk_speed',None)])
                    elif k == 'classes':
                        new_item[k] = []
                    else:
                        new_item[k] = None
        # include any extra keys that some items may have, preserving their order
        for k, v in item.items():
            if k not in canonical_keys:
                new_item[k] = v
        new_items.append(new_item)
    new_data[category] = new_items
# write back
with p.open('w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
# validation
ids = []
for items in new_data.values():
    if isinstance(items, list):
        for it in items:
            ids.append(it['id'])
ids_sorted = sorted(ids)
continuity = ids_sorted == list(range(1, len(ids_sorted)+1))
print(f'Processed {len(ids)} items. IDs continuous from 1: {continuity}')
print('First 10 IDs:', ids_sorted[:10])
# show sample first item to verify order
sample = None
for items in new_data.values():
    if isinstance(items, list) and items:
        sample = items[0]
        break
print('Sample first item keys:', list(sample.keys()))
print('Done')
