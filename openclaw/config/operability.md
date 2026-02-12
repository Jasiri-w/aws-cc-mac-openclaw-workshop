# How Hatch Works - User Guide

## Overview
Hatch is your AI assistant for the McMaster AWS Cloud Club workshop. It helps you build, debug, and understand the note-taking + OpenClaw system.

---

## How to Interact with Hatch

### Via Discord (Easiest)
1. **Mention Hatch** in any message:
   ```
   @Hatch what's the difference between IAM roles and policies?
   ```
2. **Ask anything workshop-related** — it will respond in the thread
3. **Use follow-ups** for clarification

### Via Direct Message
- Send a DM to Hatch for private questions
- Useful for troubleshooting or detailed discussions

---

## What Hatch Can Do

### 📚 Answer Questions
- AWS concepts (EC2, S3, IAM, VPC, etc.)
- OpenClaw architecture and usage
- Discord bot best practices
- Python FastAPI and local AI (Whisper, Ollama)

### 🐛 Help With Debugging
- **Stuck on an error?** Share the error message
  ```
  @Hatch I'm getting "Permission denied (publickey)" when SSH-ing
  ```
- Hatch will suggest solutions based on the workshop guides

### 💡 Provide Context
- Hatch can read your meeting summaries and notes
- Ask it to summarize or interpret stored information
  ```
  @Hatch What were the key deadlines from my COMP 2101 class?
  ```

### 🎯 Guide Next Steps
- Ask what to do next in the workshop
- Get tips for optimizing your implementation
  ```
  @Hatch What should I do after deploying my bot?
  ```

---

## Example Conversations

### Example 1: Learning
```
You: @Hatch explain what an IAM role is
Hatch: An IAM role is a permission set for AWS services. Unlike IAM users (which have credentials), 
roles are attached to resources like EC2 instances. Your instance assumes the role and gets permissions 
automatically. This is safer than hardcoding credentials.
```

### Example 2: Troubleshooting
```
You: @Hatch The Discord bot is not responding. I created the token and updated the config.
Hatch: Let's debug:
1. Is the OpenClaw process running? Check: ps aux | grep openclaw
2. Did you restart the gateway after updating config? Try: npx openclaw gateway restart
3. Is the bot actually in your Discord server? Verify in server settings.
Send me the output of those commands and we'll dig deeper.
```

### Example 3: Context-Aware Help
```
You: @Hatch summarize the meeting summaries in S3
Hatch: Based on your stored files:
- COMP 2101: Computational systems course with midterm on Oct 17 and cloud project due Dec 3
- MDIA 1020: Media literacy with research essay due Nov 28
- CS 3202: Machine learning with capstone project due Dec 16
```

---

## Tips for Best Results

1. **Be Specific** — "I'm getting an error" is less helpful than providing the error message
2. **Provide Context** — Tell Hatch which step of the workshop you're on
3. **Ask Follow-ups** — Hatch remembers the conversation thread
4. **Use Keywords** — Mention "AWS," "Discord," "local app," etc. to stay focused
5. **Try Again** — If Hatch doesn't understand, rephrase or break into smaller questions

---

## What Hatch Cannot Do

- ❌ Access your actual AWS account or make changes
- ❌ Provide sensitive passwords or API keys (and won't store them)
- ❌ Replace the workshop guides for official documentation
- ❌ Guarantee real-time accuracy (especially for rapidly changing AWS features)
- ❌ Solve non-workshop-related problems

---

## Common Questions

**Q: How do I know Hatch has access to my notes and meetings?**  
A: Hatch reads files you've uploaded to the `openclaw/` folder (meeting_summaries, notes, config). It doesn't access your email or other systems.

**Q: Can Hatch help me with other projects?**  
A: Hatch is specialized for this workshop. For unrelated help, ask in the general AWS Cloud Club channel.

**Q: What if Hatch gives me incorrect information?**  
A: Check the workshop guides (`openclaw-guide.md`, `web-app-guide.md`) as the source of truth. Report discrepancies in the Discord channel.

---

**Happy building! 🚀**
