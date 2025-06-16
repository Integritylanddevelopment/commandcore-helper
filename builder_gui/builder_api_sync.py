import os
import json
import openai
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
print(f"Loaded API key: {API_KEY}")  # DEBUG LINE
openai.api_key = API_KEY


# === CONFIG ===
TASK_FILE = "../task.json"
RESPONSE_DIR = "response"
MODEL = "gpt-4o"  # or "gpt-4" / "gpt-3.5-turbo"
API_KEY = os.getenv("OPENAI_API_KEY")  # Put your key in .env or set manually
POLL_INTERVAL = 10  # seconds

# === INIT ===
openai.api_key = API_KEY
os.makedirs(RESPONSE_DIR, exist_ok=True)

def load_task():
    if os.path.exists(TASK_FILE):
        print("📥 Found task.json! Reading...")
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("👀 Still watching. No task.json found.")
    return None

def save_response(output, task_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{task_name}_{timestamp}.md"
    filepath = os.path.join(RESPONSE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"✅ Response saved to: {filepath}")

def query_gpt(task):
    messages = [
        {"role": "system", "content": task.get("system", "You are a helpful assistant.")},
        {"role": "user", "content": task["task"]}
    ]
    print(f"⏳ Sending task to GPT: {task['task'][:80]}...")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=task.get("temperature", 0.5),
        max_tokens=task.get("max_tokens", 1000)
    )
    return response['choices'][0]['message']['content']

def archive_task_file(task_file):
    archive_dir = "archived_tasks"
    os.makedirs(archive_dir, exist_ok=True)
    archive_path = os.path.join(archive_dir, os.path.basename(task_file))
    os.rename(task_file, archive_path)
    print(f"📦 Task file archived to: {archive_path}")

def main_loop():
    print("🧠 CommandCore Sync is live.")
    print(f"Watching for: {TASK_FILE}")
    while True:
        try:
            task = load_task()
            if task:
                result = query_gpt(task)
                save_response(result, task_name=task.get("name", "response"))
                archive_task_file(TASK_FILE)
                print("🎯 Task complete. Awaiting next.")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main_loop()
