# AWS Cloud Club: OpenClaw Workshop

A hands-on workshop for building an AI-powered note-taking system and cloud-hosted Discord bot.

## Project Overview

This workshop walks through two main components:

1. **Local AI Note-Taker Web App** — Record audio in your browser, transcribe locally with Whisper, and summarize with a local LLM
2. **OpenClaw on AWS EC2 + Discord** — Deploy a cloud-hosted AI agent connected to OpenAI's GPT API and Discord, with persistent S3 storage

## Quick Start

### Web App (Local Development)
```bash
cd ai-note-taker-web-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Then open: `http://localhost:8000`

### Workshop Guides

Detailed step-by-step guides are in the [`workshop/`](workshop/) folder:

- **[OpenClaw Guide](workshop/openclaw-guide.md)** — Deploy OpenClaw on AWS EC2, connect to OpenAI, integrate with Discord, and add S3 file access skills
- **[Web App Guide](workshop/web-app-guide.md)** — Build and demo the local note-taking module with live model tradeoff showcase

## Project Structure

```
.
├── ai-note-taker-web-app/    # Local web app with FastAPI backend
├── openclaw/                  # OpenClaw agent files (to be configured during workshop)
├── workshop/                  # Detailed workshop guides and screenshots
└── README.md                  # This file
```

## Prerequisites

- AWS account with EC2 permissions
- OpenAI API key
- Discord account
- Python 3.10+
- `ffmpeg` and `ollama` (for local web app)
- SSH client (Windows 10+, macOS, or Linux built-in)

## Estimated Workshop Time

- **Web App (Step 1):** 20–25 minutes
- **OpenClaw + AWS (Step 2+):** 30–40 minutes
- **Full workshop:** ~1 hour

## Support & Troubleshooting

Refer to the [OpenClaw Guide](workshop/openclaw-guide.md#troubleshooting-guide) and [Web App Guide](workshop/web-app-guide.md#common-issues) troubleshooting sections for common issues.

---

**Let's build! 🚀**
