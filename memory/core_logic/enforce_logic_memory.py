import os
import re
import sys

# Ensure output supports Unicode
sys.stdout.reconfigure(encoding='utf-8')

# Path to primary logic memory
PRIMARY_LOGIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../memory/core_logic/primary_logic_memory.md"))
MEMORY_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../memory"))
VIOLATIONS_LOG = os.path.join(os.path.dirname(__file__), "../../CommandCore-OS/memory/logs/logic_enforcement_violations.md")

# Hard rules extracted manually from the PLM
PROTECTED_TAGS = ["#neverdelete", "#corelogic", "#builderintent"]
PROHIBITED_SCRIPTS = ["memory_decay.py", "auto_clean.py"]
FORBIDDEN_PATTERNS = [
    r"os\.remove\(",
    r"shutil\.rmtree\(",
    r"unlink\(",
    r"rm ",
    r"del ",
    r"TTL|expire|lifetime"
]

# Ensure the directory for the violations log exists
os.makedirs(os.path.dirname(VIOLATIONS_LOG), exist_ok=True)

def scan_script(path):
    violations = []
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, content):
                violations.append(f"⚠️  Forbidden pattern `{pattern}` found in: {os.path.basename(path)}")
    return violations

def scan_script_with_context(path):
    """
    Scan a script for forbidden patterns and provide context for each match.

    Args:
        path (str): Path to the script file.

    Returns:
        list: A list of violations with context.
    """
    violations = []
    with open(path, "r", encoding="utf-8") as file:
        content = file.readlines()

    for i, line in enumerate(content):
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, line):
                # Provide context: 2 lines before and after the match
                start = max(0, i - 2)
                end = min(len(content), i + 3)
                context = "".join(content[start:end])
                violations.append(
                    f"⚠️  Forbidden pattern `{pattern}` found in: {os.path.basename(path)}\nContext:\n{context}"
                )
    return violations

def scan_script_with_context_and_filter(path):
    """
    Scan a script for forbidden patterns, provide context for each match,
    and filter out false positives (e.g., matches in comments or strings).

    Args:
        path (str): Path to the script file.

    Returns:
        list: A list of real violations with context.
    """
    violations = []
    with open(path, "r", encoding="utf-8") as file:
        content = file.readlines()

    for i, line in enumerate(content):
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, line):
                # Check if the match is in a comment or string
                stripped_line = line.strip()
                if stripped_line.startswith("#") or (stripped_line.startswith("\"") and stripped_line.endswith("\"")):
                    # False positive: skip
                    continue

                # Provide context: 2 lines before and after the match
                start = max(0, i - 2)
                end = min(len(content), i + 3)
                context = "".join(content[start:end])
                violations.append(
                    f"⚠️  Real violation of `{pattern}` found in: {os.path.basename(path)}\nContext:\n{context}"
                )
    return violations

def scan_all_scripts():
    memory_scripts = []
    excluded_dirs = {".venv", "__pycache__", "env", "venv"}  # Directories to exclude

    # Traverse the entire workspace
    workspace_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    for root, dirs, files in os.walk(workspace_folder):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                memory_scripts.append(full_path)

    all_violations = []
    for script in memory_scripts:
        file_name = os.path.basename(script)
        if file_name in PROHIBITED_SCRIPTS:
            all_violations.append(f"❌ Script is blacklisted: {file_name}")
        all_violations += scan_script(script)
        all_violations += scan_script_with_context(script)
        all_violations += scan_script_with_context_and_filter(script)

    return all_violations

def check_primary_logic_file():
    if not os.path.exists(PRIMARY_LOGIC_PATH):
        return ["❌ PRIMARY LOGIC FILE IS MISSING! Expected: " + PRIMARY_LOGIC_PATH]
    return []

# Update file handling to treat it as a markdown file
def write_violations(violations):
    with open(VIOLATIONS_LOG, "w", encoding="utf-8") as file:
        file.write("# Logic Enforcement Violations\n\n")
        file.write("\n".join(violations))

def main():
    violations = []
    violations += check_primary_logic_file()
    violations += scan_all_scripts()

    if violations:
        print("\n⚠️  LOGIC ENFORCEMENT VIOLATIONS DETECTED:\n")
        for v in violations:
            print(v)
        write_violations(violations)
    else:
        print("✅ All memory scripts pass logic enforcement rules.")

if __name__ == "__main__":
    main()
