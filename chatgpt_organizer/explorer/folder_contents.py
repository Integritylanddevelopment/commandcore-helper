import os
from pathlib import Path

def show_folder_contents(folder):
    path = Path(folder)
    if not path.exists() or not path.is_dir():
        print(f"[CONTENTS] Invalid folder path: {folder}")
        return

    print(f"Contents of {folder}:\n")
    for file in sorted(path.iterdir()):
        if file.is_file():
            print(f" - {file.name}")
        elif file.is_dir():
            print(f" + {file.name}/")
