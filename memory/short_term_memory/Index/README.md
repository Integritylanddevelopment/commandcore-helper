# Index

## Purpose
This subfolder handles indexing of files and metadata.

## Contents
- `index_log/`: Stores indexed metadata in JSON and markdown formats.
- `index_script/`: Contains scripts for managing the indexing process.

## Interactions
- Interacts with the `full_chat` folder to index chat logs.
- Outputs indexed metadata to `index_log.json` and `index_log.md`.

## Conventions
- JSON files follow a schema with fields like `name`, `path`, `size`, `last_modified`, and `semantic_tags`.
- Markdown files are human-readable summaries of the JSON index.

## Usage
- Use `index_script/index_scrpt.py` to update the index.
- Example: Run the script to index new markdown files in the `full_chat_logs` folder.

## Notes
- Ensure the JSON schema is consistent to avoid compatibility issues.
- Regularly back up the `index_log.json` file to prevent data loss.
