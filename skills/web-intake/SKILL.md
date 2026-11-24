---
name: web-intake
description: "Get content from the internet and break it down. Use when the user gives a YouTube URL and wants it broken down (transcript, structure, hook, key moments, script formula, \"analyze this video\", \"break down this video\", \"steal this structure\"), or an Instagram Reel or post URL (instagram.com/reel/ or /p/, \"xem reel này\", \"phân tích reel\", \"reel này nói gì\", \"transcribe this Instagram video\"), or wants to research, search or look something up online (调研, 搜索, 查, 找, 全网调研, \"look up\", \"research this topic\", tra cứu, tìm hiểu), or shares any other URL or mentions a platform such as Xiaohongshu, Twitter/X, Bilibili, Reddit, Facebook, V2EX, LinkedIn, Boss, jobs, GitHub code search, podcasts, stocks, RSS or web pages. Read-only: no posting, commenting or liking."
---

# web-intake

This bundle merges three skills for pulling content off the web. **This file holds the final decisions.** The `sources/` folder keeps each original unchanged except that `SKILL.md` was renamed `GUIDE.md`. **When a source file contradicts this file, this file wins.** Read only the source files the task needs.

## 1. Routing

| Task | Read |
|---|---|
| YouTube URL breakdown | `sources/youtube-analyzer/GUIDE.md` |
| Instagram Reel or post URL | `sources/instagram-analyzer/GUIDE.md` |
| Search, research, any other platform or URL, RSS, jobs, finance | `sources/agent-reach/GUIDE.md`, then the matching `sources/agent-reach/references/*.md` (search, social, career, dev, web, video, finance) only when needed |

**Dedicated analyzers go first for YouTube and Instagram.** Use agent-reach for those two platforms only when the dedicated analyzer cannot do the job (for example, searching YouTube for videos rather than analyzing a given URL, or a post that is not a video).

### Instagram script path
`instagram-analyzer` is a Python script. Its old `<skill-dir>/scripts/` path is now:

`<installed skill dir>/sources/instagram-analyzer/scripts/analyze_reel.py`

where `<installed skill dir>` is the folder that holds this `web-intake` SKILL.md (for example `~/.claude/skills/web-intake`). Resolve it to a real absolute path before running.

## 2. Final decisions

### Transcription
1. **Run locally first** with faster-whisper (the Instagram script does this already; do the same for YouTube audio).
2. Send audio to a **cloud API** (agent-reach transcribe with Groq or OpenAI) **only after the user agrees**. Say what will be uploaded and to whom, then wait for a yes.
3. **YouTube without captions: do not stop.** Download the audio (yt-dlp) and transcribe it with local Whisper. The youtube-analyzer rule to stop when there are no captions is overruled.

### Working files
Write downloads, transcripts, frames and any scratch output to a **temp folder**: the session scratchpad or `/tmp`. **Never write into the current project folder.** The Instagram script defaults to `./reel-<id>`, so always pass `--out <temp folder>/reel-<id>`. Agent-reach already says to use `/tmp/` and `~/.agent-reach/`; keep that.

### Cookies and logins
- **Try without cookies first.**
- If that fails, say why in one line and **ask before reading browser cookies** (`--cookies-from-browser`, agent-reach cookie setup, browser-profile probing). A cookies.txt the user supplies is also an ask-first step.
- Never ask for a password. Do not post, comment, like or send anything.

### Tools
If a needed tool is missing (yt-dlp, ffmpeg, faster-whisper, agent-reach), install it only after asking, since it changes the user's machine. If you cannot install, report exactly what is missing and what you could still do.

### Output language
Answer in the user's language, even when the video, page or source is in another language. Quote short source lines in the original language only when the exact wording matters.
