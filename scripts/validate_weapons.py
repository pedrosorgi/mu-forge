from collections import OrderedDict
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "src" / "data" / "items" / "weapons" / "weapons.json"
with p.open('r', encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)
# find canonical keys from swords
canonical_keys = list(data['swords'][0].keys())
# gather ids and check keys
ids = []
missing_keys = []
key_order_issues = []
counts = {}
for category, items in data.items():
    if isinstance(items, list):
        counts[category] = len(items)
        for it in items:
            ids.append(it.get('id'))
            # check keys presence
            for k in canonical_keys:
                if k not in it:
                    missing_keys.append((it.get('id'), k))
            # check key order
            keys = list(it.keys())
            if keys[:len(canonical_keys)] != canonical_keys:
                key_order_issues.append(it.get('id'))
# checks
ids_sorted = sorted(ids)
unique_ids = len(set(ids)) == len(ids)
continuous = ids_sorted == list(range(1, len(ids_sorted)+1))
print('Total items:', len(ids))
print('Per-category counts:', counts)
print('Unique ids:', unique_ids)
print('Continuous sequence from 1:', continuous)
print('Any missing keys:', missing_keys[:5])
print('Key order issues (sample):', key_order_issues[:10])

if not unique_ids or not continuous or missing_keys or key_order_issues:
    print('VALIDATION FAILED')
    raise SystemExit(1)
print('VALIDATION OK')
