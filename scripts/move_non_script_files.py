import os
import shutil

# Define paths
memory_sys_scripts_path = "d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01\\memory\\memory_sys_scripts"
sync_story_history_path = "d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01\\memory\\Sync story history"

# Ensure destination folder exists
os.makedirs(sync_story_history_path, exist_ok=True)

# Get all non-script files in memory_sys_scripts
non_script_files = [
    os.path.join(memory_sys_scripts_path, f)
    for f in os.listdir(memory_sys_scripts_path)
    if not f.endswith(".py")
]

# Move files to Sync story history folder
def move_files():
    for file in non_script_files:
        destination = os.path.join(sync_story_history_path, os.path.basename(file))
        print(f"Moving {file} to {destination}")
        shutil.move(file, destination)

if __name__ == "__main__":
    move_files()
