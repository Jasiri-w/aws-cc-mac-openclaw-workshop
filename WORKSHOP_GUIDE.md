# Workshop Guide (Angad Section): Local AI Notes UI

## Objective

Build and run the local AI note-taking module that:
1. captures voice in browser
2. transcribes with local Whisper
3. summarizes with local LLM
4. saves notes locally for iteration during the workshop

## Scope boundary

This section is Step 1 only (Web Dev):
- UI + local AI pipeline
- no AWS persistence/search implementation
- no OpenClaw provisioning implementation

Those are handled by other team roles.

## Timebox (suggested 20-25 min inside the 1-hour workshop)

1. Environment setup (8 min)
2. First end-to-end run (5 min)
3. Model tradeoff demo (5 min)
4. Save/reload notes + Q&A (5-7 min)

## Step-by-step

1. Install dependencies:
```bash
brew install ffmpeg ollama
ollama serve
ollama pull llama3.2:3b
```

2. Start Python app:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --reload-dir app --port 8000
```

3. Open app:
```text
http://localhost:8000
```

4. Demo flow:
- click `Start Recording` and speak a short note (or click `Use Sample Audio`)
- click `Stop Recording`
- click `Transcribe + Summarize`
- inspect transcript + confidence note
- click `Save Note`
- from `Recent Notes`, demo `Load`, `Copy`, and `Download`

## Files to explain live

- `app/frontend/index.html`
  - step-based UX
  - recording, transcribe, summarize actions
  - local note save/load
- `app/main.py`
  - `/api/transcribe` local speech-to-text
  - `/api/summarize` local LLM summary
- `.env.example`
  - local model/runtime configuration

## Suggested talking points

- Why local AI for workshops: cost control, fewer billing issues, realistic dev flow.
- Whisper tradeoff: `tiny.en` (fast) vs `base` (better quality).
- LLM portability: changing `OLLAMA_MODEL` changes summary style/quality.
- Team handoff: this module outputs transcript/summary payload for AWS layer.

## Handoff payload shape

```json
{
  "transcript": "...",
  "summary": "...",
  "confidence_note": "...",
  "whisper_model": "tiny.en"
}
```

## Troubleshooting checklist

1. `ffmpeg` missing -> install with Homebrew.
2. Ollama not responding -> ensure `ollama serve` is running in another terminal.
3. Microphone blocked -> enable site permissions.
4. First run is slow -> model download and warm-up are expected.
