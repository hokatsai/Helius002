---
name: youtube-diagnostics
description: Diagnose YouTube access problems for yt-dlp workflows, including runtime checks, cookies.txt support, browser cookie status, subtitle/download probing, challenge/PO token detection, and fallback guidance. Use when YouTube 字幕抓不到, yt-dlp 下载失败, 需要 cookies.txt 支持, 需要 runtime 检查, 或排查 challenge / PO token / format unavailable 问题。
---

# YouTube Diagnostics

Use this skill before assuming the content-analysis pipeline is broken.

## What it does
- Check runtime dependencies
- Detect yt-dlp execution path
- Detect ffmpeg availability
- Probe browser cookies status
- Probe YouTube subtitle access
- Probe YouTube download formats
- Classify failures into likely causes

## Primary script
Run:

```bash
python3 scripts/diagnose_youtube.py <youtube-url> [--cookies /path/to/cookies.txt]
```

## Output
Write a JSON diagnostic report with:
- runtime status
- cookie status
- subtitle probe status
- download probe status
- detected blockers
- suggested next actions

## Failure classes
- `runtime-missing`
- `cookies-missing`
- `browser-cookie-failed`
- `youtube-n-challenge`
- `youtube-po-token`
- `format-unavailable`
- `subtitle-unavailable`
- `unknown`

## Use in Helius
When a YouTube analysis/transcription job fails:
1. Run diagnostics first.
2. Read the failure class.
3. Choose the next path:
   - subtitle retry
   - cookie file retry
   - runtime fix
   - metadata-only fallback
