#!/usr/bin/env python3
"""Download an Instagram Reel, transcribe it with Whisper, and pull keyframes.

Usage:
    python3 analyze_reel.py <reel-url> [--out DIR] [--cookies FILE]
        [--cookies-from-browser BROWSER] [--model small] [--language vi]
        [--frame-every 2]

Writes into the output folder:
    video.mp4         the downloaded Reel
    meta.json         caption, author, duration, view/like/comment counts
    transcript.txt    timestamped transcript, one segment per line
    transcript.json   segments with start/end seconds and text
    frames/           JPEG keyframes, named by timestamp (t0004.0s.jpg)
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def check_tools():
    if not shutil.which("ffmpeg"):
        fail("ffmpeg is not installed. Install it first (apt install ffmpeg / brew install ffmpeg).")
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        fail("yt-dlp is not installed. Run: pip install -U yt-dlp")


def reel_id(url):
    m = re.search(r"instagram\.com/(?:[^/]+/)?(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)", url)
    return m.group(1) if m else "reel"


class _QuietLogger:
    """Swallow yt-dlp's own console output; errors are reported once by fail()."""

    def debug(self, msg):
        pass

    warning = info = error = debug


def download(url, out_dir, cookies, cookies_browser):
    import yt_dlp

    opts = {
        "outtmpl": str(out_dir / "video.%(ext)s"),
        "format": "best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "logger": _QuietLogger(),
    }
    if cookies:
        opts["cookiefile"] = cookies
    if cookies_browser:
        opts["cookiesfrombrowser"] = (cookies_browser,)

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as e:  # yt-dlp raises DownloadError with a readable message
        msg = str(e)
        hint = ""
        if re.search(r"proxy|connect|resolve|timed out", msg, re.I):
            hint = "\nThis is a network problem, not a login problem: this machine cannot reach instagram.com."
        elif re.search(r"login|rate-limit|cookies|401|403", msg, re.I):
            hint = ("\nInstagram wants a logged-in session. Retry with "
                    "--cookies-from-browser chrome (or firefox/safari/edge), "
                    "or export cookies.txt and pass --cookies cookies.txt.")
        fail(f"download failed: {msg}{hint}")

    video = next(out_dir.glob("video.*"), None)
    if not video:
        fail("yt-dlp finished but no video file was written.")

    meta = {
        "url": url,
        "id": info.get("id"),
        "author": info.get("uploader") or info.get("channel"),
        "author_handle": info.get("uploader_id"),
        "caption": info.get("description"),
        "duration_s": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "views": info.get("view_count"),
        "likes": info.get("like_count"),
        "comments": info.get("comment_count"),
        "width": info.get("width"),
        "height": info.get("height"),
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    return video, meta


def extract_audio(video, out_dir):
    audio = out_dir / "audio.wav"
    r = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
         "-vn", "-ac", "1", "-ar", "16000", str(audio)],
    )
    return audio if r.returncode == 0 and audio.exists() else None


def transcribe(audio, model_name, language):
    """Prefer faster-whisper (fast on CPU); fall back to openai-whisper."""
    try:
        from faster_whisper import WhisperModel

        model = WhisperModel(model_name, device="auto", compute_type="int8")
        segs, info = model.transcribe(str(audio), language=language, vad_filter=True)
        segments = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segs]
        return segments, info.language
    except ImportError:
        pass

    try:
        import whisper
    except ImportError:
        fail("No Whisper backend found. Run: pip install -U faster-whisper "
             "(or pip install -U openai-whisper).")

    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio), language=language)
    segments = [{"start": s["start"], "end": s["end"], "text": s["text"].strip()}
                for s in result["segments"]]
    return segments, result.get("language")


def fmt_ts(sec):
    m, s = divmod(sec, 60)
    return f"{int(m):02d}:{s:04.1f}"


def extract_frames(video, out_dir, every, duration):
    frames = out_dir / "frames"
    frames.mkdir(exist_ok=True)
    # Always grab 0.0s (the hook frame), then one frame every `every` seconds.
    duration = duration or 60
    t = 0.0
    while t < duration:
        name = frames / f"t{t:06.1f}s.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t}", "-i", str(video),
             "-frames:v", "1", "-vf", "scale=540:-2", "-q:v", "4", str(name)],
            check=False,
        )
        t += every
    return sorted(frames.glob("*.jpg"))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url")
    p.add_argument("--out", help="output folder (default: ./reel-<id>)")
    p.add_argument("--cookies", help="Netscape cookies.txt exported from a logged-in browser")
    p.add_argument("--cookies-from-browser", help="chrome, firefox, safari, edge, brave ...")
    p.add_argument("--model", default="small", help="Whisper model: tiny, base, small, medium, large-v3")
    p.add_argument("--language", default=None, help="force language code, e.g. vi or en (default: auto)")
    p.add_argument("--frame-every", type=float, default=2.0, help="seconds between keyframes")
    p.add_argument("--no-frames", action="store_true")
    a = p.parse_args()

    if "instagram.com" not in a.url:
        fail("this does not look like an Instagram URL.")
    check_tools()

    out_dir = Path(a.out or f"reel-{reel_id(a.url)}").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] Downloading {a.url}")
    video, meta = download(a.url, out_dir, a.cookies, a.cookies_from_browser)

    print("[2/4] Extracting audio")
    audio = extract_audio(video, out_dir)

    print(f"[3/4] Transcribing with Whisper ({a.model})")
    if audio:
        segments, lang = transcribe(audio, a.model, a.language)
    else:
        print("      no audio track found, skipping transcription")
        segments, lang = [], None
    (out_dir / "transcript.json").write_text(
        json.dumps({"language": lang, "segments": segments}, ensure_ascii=False, indent=2))
    lines = [f"[{fmt_ts(s['start'])} - {fmt_ts(s['end'])}] {s['text']}" for s in segments]
    (out_dir / "transcript.txt").write_text("\n".join(lines) + "\n")
    if audio:
        audio.unlink(missing_ok=True)

    frames = []
    if not a.no_frames:
        print(f"[4/4] Extracting keyframes every {a.frame_every}s")
        frames = extract_frames(video, out_dir, a.frame_every, meta.get("duration_s"))

    print("\nDONE")
    print(f"folder:     {out_dir}")
    print(f"duration:   {meta.get('duration_s')}s | language: {lang} | segments: {len(segments)}")
    print(f"frames:     {len(frames)}")
    if not segments:
        print("note:       no speech detected (music-only or text-on-screen Reel). Rely on frames + caption.")


if __name__ == "__main__":
    main()
