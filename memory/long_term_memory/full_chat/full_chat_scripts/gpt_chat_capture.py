import pyautogui
import pyperclip
import time
import os
import subprocess
import argparse
from datetime import datetime
import pygetwindow as gw

# === CONFIG ===
output_dir = r"D:\ActiveProjects\CommandCore-Hub_v2025.01.01\memory\full_chat\full_chat_logs"
summary_script = r"D:\ActiveProjects\CommandCore-Hub_v2025.01.01\memory\logs\summary\summary_scripts\summary.py"

# === CLI ARGUMENTS ===
parser = argparse.ArgumentParser()
parser.add_argument("--summary", action="store_true", help="Run summarizer after capture")
args = parser.parse_args()

# === Default tags (no prompt)
tag_list = ["auto_capture"]

# === Window info after click
def get_source_window_title():
    active_win = gw.getActiveWindow()
    title = active_win.title if active_win else "unknown"
    return title, title.split()[0].lower()

# === Confirm and capture
print("🖱 Click the chat window you want to capture... waiting 1 second.")
time.sleep(1)
pyautogui.click()

window_title = "manual"
source_name = "copilot"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"full_chat_log_{source_name}_{timestamp}.md"
filename = filename.replace(":", "-").replace("\\", "-").replace("/", "-")
output_path = os.path.join(output_dir, filename)

def capture_full_chat():
    pyautogui.hotkey("ctrl", "home")
    time.sleep(1.2)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)
    return pyperclip.paste().strip()

def estimate_tokens(text):
    return len(text.split())

def write_markdown(text):
    os.makedirs(output_dir, exist_ok=True)
    token_count = estimate_tokens(text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"source: {source_name}\n")
        f.write(f"timestamp: {timestamp.replace('_', ' ')}\n")
        f.write(f"window_title: {window_title}\n")
        f.write("vector_ready: true\n")
        f.write(f"tags: {tag_list}\n")
        f.write("---\n\n")
        f.write("# Captured AI Chat Log\n\n")
        f.write(text + "\n\n")
        f.write(f"---\nEstimated Token Count: {token_count}\n")

    print(f"✅ Log saved: {output_path}")

def run_summary():
    print("🧠 Running summary script...")
    subprocess.run(["python", summary_script])

if __name__ == "__main__":
    full_text = capture_full_chat()
    write_markdown(full_text)
    if args.summary:
        run_summary()
