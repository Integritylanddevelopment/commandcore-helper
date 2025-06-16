# memory_sys_scripts

## Purpose
This subfolder contains system-level scripts for managing the memory system.

## Contents
- `orchestrator.py`: Coordinates memory-related tasks.
- `whoosh_index/`: Contains scripts for search indexing.

## Interactions
- Coordinates with the `logs` subfolder to manage indexing, merging, and summarization tasks.
- Interacts with the `full_chat` subfolder to process chat logs for indexing and search.
- Outputs processed data to the `whoosh_index` subfolder for search indexing.

## Conventions
- Scripts follow a modular design to ensure reusability and clarity.
- File names are descriptive and indicate their primary function (e.g., `orchestrator.py`).

## Usage
- Use `orchestrator.py` to coordinate memory-related tasks across subfolders.
- Example: Run `orchestrator.py` to trigger indexing, merging, and summarization workflows.
- Use scripts in the `whoosh_index` subfolder to manage search indexing.

## Notes
- Ensure all dependencies are installed before running scripts (refer to `requirements.txt`).
- Regularly update scripts to incorporate new features or fix bugs.
