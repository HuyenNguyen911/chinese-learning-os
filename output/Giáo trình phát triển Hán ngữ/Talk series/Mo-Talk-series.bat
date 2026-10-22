@echo off
chcp 65001 >nul
cd /d "%~dp0..\..\.."
python ".claude\skills\talk-series\scripts\sync_server.py" %*
pause
