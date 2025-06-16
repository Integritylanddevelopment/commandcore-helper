import os
import shutil
from datetime import datetime, timedelta
import openai
from dotenv import load_dotenv
from memory.memory_router import BASE_PATH, log_event, log_violation

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Paths
WORKING_TODAY_DIR = os.path.join(BASE_PATH, "working_memory", "working_today")
ARCHIVE_DIR = os.path.join(BASE_PATH, "working_memory", "archive")
INDEX_DIR = os.path.join(BASE_PATH, "short_term", "index")
LONG_TERM_DIR = os.path.join(BASE_PATH, "long_term", "full")

# Ensure directories exist
os.makedirs(ARCHIVE_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(LONG_TERM_DIR, exist_ok=True)

# Function to summarize file content
def summarize_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Summarize this file content."},
                {"role": "user", "content": content}
            ]
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        log_violation(f"Failed to summarize file {file_path}: {e}")
        return None

# Function to process files
def process_files():
    cutoff_date = datetime.now() - timedelta(days=5)

    for file_name in os.listdir(WORKING_TODAY_DIR):
        file_path = os.path.join(WORKING_TODAY_DIR, file_name)

        if not file_name.endswith(".md"):
            continue

        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        if file_mtime > cutoff_date:
            continue

        # Move to archive
        archive_path = os.path.join(ARCHIVE_DIR, file_name)
        shutil.move(file_path, archive_path)
        log_event(f"Moved to archive: {archive_path}")

        # Summarize and write to index
        summary = summarize_file(archive_path)
        if summary:
            index_file_path = os.path.join(INDEX_DIR, file_name)
            with open(index_file_path, "w", encoding="utf-8") as f:
                f.write(summary)
            log_event(f"Summarized and indexed: {index_file_path}")

        # Copy to long-term memory
        long_term_path = os.path.join(LONG_TERM_DIR, file_name)
        shutil.copy(archive_path, long_term_path)
        log_event(f"Copied to long-term memory: {long_term_path}")

if __name__ == "__main__":
    process_files()
