#!/usr/bin/env python3
import argparse, json, os, re, shutil, subprocess, sys
from pathlib import Path


def resolve_ytdlp_cmd():
    binary = shutil.which('yt-dlp')
    if binary:
        return [binary]
    return [sys.executable, '-m', 'yt_dlp']


def resolve_ffmpeg():
    binary = shutil.which('ffmpeg')
    if binary:
        return binary
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        return {"code": r.returncode, "stdout": r.stdout[-3000:], "stderr": r.stderr[-3000:]}
    except Exception as e:
        return {"code": 999, "stdout": '', "stderr": str(e)}


def classify(text):
    t = text.lower()
    hits = []
    if 'n challenge' in t:
        hits.append('youtube-n-challenge')
    if 'po token' in t or 'gvs po token' in t:
        hits.append('youtube-po-token')
    if 'requested format is not available' in t or 'format is not available' in t:
        hits.append('format-unavailable')
    if 'cookies from browser' in t or 'could not copy chrome cookie database' in t:
        hits.append('browser-cookie-failed')
    if 'subtitle' in t and 'not available' in t:
        hits.append('subtitle-unavailable')
    return hits or ['unknown']


def suggestions(classes, cookies_provided):
    out = []
    if 'youtube-n-challenge' in classes:
        out.append('需要 JS/runtime/challenge 规避；不要只靠裸 yt-dlp。')
    if 'youtube-po-token' in classes:
        out.append('该视频可能需要 PO Token；优先走 metadata-only 或浏览器辅助方案。')
    if 'browser-cookie-failed' in classes:
        out.append('浏览器 cookie 提取失败，优先尝试 cookies.txt。')
    if 'format-unavailable' in classes:
        out.append('切换 relaxed format / best single file / subtitles-first。')
    if not cookies_provided:
        out.append('建议提供 cookies.txt 作为额外重试入口。')
    if not out:
        out.append('可继续走常规下载/字幕流程。')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--cookies')
    args = ap.parse_args()

    ytdlp = resolve_ytdlp_cmd()
    ffmpeg = resolve_ffmpeg()

    runtime = {
        'python': sys.executable,
        'yt_dlp_cmd': ytdlp,
        'yt_dlp_on_path': bool(shutil.which('yt-dlp')),
        'ffmpeg': ffmpeg,
        'node': shutil.which('node'),
    }

    cookie_status = {
        'cookies_txt_provided': bool(args.cookies),
        'cookies_txt_exists': bool(args.cookies and Path(args.cookies).exists()),
        'chrome_exists': Path.home().joinpath('Library/Application Support/Google/Chrome').exists(),
        'safari_exists': Path.home().joinpath('Library/Safari').exists(),
    }

    subtitle_probe = run(ytdlp + ['--write-subs', '--write-auto-subs', '--skip-download', '--sub-langs', 'zh-Hant,zh-TW,zh-Hans,zh-CN,zh,en.*,en', '--simulate', args.url])
    download_probe = run(ytdlp + ['-F', args.url])

    text = '\n'.join([subtitle_probe['stdout'], subtitle_probe['stderr'], download_probe['stdout'], download_probe['stderr']])
    failure_classes = classify(text)

    report = {
        'url': args.url,
        'runtime': runtime,
        'cookie_status': cookie_status,
        'subtitle_probe': subtitle_probe,
        'download_probe': download_probe,
        'failure_classes': failure_classes,
        'suggestions': suggestions(failure_classes, cookie_status['cookies_txt_provided']),
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
