#!/bin/bash
# Polyglot — run the app, then open it in the browser.
cd "$(dirname "$0")"
python -m pip install -q -r requirements.txt
python -c "import uvicorn" 2>/dev/null || python -m pip install -q uvicorn fastapi pandas scikit-learn python-multipart
cd backend
python -m uvicorn main:app --port 8001
