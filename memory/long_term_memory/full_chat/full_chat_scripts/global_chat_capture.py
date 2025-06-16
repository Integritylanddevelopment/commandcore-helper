#!/usr/bin/env python3

import pyautogui
import pyperclip
import time
import os
import subprocess
import keyboard
from datetime import datetime
import pygetwindow as gw

# === CONFIG ===
output_dir = r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/full_chat/full_chat_logs"
summary_script = r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/logs/summary/summary_scripts/summary.py"
tags = ["global_hotkey_capture"]

def scroll_to_top_fast():
    print("⬆ Scrolling to top at high speed...")
    for _ in range(60):
        pyautogui.scroll(2000)
        time.sleep(0.05)

def get_window_title():
    win = gw.getActiveWindow()
    title = win.title if win else "unknown"
    return title, title.split()[0].lower()

def capture_chat():
    scroll_to_top_fast()
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)
    return pyperclip.paste().strip()

def save_markdown(text, source_name, window_title):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Generate a shorter alphabetical filename
    filename = f"log_{chr(97 + (int(timestamp.replace('-', '').replace(':', '').replace('_', '')) % 26))}.md"
    output_path = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)
    token_count = len(text.split())

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"source: {source_name}\n")
        f.write(f"timestamp: {timestamp.replace('_', ' ')}\n")
        f.write(f"window_title: {window_title}\n")
        f.write("vector_ready: true\n")
        f.write(f"tags: {tags}\n")
        f.write("---\n\n")
        f.write("# Captured AI Chat Log\n\n")
        f.write(text + "\n\n")
        f.write(f"---\nEstimated Token Count: {token_count}\n")

    print(f"✅ Chat saved: {output_path}")
    return output_path

def run_summary():
    print("🧠 Running summary script...")
    subprocess.run(["python", summary_script])

def on_hotkey_triggered():
    print("📌 Hotkey pressed! Capturing chat...")
    pyautogui.click()
    window_title, source_name = get_window_title()
    text = capture_chat()
    save_markdown(text, source_name, window_title)
    run_summary()

def main():
    print("🔁 Waiting for Ctrl + Alt + C to capture chat...")
    keyboard.add_hotkey("ctrl+alt+c", on_hotkey_triggered)
    keyboard.wait()

if __name__ == "__main__":
    main()
