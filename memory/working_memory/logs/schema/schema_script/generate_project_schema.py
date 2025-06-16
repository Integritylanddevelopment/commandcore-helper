import os
import json
from datetime import datetime
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

def update_project_schema(folder_path, output_folder):
    """
    Generate schema logs for the entire project.

    Args:
        folder_path (str): Path to the root folder of the project.
        output_folder (str): Path to the folder where schema logs will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    schema_log_path = os.path.join(output_folder, "project_schema_log.md")
    schema_json_path = os.path.join(output_folder, "project_schema_log.json")
    schema_1_md_path = os.path.join(output_folder, "1_schema.md")

    # Generate folder tree
    folder_tree = generate_folder_tree(folder_path)

    # Write the schema log file
    with open(schema_log_path, "w", encoding="utf-8") as f:
        f.write(f"# Project Schema Log\n\n")
        f.write("## Folder Tree\n\n")
        f.write(f"```\n{folder_tree}\n```\n\n")

        # Add metadata
        f.write("\n## Metadata\n\n")
        f.write(f"- Last Updated: {datetime.now().isoformat()}\n")

    # Write the schema JSON file
    schema_data = {
        "folder": os.path.basename(folder_path),
        "last_updated": datetime.now().isoformat(),
        "tree": folder_tree
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

    print(f"Project schema logs generated in {output_folder}")

if __name__ == "__main__":
    project_root = r"d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01"
    output_folder = os.path.join(project_root, "memory", "logs", "schema")

    update_project_schema(project_root, output_folder)
