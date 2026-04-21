---
name: video-content-analysis
description: Analyze video content from YouTube links, local video/audio files, or downloaded platform videos using a Funnel architecture. L1 performs rapid extraction of metrics and transcripts to produce a Clone-worthiness Quick Note. L2 performs a deep structural teardown (hooks/structure/CTA) generating reusable assets. Use when asked to analyze a video,拆解视频内容,提取字幕,做内容分析,研究竞品视频.
---

# Video Content Analysis

Run this skill when the user wants analysis, utilizing a two-stage Funnel mechanism (L1 quick scout vs L2 heavy factory).

## Workflow

1. Collect full metadata (including views/likes/saves/comments metrics).
2. Get subtitles. If no official subtitles exist, immediately fallback to audio download + Whisper transcription.
3. Generate L1 Quick Note & Clone-worthiness Score (Pre-filtering).
4. If Score >= 7 or user explicitly cmds `/deepdive`: Proceed to L2 Deep Teardown.
5. In L2, clean transcript slightly (retaining creator quirks).
6. Analyze content structure and persuasion logic.
7. Extract reusable assets & style map.
8. Save L2 results into the Helius-002 outputs library.

## Output contract (L1 / L2 Architecture)

### L1 - Quick Mode / Scout (Default)
Extract core metadata and transcript. Generate a rapid overview and Clone-worthiness score.
- Output path: `~/Desktop/Helius-002/05-temp/notes/<video_id>-quick.md`

### L2 - Full Mode / Deep Dive
Triggered only if L1 score >= 7, or explicitly requested via `/deepdive`. Perform full structural breakdown.
For each analyzed video, create a folder under:
- `~/Desktop/Helius-002/04-outputs/<video_id>/`

Write these files when possible:
- `meta.json`
- `raw_transcript.txt`
- `clean_transcript.md`
- `analysis_report.md`
- `highlights.json`
- `reusable_angles.md`

## Execution notes

### 1) Metadata

Capture:
- title
- creator/channel
- source url
- platform
- publish date if available
- video id
- summary/description if available
- **Performance metrics**: Views, Likes, Saves (Favorites), Shares, Comments.

### 2) Transcript priority

Always prefer this order:
1. Official subtitles
2. **Audio extraction + AI Transcription**: If no official captions, DO NOT default to bad auto-captions immediately. Download the audio file, and run offline/online transcription (e.g. Whisper) to ensure high-fidelity text for analysis.
3. Auto subtitles (fallback only if AI transcription unavailable).

If all fail, still continue with a partial analysis from title/description/channel style, but label confidence clearly.

### 3) L1 Pre-filtering (The Valve)

After getting transcript and metadata, evaluate the "Clone-worthiness" (out of 10). Output `quick_notes.md` to `05-temp/`. Pause here in interactive environments unless authorized to proceed to L2.

### 4) Cleaning (L2)

Normalize transcript into readable paragraphs.
**CRITICAL**: Preserve unique vocal cadences, pauses, filler words, and specific phrasing, as these are critical for creator style mapping later. Do not aggressively delete them. Only remove pure transcription artifacts.

### 5) Analysis framework (L2)

Use the framework in `references/analysis-framework.md`.

Minimum sections in the report:
- Core topic
- Why people click
- Structure breakdown
- Key arguments / emotional turns
- Hooks / key lines / CTA
- What is reusable
- Style mapping
- Suggested content angles for Helius

### 6) Style mapping (L2)

When applicable, compare against:
- MoneyXYZ
- Dan Koe
- 認知便利店M
- Other creator profiles the user adds later

Read `references/creator-style-map.md` when style matching matters.

## Scripts

Use these bundled scripts:

- `scripts/fetch_metadata.py` — fetch video id and full performance metrics
- `scripts/get_transcript.py` — probe platform transcript tracks or trigger audio extraction + whisper
- `scripts/clean_transcript.py` — format text without destroying style
- `scripts/analyze_content.py` — generate structured analysis JSON/Markdown payload
- `scripts/save_report.py` — create outputs in `04-outputs/` or `05-temp/`
- `scripts/run_pipeline.py` — integrated v2.1 L1/L2 orchestrator

## Failure handling

If transcript extraction fails:
- say transcript was unavailable
- continue with title/description/channel-style analysis
- mark result as partial
- suggest rerun after download/transcription support is added

Do not pretend to have watched content you did not actually parse.
