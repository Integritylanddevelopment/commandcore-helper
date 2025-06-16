import os
import json
from datetime import datetime, timedelta
from memory.memory_router import BASE_PATH, log_event, log_violation
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Agent Metadata
agent_meta = {
    "name": "recall_agent",
    "purpose": "Semantic memory retrieval agent",
    "inputs": "Natural language query",
    "outputs": "Relevant full memory entries",
    "strategy": "Index → Summary → Full match funnel"
}

# Paths
INDEX_DIR = os.path.join(BASE_PATH, "short_term", "index")
SUMMARY_DIR = os.path.join(BASE_PATH, "short_term", "summary")
FULL_CHAT_DIR = os.path.join(BASE_PATH, "long_term", "full")
RECALL_HISTORY = os.path.join(BASE_PATH, "working_memory", "recall_history.md")

# Ensure directories exist
os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)
os.makedirs(FULL_CHAT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(RECALL_HISTORY), exist_ok=True)

def prune_recall_history():
    """Prune recall history to keep entries within the last 10 days."""
    if not os.path.exists(RECALL_HISTORY):
        return

    ten_days_ago = datetime.now() - timedelta(days=10)
    filtered_entries = []

    with open(RECALL_HISTORY, "r", encoding="utf-8") as f:
        entries = f.read().split("---\n")
        for entry in entries:
            if entry.strip():
                lines = entry.split("\n")
                timestamp_line = lines[0].strip()
                if timestamp_line.startswith("[") and timestamp_line.endswith("]"):
                    timestamp_str = timestamp_line[1:-1]
                    try:
                        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
                        if timestamp >= ten_days_ago:
                            filtered_entries.append(entry)
                    except ValueError:
                        pass

    with open(RECALL_HISTORY, "w", encoding="utf-8") as f:
        f.write("---\n".join(filtered_entries) + ("---\n" if filtered_entries else ""))

def save_query_to_history(query, response_count):
    """Save the query and response count to recall history."""
    prune_recall_history()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"---\n[{timestamp}]\nQuery: {query}\nResult Count: {response_count}\n---\n"
    with open(RECALL_HISTORY, "a", encoding="utf-8") as f:
        f.write(entry)

def index_scan(search_term):
    """Scan the index for relevant entries."""
    results = []
    for file_name in os.listdir(INDEX_DIR):
        file_path = os.path.join(INDEX_DIR, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if search_term.lower() in content.lower():
                results.append(file_name)
    return results

def summary_scan(index_results, search_term):
    """Filter summaries based on the search term."""
    results = []
    for file_name in index_results:
        summary_path = os.path.join(SUMMARY_DIR, file_name)
        if os.path.exists(summary_path):
            with open(summary_path, "r", encoding="utf-8") as f:
                content = f.read()
                if search_term.lower() in content.lower():
                    results.append(file_name)
    return results

def full_chat_retrieval(summary_results):
    """Retrieve full chat files based on filtered summaries."""
    results = {}
    for file_name in summary_results:
        full_chat_path = os.path.join(FULL_CHAT_DIR, file_name)
        if os.path.exists(full_chat_path):
            with open(full_chat_path, "r", encoding="utf-8") as f:
                results[file_name] = f.read()
    return results

def recall(query):
    """Recall memory based on a query."""
    log_event(f"Starting memory recall for query: {query}")
    
    # Stage 1: Index Scan
    index_results = index_scan(query)
    log_event(f"Index scan results: {index_results}")

    # Stage 2: Summary Scan
    summary_results = summary_scan(index_results, query)
    log_event(f"Summary scan results: {summary_results}")

    # Stage 3: Full Chat Retrieval
    full_chat_results = full_chat_retrieval(summary_results)
    log_event(f"Full chat retrieval results: {list(full_chat_results.keys())}")

    # Save query to history
    save_query_to_history(query, len(full_chat_results))

    return [(file_name, content) for file_name, content in full_chat_results.items()]

# This module follows the CommandCore agent naming convention.
# Metadata for this agent is stored in agent.meta.json.

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python recall_agent.py \"search phrase\"")
        sys.exit(1)

    query = sys.argv[1]
    results = recall(query)
    print(json.dumps(results, indent=2))
