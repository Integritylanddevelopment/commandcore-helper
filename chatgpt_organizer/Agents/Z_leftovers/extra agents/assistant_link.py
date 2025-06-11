# chatgpt_organizer/agents/assistant_link.py

import os
import json
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

STORE_PATH = Path("config/assistant_links.json")
STORE_PATH.parent.mkdir(parents=True, exist_ok=True)

def link_assistant(project_name, assistant_id, thread_id):
    print(f"[link] Linking project '{project_name}' to Assistant/Thread...")

    if STORE_PATH.exists():
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data[project_name] = {
        "assistant_id": assistant_id,
        "thread_id": thread_id
    }

    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[link] ✅ Linked and saved in {STORE_PATH}")

def get_link(project_name):
    if not STORE_PATH.exists():
        return None

    with open(STORE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get(project_name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--assistant", required=True)
    parser.add_argument("--thread", required=True)
    args = parser.parse_args()

    link_assistant(args.project, args.assistant, args.thread)
