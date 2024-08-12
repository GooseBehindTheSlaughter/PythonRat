@echo off

REM This needs pyinstaller to work if you dont have this then it will fail see https://pyinstaller.org/en/stable/ for installing

pause

pyinstaller --onefile --noconsole client.py

timeout 2