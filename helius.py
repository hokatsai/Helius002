#!/usr/bin/env python3
"""
Helius-002 统一入口
用法：
    python helius.py download <url>
    python helius.py transcribe <url>
    python helius.py organize
    python helius.py list
"""

import argparse
import os
import sys
import time
import traceback
from pathlib import Path
from datetime import datetime

WORKSPACE_ROOT = Path(__file__).parent
INPUTS_DIR = WORKSPACE_ROOT / "03-inputs"
OUTPUTS_DIR = WORKSPACE_ROOT / "04-outputs"
TEMP_DIR = WORKSPACE_ROOT / "05-temp"
LOGS_DIR = WORKSPACE_ROOT / "06-logs"

MAX_RETRIES = 3
RETRY_DELAY = 2


def ensure_dirs():
    """确保必要目录存在"""
    for d in [INPUTS_DIR, OUTPUTS_DIR, TEMP_DIR, LOGS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def log_error(operation: str, error: Exception, context: str = ""):
    """记录错误到日志文件"""
    ensure_dirs()
    log_file = LOGS_DIR / f"helius-{datetime.now().strftime('%Y-%m-%d')}.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] ERROR in {operation}\n"
        f"  Context: {context}\n"
        f"  Error: {type(error).__name__}: {error}\n"
        f"  Traceback:\n{traceback.format_exc()}\n"
        + "-" * 50 + "\n"
    )
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"  [ERROR] 已记录到 {log_file.relative_to(WORKSPACE_ROOT)}")


def with_retry(operation_name: str):
    """重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < MAX_RETRIES:
                        print(f"  [RETRY] {operation_name} 失败 ({attempt}/{MAX_RETRIES}), {RETRY_DELAY}s 后重试...")
                        time.sleep(RETRY_DELAY)
                    else:
                        print(f"  [FAIL] {operation_name} 最终失败")
                        log_error(operation_name, e, str(args))
            return 1
        return wrapper
    return decorator


def with_fallback(primary_func, fallback_func, operation_name: str):
    """降级方案包装器：主方法失败时使用备用方法"""
    try:
        return primary_func()
    except Exception as e:
        print(f"  [FALLBACK] {operation_name} 主方法失败，尝试降级方案...")
        log_error(f"{operation_name}_fallback", e, "降级到备用方法")
        try:
            return fallback_func()
        except Exception as e2:
            print(f"  [FATAL] {operation_name} 降级方案也失败")
            log_error(f"{operation_name}_fallback_fail", e2, "降级方案失败")
            return 1


@with_retry("视频下载")
def cmd_download_impl(url: str) -> int:
    """下载视频到 workspace/inputs/"""
    print(f"[Helius-002] 下载视频: {url}")
    import subprocess

    cmd = [
        "yt-dlp",
        "--output", str(INPUTS_DIR / "%(title)s-%(id)s.%(ext)s"),
        "--format", "bv*[vcodec^=avc1][height<=1080][fps<=60]+ba[ext=m4a]",
        "--merge-output-format", "mp4",
        url,
    ]
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp returned code {result.returncode}")
    return result.returncode


def cmd_download_fallback(url: str) -> int:
    """下载降级方案：使用更宽松的格式条件"""
    print(f"  [FALLBACK] 使用降级格式条件...")
    import subprocess

    cmd = [
        "yt-dlp",
        "--output", str(INPUTS_DIR / "%(title)s-%(id)s.%(ext)s"),
        "--format", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "--merge-output-format", "mp4",
        url,
    ]
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode


def cmd_download(url: str) -> int:
    """下载视频（带重试和降级）"""
    def primary():
        return cmd_download_impl(url)
    return with_fallback(primary, lambda: cmd_download_fallback(url), "视频下载")


@with_retry("视频转录")
def cmd_transcribe_impl(url: str) -> int:
    """下载 + 转录视频"""
    print(f"[Helius-002] 转录视频: {url}")
    print("  -> 1. 下载视频...")
    rc = cmd_download(url)
    if rc != 0:
        raise RuntimeError(f"下载失败，returncode={rc}")
    print("  -> 2. 执行 Whisper 转录...")
    print("  [TODO] 调用 transcription skill 完成转录")
    return 0


def cmd_transcribe(url: str) -> int:
    """转录视频（带重试）"""
    return cmd_transcribe_impl(url)


@with_retry("素材整理")
def cmd_organize_impl() -> int:
    """整理 workspace/inputs/ 中的素材"""
    print(f"[Helius-002] 整理素材...")
    import subprocess

    script = WORKSPACE_ROOT / "01-system" / "organize.py"
    if script.exists():
        result = subprocess.run(["python", str(script)], capture_output=False)
        if result.returncode != 0:
            raise RuntimeError(f"organize.py returned code {result.returncode}")
        return result.returncode
    else:
        print(f"  [FALLBACK] organize.py 不存在，执行基础扫描...")
        ensure_dirs()
        if not INPUTS_DIR.exists():
            INPUTS_DIR.mkdir(parents=True, exist_ok=True)
        files = list(INPUTS_DIR.rglob("*"))
        for f in files:
            if f.is_file():
                print(f"  发现文件: {f.relative_to(INPUTS_DIR)}")
        return 0


def cmd_organize() -> int:
    """整理素材（带降级）"""
    def primary():
        return cmd_organize_impl()
    def fallback():
        print("  [FALLBACK] 基础扫描模式...")
        ensure_dirs()
        if not INPUTS_DIR.exists():
            INPUTS_DIR.mkdir(parents=True, exist_ok=True)
        for f in sorted(INPUTS_DIR.rglob("*")):
            if f.is_file():
                size = f.stat().st_size / (1024 * 1024)
                print(f"  发现文件: {f.relative_to(INPUTS_DIR)} ({size:.1f} MB)")
        return 0
    return with_fallback(primary, fallback, "素材整理")


def cmd_list() -> int:
    """列出 workspace/inputs/ 和 workspace/outputs/ 的内容"""
    print(f"[Helius-002] 素材列表\n")

    print(f"📥 输入目录 ({INPUTS_DIR}):")
    if not INPUTS_DIR.exists():
        print("  (空目录)")
    else:
        for f in sorted(INPUTS_DIR.rglob("*")):
            if f.is_file():
                size = f.stat().st_size / (1024 * 1024)
                print(f"  {f.relative_to(INPUTS_DIR)}  ({size:.1f} MB)")
        dirs = [d for d in INPUTS_DIR.iterdir() if d.is_dir()]
        for d in dirs:
            print(f"  📁 {d.name}/")

    print(f"\n📤 输出目录 ({OUTPUTS_DIR}):")
    if not OUTPUTS_DIR.exists():
        print("  (空目录)")
    else:
        for f in sorted(OUTPUTS_DIR.rglob("*")):
            if f.is_file():
                print(f"  {f.relative_to(OUTPUTS_DIR)}")
        dirs = [d for d in OUTPUTS_DIR.iterdir() if d.is_dir()]
        for d in dirs:
            print(f"  📁 {d.name}/")
    return 0


def main():
    ensure_dirs()
    parser = argparse.ArgumentParser(description="Helius-002 统一入口")
    sub = parser.add_subparsers(dest="command")

    dl = sub.add_parser("download", help="下载视频")
    dl.add_argument("url", help="视频 URL")

    tr = sub.add_parser("transcribe", help="下载 + 转录")
    tr.add_argument("url", help="视频 URL")

    sub.add_parser("organize", help="整理素材")
    sub.add_parser("list", help="列出素材")

    av = sub.add_parser("analyze-video", help="视频内容分析")
    av.add_argument("source", help="视频 URL 或本地媒体路径")
    av.add_argument("--mode", choices=["quick", "full"], default="full")

    yd = sub.add_parser("youtube-diagnose", help="诊断 YouTube 抓取问题")
    yd.add_argument("url", help="YouTube URL")
    yd.add_argument("--cookies", default=None, help="cookies.txt 路径")

    args = parser.parse_args()

    if args.command == "download":
        return cmd_download(args.url)
    elif args.command == "transcribe":
        return cmd_transcribe(args.url)
    elif args.command == "organize":
        return cmd_organize()
    elif args.command == "list":
        return cmd_list()
    elif args.command == "analyze-video":
        import subprocess
        script = WORKSPACE_ROOT / "02-skills" / "video-content-analysis" / "scripts" / "run_pipeline.py"
        result = subprocess.run([sys.executable, str(script), args.source, "--mode", args.mode], capture_output=False)
        return result.returncode
    elif args.command == "youtube-diagnose":
        import subprocess
        script = WORKSPACE_ROOT / "02-skills" / "youtube-diagnostics" / "scripts" / "diagnose_youtube.py"
        cmd = [sys.executable, str(script), args.url]
        if args.cookies:
            cmd += ["--cookies", args.cookies]
        result = subprocess.run(cmd, capture_output=False)
        return result.returncode
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
