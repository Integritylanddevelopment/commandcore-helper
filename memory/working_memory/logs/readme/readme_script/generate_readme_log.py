import os
import datetime
import shutil

# Define paths
readme_logs_dir = r"d:\ActiveProjects\CommandCore-Hub_v2025.01.01\memory\logs\readme\readme_logs"
original_readme_path = r"d:\ActiveProjects\CommandCore-Hub_v2025.01.01\README_FULL.md"
pinned_readme_path = os.path.join(readme_logs_dir, "README_Original.md")

# Ensure the logs directory exists
os.makedirs(readme_logs_dir, exist_ok=True)

# Pin the original README to the top of the log
if os.path.exists(original_readme_path):
    shutil.copy(original_readme_path, pinned_readme_path)
    print(f"Pinned original README as: {pinned_readme_path}")

def generate_readme_log():
    """Generate a versioned README log."""
    if not os.path.exists(original_readme):
        print(f"[ERROR] Original README not found: {original_readme}")
        return

    # Read the original README content
    with open(original_readme, 'r', encoding='utf-8') as file:
        content = file.read()

    # Generate a versioned filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    versioned_filename = f"readme_log_{timestamp}.md"
    versioned_filepath = os.path.join(readme_logs_dir, versioned_filename)

    # Write the content to the versioned log file
    with open(versioned_filepath, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"[OK] README log generated: {versioned_filepath}")

def update_all_readmes(new_content):
    """Update all README files with the provided new content."""
    readme_files = [original_readme, "README_Scripts_Documentation.md", "README_Usage_Guide.md"]
    for readme in readme_files:
        if os.path.exists(readme):
            with open(readme, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated README: {readme}")

if __name__ == "__main__":
    generate_readme_log()
    # Example usage:
    # new_content = "# Updated Content\n\nThis is the new content for all README files."
    # update_all_readmes(new_content)
