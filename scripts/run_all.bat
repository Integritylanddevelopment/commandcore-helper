@echo off
REM ---------------------------------------------------------------------
REM run_all.bat
REM A single batch file to execute all key scripts in sequence.
REM Adjust filenames/order as needed.
REM ---------------------------------------------------------------------

REM Change directory to where this .bat file is located
cd /d %~dp0

echo [1/9] Validating hub structure...
python scripts\validate_hub.py

echo [2/9] Merging duplicate logs...
python scripts\merge_logs.py

echo [3/9] Summarizing memory logs...
python scripts\summarize_sessions.py

echo [4/9] Extracting code blocks from memory...
python scripts\extract_scripts.py

echo [5/9] Indexing memory with Whoosh...
python scripts\index_memory_whoosh.py

echo [6/9] Syncing to Google Drive (if configured)...
python scripts\sync_to_gdrive.py

echo [7/9] Auto-documenting scripts usage (appends docstrings to README.md)...
python scripts\auto_document.py

echo [8/9] (Optional) Searching Whoosh index (example usage)...
REM python scripts\search_index_whoosh.py "your search query"

echo [9/9] Launching CommandCore interface (CLI/GUI)...
python launcher\launcher.py

echo ---------------------------------------------------------------------
echo Done running all scripts. Press any key to close.
pause
