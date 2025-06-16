# chatgpt_organizer/plugins/auto_summary.py

import os
import openai
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(folder):
    chat_path = Path(folder) / "chat.md"
    summary_path = Path(folder) / "README.md"

    if not chat_path.exists():
        print(f"[auto_summary] ❌ chat.md not found in {folder}")
        return

    with open(chat_path, "r", encoding="utf-8") as f:
        chat_content = f.read()

    prompt = f"""
You are a summarization assistant. Summarize the following conversation clearly, highlight key topics, and keep it structured. Use Markdown.

Conversation:
---
{chat_content}
---
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        summary = response.choices[0].message.content.strip()

        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"[auto_summary] ✅ Summary saved to {summary_path}")

    except Exception as e:
        print(f"[auto_summary] ❌ Error: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        generate_summary(args.folder)
