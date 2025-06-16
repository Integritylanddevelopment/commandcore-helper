# Memory Orchestrator
# This script coordinates tasks within the memory folder.

import subprocess
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from memory.memory_agent_router import route as memory_route
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_path, description):
    """Run a script and log its status."""
    try:
        logging.info(f"Starting: {description}")
        subprocess.run(["python", script_path], check=True)
        logging.info(f"Completed: {description}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed: {description} with error: {e}")
        raise

def get_scripts_order():
    """Define the order of scripts to be executed."""
    return [
        # Step 0: Promote old working memory
        ("memory/working_memory/memory_decay.py", "Promote old working memory"),

        # Step 1: Indexing and organizing
        ("memory/logs/schema/schema_script/generate_project_schema.py", "Generate Project Schema"),
        ("memory/logs/Index/index_script/index_scrpt.py", "Index Markdown Files"),
        ("memory/logs/summary/summary_scripts/summary.py", "Generate Summaries"),

        # Step 2: Perform searches
        ("memory/logs/search/simple_search.py", "Perform Simple Search"),
        ("memory/logs/search/fuzzy_search.py", "Perform Fuzzy Search"),
        ("memory/logs/search/whoosh_search.py", "Perform Whoosh Search"),

        # Step 3: Process full chat logs
        ("memory/full_chat/full_chat_scripts/rename_chat_logs.py", "Rename Chat Logs"),
        ("memory/full_chat/full_chat_scripts/process_full_chat_logs.py", "Process Full Chat Logs"),

        # Step 4: Additional scripts
        ("memory/logs/scripts/script_script/extract_scripts.py", "Extract Scripts"),
    ]

class ScriptHandler(FileSystemEventHandler):
    def __init__(self, scripts_order):
        self.scripts_order = scripts_order

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".py"):
            return

        new_script = event.src_path
        print(f"New script detected: {new_script}")
        description = input(f"Enter a description for the new script '{new_script}': ")
        position = input(f"Enter the position (0 for first, {len(self.scripts_order)} for last) to insert the script: ")

        try:
            position = int(position)
            self.scripts_order.insert(position, (new_script, description))
            print(f"Updated execution order: {self.scripts_order}")
        except ValueError:
            print("Invalid position. Script not added.")

def monitor_memory_folder(scripts_order):
    event_handler = ScriptHandler(scripts_order)
    observer = Observer()
    observer.schedule(event_handler, path="memory", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    """Coordinate the execution of scripts within the memory folder."""
    try:
        scripts_order = get_scripts_order()
        monitor_memory_folder(scripts_order)

        for script_path, description in scripts_order:
            run_script(script_path, description)

        # Interactive or dev mode flag
        dev_mode = True  # Set this flag to False to disable router step
        if dev_mode:
            query = "find all mentions of memory tagging"
            result = memory_route(query)
            print("[Memory Agent Result]")
            print(result)

            # Log the result
            routed_output_log = os.path.join("memory", "logs", "memory_agent_routed_output.md")
            os.makedirs(os.path.dirname(routed_output_log), exist_ok=True)
            with open(routed_output_log, "a", encoding="utf-8") as f:
                f.write(f"[Memory Agent Result]\nQuery: {query}\nResult: {result}\n\n")

        logging.info("Memory orchestration completed successfully.")
    except Exception as e:
        logging.error(f"Memory orchestration failed: {e}")

if __name__ == "__main__":
    main()
