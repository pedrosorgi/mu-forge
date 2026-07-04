import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "src" / "data" / "items" / "weapons" / "weapons.json"
bak = p.with_suffix('.json.bak')

def load(path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)

cur = load(p)
if not bak.exists():
    print('Backup not found:', bak)
    raise SystemExit(1)
old = load(bak)

# build lookup by (name, category) -> item
old_lookup = {}
for cat, items in old.items():
    if not isinstance(items, list):
        continue
    for it in items:
        key = (it.get('name'), it.get('category'))
        old_lookup[key] = it

results = []

for cat, items in cur.items():
    if not isinstance(items, list):
        continue
    for it in items:
        key = (it.get('name'), it.get('category'))
        prev = old_lookup.get(key)
        if prev is None:
            # new item, check if requirements are default (all null)
            req = it.get('requirements', {})
            if all(v is None for v in req.values()):
                results.append((it['id'], it['name'], it['category'], 'new_item_default_requirements'))
            continue
        # prev exists: check if prev had requirements key
        if 'requirements' not in prev:
            results.append((it['id'], it['name'], it['category'], 'previously_missing'))
        else:
            # prev had requirements; check if all were null or some had values
            prev_req = prev.get('requirements') or {}
            cur_req = it.get('requirements') or {}
            if all(v is None for v in prev_req.values()) and not all(v is None for v in cur_req.values()):
                results.append((it['id'], it['name'], it['category'], 'previously_all_null_now_populated'))
            elif all(v is None for v in cur_req.values()) and not all(v is None for v in prev_req.values()):
                results.append((it['id'], it['name'], it['category'], 'now_all_null_but_prev_had_values'))

# print results sorted by id
results.sort()
print(f'Found {len(results)} items that likely received default requirements or had notable changes:')
for r in results:
    print('-', r)

# also print a compact JSON
out = [{'id':r[0],'name':r[1],'category':r[2],'reason':r[3]} for r in results]
print('\nJSON output:')
print(json.dumps(out, indent=2, ensure_ascii=False))
