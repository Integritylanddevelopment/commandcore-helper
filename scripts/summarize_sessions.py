#!/usr/bin/env python3
"""
summarize_sessions.py

Generates a simple summarization of each file in /memory/. 
Saves the result to /logs/session_summaries.md.

Summary Logic (naive example):
  - For each file, extracts:
      - First heading (if any)
      - Count of lines
      - First ~5 lines as a preview
"""

import os

MEMORY_DIR = os.path.join("..", "memory")
OUTPUT_FILE = os.path.join("..", "logs", "session_summaries.md")

def get_first_heading(lines):
    """
    Returns the first markdown heading found, or 'No Heading Found'
    """
    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith("#"):
            return line_stripped
    return "No Heading Found"

def get_preview(lines, count=5):
    """
    Returns up to 'count' lines joined with newline.
    """
    snippet = lines[:count]
    return "\n".join(snippet)

def summarize_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.splitlines()

    heading = get_first_heading(lines)
    total_lines = len(lines)
    preview = get_preview(lines, 5)
    return heading, total_lines, preview

def main():
    if not os.path.exists(MEMORY_DIR):
        print(f"[WARNING] Memory folder not found: {MEMORY_DIR}")
        return

    files = [f for f in os.listdir(MEMORY_DIR) if f.lower().endswith(('.md', '.txt', '.log'))]
    files.sort()

    summaries = []

    for filename in files:
        filepath = os.path.join(MEMORY_DIR, filename)
        heading, total_lines, preview = summarize_file(filepath)
        summary = f"""
## File: {filename}
**Heading:** {heading}
**Total Lines:** {total_lines}

**Preview:**
"""
        summaries.append(summary)

    if not summaries:
        print("[INFO] No files to summarize in memory/ folder.")
        return

    # Write combined summary
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        out.write("# Session Summaries\n")
        out.write("\n".join(summaries))

    print(f"[OK] Created summaries in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
