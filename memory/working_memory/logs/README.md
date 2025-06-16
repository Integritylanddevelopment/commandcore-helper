# logs

## Purpose
This subfolder contains logs and related scripts for indexing, merging, and summarizing data.

## Contents
- `Index/`: Handles indexing of files.
- `merged/`: Stores merged logs.
- `readme/`: Contains readme-related logs.
- `schema/`: Manages schema definitions.
- `scripts/`: Contains scripts for log processing.
- `search/`: Handles search-related logs.
- `summary/`: Stores summary logs.

## Interactions
- Interacts with the `full_chat` subfolder to process chat logs for indexing and merging.
- Provides data to the `memory_sys_scripts` subfolder for system-level operations.
- Outputs processed logs and summaries for use in search and analysis tasks.

## Conventions
- Subfolders follow a modular structure, each dedicated to a specific task (e.g., indexing, merging, summarizing).
- File names include timestamps and descriptive labels for clarity.

## Usage
- Use scripts in the `scripts/` subfolder to process logs.
- Example: Run `merge_logs.py` to consolidate logs from multiple sources.
- Refer to individual subfolder `README.md` files for detailed usage instructions.

## Notes
- Regularly back up critical files like `index_log.json` to prevent data loss.
- Ensure all logs are properly formatted before processing to avoid errors.
