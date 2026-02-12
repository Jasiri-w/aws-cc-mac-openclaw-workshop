import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from faster_whisper import WhisperModel
from openai import OpenAI


ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT / "frontend"

WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL", "tiny.en")
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPPORTED_WHISPER_MODELS = {"tiny.en", "base"}

app = FastAPI(title="AI Notes Workshop App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

_whisper_models: dict[str, WhisperModel] = {}


def get_whisper_model(model_name: str) -> WhisperModel:
    if model_name not in _whisper_models:
        _whisper_models[model_name] = WhisperModel(
            model_name,
            device="cpu",
            compute_type=WHISPER_COMPUTE_TYPE,
        )
    return _whisper_models[model_name]


def transcribe_audio_file(file_path: str, whisper_model: str) -> str:
    model = get_whisper_model(whisper_model)
    segments, _ = model.transcribe(file_path, vad_filter=True, beam_size=1)
    transcript = " ".join(segment.text.strip() for segment in segments).strip()
    return transcript


def confidence_note_for_transcript(transcript: str) -> str:
    words = transcript.split()
    if not words:
        return "Low confidence: no speech detected."
    if len(words) < 12:
        return "Low confidence: transcript is very short; try clearer audio."
    if len(words) < 35:
        return "Medium confidence: transcript captured limited context."
    return "Higher confidence: transcript length is sufficient for summary quality."


def validate_whisper_model(model_name: str) -> str:
    if model_name in SUPPORTED_WHISPER_MODELS:
        return model_name
    return WHISPER_MODEL_NAME


def fallback_summary(text: str) -> str:
    words = text.split()
    if len(words) <= 40:
        return text
    return " ".join(words[:40]) + "... (fallback summary)"


async def summarize_with_ollama(text: str) -> Optional[str]:
    prompt = (
        "You are an assistant that summarizes notes. Return short bullet points.\n\n"
        f"Notes:\n{text}"
    )
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
            res.raise_for_status()
            data = res.json()
            return data.get("message", {}).get("content")
    except Exception:
        return None


def summarize_with_openai(text: str) -> Optional[str]:
    if not OPENAI_API_KEY:
        return None
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Summarize notes into concise bullet points with action items.",
                },
                {"role": "user", "content": text},
            ],
        )
        return completion.choices[0].message.content
    except Exception:
        return None


async def summarize_text(text: str) -> str:
    if not text.strip():
        return "No transcript text was detected. Record a clearer voice sample and try again."

    ollama_result = await summarize_with_ollama(text)
    if ollama_result:
        return ollama_result

    openai_result = summarize_with_openai(text)
    if openai_result:
        return openai_result

    return fallback_summary(text)


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/api/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    whisper_model: str = Form(WHISPER_MODEL_NAME),
):
    whisper_model = validate_whisper_model(whisper_model)
    suffix = Path(audio.filename or "recording.webm").suffix or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = tmp.name
        tmp.write(await audio.read())
    try:
        transcript = transcribe_audio_file(tmp_path, whisper_model=whisper_model)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {exc}") from exc
    finally:
        os.unlink(tmp_path)

    if not transcript:
        return {
            "transcript": "",
            "confidence_note": confidence_note_for_transcript(transcript),
            "warning": "No speech detected in the recording. Try speaking closer to the mic.",
            "whisper_model": whisper_model,
        }

    return {
        "transcript": transcript,
        "confidence_note": confidence_note_for_transcript(transcript),
        "whisper_model": whisper_model,
    }


@app.post("/api/summarize")
async def summarize(text: str = Form(...)):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    summary = await summarize_text(text)
    return {"summary": summary}


@app.post("/api/process")
async def process(
    audio: UploadFile = File(...),
    whisper_model: str = Form(WHISPER_MODEL_NAME),
):
    whisper_model = validate_whisper_model(whisper_model)
    suffix = Path(audio.filename or "recording.webm").suffix or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = tmp.name
        tmp.write(await audio.read())
    try:
        transcript = transcribe_audio_file(tmp_path, whisper_model=whisper_model)
        if not transcript:
            return {
                "transcript": "",
                "summary": "No transcript text was detected. Try a short direct microphone recording.",
                "confidence_note": confidence_note_for_transcript(transcript),
                "warning": "No speech detected in the recording.",
                "whisper_model": whisper_model,
            }
        summary = await summarize_text(transcript)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing failed: {exc}") from exc
    finally:
        os.unlink(tmp_path)
    return {
        "transcript": transcript,
        "summary": summary,
        "confidence_note": confidence_note_for_transcript(transcript),
        "whisper_model": whisper_model,
    }


@app.get("/api/preflight")
async def preflight(whisper_model: str = WHISPER_MODEL_NAME):
    whisper_model = validate_whisper_model(whisper_model)

    mic_hint = {
        "ok": None,
        "detail": "Mic availability is checked in-browser by the frontend.",
    }

    ollama = {"ok": False, "detail": "unreachable"}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get(f"{OLLAMA_URL}/api/tags")
            res.raise_for_status()
            ollama = {"ok": True, "detail": "reachable"}
    except Exception as exc:
        ollama = {"ok": False, "detail": str(exc)}

    whisper = {"ok": False, "detail": "not loaded", "model": whisper_model}
    try:
        get_whisper_model(whisper_model)
        whisper = {"ok": True, "detail": "loaded", "model": whisper_model}
    except Exception as exc:
        whisper = {"ok": False, "detail": str(exc), "model": whisper_model}

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "mic": mic_hint,
        "ollama": ollama,
        "whisper": whisper,
    }
