#!/usr/bin/env python3
"""
extract_scripts.py

Scans text files in /memory/ for Markdown code blocks (triple backticks).
Extracts each code block into a separate file within /logs/extracted_scripts/.

The filename is derived from:
  - Original chat log name
  - Code block index
  - Language if indicated (e.g., ```python => .py)

Example logic:
  - For each code block, we guess the file extension from the code fence:
      ```python  => .py
      ```batch   => .bat
      ```js      => .js
      etc.

If no language is specified, we default to .txt.
"""

import os
import re

MEMORY_DIR = os.path.join("..", "memory")
OUTPUT_DIR = os.path.join("..", "logs", "extracted_scripts")

CODE_BLOCK_PATTERN = re.compile(
    r"```([\w+-]*)\n(.*?)```", 
    re.DOTALL | re.IGNORECASE
)

EXTENSION_MAP = {
    "python": "py",
    "py": "py",
    "batch": "bat",
    "bat": "bat",
    "bash": "sh",
    "shell": "sh",
    "js": "js",
    "javascript": "js",
    "ts": "ts",
    "typescript": "ts",
    "html": "html",
    "css": "css",
    "json": "json",
    # add more as needed
}

def extract_code_blocks(content):
    """
    Return list of tuples: [(lang, code), ...]
    """
    matches = CODE_BLOCK_PATTERN.findall(content)
    # matches -> List[Tuple(languageInFence, codeText)]
    # e.g. [("python","print('hello')"), ("","some code"), ...]
    result = []
    for lang, code_text in matches:
        lang_clean = lang.lower().strip()
        code_clean = code_text.strip("\n\r ")
        result.append((lang_clean, code_clean))
    return result

def determine_extension(lang):
    return EXTENSION_MAP.get(lang, "txt")

def process_file(filepath):
    """
    Extract code blocks from a single file, write them to OUTPUT_DIR.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    code_blocks = extract_code_blocks(content)
    if not code_blocks:
        return 0

    base_name = os.path.basename(filepath)
    file_root, _ = os.path.splitext(base_name)

    count = 0
    for i, (lang, code_text) in enumerate(code_blocks, start=1):
        ext = determine_extension(lang)
        output_name = f"{file_root}_block{i}.{ext}"
        output_path = os.path.join(OUTPUT_DIR, output_name)
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(code_text)
        count += 1
    return count

def main():
    if not os.path.exists(MEMORY_DIR):
        print(f"[WARNING] Memory folder not found: {MEMORY_DIR}")
        return
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [f for f in os.listdir(MEMORY_DIR) if f.lower().endswith(('.md', '.txt', '.log'))]
    total_extracted = 0
    for filename in files:
        path = os.path.join(MEMORY_DIR, filename)
        extracted_count = process_file(path)
        if extracted_count > 0:
            print(f"[OK] Extracted {extracted_count} code block(s) from {filename}")
            total_extracted += extracted_count

    if total_extracted == 0:
        print("[INFO] No code blocks found in any files.")
    else:
        print(f"[DONE] Total extracted code blocks: {total_extracted}")

if __name__ == "__main__":
    main()
