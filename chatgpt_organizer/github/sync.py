"""
sync.py
Description: Pull latest changes from GitHub repo.
Run: python github/sync.py --folder path/to/repo --test
"""

import argparse
import subprocess
import os

def run(folder_path: str):
    try:
        os.chdir(folder_path)
        subprocess.run(["git", "pull"], check=True)
        print(f"[sync] ✅ Pulled latest from GitHub: {folder_path}")
    except Exception as e:
        print(f"[sync] ❌ GitHub sync failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, required=True)
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    if args.test:
        run(args.folder)
