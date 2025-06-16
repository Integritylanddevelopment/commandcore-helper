import os
import json
from datetime import datetime

def index_memory(folder_path, output_file):
    """
    Indexes all text files in the specified folder and saves the index as a JSON file.

    Args:
        folder_path (str): Path to the folder containing memory files.
        output_file (str): Path to the output JSON file.
    """
    index = {"files": []}

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                file_info = {
                    "name": file,
                    "path": os.path.relpath(file_path, folder_path),
                    "content": content[:500],  # Store a snippet of the content (first 500 chars)
                    "size": os.path.getsize(file_path),
                    "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                }
                index["files"].append(file_info)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

    print(f"Index created at {output_file}")

if __name__ == "__main__":
    memory_folder = os.path.dirname(os.path.abspath(__file__))  # Current folder
    output_json = os.path.join(memory_folder, "memory_index.json")
    index_memory(memory_folder, output_json)
