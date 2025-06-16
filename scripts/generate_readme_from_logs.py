#!/usr/bin/env python3
"""
generate_readme_from_logs.py

Scans the /logs/ directory for session logs and compiles them into a 
README-friendly summary. Saves or prints output to console.
"""

import os

def main():
    logs_dir = "../logs/"
    output_file = "../AUTO_GENERATED_README.md"
    if not os.path.exists(logs_dir):
        print("No logs directory found.")
        return
    
    summaries = []
    for filename in os.listdir(logs_dir):
        if filename.endswith(".md") or filename.endswith(".log"):
            filepath = os.path.join(logs_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                summaries.append(f"## {filename}\n{content}\n\n")
    
    final_text = "# Auto-Generated README from Logs\n\n" + "".join(summaries)
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(final_text)
    
    print(f"Generated summary in {output_file}")

if __name__ == "__main__":
    main()
