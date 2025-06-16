import os
from pathlib import Path
import json

def show_preview(item_path):
    path = Path(item_path)
    if not path.exists():
        print(f"[PREVIEW] Item not found: {item_path}")
        return

    if path.is_dir():
        readme = path / 'README.md'
        if readme.exists():
            print(f"\n--- README for {path.name} ---\n")
            print(readme.read_text(encoding="utf-8"))
        else:
            print(f"[PREVIEW] No README found in: {path}")
    elif path.is_file() and path.suffix == '.json':
        print(f"\n--- Preview: {path.name} ---\n")
        with open(path, 'r', encoding='utf-8') as f:
            messages = json.load(f)
            for msg in messages[:5]:
                role = msg.get("role", "unknown").upper()
                content = msg.get("content", "")[:100]
                print(f"{role}: {content}...\n")
    else:
        print(f"[PREVIEW] Unsupported file type: {path}")
