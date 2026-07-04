import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "src" / "data" / "items" / "weapons" / "weapons.json"
bak = p.with_suffix('.json.bak')
if not bak.exists():
    print('Backup not found:', bak)
    raise SystemExit(1)

def load(path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)

cur = load(p)
old = load(bak)

# build lookup by (name, category) -> item
old_lookup = {}
for cat, items in old.items():
    if not isinstance(items, list):
        continue
    for it in items:
        key = (it.get('name'), it.get('category'))
        old_lookup[key] = it

changes = []
new_items = []
removed_items = []

for cat, items in cur.items():
    if not isinstance(items, list):
        continue
    for it in items:
        key = (it.get('name'), it.get('category'))
        prev = old_lookup.get(key)
        if prev is None:
            new_items.append((it['id'], it['name'], it['category']))
            continue
        # compare values for keys present in either
        all_keys = set(prev.keys()) | set(it.keys())
        item_changes = []
        for k in sorted(all_keys):
            v_prev = prev.get(k, '<MISSING>')
            v_cur = it.get(k, '<MISSING>')
            if v_prev != v_cur:
                item_changes.append((k, v_prev, v_cur))
        if item_changes:
            changes.append((prev.get('id'), it.get('id'), it.get('name'), it.get('category'), item_changes))

# detect removed items
cur_lookup = {(it.get('name'), it.get('category')) for cat, items in cur.items() if isinstance(items, list) for it in items}
for cat, items in old.items():
    if not isinstance(items, list):
        continue
    for it in items:
        key = (it.get('name'), it.get('category'))
        if key not in cur_lookup:
            removed_items.append((it.get('id'), it.get('name'), it.get('category')))

# print summary
print('Summary of changes:')
print('-', len(changes), 'items with differing values')
print('-', len(new_items), 'new items')
print('-', len(removed_items), 'removed items')

# print sample of changes
for prev_id, cur_id, name, cat, diffs in changes[:50]:
    print(f"\nItem: {name} ({cat}) prev_id={prev_id} cur_id={cur_id}")
    for k, vp, vc in diffs:
        print(f" - {k}: prev={vp!r} -> cur={vc!r}")

# If only differences are id and key order, still counts as change; filter if user wants
# Also produce JSON output
out = {'changes': [], 'new_items': new_items, 'removed_items': removed_items}
for prev_id, cur_id, name, cat, diffs in changes:
    out['changes'].append({'name': name, 'category': cat, 'prev_id': prev_id, 'cur_id': cur_id, 'diffs': [{'key':k, 'prev':vp, 'cur':vc} for k,vp,vc in diffs]})

print('\nJSON output (truncated):')
print(json.dumps(out, indent=2, ensure_ascii=False)[:2000])
