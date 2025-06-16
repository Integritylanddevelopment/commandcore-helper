import os
import json
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search_memory(index_dir, query_str):
    """
    Searches the indexed memory files for the given query string.

    Args:
        index_dir (str): Path to the directory where the index is stored.
        query_str (str): The search query.
    """
    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query, limit=10)
        for result in results:
            print(f"File: {result['name']}")
            print(f"Path: {result['path']}")
            print(f"Snippet: {result.highlights('content')}")
            print("---")

def index_memory(folder_path, output_json):
    """
    Indexes all files in the specified folder and writes the index to a JSON file.

    Args:
        folder_path (str): Path to the folder containing files to index.
        output_json (str): Path to the output JSON file.
    """
    index_data = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                metadata = {
                    "name": file,
                    "path": file_path,
                    "tags": [],  # Placeholder for tags, can be extracted later
                    "timestamp": None  # Placeholder for timestamp, can be extracted from filename
                }
                index_data.append(metadata)

    with open(output_json, "w") as json_file:
        json.dump({"files": index_data}, json_file, indent=4)

if __name__ == "__main__":
    index_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whoosh_index")
    user_query = input("Enter your search query: ")
    search_memory(index_directory, user_query)

    folder_to_index = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "full_chat", "full_chat_logs")
    output_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "full_chat", "full_chat_scripts", "chat_index.json")

    index_memory(folder_to_index, output_json_path)
    print(f"Index written to {output_json_path}")
