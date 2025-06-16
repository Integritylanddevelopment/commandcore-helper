# Summary: Data extraction protocol.md

**Source Path:** D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/full_chat/full_chat_logs\Data extraction protocol.md

## 1. Extract in Logical Groups (Line 102)
- Divide the archive into smaller, clearly defined groups by file type. (Line 103)
- Each group must be processed one at a time to avoid overload or missed files. (Line 104)

## 2. Sequential Confirmation (Line 106)
- After each group is processed, confirm extraction success before continuing. (Line 107)
- Do not proceed to the next group until explicitly confirmed. (Line 108)

## 3. Grouping Sequence (can expand) (Line 110)
- Group 1: Markdown Files (`.md`) (Line 111)
- Group 2: Plain Text Files (`.txt`) (Line 112)
- Group 3: JSON or Config Files (`.json`, `.config`, `.ini`) (Line 113)
- Group 4: JavaScript or Code Files (`.js`, `.ts`, `.py`, `.java`, `.cpp`) (Line 114)
- Group 5: Stylesheets (`.css`, `.scss`, `.less`) (Line 115)
- Group 6: HTML/XML Files (`.html`, `.htm`, `.xml`) (Line 116)
- Group 7: Media Files (`.png`, `.jpg`, `.jpeg`, `.svg`, `.gif`, `.mp3`, `.wav`, `.mp4`) (Line 117)
- Group 8: Archive Files (`.zip`, `.rar`, `.7z`, `.tar.gz`) (Line 118)
- Group 9: Logs and Reports (`.log`, `.out`, `.report`, `.csv`, `.tsv`) (Line 119)
- Group 10: Misc Config & Metadata (`.env`, `.yaml`, `.yml`, `.toml`, `.lock`, `.bat`, `.sh`) (Line 120)

## 4. Standardization and Cleanup (Line 122)
- Deduplicate any overlapping or cloned files. (Line 123)
- Normalize file names for readability and traceability. (Line 124)
- Convert files to UTF-8 if encoding is inconsistent. (Line 125)
- Ensure consistent line endings (LF preferred). (Line 126)

## 5. Integrity Check (COMPLETE-YES-CHECK) (Line 128)
- [ ] No placeholder files (e.g., "template.md", "placeholder.txt") (Line 129)
- [ ] No blank or empty files (Line 130)
- [ ] No corrupt or partial files (e.g., truncated JSON) (Line 131)
- [ ] All source code files contain valid syntax and complete logic (Line 132)
- [ ] All config and env files contain real, usable values (Line 133)
- [ ] All media files render/play without error (Line 134)
- [ ] Latest API versions and runtime syntax used (Node, Python, etc.) (Line 135)
- [ ] No dependency links to deprecated or offline sources (Line 136)
- [ ] Files logically belong to the current project (no unrelated content) (Line 137)

## 6. No Emojis or Extra Spacing (Line 139)
- Use **plain text only**. (Line 140)
- No emojis, no decorative formatting. (Line 141)
- One line space max between items. (Line 142)

## 7. Zip Final Output (Line 144)
- Organize the final extracted groups into structured folders. (Line 145)
- Include a `README.md` for clarity. (Line 146)
- Run final validation before zipping. (Line 147)
- Compress into a `.zip` archive using folder name or project title. (Line 148)

## Contextual Tags
- Original Log: Data extraction protocol.md
- Source Path: D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/full_chat/full_chat_logs\Data extraction protocol.md
