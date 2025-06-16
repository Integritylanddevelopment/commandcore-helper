import os
import filecmp

# Define paths
memory_sys_scripts_path = "d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01\\memory"
full_chat_logs_path = "d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01\\memory\\full_chat\\full_chat_logs"

# Get all .txt files in memory_sys_scripts
memory_sys_scripts_files = [
    os.path.join(memory_sys_scripts_path, f)
    for f in os.listdir(memory_sys_scripts_path)
    if f.endswith(".txt")
]

# Get all .txt files in full_chat_logs
full_chat_logs_files = [
    os.path.join(full_chat_logs_path, f)
    for f in os.listdir(full_chat_logs_path)
    if f.endswith(".txt")
]

# Define an archive directory for duplicates
archive_dir = os.path.join(memory_sys_scripts_path, "archived_duplicates")
os.makedirs(archive_dir, exist_ok=True)

# Compare files and delete duplicates
def compare_and_clean():
    for memory_file in memory_sys_scripts_files:
        is_duplicate = False
        for chat_file in full_chat_logs_files:
            if filecmp.cmp(memory_file, chat_file, shallow=False):
                is_duplicate = True
                break
        if is_duplicate:
            archive_file(memory_file)
        else:
            print(f"Keeping unique file: {memory_file}")

def archive_file(file_path):
    archive_path = os.path.join(archive_dir, os.path.basename(file_path))
    os.rename(file_path, archive_path)
    print(f"📦 Archived duplicate: {file_path} -> {archive_path}")

if __name__ == "__main__":
    compare_and_clean()
