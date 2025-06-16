# CommandCore Hub

CommandCore Hub is a local, persistent memory system for coordinating development of the CommandCore OS. 
It preserves logs, scripts, and references so that ongoing ChatGPT sessions can pick up where they left off.

---

## Quick Start

1. **Index your files:**  
   Run `python scripts/index_memory_whoosh.py` to build the Whoosh index.

2. **Launch the Hub:**  
   Run `python launch/launch.py` and follow the prompts.

3. **Search the index:**  
   - In VS Code, press `Ctrl+Shift+B` to run the CLI search task.
   - Or run `python scripts/search_index_whoosh.py "your query"` (add `--fuzzy` for fuzzy search).

---

## Folder Overview

1. **memory/**  
   - Stores summaries of past work or crucial references.
