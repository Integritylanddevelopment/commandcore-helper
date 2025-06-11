# chatgpt_organizer/plugins/content_indexer.py

import os
import json
from pathlib import Path
from datetime import datetime

def index_folder(folder):
    folder = Path(folder)
    if not folder.exists():
        print(f"[indexer] ❌ Invalid folder: {folder}")
        return

    index = {
        "project": folder.name,
        "path": str(folder),
        "timestamp": datetime.now().isoformat(),
        "files": [],
        "tags": [],
        "code_blocks": 0,
        "links": []
    }

    for root, _, files in os.walk(folder):
        for name in files:
            if name.endswith((".md", ".json", ".txt")):
                path = Path(root) / name
                try:
                    text = path.read_text(encoding="utf-8")
                    index["files"].append(str(path))
                    index["code_blocks"] += text.count("```")
                    index["links"].extend([word for word in text.split() if word.startswith("http")])
                    index["tags"].extend([word for word in text.split() if word.startswith("#")])
                except:
                    continue

    out = folder / "inventory.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print(f"[indexer] ✅ Inventory written to {out}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        index_folder(args.folder)
