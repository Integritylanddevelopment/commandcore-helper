#!/usr/bin/env python3
"""
merge_logs.py

Searches for duplicate or overlapping logs in /memory/ and /logs/.
Merges them to ensure a clean, non-redundant set of files.

Strategy:
  1. Compute a hash of each file's content.
  2. If two files share the same hash, they are duplicates.
  3. Merge them by appending unique lines from the second into the first, 
     or skip merging if they are byte-for-byte duplicates.
  4. (Optional) remove the duplicate file or rename it.

Note: This simple script merges exact duplicates only (exact same content).
      For partial or content-based merges, you'd need more advanced logic.
"""

import os
import hashlib
import shutil

MEMORY_DIR = os.path.join("..", "memory")
LOGS_DIR = os.path.join("..", "logs")

def file_md5(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest(), buf.decode('utf-8', errors='replace')

def merge_file_contents(original, new_content):
    """
    If the original doesn't contain new_content lines, append them.
    This ensures we preserve all unique lines.
    """
    original_lines = original.splitlines()
    new_lines = new_content.splitlines()
    merged = list(original_lines)  # copy

    # Only append lines that are not already in the original
    for line in new_lines:
        if line not in original_lines:
            merged.append(line)
    return "\n".join(merged)

def process_folder(folder_path):
    # key: md5_hash -> (filename, file_content)
    seen_hashes = {}
    merged_count = 0

    if not os.path.exists(folder_path):
        print(f"[INFO] Folder not found: {folder_path}. Skipping.")
        return 0

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.md', '.txt', '.log'))]
    files = sorted(files)  # consistent order

    for filename in files:
        filepath = os.path.join(folder_path, filename)
        filehash, filecontent = file_md5(filepath)

        if filehash not in seen_hashes:
            # Haven't seen this exact content before
            seen_hashes[filehash] = (filepath, filecontent)
        else:
            # Duplicate detected -> merge
            orig_path, orig_content = seen_hashes[filehash]
            if orig_content == filecontent:
                # Exact duplicate, no difference
                print(f"[DUPLICATE] Removing exact duplicate: {filename}")
                # Replace os.remove with archiving the duplicate file
                archive_path = os.path.join(LOGS_DIR, "archived_duplicates", filename)
                os.makedirs(os.path.dirname(archive_path), exist_ok=True)
                shutil.move(filepath, archive_path)
            else:
                # Different content but same MD5? Rare collision or partial match 
                # We'll attempt to merge line-by-line. 
                new_merged_content = merge_file_contents(orig_content, filecontent)
                with open(orig_path, 'w', encoding='utf-8') as out:
                    out.write(new_merged_content)
                print(f"[MERGED] Appended unique lines from {filename} into {os.path.basename(orig_path)}")
                # Replace os.remove with archiving the duplicate file
                archive_path = os.path.join(LOGS_DIR, "archived_duplicates", filename)
                os.makedirs(os.path.dirname(archive_path), exist_ok=True)
                shutil.move(filepath, archive_path)
                # Update the stored content
                new_hash, final_content = file_md5(orig_path)
                # Overwrite the old hash entry
                seen_hashes.pop(filehash)
                seen_hashes[new_hash] = (orig_path, final_content)
            merged_count += 1
    return merged_count

def main():
    total_merged = 0
    # Merge in memory folder
    merged = process_folder(MEMORY_DIR)
    total_merged += merged

    # Merge in logs folder
    merged = process_folder(LOGS_DIR)
    total_merged += merged

    if total_merged == 0:
        print("[OK] No duplicates found or no merges were performed.")
    else:
        print(f"[DONE] Total merges or deletions: {total_merged}")

if __name__ == "__main__":
    main()
