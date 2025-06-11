import os
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# === Configuration ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PROJECT_NAME = "gpt_project"
SESSION_NAME = datetime.now().strftime("%Y%m%d_%H%M%S")
DATA_PATH = Path("data/organized") / PROJECT_NAME / SESSION_NAME
DATA_PATH.mkdir(parents=True, exist_ok=True)

# === Prompt ===
messages = [
    {"role": "system", "content": "You are CommandCoreOS. Respond clearly and intelligently."},
    {"role": "user", "content": "Summarize the goal of CommandCore OS and its agent system."}
]

def run():
    print("[gpt_sync] 🔄 Connecting to GPT API...")

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )

        content = response.choices[0].message.content
        out_path = DATA_PATH / "chat.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[gpt_sync] ✅ Saved GPT response to {out_path}")

    except Exception as e:
        print(f"[gpt_sync] ❌ Error: {e}")

if __name__ == "__main__":
    run()
