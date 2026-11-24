---
name: instagram-analyzer
description: Use when the user gives an Instagram Reel (or video post) URL and wants to know what is in it, such as the transcript, what is said and shown, the hook, structure, key moments, on-screen text, or the script formula behind it. Downloads the Reel with yt-dlp, transcribes it locally with Whisper, and pulls keyframes so Claude can see the visuals. Triggers on "/instagram-analyzer" with a URL, any instagram.com/reel/ or /p/ link, "xem reel này", "phân tích reel", "reel này nói gì", "break down this reel", "transcribe this Instagram video".
---

# Instagram Analyzer

Turns an Instagram Reel link into something Claude can actually read: a timestamped transcript, the caption and stats, and a strip of keyframes. Then Claude breaks it down.

## Requirements

- `ffmpeg` on PATH
- `pip install -U yt-dlp faster-whisper` (the script falls back to `openai-whisper` if that is what is installed)
- Network access to instagram.com and, on first run, to huggingface.co to download the Whisper model. Locked-down cloud sandboxes often block both; the script says "network problem" when that happens, so run it on the user's own machine instead.

Check quickly before running:

```bash
ffmpeg -version >/dev/null && python3 -c "import yt_dlp, faster_whisper" && echo ok
```

If something is missing, install it (ask first if you are on the user's own machine).

## Step 1: Run the script

```bash
python3 <installed skill dir>/sources/instagram-analyzer/scripts/analyze_reel.py "<reel-url>" --out <work-dir>/reel-<id>
```

Useful flags:

| Flag | When to use |
|---|---|
| `--cookies-from-browser chrome` | Download fails with "login required", "rate-limit" or 401/403. Use the browser the user is logged into Instagram with. |
| `--cookies cookies.txt` | Same, when browser cookies are not reachable (cloud sessions). The user exports cookies.txt with a browser extension. |
| `--language vi` | Whisper guesses the language wrong, or the Reel mixes Vietnamese and English. |
| `--model medium` | Transcript quality is poor. `small` is the default, `tiny`/`base` are faster. |
| `--frame-every 1` | Fast-cut Reel or heavy on-screen text. Use 3 to 4 for long talking-head videos. |

Instagram often blocks logged-out downloads. Try once without cookies. If it fails, tell the user why in one line and ask for a cookies option. Never ask for their password.

## Step 2: Read the outputs

In the output folder:

- `meta.json`: author, caption, duration, views, likes, comments
- `transcript.txt`: `[mm:ss.s - mm:ss.s] text` per segment
- `frames/t0000.0s.jpg ...`: keyframes, named by timestamp

Read `meta.json` and `transcript.txt` in full. Then look at the frames with the Read tool. Always look at `t0000.0s.jpg` (the hook frame). For a Reel under 60 seconds, look at all of them. For longer ones, look at the first 3 and then sample evenly.

Many Reels have no speech (music plus text on screen). If the transcript is empty, read the on-screen text from the frames and say that the content comes from visuals, not audio.

Whisper makes mistakes with names, brand terms and slang. If something in the transcript looks wrong and a frame or the caption shows the correct spelling, use the correct one and say you fixed it.

## Step 3: Deliver the breakdown

Answer what the user asked. If they only said "xem reel này" or gave a bare link, use this default format and write it in the user's language:

1. **Tóm tắt / Summary**: 2 to 3 sentences on what the Reel says and shows.
2. **Thông số / Stats**: author, duration, views, likes, comments (skip the ones that are null).
3. **Hook (0 to 3s)**: the first line spoken and the first frame's visual or on-screen text. Say why it does or does not stop the scroll.
4. **Cấu trúc / Structure**: beats with timestamps, for example hook, problem, payoff, CTA.
5. **Transcript**: the full cleaned transcript with timestamps. If it is long, put it last.
6. **Text on screen and visuals**: what the frames show that the audio does not.
7. **Công thức / Formula** (only when the user wants to copy the style): a reusable template made from the structure.

Do not invent numbers. If yt-dlp did not return a stat, leave it out.

## Cleanup

`video.mp4` can be large. Leave the folder in place unless the user asks to delete it, and tell them where it is.

## Limits

- Private accounts and Stories need cookies from an account that can see them.
- Image-only posts have no audio. The script skips transcription and the transcript comes back empty. Read the frames, or ask the user for screenshots.
- Use this for analysis and personal reference. Reposting someone else's video needs the creator's permission.
