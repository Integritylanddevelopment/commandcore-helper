import os
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from anytree import Node, RenderTree

def generate_folder_tree(folder_path):
    """
    Generate a visual representation of the folder tree.

    Args:
        folder_path (str): Path to the folder to generate the tree for.

    Returns:
        str: A string representation of the folder tree.
    """
    def build_tree(path, parent_node):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            node = Node(item, parent=parent_node)
            if os.path.isdir(item_path):
                build_tree(item_path, node)

    root = Node(os.path.basename(folder_path))
    build_tree(folder_path, root)

    tree_str = "\n".join([f"{pre}{node.name}" for pre, _, node in RenderTree(root)])
    return tree_str

def update_schema_log(folder_path):
    """
    Updates the schema log files in the specified folder based on its contents.

    Args:
        folder_path (str): Path to the folder to update the schema log files for.
    """
    schema_logs_folder = os.path.join(folder_path, "memory", "logs", "schema", "schema_logs")
    os.makedirs(schema_logs_folder, exist_ok=True)

    schema_log_md_path = os.path.join(schema_logs_folder, "project_schema_log.md")
    schema_json_path = os.path.join(schema_logs_folder, "project_schema_log.json")
    schema_1_md_path = os.path.join(schema_logs_folder, "1_schema.md")

    # Check if logs already exist
    logs_exist = all(os.path.exists(path) for path in [schema_log_md_path, schema_json_path, schema_1_md_path])

    if logs_exist:
        print("Logs already exist. Updating them...")
    else:
        print("Logs do not exist. Creating them...")

    # Gather folder contents
    folder_contents = os.listdir(folder_path)
    folder_contents = [item for item in folder_contents if item not in ["project_schema_log.md", "project_schema_log.json", "1_schema.md"]]

    # Generate folder tree
    folder_tree = generate_folder_tree(folder_path)

    # Write or update the schema log markdown file
    with open(schema_log_md_path, "w", encoding="utf-8") as f:
        f.write(f"# Project Schema Log\n\n")
        f.write("## Folder Tree\n\n")
        f.write(f"```\n{folder_tree}\n```\n\n")
        f.write("## Contents\n\n")
        for item in folder_contents:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                f.write(f"- [Folder] {item}\n")
            else:
                f.write(f"- [File] {item}\n")

        # Add metadata
        f.write("\n## Metadata\n\n")
        f.write(f"- Last Updated: {datetime.now().isoformat()}\n")

    # Write or update the schema JSON file
    schema_data = {
        "folder": os.path.basename(folder_path),
        "contents": folder_contents,
        "last_updated": datetime.now().isoformat()
    }
    with open(schema_json_path, "w", encoding="utf-8") as f:
        json.dump(schema_data, f, indent=4)

    # Write or update the lightweight schema markdown file
    with open(schema_1_md_path, "w", encoding="utf-8") as f:
        f.write("# 📐 CommandCore-Hub Lightweight Schema\n\n")
        f.write("This schema defines the structure of the lightweight memory-enabled CommandCore-Hub system.\n")
        f.write("It is optimized for Visual Studio and acts as a persistent memory shell to support CommandCore OS development.\n\n")
        f.write("---\n\n")
        f.write("## 🗂 Folder Structure\n\n")
        for pre, _, node in RenderTree(Node(os.path.basename(folder_path))):
            f.write(f"- {pre}{node.name}\n")

        f.write("---\n\n")
        f.write("## 🧠 Memory Vault Purpose\n\n")
        f.write("- Acts as an external memory anchor for ChatGPT sessions.\n")
        f.write("- Includes backup scripts, assistant prompts, and historical context files.\n")
        f.write(f"- Located in `{folder_path}`.\n\n")

    print(f"Schema logs updated in folder: {schema_logs_folder}")

class SchemaUpdateHandler(FileSystemEventHandler):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def on_any_event(self, event):
        print(f"Event detected: {event.event_type} - {event.src_path}")
        if event.is_directory:
            return

        # Update the schema log file whenever a change is detected
        update_schema_log(self.folder_path)

if __name__ == "__main__":
    folder_to_watch = r"d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01"

    # Trigger a full scan and update the schema log for the entire project
    update_schema_log(folder_to_watch)

    # Set up the observer
    event_handler = SchemaUpdateHandler(folder_to_watch)
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)
    print(f"Watching for changes in {folder_to_watch}...")
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
