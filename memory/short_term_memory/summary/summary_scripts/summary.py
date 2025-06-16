#!/usr/bin/env python3
"""
summarize_sessions.py

Generates human-readable summaries of session logs stored in /memory/logs/ and /memory/full_chat/full_chat_logs/.
Summaries are stored in /memory/summaries/.

Now supports:
- .log and .md files
- YAML frontmatter (source, tags, timestamp)
"""

import os
import re
import yaml

BASE_DIR = os.path.dirname(__file__)
LOGS_DIRS = [
    r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/full_chat/full_chat_logs"
]
SUMMARIES_DIR = r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/logs/summary/summary_logs"


def parse_log_file(filepath):
    """Extract headings, bullet points, and their line numbers from the log file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.readlines()

    content_by_heading = {}
    current_heading = None
    heading_start_line = None

    for i, line in enumerate(content):
        heading_match = re.match(r"^#+\s*(.+)$", line)
        if heading_match:
            # Save the previous heading's content
            if current_heading:
                content_by_heading[current_heading]['content'] = current_heading_content

            # Start a new heading
            current_heading = heading_match.group(1)
            heading_start_line = i + 1  # Line numbers are 1-based
            current_heading_content = []
            content_by_heading[current_heading] = {
                'start_line': heading_start_line,
                'content': []
            }
        elif current_heading:
            # Collect bullet points or lines under the current heading
            bullet_match = re.match(r"^[-*]\s*(.+)$", line)
            if bullet_match:
                current_heading_content.append((bullet_match.group(1), i + 1))

    # Save the last heading's content
    if current_heading:
        content_by_heading[current_heading]['content'] = current_heading_content

    return {
        "filename": os.path.basename(filepath),
        "source_path": filepath,
        "sections": content_by_heading
    }

def generate_summary(data):
    """Create a human-readable summary with line numbers from parsed log data."""
    summary = f"# Summary: {data['filename']}\n\n"
    summary += f"**Source Path:** {data['source_path']}\n\n"
    for heading, details in data['sections'].items():
        summary += f"## {heading} (Line {details['start_line']})\n"
        for point, line in details['content']:
            summary += f"- {point} (Line {line})\n"
        summary += "\n"

    # Add contextual tags for traceability
    summary += "## Contextual Tags\n"
    summary += f"- Original Log: {data['filename']}\n"
    summary += f"- Source Path: {data['source_path']}\n"
    return summary

def save_summary(filename, summary):
    """Save the summary to the summaries directory in Markdown format."""
    os.makedirs(SUMMARIES_DIR, exist_ok=True)
    summary_path = os.path.join(SUMMARIES_DIR, filename.replace(".log", ".md").replace(".md", "_summary.md"))
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)

def generate_summary_from_file(file_path):
    """Generate a summary string from a given log file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if os.path.getsize(file_path) == 0:
        raise ValueError(f"File is empty: {file_path}")

    parsed_data = parse_log_file(file_path)
    return generate_summary(parsed_data)

def process_logs():
    """Process all log files from multiple directories and generate summaries."""
    for log_dir in LOGS_DIRS:
        if not os.path.isdir(log_dir):
            continue
        for file in os.listdir(log_dir):
            if file.endswith((".log", ".md")):
                filepath = os.path.join(log_dir, file)
                try:
                    summary = generate_summary_from_file(filepath)
                    save_summary(file, summary)
                except (FileNotFoundError, ValueError) as e:
                    print(f"[ERROR] {e}")
