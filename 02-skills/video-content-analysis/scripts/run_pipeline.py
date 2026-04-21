#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = Path.home() / "Desktop/Helius-002"
REPORT_BASE = WORKSPACE_ROOT / "workspace" / "video-analysis" / "reports"
TEMP_BASE = WORKSPACE_ROOT / "workspace" / "temp" / "video-analysis"
TOOLS_DIR = WORKSPACE_ROOT / "tools"
FETCH = SKILL_DIR / "scripts" / "fetch_metadata.py"
GET_TRANSCRIPT = SKILL_DIR / "scripts" / "get_transcript.py"
CLEAN = SKILL_DIR / "scripts" / "clean_transcript.py"
ANALYZE = SKILL_DIR / "scripts" / "analyze_content.py"
SAVE = SKILL_DIR / "scripts" / "save_report.py"


def run(cmd, check=True, capture=True):
    return subprocess.run(cmd, check=check, text=True, capture_output=capture)


def ensure_dirs(video_id: str):
    target = REPORT_BASE / video_id
    target.mkdir(parents=True, exist_ok=True)
    TEMP_BASE.mkdir(parents=True, exist_ok=True)
    return target


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def try_fetch_metadata(url: str, meta_path: Path):
    out = run([sys.executable, str(FETCH), url])
    write(meta_path, out.stdout)
    return json.loads(out.stdout)


def try_platform_transcript(url: str, probe_path: Path):
    out = run([sys.executable, str(GET_TRANSCRIPT), url])
    write(probe_path, out.stdout)
    return json.loads(out.stdout)


def detect_subtitle_file(transcription_dir: Path):
    exts = {".vtt", ".srt"}
    files = [p for p in transcription_dir.glob("**/*") if p.is_file() and p.suffix.lower() in exts]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def try_download_subtitles(url: str, out_dir: Path):
    tool = TOOLS_DIR / "transcribe.py"
    if not tool.exists():
        return None
    try:
        subprocess.run([sys.executable, str(tool), "download", url, "--output-dir", str(out_dir)], check=False, text=True)
    except Exception:
        return None
    return detect_subtitle_file(out_dir)


def try_download_video(url: str):
    tool = TOOLS_DIR / "download.py"
    if not tool.exists():
        return None
    inputs = WORKSPACE_ROOT / "workspace" / "inputs"
    before = {p for p in inputs.glob("**/*") if p.is_file()}
    subprocess.run([sys.executable, str(tool), url, "--output-dir", str(inputs)], check=False, text=True)
    after = [p for p in inputs.glob("**/*") if p.is_file() and p not in before]
    after.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return after[0] if after else None


def try_transcribe_local(media_path: Path, out_dir: Path):
    tool = TOOLS_DIR / "transcribe.py"
    if not tool.exists():
        return None
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return None
    out_file = out_dir / f"{media_path.stem}.txt"
    subprocess.run([
        sys.executable, str(tool), "transcribe", str(media_path), "--api-key", api_key, "--output", str(out_file)
    ], check=False, text=True)
    return out_file if out_file.exists() else None


def clean_input(raw_path: Path, clean_path: Path):
    out = run([sys.executable, str(CLEAN), str(raw_path)])
    write(clean_path, out.stdout)


def analyze(meta_path: Path, clean_path: Path, analysis_path: Path):
    out = run([sys.executable, str(ANALYZE), str(meta_path), str(clean_path)])
    write(analysis_path, out.stdout)


def save(video_id: str, meta_path: Path, analysis_path: Path, clean_path: Path):
    out = run([sys.executable, str(SAVE), video_id, str(meta_path), str(analysis_path), str(clean_path)])
    return out.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description="Run Helius video-content-analysis pipeline")
    ap.add_argument("source", help="YouTube URL or local media file")
    ap.add_argument("--mode", choices=["quick", "full"], default="full")
    args = ap.parse_args()

    source = args.source
    is_url = source.startswith("http://") or source.startswith("https://")

    if is_url:
        tmp_meta = TEMP_BASE / "meta.json"
        meta = try_fetch_metadata(source, tmp_meta)
        video_id = meta.get("video_id") or "unknown"
    else:
        p = Path(source)
        video_id = p.stem
        tmp_meta = TEMP_BASE / f"{video_id}-meta.json"
        meta = {
            "url": str(p),
            "platform": "local",
            "video_id": video_id,
            "title": p.stem,
            "creator": "local-file",
            "description": "",
        }
        write(tmp_meta, json.dumps(meta, ensure_ascii=False, indent=2))

    target = ensure_dirs(video_id)
    temp_dir = TEMP_BASE / video_id
    temp_dir.mkdir(parents=True, exist_ok=True)

    raw_path = temp_dir / "raw_transcript.txt"
    clean_path = temp_dir / "clean_transcript.md"
    analysis_path = temp_dir / "analysis.json"
    probe_path = temp_dir / "transcript_probe.json"

    transcript_source = None
    confidence_note = "metadata-only"

    if is_url:
        probe = try_platform_transcript(source, probe_path)
        subtitle_file = try_download_subtitles(source, temp_dir)
        if subtitle_file and subtitle_file.exists():
            if subtitle_file.suffix.lower() in {".vtt", ".srt"}:
                cleaned = run([sys.executable, str(CLEAN), str(subtitle_file)])
                write(raw_path, cleaned.stdout)
            else:
                write(raw_path, subtitle_file.read_text(encoding="utf-8", errors="ignore"))
            transcript_source = f"subtitle:{subtitle_file.name}"
            confidence_note = "subtitle"
        elif args.mode == "full":
            media = try_download_video(source)
            if media:
                local_txt = try_transcribe_local(media, temp_dir)
                if local_txt and local_txt.exists():
                    write(raw_path, local_txt.read_text(encoding="utf-8", errors="ignore"))
                    transcript_source = f"stt:{local_txt.name}"
                    confidence_note = "stt"
    else:
        media = Path(source)
        local_txt = try_transcribe_local(media, temp_dir)
        if local_txt and local_txt.exists():
            write(raw_path, local_txt.read_text(encoding="utf-8", errors="ignore"))
            transcript_source = f"stt:{local_txt.name}"
            confidence_note = "stt"

    if not raw_path.exists():
        fallback_text = (meta.get("description") or meta.get("title") or "").strip()
        write(raw_path, fallback_text)

    clean_input(raw_path, clean_path)
    analyze(tmp_meta, clean_path, analysis_path)

    report_data = json.loads(analysis_path.read_text(encoding="utf-8"))
    report_data["transcript_source"] = transcript_source
    report_data["pipeline_confidence_note"] = confidence_note
    write(analysis_path, json.dumps(report_data, ensure_ascii=False, indent=2))

    saved = save(video_id, tmp_meta, analysis_path, clean_path)
    print(json.dumps({
        "video_id": video_id,
        "report_dir": saved,
        "transcript_source": transcript_source,
        "confidence_note": confidence_note,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
