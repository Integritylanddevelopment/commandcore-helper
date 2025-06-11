import os
import shutil
from pathlib import Path
from datetime import datetime
from configparser import ConfigParser

# === Load settings ===
config = ConfigParser()
config.read("config/settings.ini")
RAW_PATH = Path("data/raw_chats")
ORG_PATH = Path(config.get("paths", "data_path", fallback="data/organized"))
LOG_PATH = Path(config.get("paths", "log_path", fallback="logs"))

def sync_chats():
    print("[sync] 🔄 Starting sync...")
    ORG_PATH.mkdir(parents=True, exist_ok=True)
    LOG_PATH.mkdir(parents=True, exist_ok=True)

    for file in RAW_PATH.glob("*.*"):
        if file.suffix not in [".json", ".md"]:
            continue

        # Extract parts from filename: project__session.ext (e.g., blog__call1.json)
        parts = file.stem.split("__")
        project = parts[0] if len(parts) > 1 else "default_project"
        session = parts[1] if len(parts) > 1 else datetime.now().strftime("%Y%m%d_%H%M%S")

        # Build full target path
        target_dir = ORG_PATH / project / session
        target_dir.mkdir(parents=True, exist_ok=True)

        # Rename file to standard chat.md/json
        target_name = "chat.md" if file.suffix == ".md" else "chat.json"
        shutil.move(str(file), target_dir / target_name)

        # Log it
        with open(LOG_PATH / "sync.log", "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now()}] Moved {file.name} → {target_dir / target_name}\n")

    print("[sync] ✅ Sync complete.")

if __name__ == "__main__":
    sync_chats()
