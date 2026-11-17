"""Polyglot — Programming Language Identifier (FastAPI backend).

No login, no accounts: a public lab tool. The engine trains 3 models on
data.csv at startup and retrains whenever snippets are added.
"""
import os
import random
import shutil
import tempfile
import threading
import webbrowser
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    # When run from inside backend/ as `uvicorn main:app`
    from model import LANGUAGES, Engine, length_bucket
except ImportError:
    # When run from the project root as `uvicorn backend.main:app`
    from backend.model import LANGUAGES, Engine, length_bucket

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND = os.path.join(BASE, "frontend")


def _open_browser_when_ready():
    """Open the app in Chrome (or the default browser) once the server is up.

    Runs in a background thread at startup, so the server works the same
    no matter how it was started (run.bat, run.sh, or plain uvicorn) —
    no manual tab needed.

    Wait for Polyglot's own port (8001) for the full window BEFORE ever
    trying 8000. That order matters: uvicorn runs the app's lifespan
    startup before it binds the listening socket, so on the first poll
    8001 is not up yet. If an old project (e.g. NoteWise) is still
    listening on 8000, grabbing whichever port answers first would open
    the wrong app. Only if 8001 never appears do we fall back to 8000,
    which covers plain `uvicorn backend.main:app` without --port.
    """
    import socket
    import time

    url = None
    for _ in range(12):  # up to ~6s waiting for our own port (8001)
        try:
            with socket.create_connection(("127.0.0.1", 8001), timeout=0.5):
                url = "http://127.0.0.1:8001"
                break
        except OSError:
            time.sleep(0.5)
    if not url:
        for _ in range(4):  # plain uvicorn without --port serves on 8000
            try:
                with socket.create_connection(("127.0.0.1", 8000), timeout=0.5):
                    url = "http://127.0.0.1:8000"
                    break
            except OSError:
                time.sleep(0.5)
    if not url:
        return
    try:
        webbrowser.get("chrome").open(url)
    except Exception:
        try:
            webbrowser.open(url)
        except Exception:
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.environ.get("VERCEL") != "1":
        threading.Thread(target=_open_browser_when_ready, daemon=True).start()
    yield


app = FastAPI(title="Polyglot — Programming Language Identifier", lifespan=lifespan)
engine = Engine()


class PredictRequest(BaseModel):
    code: str
    model: str | None = None


class AddRequest(BaseModel):
    language: str
    code: str


@app.get("/api/health")
def health():
    return {"status": "ok", "models": list(engine.trained.keys()),
            "snippets": int(len(engine.df))}


@app.post("/api/predict")
def predict(req: PredictRequest):
    code = (req.code or "").strip("\n")
    if len(code.strip()) < 3:
        raise HTTPException(status_code=400, detail="Paste a code snippet first (at least a few characters).")
    if req.model and req.model not in engine.trained:
        raise HTTPException(status_code=400, detail=f"Unknown model: {req.model}")
    all_models = engine.predict_all(code)
    best = engine.predict(code, req.model)
    lines = code.count("\n") + 1
    return {
        "language": best["language"],
        "confidence": round(best["confidence"], 4),
        "model": best["model"],
        "top3": [{**t, "probability": round(t["probability"], 4)} for t in best["top3"]],
        "votes": all_models["votes"],
        "models": {
            name: {
                "language": r["language"],
                "confidence": round(r["confidence"], 4),
                "top3": [{**t, "probability": round(t["probability"], 4)} for t in r["top3"]],
            }
            for name, r in all_models["models"].items()
        },
        "length": {"lines": lines, "chars": len(code), "bucket": length_bucket(code)},
    }


@app.get("/api/models")
def models():
    ev = engine.evaluation
    return {"best_model": ev["best_model"], "models": ev["models"]}


@app.get("/api/evaluate")
def evaluate():
    return engine.evaluation


@app.get("/api/dataset")
def dataset():
    return engine.dataset_stats()


@app.get("/api/samples/{language}")
def samples(language: str):
    if language not in LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unknown language: {language}")
    pool = engine.df[engine.df["language"] == language]["code"].tolist()
    if not pool:
        return {"language": language, "sample": ""}
    return {"language": language, "sample": random.choice(pool)}


@app.post("/api/dataset/add")
def add_snippet(req: AddRequest):
    try:
        row = engine.add_snippet(req.language, req.code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"added": row, "stats": engine.dataset_stats(),
            "message": "Snippet added and all 3 models retrained."}


@app.post("/api/dataset/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file with columns: language,code")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(file.file, tmp)
        path = tmp.name
    try:
        added = engine.add_csv(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        os.unlink(path)
    return {"added": added, "stats": engine.dataset_stats(),
            "message": f"{added} snippets added and all 3 models retrained."}


@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND, "index.html"))


app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


if __name__ == "__main__":
    import uvicorn

    # Port 8001: the other projects (SupervisorMatch, NoteWise, SpamShield)
    # use 8000, so Polyglot gets its own port and never opens the wrong app.
    uvicorn.run(app, host="127.0.0.1", port=8001)
