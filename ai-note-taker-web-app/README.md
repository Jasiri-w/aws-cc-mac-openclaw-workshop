# aws-cc-mac-openclaw-workshop

Workshop scaffold for an AI note-taking app:
- record audio in browser
- transcribe locally with Whisper
- summarize locally with an LLM (Ollama)
- model toggle for reliability demos
- save recent notes locally for demo continuity
- hand off clean JSON output to AWS/OpenClaw teammates

## Scope of this repo section (Angad / Step 1)

This implementation focuses only on the local web app + local AI pipeline:
- in-browser recording UI
- local speech-to-text
- local summarization
- local note save/load for iteration

It intentionally does not implement AWS persistence/search or OpenClaw provisioning.

## What this repo includes now

- `app/frontend/index.html`: workshop UI with:
  - whisper model selector (`tiny.en` vs `base`)
  - sample audio fallback button
  - simple step flow (`Record -> Transcribe + Summarize -> Save`)
  - transcript confidence note
  - local saved notes list with copy/download actions
- `app/main.py`: FastAPI backend (`/api/transcribe`, `/api/summarize`, `/api/process`, `/api/preflight`)
- `app/frontend/sample-note.wav`: bundled sample speech clip
- `.env.example`: local config template
- `requirements.txt`: Python dependencies

## Local architecture

1. Browser records audio (`MediaRecorder`) or loads sample clip
2. Audio is posted to local FastAPI backend
3. Backend transcribes using `faster-whisper`
4. Backend summarizes transcript with local Ollama model
5. Output is shown and can be edited/saved locally

## Prerequisites (macOS)

- Python 3.10+ (3.12 recommended for stability)
- `ffmpeg` installed:
  - `brew install ffmpeg`
- Ollama installed and running:
  - `brew install ollama`
  - `ollama serve`
  - `ollama pull llama3.2:3b`

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --reload-dir app --port 8000
```

Open: `http://localhost:8000`

## API endpoints

- `POST /api/transcribe` (multipart form fields `audio`, optional `whisper_model`) -> transcript + confidence
- `POST /api/summarize` (form field `text`) -> summary from transcript text
- `POST /api/process` (multipart form fields `audio`, optional `whisper_model`) -> combined helper endpoint

## Workshop flow for this section (Angad)

1. Students open app and record a short note (10-20s), or click `Use Sample Audio`.
2. Click `Transcribe + Summarize`.
3. Inspect transcript quality and confidence note; switch `tiny.en` vs `base`.
4. Save locally and demo `Load`, `Copy`, and `Download` from recent notes.

## Handoff contract to AWS/OpenClaw teammates

After local processing, pass this payload shape to AWS endpoints:

```json
{
  "transcript": "...",
  "summary": "...",
  "confidence_note": "...",
  "whisper_model": "tiny.en"
}
```

AWS/OpenClaw team can add IDs/timestamps/user metadata server-side.

## Common issues

- `Processing failed` with decoder errors:
  - verify `ffmpeg -version`
- Slow first request:
  - Whisper model download/load happens on first use
- Ollama errors:
  - verify `ollama serve` is running and model exists (`ollama list`)
- Microphone blocked:
  - allow mic permissions in browser settings
