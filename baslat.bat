@echo off
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js bulunamadi. https://nodejs.org adresinden kurun.
  pause
  exit /b 1
)
start "" /b cmd /c "timeout /t 1 /nobreak >nul & start http://localhost:5173"
node server.js
pause
