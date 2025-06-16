import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from datetime import datetime
import argparse

def setup_logging():
    """Set up logging for the script."""
    logging.basicConfig(
        filename="readme_updater.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def update_readme(folder_path):
    """
    Updates the README.md file in the specified folder based on its contents.

    Args:
        folder_path (str): Path to the folder to update the README.md file for.
    """
    readme_path = os.path.join(folder_path, "README.md")

    # Gather folder contents
    folder_contents = os.listdir(folder_path)
    folder_contents = [item for item in folder_contents if item != "README.md"]

    # Write the README.md file
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {os.path.basename(folder_path)}\n\n")
        f.write("## Contents\n\n")
        for item in folder_contents:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                f.write(f"- [Folder] {item}\n")
            else:
                f.write(f"- [File] {item}\n")

        # Add last updated timestamp
        f.write("\n## Metadata\n\n")
        f.write(f"- Last Updated: {datetime.now().isoformat()}\n")

    logging.info(f"README.md updated for folder: {folder_path}")

class ReadmeUpdateHandler(FileSystemEventHandler):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def on_created(self, event):
        if event.is_directory:
            return

        # Update the README.md file whenever a new file is created
        update_readme(self.folder_path)

    def on_modified(self, event):
        if event.is_directory:
            return

        # Update the README.md file whenever a file is modified
        update_readme(self.folder_path)

    def on_deleted(self, event):
        if event.is_directory:
            return

        # Update the README.md file whenever a file is deleted
        update_readme(self.folder_path)

if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser(description="Monitor a folder and update its README.md dynamically.")
    parser.add_argument("folder", type=str, help="The folder to monitor and update the README.md for.")
    args = parser.parse_args()

    folder_to_watch = args.folder

    # Initial README update
    update_readme(folder_to_watch)

    # Set up the observer
    event_handler = ReadmeUpdateHandler(folder_to_watch)
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)
    logging.info(f"Watching for changes in {folder_to_watch}...")
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopped monitoring.")
    observer.join()
