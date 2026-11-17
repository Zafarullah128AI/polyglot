@echo off
REM Polyglot — run the app, then open it in the browser.
cd /d %~dp0
python -m pip install -q -r requirements.txt
cd backend
python -m uvicorn main:app --port 8001
