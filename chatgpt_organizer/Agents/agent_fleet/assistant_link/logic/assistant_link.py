# chatgpt_organizer/agents/assistant_link.py

import os
import json
from dotenv import load_dotenv
from pathlib import Path
from agent_core import upgrade_agent_core, train_llm
import openai
from chatgpt_organizer.utils.agent_utils import batch_and_throttle_requests

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

    # Example OpenAI API integration
    try:
        response = batch_and_throttle_requests(
            lambda: openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant link bot."},
                    {"role": "user", "content": f"Link project '{project_name}' with assistant ID '{assistant_id}' and thread ID '{thread_id}'."}
                ]
            )
        )
        print("OpenAI Response:", response)
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")

    # Simulate linking logic
    data[project_name] = {"assistant_id": assistant_id, "thread_id": thread_id}
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    upgrade_agent_core()  # Upgrade the agent core after linking
    train_llm()  # Train the LLM after linking
    print("Linking complete.")

def upgrade_self():
    print("Upgrading assistant_link bot...")
    # Simulate upgrade logic
    print("assistant_link bot upgrade complete.")

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
