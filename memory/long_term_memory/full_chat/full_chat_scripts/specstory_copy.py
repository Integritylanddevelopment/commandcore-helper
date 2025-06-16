#!/usr/bin/env python3

import os
import shutil

# === CONFIG ===
source_dir = r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/.specstory/history"
destination_dir = r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/full_chat/full_chat_logs"

# Copy all markdown files from source to destination
def copy_markdown_files():
    try:
        for filename in os.listdir(source_dir):
            if filename.endswith(".md"):
                source_path = os.path.join(source_dir, filename)
                destination_path = os.path.join(destination_dir, filename)
                shutil.copy(source_path, destination_path)
                print(f"Copied: {filename}")
    except Exception as e:
        print(f"Error during file copy: {e}")

if __name__ == "__main__":
    copy_markdown_files()