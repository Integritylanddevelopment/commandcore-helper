import os
import shutil
from datetime import datetime, timedelta

def run_decay(days_old: int = 5) -> str:
    """Promote old working memory into archive/index/full memory layers."""
    base_path = os.path.join(os.path.dirname(__file__), '../working_memory/working_today/')
    archive_path = os.path.join(os.path.dirname(__file__), '../working_memory/archive/')
    index_path = os.path.join(os.path.dirname(__file__), '../short_term_memory/index/')
    full_path = os.path.join(os.path.dirname(__file__), '../long_term_memory/full/')
    log_path = os.path.join(os.path.dirname(__file__), '../logs/decay_agent_log.md')

    os.makedirs(archive_path, exist_ok=True)
    os.makedirs(index_path, exist_ok=True)
    os.makedirs(full_path, exist_ok=True)

    cutoff_date = datetime.now() - timedelta(days=days_old)
    summary = []

    for filename in os.listdir(base_path):
        file_path = os.path.join(base_path, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < cutoff_date:
                # Move to archive
                shutil.move(file_path, os.path.join(archive_path, filename))

                # Summarize and save to index
                with open(os.path.join(archive_path, filename), 'r', encoding='utf-8') as file:
                    content = file.read()
                summary_content = f"Summary of {filename}:\n{content[:200]}..."  # Placeholder for actual summarization logic
                with open(os.path.join(index_path, filename), 'w', encoding='utf-8') as index_file:
                    index_file.write(summary_content)

                # Copy to full memory
                shutil.copy(os.path.join(archive_path, filename), os.path.join(full_path, filename))

                summary.append(f"Processed {filename}")

    # Log the decay process
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"[{datetime.now()}] Decay process completed:\n" + "\n".join(summary) + "\n")

    return "\n".join(summary)

if __name__ == "__main__":
    import sys
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(run_decay(days))
