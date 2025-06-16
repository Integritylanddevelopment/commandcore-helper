#!/usr/bin/env python3
"""
index_memory_whoosh.py

Creates a Whoosh-based full-text search index from ../memory.
Files indexed: .md, .txt, .log
Index is stored in ../whoosh_index.

We remove any existing index folder to ensure a clean reindex.
Requires: pip install whoosh
"""

import os
import sys
import shutil
import json
import time
import openai
from whoosh import index
from whoosh.fields import Schema, ID, TEXT
from whoosh.analysis import StemmingAnalyzer
from datetime import datetime

INDEX_DIR = os.path.join("..", "whoosh_index")
MEMORY_DIR = os.path.join("..", "memory")

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_schema():
    return Schema(
        path=ID(unique=True, stored=True),
        filename=TEXT(stored=True),
        content=TEXT(stored=True, analyzer=StemmingAnalyzer()),
        semantic_tags=TEXT(stored=True),
        contextual_tags=TEXT(stored=True),
        timestamp=TEXT(stored=True)
    )

def rebuild_index(schema):
    """
    1. Delete any existing whoosh_index folder
    2. Create a fresh index
    """
    if os.path.exists(INDEX_DIR):
        archive_existing_index(INDEX_DIR)
    os.makedirs(INDEX_DIR, exist_ok=True)
    return index.create_in(INDEX_DIR, schema)

def call_openai_api(batch_content):
    """Call OpenAI API for semantic tagging."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract semantic and contextual tags from the following text."},
                {"role": "user", "content": batch_content}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return ""

def extract_contextual_tags(file_path, timestamp):
    """Generate contextual tags based on metadata."""
    tags = []
    if datetime.now().strftime("%Y-%m-%d") == timestamp.split("T")[0]:
        tags.append("recent")
    if "archived" in file_path.lower():
        tags.append("archived")
    return tags

def index_files(folder_path, index_dir, json_output, batch_size=5, throttle_seconds=2):
    """Index files and generate JSON metadata."""
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
    ix = create_in(index_dir, schema)

    writer = ix.writer()
    json_data = {"files": []}
    batch = []
    batch_metadata = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".md", ".txt", ".log")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                timestamp = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                contextual_tags = extract_contextual_tags(file_path, timestamp)

                # Add file to batch
                batch.append(content)
                batch_metadata.append({
                    "name": file,
                    "path": file_path,
                    "timestamp": timestamp,
                    "contextual_tags": contextual_tags
                })

                # Process batch if size limit is reached
                if len(batch) >= batch_size:
                    batch_content = "\n\n".join(batch)
                    semantic_tags = call_openai_api(batch_content).split(",")  # Assuming API returns comma-separated tags

                    for i, metadata in enumerate(batch_metadata):
                        metadata["semantic_tags"] = semantic_tags[i] if i < len(semantic_tags) else []
                        writer.add_document(
                            name=metadata["name"],
                            path=metadata["path"],
                            content=batch[i],
                            semantic_tags=",".join(metadata["semantic_tags"]),
                            contextual_tags=",".join(metadata["contextual_tags"]),
                            timestamp=metadata["timestamp"]
                        )
                        json_data["files"].append({
                            "name": metadata["name"],
                            "path": metadata["path"],
                            "tags": {
                                "semantic": metadata["semantic_tags"],
                                "contextual": metadata["contextual_tags"]
                            },
                            "timestamp": metadata["timestamp"]
                        })

                    # Clear batch and metadata
                    batch = []
                    batch_metadata = []

                    # Throttle API calls
                    time.sleep(throttle_seconds)

    # Commit remaining batch
    if batch:
        batch_content = "\n\n".join(batch)
        semantic_tags = call_openai_api(batch_content).split(",")
        for i, metadata in enumerate(batch_metadata):
            metadata["semantic_tags"] = semantic_tags[i] if i < len(semantic_tags) else []
            writer.add_document(
                name=metadata["name"],
                path=metadata["path"],
                content=batch[i],
                semantic_tags=",".join(metadata["semantic_tags"]),
                contextual_tags=",".join(metadata["contextual_tags"]),
                timestamp=metadata["timestamp"]
            )
            json_data["files"].append({
                "name": metadata["name"],
                "path": metadata["path"],
                "tags": {
                    "semantic": metadata["semantic_tags"],
                    "contextual": metadata["contextual_tags"]
                },
                "timestamp": metadata["timestamp"]
            })

    writer.commit()

    # Write JSON file
    with open(json_output, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)

def archive_existing_index(index_dir):
    """Archive the existing index directory instead of deleting it."""
    archive_dir = os.path.join(index_dir + "_archive")
    if os.path.exists(archive_dir):
        shutil.rmtree(archive_dir)  # Clean up any previous archive
    os.rename(index_dir, archive_dir)
    print(f"Archived existing index to: {archive_dir}")

# Ensure the memory directory exists
if not os.path.exists(MEMORY_DIR):
    print(f"[ERROR] Memory directory not found: {MEMORY_DIR}")
    sys.exit(1)

# Update indexing logic to include all files in the memory folder
schema = Schema(path=ID(unique=True, stored=True), filename=TEXT(stored=True), content=TEXT(analyzer=StemmingAnalyzer(), stored=True))
if os.path.exists(INDEX_DIR):
    shutil.rmtree(INDEX_DIR)
index.create_in(INDEX_DIR, schema)
ix = index.open_dir(INDEX_DIR)
writer = ix.writer()

for root, _, files in os.walk(MEMORY_DIR):
    for file in files:
        if file.endswith(('.md', '.txt', '.log')):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            writer.add_document(path=file_path, filename=file, content=content)
writer.commit()
print("Indexing complete.")

def main():
    schema = create_schema()
    ix = rebuild_index(schema)
    index_files(ix)

if __name__ == "__main__":
    main()
