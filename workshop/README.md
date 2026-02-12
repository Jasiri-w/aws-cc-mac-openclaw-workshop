# Workshop Guides

This folder contains step-by-step guides for building the OpenClaw workshop project.

## Guides

### 🌐 [Web App Guide](web-app-guide.md)
**For:** Building and running the local AI note-taking web app

- Record audio in your browser
- Transcribe with local Whisper
- Summarize with local LLM (Ollama)
- Save notes locally
- **Time:** ~20–25 minutes

**Start here if:** You're handling the UI/frontend and local AI pipeline

---

### ☁️ [OpenClaw Guide](openclaw-guide.md)
**For:** Deploying OpenClaw on AWS EC2 and connecting it to Discord

- Launch and configure an EC2 instance
- Install OpenClaw and dependencies
- Get API keys (OpenAI, Discord)
- Deploy the Discord bot
- Add S3 file access skills for persistent memory
- **Time:** ~30–40 minutes

**Start here if:** You're handling cloud infrastructure and the Discord bot integration

---

## Workshop Flow

1. **Team 1:** Follow the Web App guide to build and demo the local note-taking UI
2. **Team 2:** Follow the OpenClaw guide to deploy the bot to AWS and Discord
3. **Integration:** Both teams meet to test end-to-end (notes → bot response)

---

**Questions?** Check the troubleshooting sections in each guide.
