#!/usr/bin/env python3
"""
Helius-002 字幕/转录工具
支持：yt-dlp 字幕下载 + Whisper API 转录 + 字幕清理
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

VIDEO_ID_RE = re.compile(r"\[(?P<id>[A-Za-z0-9_-]{11})\]")


def extract_video_id(name: str) -> str:
    m = VIDEO_ID_RE.search(name)
    return m.group("id") if m else ""


def resolve_ytdlp_cmd() -> list[str]:
    binary = shutil.which("yt-dlp")
    if binary:
        return [binary]
    return [sys.executable, "-m", "yt_dlp"]


def resolve_ffmpeg_cmd() -> list[str]:
    binary = shutil.which("ffmpeg")
    if binary:
        return [binary]
    try:
        import imageio_ffmpeg
        return [imageio_ffmpeg.get_ffmpeg_exe()]
    except Exception:
        return ["ffmpeg"]


def resolve_ffmpeg_location() -> str | None:
    cmd = resolve_ffmpeg_cmd()
    return str(Path(cmd[0]).parent) if cmd else None


def resolve_js_runtime_args() -> list[str]:
    node = shutil.which('node')
    deno = shutil.which('deno')
    runtimes = []
    if node:
        runtimes.append(f"node:{node}")
    if deno:
        runtimes.append(f"deno:{deno}")
    return ['--js-runtimes', ','.join(runtimes)] if runtimes else []


def find_default_cookies_txt() -> str | None:
    candidates = [
        Path.home() / 'Desktop' / 'youtube_cookies.txt',
        Path.home() / 'Desktop' / 'cookies.txt',
        Path.home() / '.openclaw' / 'cookies.txt',
    ]
    for p in candidates:
        if p.exists() and p.is_file():
            return str(p)
    return None


def browser_cookie_attempts() -> list[tuple[str, list[str]]]:
    attempts = []
    for browser in ['chrome', 'safari']:
        attempts.append((f'{browser} cookies', ['--cookies-from-browser', browser]))
    cookies_txt = find_default_cookies_txt()
    if cookies_txt:
        attempts.append(('cookies.txt', ['--cookies', cookies_txt]))
    attempts.append(('no cookies', []))
    return attempts


def scan_subtitle_files(output_dir: str) -> dict[str, str]:
    lang_map = {}
    for f in Path(output_dir).iterdir():
        if not f.is_file():
            continue
        n = f.name.lower()
        if f.suffix.lower() not in {".vtt", ".srt", ".ass", ".srv3", ".json3", ".ttml"}:
            continue
        if "zh-hant" in n or "zh_hant" in n or "zh-tw" in n or ".zh-tw" in n or ".zh-hant" in n:
            lang_map["zh-Hant"] = str(f)
        elif "zh" in n and "hant" not in n:
            lang_map.setdefault("zh-Hans", str(f))
        elif ".en." in n or "english" in n or n.endswith(".en.vtt") or n.endswith(".en.srt"):
            lang_map.setdefault("en", str(f))
        else:
            lang_map.setdefault("other", str(f))
    return lang_map


def run_subtitle_attempt(label: str, cmd: list[str], output_dir: str) -> dict[str, str]:
    print(f"[transcribe] 下载字幕尝试: {label}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        tail = (result.stderr or result.stdout or "")[-500:]
        print(f"[transcribe] yt-dlp output: {tail}")
    except FileNotFoundError:
        print("[transcribe] yt-dlp 未找到")
        return {}
    files = scan_subtitle_files(output_dir)
    if files:
        print(f"[transcribe] ✓ 获取到字幕: {list(files.keys())}")
    return files


def download_subtitles(url: str, output_dir: str = "workspace/temp/transcription/") -> dict[str, str]:
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    ffmpeg_location = resolve_ffmpeg_location()
    output_args = ["-o", os.path.join(output_dir, "%(title)s [%(id)s].%(ext)s")]

    base_common = resolve_js_runtime_args() + [
        "--write-subs",
        "--write-auto-subs",
        "--skip-download",
        "--sub-langs", "zh-Hant,zh-TW,zh-Hans,zh-CN,zh,en.*,en",
        "--convert-subs", "vtt",
    ]
    if ffmpeg_location:
        base_common += ["--ffmpeg-location", ffmpeg_location]

    player_variants = [
        ('web subtitles', ['--extractor-args', 'youtube:player_client=web']),
        ('android,web subtitles', ['--extractor-args', 'youtube:player_client=android,web']),
        ('mweb subtitles', ['--extractor-args', 'youtube:player_client=mweb,web']),
    ]

    attempts = []
    for cookie_label, cookie_args in browser_cookie_attempts():
        for variant_label, variant_args in player_variants:
            label = f"{cookie_label} + {variant_label}"
            cmd = resolve_ytdlp_cmd() + cookie_args + base_common + variant_args + output_args + [url]
            attempts.append((label, cmd))

    for label, cmd in attempts:
        lang_map = run_subtitle_attempt(label, cmd, output_dir)
        if lang_map:
            return lang_map

    print("[transcribe] 检测到字幕: []")
    return {}


def clean_transcript(vtt_or_srt: str) -> str:
    lines = []
    with open(vtt_or_srt, encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line or "-->" in line:
                continue
            if line.startswith("<") and line.endswith(">"):
                continue
            if re.match(r"^(WEBVTT|NOTE|STYLE)", line):
                continue
            line = re.sub(r"<[^>]+>", "", line)
            if line:
                lines.append(line)
    return "".join(lines)


def transcribe_with_whisper(api_key: str, audio_path: str, model: str = "whisper-1") -> str:
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(model=model, file=f)
        return transcript.text
    except ImportError:
        import requests
        with open(audio_path, "rb") as f:
            files = {"file": (os.path.basename(audio_path), f, "audio/mpeg")}
            data = {"model": model}
            headers = {"Authorization": f"Bearer {api_key}"}
            resp = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, data=data, files=files, timeout=120)
        resp.raise_for_status()
        return resp.json().get("text", "")


def extract_audio(video_path: str, output_path: str | None = None) -> str:
    if output_path is None:
        output_path = video_path.rsplit(".", 1)[0] + ".m4a"
    cmd = resolve_ffmpeg_cmd() + ["-y", "-i", video_path, "-vn", "-c:a", "aac", "-b:a", "128k", output_path]
    print(f"[transcribe] 提取音频: {video_path} -> {output_path}")
    subprocess.run(cmd, capture_output=True)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Helius-002 字幕/转录工具")
    sub = parser.add_subparsers(dest="cmd", required=True)
    dl = sub.add_parser("download", help="下载字幕")
    dl.add_argument("url", help="视频 URL")
    dl.add_argument("--output-dir", "-o", default="workspace/temp/transcription/")
    tr = sub.add_parser("transcribe", help="Whisper API 转录")
    tr.add_argument("audio", help="音频/视频文件路径")
    tr.add_argument("--api-key", "-k", required=True, help="OpenAI API Key")
    tr.add_argument("--model", default="whisper-1")
    tr.add_argument("--output", "-o", default=None, help="输出 .txt 路径")
    cl = sub.add_parser("clean", help="清理字幕为纯文本")
    cl.add_argument("subtitle", help="VTT/SRT 文件路径")
    cl.add_argument("--output", "-o", default=None)
    args = parser.parse_args()

    if args.cmd == "download":
        lang_map = download_subtitles(args.url, args.output_dir)
        for lang, path in lang_map.items():
            print(f"  [{lang}] {path}")
    elif args.cmd == "transcribe":
        audio = args.audio
        ext = os.path.splitext(audio)[1].lower()
        if ext in (".mp4", ".mkv", ".avi", ".mov", ".webm"):
            audio = extract_audio(audio)
        text = transcribe_with_whisper(args.api_key, audio, args.model)
        out_path = args.output or (audio.rsplit(".", 1)[0] + ".txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[transcribe] ✓ 转录完成: {out_path}")
    elif args.cmd == "clean":
        text = clean_transcript(args.subtitle)
        out_path = args.output or (args.subtitle.rsplit(".", 1)[0] + ".txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[transcribe] ✓ 清理完成: {out_path}")


if __name__ == "__main__":
    main()
