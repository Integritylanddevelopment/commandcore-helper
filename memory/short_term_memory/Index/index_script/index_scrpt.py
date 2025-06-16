import os
import json
import re
from datetime import datetime
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def extract_semantic_tags(content):
    """
    Extract semantic tags from the content based on specific patterns.

    Args:
        content (str): The content of the markdown file.

    Returns:
        list: A list of extracted semantic tags.
    """
    tags = set()

    # Example: Extract tags from lines starting with '## Semantic Tags' or similar patterns
    tag_lines = re.findall(r"## Semantic Tags\n(.*?)(?:\n\n|$)", content, re.DOTALL)
    for line in tag_lines:
        tags.update(tag.strip() for tag in line.split(',') if tag.strip())

    return list(tags)

def index_markdown(folder_path, output_file):
    """
    Indexes all markdown files in the specified folder and updates the JSON file without overwriting past data.

    Args:
        folder_path (str): Path to the folder containing markdown files.
        output_file (str): Path to the output JSON file.
    """
    # Load existing data if the file exists
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = {"files": []}

    # Create a set of already indexed file paths to avoid duplicates
    existing_paths = {file_info["path"] for file_info in index["files"]}

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)

                # Skip files that are already indexed
                if relative_path in existing_paths:
                    continue

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract semantic tags
                semantic_tags = extract_semantic_tags(content)

                file_info = {
                    "name": file,
                    "path": relative_path,
                    "content": content,  # Store full content for semantic indexing
                    "size": os.path.getsize(file_path),
                    "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                    "semantic_tags": semantic_tags
                }
                index["files"].append(file_info)

    # Save the updated index back to the JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

    print(f"Index updated at {output_file}")

def update_index_md(index, md_file_path):
    """
    Updates the index_log.md file with a human-readable version of the index.

    Args:
        index (dict): The index data.
        md_file_path (str): Path to the markdown file.
    """
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write("# Index Log\n\n")
        for file_info in index["files"]:
            f.write(f"## {file_info['name']}\n")
            f.write(f"- Path: {file_info['path']}\n")
            f.write(f"- Size: {file_info['size']} bytes\n")
            f.write(f"- Last Modified: {file_info['last_modified']}\n")
            if file_info['semantic_tags']:
                f.write(f"- Semantic Tags: {', '.join(file_info['semantic_tags'])}\n")
            f.write("\n")

class MarkdownFileHandler(FileSystemEventHandler):
    def __init__(self, folder_path, json_file_path, md_file_path):
        self.folder_path = folder_path
        self.json_file_path = json_file_path
        self.md_file_path = md_file_path

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".md"):
            print(f"New markdown file detected: {event.src_path}")
            index_markdown(self.folder_path, self.json_file_path)

            # Load the updated index
            with open(self.json_file_path, "r", encoding="utf-8") as f:
                index_data = json.load(f)

            # Update the markdown file
            update_index_md(index_data, self.md_file_path)

            print(f"Index updated for new file: {event.src_path}")

def search_whoosh(index_dir, query):
    """Perform a Whoosh search on the indexed summaries."""
    from whoosh.index import open_dir
    from whoosh.qparser import QueryParser

    results = []
    try:
        ix = open_dir(index_dir)
        with ix.searcher() as searcher:
            query_parser = QueryParser("content", ix.schema)
            parsed_query = query_parser.parse(query)
            hits = searcher.search(parsed_query, limit=None)
            for hit in hits:
                results.append({
                    "title": hit["title"],
                    "path": hit["path"],
                    "content": hit["content"]
                })
    except Exception as e:
        print(f"Whoosh search error: {e}")
    return results

def fuzzy_search(folder_path, query):
    """Perform a fuzzy search on markdown files in the folder."""
    import difflib

    results = []
    query = query.lower()
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Fuzzy matching on file content
                    if query in content.lower():
                        # Get a snippet around the query
                        snippet = difflib.get_close_matches(query, content.split(), n=10, cutoff=0.1)
                        results.append({
                            "file": file,
                            "path": relative_path,
                            "snippet": " ".join(snippet)
                        })
    return results

def search_combined(query):
    """Perform a combined search using Whoosh and fuzzy search."""
    # Whoosh search on summaries
    whoosh_results = search_whoosh(r"d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01\\memory\\memory_sys_scripts\\whoosh_index", query)

    # Fuzzy search on full chat logs
    fuzzy_results = fuzzy_search(r"d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01\\memory\\full_chat\\full_chat_logs", query)

    # Combine results
    combined_results = {
        "whoosh": whoosh_results,
        "fuzzy": fuzzy_results
    }
    return combined_results

if __name__ == "__main__":
    full_chat_folder = r"d:\ActiveProjects\CommandCore-Hub_v2025.01.01\memory\full_chat\full_chat_logs"
    summary_logs_folder = r"d:\ActiveProjects\CommandCore-Hub_v2025.01.01\memory\logs\summary\summary_logs"
    output_json = r"d:\ActiveProjects\CommandCore-Hub_v2025.01.01\memory\logs\Index\index_log\index_log.json"
    output_md = r"d:\ActiveProjects\CommandCore-Hub_v2025.01.01\memory\logs\Index\index_log\index_log.md"

    # Index full chat logs
    index_markdown(full_chat_folder, output_json)

    # Index summary logs
    index_markdown(summary_logs_folder, output_json)

    # Load the updated index
    with open(output_json, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    # Update the markdown file
    update_index_md(index_data, output_md)

    print(f"Human-readable index updated at {output_md}")

    # Start watching the folder for new markdown files
    event_handler = MarkdownFileHandler(full_chat_folder, output_json, output_md)
    observer = Observer()
    observer.schedule(event_handler, full_chat_folder, recursive=False)
    print(f"Watching for new markdown files in {full_chat_folder}...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    search_query = input("Enter your search query: ")
    results = search_combined(search_query)

    print("\nResults from Summaries (Whoosh Search):")
    for result in results["whoosh"]:
        print(f"Title: {result['title']}")
        print(f"Path: {result['path']}")
        print(f"Snippet: {result['content']}\n")

    print("\nResults from Full Chat Logs (Fuzzy Search):")
    for result in results["fuzzy"]:
        print(f"File: {result['file']}")
        print(f"Path: {result['path']}")
        print(f"Snippet: {result['snippet']}\n")