import os
import datetime

# Define paths
original_readme = r"d:\ActiveProjects\CommandCore-Hub_v2025.01.01\README.md"
readme_logs_dir = r"d:\ActiveProjects\CommandCore-Hub_v2025.01.01\memory\logs\readme\readme_logs"
logs_dir = r"d:\ActiveProjects\CommandCore-Hub_v2025.01.01\memory\logs"

# Ensure the logs directory exists
os.makedirs(readme_logs_dir, exist_ok=True)

def get_latest_readme_log():
    """Retrieve the most recent README log."""
    readme_files = [f for f in os.listdir(readme_logs_dir) if f.startswith("readme_log") and f.endswith(".md")]
    if not readme_files:
        return None
    latest_file = max(readme_files, key=lambda f: os.path.getmtime(os.path.join(readme_logs_dir, f)))
    return os.path.join(readme_logs_dir, latest_file)

def aggregate_logs():
    """Aggregate content from other logs."""
    aggregated_content = ""
    for root, _, files in os.walk(logs_dir):
        for file in files:
            if file.endswith(".md") and "readme_log" not in file:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    aggregated_content += f"\n\n---\n\n# {file}\n\n" + f.read()
    return aggregated_content

def generate_readme_log():
    """Generate an updated README log."""
    latest_readme_log = get_latest_readme_log()

    # Start with the original README content or the latest log
    if latest_readme_log:
        with open(latest_readme_log, 'r', encoding='utf-8') as file:
            content = file.read()
    else:
        with open(original_readme, 'r', encoding='utf-8') as file:
            content = file.read()

    # Append aggregated content from other logs
    aggregated_content = aggregate_logs()
    content += f"\n\n---\n\n# Aggregated Updates\n\n{aggregated_content}"

    # Generate a versioned filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    versioned_filename = f"readme_log_{timestamp}.md"
    versioned_filepath = os.path.join(readme_logs_dir, versioned_filename)

    # Write the updated content to the new log file
    with open(versioned_filepath, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"[OK] README log updated: {versioned_filepath}")

def log_readme_versions():
    """Log the current state of all README files."""
    readme_files = [original_readme, "README_Scripts_Documentation.md", "README_Usage_Guide.md"]
    for readme in readme_files:
        if os.path.exists(readme):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            versioned_filename = f"{os.path.basename(readme).replace('.md', '')}_log_{timestamp}.md"
            versioned_filepath = os.path.join(readme_logs_dir, versioned_filename)
            with open(readme, 'r', encoding='utf-8') as file:
                content = file.read()
            with open(versioned_filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Logged version: {versioned_filename}")

if __name__ == "__main__":
    generate_readme_log()
    log_readme_versions()