#!/usr/bin/env python3
"""
auto_document.py

Parses Python scripts in the /scripts/ folder, extracts the top-level module docstring,
and appends them to the project's README.md under a "Scripts Usage Documentation" heading.

Requires Python 3.8+ (for importlib.util and AST usage).
"""

import os
import ast
import sys
import importlib.util

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
README_PATH = os.path.join(BASE_DIR, "README.md")

def extract_docstring(py_file_path):
    """
    Parse a Python file and return its top-level docstring (if any).
    """
    try:
        with open(py_file_path, "r", encoding="utf-8") as f:
            source = f.read()
        mod_ast = ast.parse(source)
        return ast.get_docstring(mod_ast) or "No module docstring found."
    except Exception as e:
        return f"Error parsing {py_file_path}: {str(e)}"

def main():
    if not os.path.exists(SCRIPTS_DIR):
        print(f"[ERROR] Scripts folder not found: {SCRIPTS_DIR}")
        sys.exit(1)

    py_files = [f for f in os.listdir(SCRIPTS_DIR) if f.lower().endswith(".py")]

    # We'll gather docstrings in a list
    docs_output = []
    docs_output.append("# Scripts Usage Documentation\n")
    docs_output.append("Below is an auto-generated list of each script in `/scripts/` and its docstring:\n")

    for fname in sorted(py_files):
        if fname == os.path.basename(__file__):
            # skip auto_document.py itself to avoid recursion
            continue
        fpath = os.path.join(SCRIPTS_DIR, fname)
        docstring = extract_docstring(fpath)
        docs_output.append(f"## {fname}\n```\n{docstring}\n```\n")

    # Append to README.md
    try:
        with open(README_PATH, "a", encoding="utf-8") as readme:
            readme.write("\n\n")
            readme.write("\n".join(docs_output))
        print(f"[OK] Scripts documentation appended to {README_PATH}.")
    except Exception as e:
        print(f"[ERROR] Could not append to README.md: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
