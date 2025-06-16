import os
import subprocess
def run():
    print("[plugin] Running GitHub push...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto push from CommandCore"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("[plugin] GitHub push completed.")
    except subprocess.CalledProcessError as e:
        print(f"[plugin] GitHub push failed: {e}")
