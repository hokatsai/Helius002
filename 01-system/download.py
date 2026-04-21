#!/usr/bin/env python3
"""
Helius-002 视频下载工具
基于 v1 download-video.ps1 逻辑迁移到 Python + yt-dlp
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def resolve_ytdlp_cmd() -> list[str]:
    binary = shutil.which("yt-dlp")
    if binary:
        return [binary]
    return [sys.executable, "-m", "yt_dlp"]


def resolve_ffmpeg_location() -> str | None:
    binary = shutil.which("ffmpeg")
    if binary:
        return os.path.dirname(binary)
    try:
        import imageio_ffmpeg
        return str(Path(imageio_ffmpeg.get_ffmpeg_exe()).parent)
    except Exception:
        return None


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


def run_attempt(label: str, cmd: list[str]) -> int:
    print(f"[download] 尝试: {label}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print("[download] yt-dlp 未找到，请先安装: python3 -m pip install --user yt-dlp")
        return 1
    except Exception as e:
        print(f"[download] 调用异常: {e}")
        return 1

    if result.returncode == 0:
        print(f"[download] ✓ 成功: {label}")
        return 0

    tail = (result.stderr or result.stdout or "")[-700:]
    print(f"[download] ✗ 失败: {label}\n{tail}")
    return result.returncode or 1


def download_video(url: str, output_dir: str = "workspace/inputs/", cookie_path: str | None = None) -> int:
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    strict_fmt = (
        "bv*[vcodec^=avc1][height<=1080][fps<=60]+ba[ext=m4a]/"
        "bv*[vcodec!=av01][height<=1080][fps<=60]+ba[ext=m4a]/"
        "best[ext=mp4]/best"
    )
    relaxed_fmt = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"

    ffmpeg_location = resolve_ffmpeg_location()
    common = resolve_js_runtime_args() + [
        "--restrict-filenames",
        "--force-overwrites",
        "-N", "8",
        "-c",
        "--retries", "3",
        "--fragment-retries", "3",
        "-o", os.path.join(output_dir, "%(title)s [%(id)s].%(ext)s"),
    ]
    if ffmpeg_location:
        common = ["--ffmpeg-location", ffmpeg_location] + common

    cookie_sources = [
        ('chrome cookies', ['--cookies-from-browser', 'chrome']),
        ('safari cookies', ['--cookies-from-browser', 'safari']),
    ]
    default_cookies = find_default_cookies_txt()
    chosen_cookie = cookie_path if cookie_path and os.path.exists(cookie_path) else default_cookies
    if chosen_cookie:
        cookie_sources.append(('cookies.txt', ['--cookies', chosen_cookie]))
    cookie_sources.append(('no cookies', []))

    player_variants = [
        ('web', ['--extractor-args', 'youtube:player_client=web']),
        ('mweb,web', ['--extractor-args', 'youtube:player_client=mweb,web']),
        ('android,web', ['--extractor-args', 'youtube:player_client=android,web']),
    ]

    attempts: list[tuple[str, list[str]]] = []
    for cookie_label, cookie_args in cookie_sources:
        for player_label, player_args in player_variants:
            attempts.append((
                f'strict format + {cookie_label} + {player_label}',
                resolve_ytdlp_cmd() + cookie_args + ['-f', strict_fmt, '--merge-output-format', 'mp4'] + common + player_args + [url],
            ))
            attempts.append((
                f'relaxed format + {cookie_label} + {player_label}',
                resolve_ytdlp_cmd() + cookie_args + ['-f', relaxed_fmt, '--merge-output-format', 'mp4'] + common + player_args + [url],
            ))

    attempts.append((
        'best single file no cookies',
        resolve_ytdlp_cmd() + ['-f', 'best[height<=1080]/best', '--no-playlist'] + common + ['--extractor-args', 'youtube:player_client=web', url],
    ))

    for label, cmd in attempts:
        rc = run_attempt(label, cmd)
        if rc == 0:
            return 0

    print("[download] 所有下载策略均失败。")
    return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Helius-002 视频下载工具")
    parser.add_argument("url", help="视频 URL")
    parser.add_argument("--output-dir", "-o", default="workspace/inputs/", help="输出目录")
    parser.add_argument("--cookies", default=None, help="本地 cookies.txt 路径 (可选)")
    args = parser.parse_args()
    sys.exit(download_video(args.url, args.output_dir, args.cookies))


if __name__ == "__main__":
    main()
