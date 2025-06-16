#!/usr/bin/env python3

import os
import re
from datetime import datetime
import openai

# === CONFIG ===
chat_logs_dir = r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/full_chat/full_chat_logs"
specstory_history_dir = r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/full_chat/full_chat_logs"

# Function to generate a name using OpenAI
openai.api_key = "your_openai_api_key_here"

def generate_name_with_openai(file_content):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Read the following chat log and generate a concise, descriptive name for it:\n{file_content}\nName:",
            max_tokens=10
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating name with OpenAI: {e}")
        return "Unnamed"

# Updated function to extract metadata using OpenAI
def extract_metadata(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Generate name using OpenAI
        generated_name = generate_name_with_openai(content)

        # Extract simple timestamp (month only)
        timestamp_match = re.search(r"\d{4}-(\d{2})", content)
        timestamp = timestamp_match.group(1) if timestamp_match else "00"

        return timestamp, generated_name
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return None, None

# Function to get list of files copied from SpecStory history
def get_specstory_files():
    try:
        return set(os.listdir(specstory_history_dir))
    except Exception as e:
        print(f"Error accessing SpecStory history directory: {e}")
        return set()

# Function to rename files
def rename_chat_logs():
    try:
        specstory_files = get_specstory_files()
        print(f"SpecStory files: {specstory_files}")  # Debugging: Log SpecStory files

        for filename in os.listdir(chat_logs_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(chat_logs_dir, filename)

                # Debugging: Log each file being processed
                print(f"Processing file: {filename}")

                # Skip files copied from SpecStory history
                if filename in specstory_files:
                    print(f"Skipping: {filename} (copied from SpecStory history)")
                    continue

                # Extract metadata
                timestamp, key_phrase = extract_metadata(file_path)
                print(f"Extracted metadata for {filename}: timestamp={timestamp}, key_phrase={key_phrase}")  # Debugging

                # Generate new filename
                if timestamp and key_phrase:
                    new_filename = f"{timestamp}-{key_phrase}.md"
                elif timestamp:
                    new_filename = f"{timestamp}.md"
                elif key_phrase:
                    new_filename = f"{key_phrase}.md"
                else:
                    new_filename = filename  # Keep original name if metadata extraction fails

                # Rename file
                new_file_path = os.path.join(chat_logs_dir, new_filename)
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")
    except Exception as e:
        print(f"Error renaming files: {e}")

if __name__ == "__main__":
    rename_chat_logs()
