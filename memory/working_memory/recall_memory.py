import os
import json
from datetime import datetime
from memory.memory_router import BASE_PATH, log_event, log_violation
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Paths
INDEX_DIR = os.path.join(BASE_PATH, "short_term", "index")
SUMMARY_DIR = os.path.join(BASE_PATH, "short_term", "summary")
FULL_CHAT_DIR = os.path.join(BASE_PATH, "long_term", "full")

# Ensure directories exist
os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)
os.makedirs(FULL_CHAT_DIR, exist_ok=True)

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

def recall_memory(search_term):
    """Main function to recall memory based on a search term."""
    log_event(f"Starting memory recall for term: {search_term}")
    
    # Stage 1: Index Scan
    index_results = index_scan(search_term)
    log_event(f"Index scan results: {index_results}")

    # Stage 2: Summary Scan
    summary_results = summary_scan(index_results, search_term)
    log_event(f"Summary scan results: {summary_results}")

    # Stage 3: Full Chat Retrieval
    full_chat_results = full_chat_retrieval(summary_results)
    log_event(f"Full chat retrieval results: {list(full_chat_results.keys())}")

    return full_chat_results

if __name__ == "__main__":
    search_term = input("Enter search term: ")
    results = recall_memory(search_term)
    print(json.dumps(results, indent=2))
