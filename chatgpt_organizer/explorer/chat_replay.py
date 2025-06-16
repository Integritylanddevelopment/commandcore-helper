import time
from pathlib import Path
import json

def replay_chat(chat_file, delay=1.0):
    path = Path(chat_file)
    if not path.exists() or not path.suffix == ".json":
        print(f"[REPLAY ERROR] Invalid chat file: {chat_file}")
        return

    print(f"\n-- Replaying: {path.name} --\n")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            messages = json.load(f)

        for msg in messages:
            role = msg.get("role", "UNKNOWN").upper()
            content = msg.get("content", "").strip()
            print(f"{role}: {content}\n")
            time.sleep(delay)

    except Exception as e:
        print(f"[REPLAY ERROR] Could not load chat: {e}")
