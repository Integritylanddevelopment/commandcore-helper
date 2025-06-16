#!/usr/bin/env python3
"""
validate_hub.py

Checks for the required CommandCore-Hub folder structure:
  - memory/
  - logs/
  - scripts/
  - launcher/
  - README.md

Exits with an error code if something is missing.
"""

import os
import sys

REQUIRED_FOLDERS = ["memory", "logs", "scripts", "launcher"]
REQUIRED_FILES = ["README.md"]

def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    missing_items = []

    # Check folders
    for folder in REQUIRED_FOLDERS:
        folder_path = os.path.join(base_path, folder)
        if not os.path.isdir(folder_path):
            missing_items.append(f"Missing folder: {folder}")

    # Check files
    for file_name in REQUIRED_FILES:
        file_path = os.path.join(base_path, file_name)
        if not os.path.isfile(file_path):
            missing_items.append(f"Missing file: {file_name}")

    if missing_items:
        print("[ERROR] Hub validation failed. The following items are missing:")
        for item in missing_items:
            print(" -", item)
        sys.exit(1)
    else:
        print("[OK] Hub structure looks valid.")

if __name__ == "__main__":
    main()
