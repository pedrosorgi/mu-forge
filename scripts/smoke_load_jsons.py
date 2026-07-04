import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "src" / "data"

errors = []
empty_files = []

for path in sorted(DATA_DIR.rglob("*.json")):
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        empty_files.append(path.relative_to(ROOT))
        continue
    try:
        json.load(path.open("r", encoding="utf-8"))
    except Exception as exc:
        errors.append((path.relative_to(ROOT), str(exc)))

total = len(errors) + len(empty_files) + sum(
    1 for p in DATA_DIR.rglob("*.json") if p.read_text(encoding="utf-8").strip()
)

print(f"Checked {sum(1 for _ in DATA_DIR.rglob('*.json'))} JSON files")

if empty_files:
    print(f"\nEmpty placeholders ({len(empty_files)}):")
    for path in empty_files:
        print(f"  - {path}")

if errors:
    print("\nInvalid JSON:")
    for path, message in errors:
        print(f"  - {path}: {message}")
    raise SystemExit(1)

if empty_files:
    print("\nNote: empty placeholders are reserved for future categories.")

print("All non-empty JSON files loaded successfully.")
