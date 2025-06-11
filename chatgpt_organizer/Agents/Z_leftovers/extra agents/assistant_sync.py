# chatgpt_organizer/agents/assistant_sync.py

import os
import openai
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_PATH = Path("data/organized")

def pull_assistant_chat(thread_id, project_name="gpt_imports", chat_name="chat_from_gpt"):
    if not thread_id or not openai.api_key:
        print("[sync] ❌ Missing thread_id or API key.")
        return

    print(f"[sync] 🧠 Pulling thread: {thread_id}")
    try:
        response = openai.beta.threads.messages.list(thread_id=thread_id)
        messages = response.data[::-1]  # most recent last

        folder = DATA_PATH / project_name / chat_name
        folder.mkdir(parents=True, exist_ok=True)

        out_path = folder / "chat.md"
        with open(out_path, "w", encoding="utf-8") as f:
            for msg in messages:
                role = msg.role.upper()
                content = msg.content[0].text.value.strip()
                f.write(f"**{role}**:\n{content}\n\n")

        print(f"[sync] ✅ Chat saved to: {out_path}")

    except Exception as e:
        print(f"[sync] ❌ Error: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--thread", required=True, help="OpenAI thread_id to sync")
    parser.add_argument("--project", default="gpt_imports")
    parser.add_argument("--chat", default="chat_from_gpt")
    args = parser.parse_args()

    pull_assistant_chat(args.thread, args.project, args.chat)
