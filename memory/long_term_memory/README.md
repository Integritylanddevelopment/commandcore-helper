# full_chat

## Purpose
This subfolder contains chat logs and related scripts.

## Contents
- `full_chat_logs/`: Stores individual chat log files.
- `full_chat_scripts/`: Contains scripts for managing chat logs.

## Interactions
- Interacts with the `logs/Index` subfolder to provide chat logs for indexing.
- Outputs chat logs that are used by the `logs/merged` and `logs/summary` subfolders for further processing.

## Conventions
- Chat log files are named using a timestamp format: `YYYY-MM-DD_HH-MM-description.md`.
- Semantic tags are included in the content to enhance search and indexing capabilities.

## Usage
- Add new chat logs to the `full_chat_logs/` subfolder.
- Use scripts in the `full_chat_scripts/` subfolder to manage and preprocess chat logs.
- Example: Run `rename_chat_logs.py` to standardize file names.

## Notes
- Ensure all chat logs are properly formatted before adding them to the folder.
- Regularly back up the `full_chat_logs/` subfolder to prevent data loss.
