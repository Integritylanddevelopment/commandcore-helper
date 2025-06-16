@echo off
echo Launching CommandCore Memory Hub...

REM OPTIONAL: Insert any steps needed to initialize environment variables or start local services
REM For example, you could open your local text editor or a terminal automatically.

echo Opening local folder structure...
explorer ..\

echo (Optional) Syncing with GitHub...
call sync_to_github.bat

echo CommandCore Hub is now live.
pause

:: 🛠 DEVELOPER NOTE FOR GITHUB COPILOT:
:: STOP chaining commands like "activate && pip list" in PowerShell — this is a Unix-style syntax.
:: PowerShell uses `;` for command separation.
::
:: EXPECTED BEHAVIOR:
:: Use the following format in PowerShell terminals:
::     .\venv\Scripts\activate
::     pip install -r requirements.txt
::
:: IF YOU MUST COMBINE:
::     .\venv\Scripts\activate; pip install -r requirements.txt
::
:: DO NOT assume pip is available until the virtual environment is activated.
:: DO NOT rely on Unix-style && or Bash behavior in Windows PowerShell scripts.
::
:: ACTION REQUESTED:
:: Update all startup/setup-related scripts or terminal suggestions
:: to follow PowerShell conventions when on Windows systems.
::
:: OPTIONAL IMPROVEMENT:
:: Add cross-platform detection to adjust for PowerShell vs Bash vs CMD context.

