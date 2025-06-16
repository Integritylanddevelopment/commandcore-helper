# Scripts Documentation

Below is a list of each script in `/HUB_scripts/` and its purpose:

## auto_document.py

Generates documentation for the project by scanning files for docstrings and comments. Outputs the documentation in Markdown format.

## deploy_commandcore.bat

Batch script to deploy the CommandCore system. Automates deployment tasks.

## extract_scripts.py

Scans text files in `/memory/` for Markdown code blocks (triple backticks). Extracts each code block into a separate file within `/logs/extracted_scripts/`.

## firebase_deploy.bat

Batch script to deploy the project to Firebase. Handles Firebase-specific deployment tasks.

## generate_readme_from_logs.py

Scans the `/logs/` directory for session logs and compiles them into a README-friendly summary. Saves or prints output to the console.

## index_memory_whoosh.py

Creates a Whoosh-based full-text search index from the files in `/memory/`. Files indexed include `.md`, `.txt`, and `.log`.

## merge_logs.py

Searches for duplicate or overlapping logs in `/memory/` and `/logs/`. Merges them to ensure a clean, non-redundant set of files.

## run_all.bat

Batch script to execute all key processes in sequence. Useful for initializing or testing the system.

## search_index_whoosh.py

Searches the Whoosh index created by `index_memory_whoosh.py`. Supports context lines and ANSI highlighting for matched terms.

## summarize_sessions.py

Generates a simple summarization of each file in `/memory/`. Saves the result to `/logs/session_summaries.md`.

## sync_to_gdrive.py

Scans text files in `/memory/` for Markdown code blocks and extracts them into `/logs/extracted_scripts/`.

## test_openai.py

Tests the OpenAI API integration. Useful for debugging and verifying API functionality.

## validate_hub.py

Checks for the required CommandCore-Hub folder structure and exits with an error code if something is missing.
