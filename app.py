"""Vercel entrypoint: re-export the FastAPI app.

Vercel's Python runtime detects this file, loads `app` as the ASGI
application, and routes every request to it. Local runs are unchanged
(run `uvicorn backend.main:app` as before).

The browser auto-open thread is gated on VERCEL inside backend/main.py.
"""
from backend.main import app
