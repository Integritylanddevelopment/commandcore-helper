@echo off
echo Starting Firebase Deploy...

REM Run 'firebase deploy' or your custom command. Example:
REM firebase deploy --only hosting

if %ERRORLEVEL% NEQ 0 (
    echo Firebase deploy failed! Logging to /logs/
    echo [ERROR] Firebase deploy failed at %DATE% %TIME% >> ..\logs\firebase_deploy_error.log
) else (
    echo Firebase deploy succeeded! >> ..\logs\firebase_deploy_success.log
)

pause
