#!/usr/bin/env python3
"""
Helius-002 素材整理工具
直接继承 v1 downloads_organizer.py 核心逻辑
"""

import argparse
import hashlib
import json
import os
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

VIDEO_ID_BRACKET_RE = re.compile(r"\[(?P<id>[A-Za-z0-9_-]{11})\]")
VIDEO_ID_PLAIN_RE = re.compile(r"(?P<id>[A-Za-z0-9_-]{11})(?=\.)")


@dataclass
class RunAsset:
    run_name: str
    run_dir: Path
    video_id: str
    title: str
    url: str
    mp4_files: list[Path] = field(default_factory=list)
    vtt_files: list[Path] = field(default_factory=list)
    srt_files: list[Path] = field(default_factory=list)
    transcript_zh_hant: Path | None = None
    transcript_en: Path | None = None
    summary_or_analysis: Path | None = None


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _try_hardlink_or_copy(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return "skip_exists"
    try:
        os.link(src, dst)
        return "hardlink"
    except Exception:
        shutil.copy2(src, dst)
        return "copy"


def _extract_video_id_from_name(name: str) -> str:
    m = VIDEO_ID_BRACKET_RE.search(name)
    if m:
        return m.group("id")
    lower = name.lower()
    allowed = (
        lower.endswith(".mp4") or lower.endswith(".vtt") or lower.endswith(".srt")
        or lower.endswith(".info.json") or lower.endswith(".vtt.txt")
        or lower.endswith(".srt.txt") or ".timedtext." in lower
    )
    if not allowed:
        return ""
    m = VIDEO_ID_PLAIN_RE.search(name)
    if m:
        return m.group("id")
    return ""


def _looks_like_youtube_id(value: str) -> bool:
    if len(value) != 11:
        return False
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return False
    return bool(re.search(r"[A-Za-z]", value))


def _pick_best_info_json(files: list[Path], video_id: str) -> Path | None:
    info = [p for p in files if p.name.endswith(".info.json")]
    if not info:
        return None
    if video_id:
        for p in info:
            if f"[{video_id}].info.json" in p.name:
                return p
    return info[0]


def _pick_best_mp4(files: list[Path], video_id: str) -> list[Path]:
    mp4s = [p for p in files if p.suffix.lower() == ".mp4"]
    if not mp4s:
        return []
    named = [p for p in mp4s if video_id and f"[{video_id}]" in p.name]
    picks = []
    if named:
        picks.append(sorted(named, key=lambda p: p.stat().st_size, reverse=True)[0])
    largest = sorted(mp4s, key=lambda p: p.stat().st_size, reverse=True)[0]
    if largest not in picks:
        picks.append(largest)
    return picks


def _pick_caption(files: list[Path], video_id: str, lang_hint: str) -> Path | None:
    wanted = []
    for p in files:
        n = p.name.lower()
        if p.suffix.lower() in (".vtt", ".srt") and lang_hint.lower() in n:
            wanted.append(p)
    if not wanted:
        return None
    if video_id:
        with_id = [p for p in wanted if f"[{video_id}]".lower() in p.name.lower()]
        if with_id:
            return sorted(with_id, key=lambda p: p.stat().st_size, reverse=True)[0]
    return sorted(wanted, key=lambda p: p.stat().st_size, reverse=True)[0]


def scan_youtube_downloads(source_dir: Path) -> list[RunAsset]:
    runs: list[RunAsset] = []
    if not source_dir.exists():
        return runs

    for run_dir in sorted([p for p in source_dir.iterdir() if p.is_dir()], key=lambda p: p.name):
        downloads_dir = run_dir / "downloads"
        files: list[Path] = []
        if downloads_dir.exists():
            files.extend([p for p in downloads_dir.iterdir() if p.is_file()])
        files.extend([p for p in run_dir.iterdir() if p.is_file()])

        url = ""
        url_file = run_dir / "url.txt"
        if url_file.exists():
            content = _safe_read_text(url_file)
            url = content.splitlines()[0].strip() if content else ""

        ids_from_names = {_extract_video_id_from_name(p.name) for p in files}
        ids_from_names = {i for i in ids_from_names if _looks_like_youtube_id(i)}
        candidate_ids = sorted(ids_from_names)

        if not candidate_ids:
            info_json_any = _pick_best_info_json(files, "")
            if info_json_any:
                try:
                    meta = json.loads(info_json_any.read_text(encoding="utf-8", errors="replace"))
                    vid = (meta.get("id") or "").strip()
                    if _looks_like_youtube_id(vid):
                        candidate_ids = [vid]
                except Exception:
                    candidate_ids = []

        if not candidate_ids:
            candidate_ids = [""]

        transcript_zh_hant = None
        transcript_en = None
        summary_or_analysis = None
        if len(candidate_ids) == 1:
            for cand in ("transcript_zh-Hant.txt", "transcript.zh-Hant.txt"):
                c = run_dir / cand
                if c.exists():
                    transcript_zh_hant = c
                    break
            transcript_en = run_dir / "transcript_en.txt" if (run_dir / "transcript_en.txt").exists() else None
            for cand in ("analysis.md", "summary.zh-Hant.md"):
                c = run_dir / cand
                if c.exists():
                    summary_or_analysis = c
                    break

        for video_id in candidate_ids:
            scoped_files = files
            if video_id:
                scoped_files = [
                    p for p in files
                    if _extract_video_id_from_name(p.name) == video_id
                    or p.name.endswith(".info.json")
                ]

            title = ""
            info_json = _pick_best_info_json(scoped_files, video_id)
            if info_json:
                try:
                    meta = json.loads(info_json.read_text(encoding="utf-8", errors="replace"))
                    title = (meta.get("title") or "").strip()
                except Exception:
                    pass

            mp4_files = _pick_best_mp4(scoped_files, video_id)
            vtt_files = [
                p for p in scoped_files
                if p.suffix.lower() == ".vtt"
                and (not video_id or _extract_video_id_from_name(p.name) == video_id)
            ]
            srt_files = [
                p for p in scoped_files
                if p.suffix.lower() == ".srt"
                and (not video_id or _extract_video_id_from_name(p.name) == video_id)
            ]

            runs.append(
                RunAsset(
                    run_name=run_dir.name,
                    run_dir=run_dir,
                    video_id=video_id,
                    title=title,
                    url=url,
                    mp4_files=mp4_files,
                    vtt_files=vtt_files,
                    srt_files=srt_files,
                    transcript_zh_hant=transcript_zh_hant if video_id and len(candidate_ids) == 1 else None,
                    transcript_en=transcript_en if video_id and len(candidate_ids) == 1 else None,
                    summary_or_analysis=summary_or_analysis if video_id and len(candidate_ids) == 1 else None,
                )
            )
    return runs


def write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(header) + "\n")
        for row in rows:
            f.write("\t".join(row) + "\n")


def organize(
    source_dir: str | Path,
    output_base: str | Path,
    run_id: str | None = None,
    apply_dedupe: bool = False,
    max_hash_mb: int = 50,
) -> Path:
    source_dir = Path(source_dir)
    output_base = Path(output_base)
    run_id = run_id or datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = output_base / run_id
    intermediate = out_dir / "intermediate"
    final = out_dir / "final"
    intermediate.mkdir(parents=True, exist_ok=True)
    final.mkdir(parents=True, exist_ok=True)

    runs = scan_youtube_downloads(source_dir)

    # 1) 索引 TSV
    assets_tsv = intermediate / "youtube_assets.tsv"
    rows: list[list[str]] = []
    for r in runs:
        mp4_mb = ""
        if r.mp4_files:
            try:
                mp4_mb = f"{round(r.mp4_files[0].stat().st_size / (1024 * 1024), 1)}"
            except Exception:
                mp4_mb = ""
        rows.append([
            r.run_name, r.video_id,
            r.title.replace("\t", " ").replace("\n", " ").strip(),
            "1" if bool(r.mp4_files) else "0",
            mp4_mb,
            str(len(r.vtt_files)), str(len(r.srt_files)),
            "1" if r.transcript_zh_hant else "0",
            "1" if r.transcript_en else "0",
            "1" if r.summary_or_analysis else "0",
            r.url,
        ])

    write_tsv(assets_tsv, [
        "run", "video_id", "title", "has_mp4", "mp4_mb",
        "vtt_count", "srt_count",
        "has_transcript_zh_hant", "has_transcript_en",
        "has_summary_or_analysis", "url",
    ], rows)

    # 2) 去重
    dedupe_rows: list[list[str]] = []
    actions_rows: list[list[str]] = []
    max_bytes = max_hash_mb * 1024 * 1024

    for r in runs:
        downloads_dir = r.run_dir / "downloads"
        if not downloads_dir.exists():
            continue
        candidates = [
            p for p in downloads_dir.iterdir()
            if p.is_file()
            and p.suffix.lower() in {".vtt", ".srt", ".json"}
            and p.stat().st_size <= max_bytes
        ]
        by_hash: dict[str, list[Path]] = {}
        for p in candidates:
            if p.name.lower().endswith((".piped.streams.json", ".pipedapi.streams.json")):
                continue
            h = _sha256(p)
            by_hash.setdefault(h, []).append(p)

        for h, group in by_hash.items():
            if len(group) <= 1:
                continue
            video_id = r.video_id
            keep = None
            if video_id:
                for p in group:
                    if f"[{video_id}]".lower() in p.name.lower():
                        keep = p
                        break
            if not keep:
                keep = sorted(group, key=lambda p: (len(p.name), p.name.lower()))[0]
            for p in group:
                dedupe_rows.append([
                    r.run_name, r.video_id, p.name,
                    str(p.stat().st_size), h,
                    "keep" if p == keep else "dup",
                ])
            if apply_dedupe:
                dup_dir = downloads_dir / "_duplicates"
                dup_dir.mkdir(parents=True, exist_ok=True)
                for p in group:
                    if p == keep:
                        continue
                    target = dup_dir / p.name
                    if target.exists():
                        continue
                    shutil.move(str(p), str(target))
                    actions_rows.append([
                        r.run_name, r.video_id, "move_to_duplicates",
                        str(p), str(target), h,
                    ])

    if dedupe_rows:
        write_tsv(intermediate / "duplicates.tsv",
                   ["run", "video_id", "file", "bytes", "sha256", "status"],
                   dedupe_rows)
    if actions_rows:
        write_tsv(intermediate / "actions_taken.tsv",
                   ["run", "video_id", "action", "src", "dst", "sha256"],
                   actions_rows)

    # 3) 构建 library
    lib_root = final / "library" / "by_video_id"
    index_lines = [
        "# YouTube 素材整理索引",
        "",
        f"- 來源：`{source_dir.as_posix()}`",
        f"- 產出：`{out_dir.as_posix()}`",
        f"- 去重模式：{'已啟用' if apply_dedupe else '未啟用'}",
        "",
        "| video_id | 標題 | library 路徑 | 來源 run |",
        "| --- | --- | --- | --- |",
    ]

    for r in runs:
        vid = r.video_id or f"unknown__{r.run_name}"
        dest = lib_root / vid / r.run_name
        dest.mkdir(parents=True, exist_ok=True)

        source_paths = [f"run={r.run_name}", f"run_dir={r.run_dir.as_posix()}"]
        if r.url:
            source_paths.append(f"url={r.url}")
        (dest / "source_paths.txt").write_text("\n".join(source_paths) + "\n", encoding="utf-8")

        for i, mp4 in enumerate(r.mp4_files):
            label = "named" if i == 0 and r.video_id and f"[{r.video_id}]" in mp4.name else f"alt{i+1}"
            _try_hardlink_or_copy(mp4, dest / "video" / f"{label}.mp4")

        all_caps = r.vtt_files + r.srt_files
        zh = _pick_caption(all_caps, r.video_id, "zh-hant")
        en = _pick_caption(all_caps, r.video_id, "en")
        if zh:
            _try_hardlink_or_copy(zh, dest / "captions" / f"zh-Hant{zh.suffix.lower()}")
        if en:
            _try_hardlink_or_copy(en, dest / "captions" / f"en{en.suffix.lower()}")

        if r.transcript_zh_hant:
            _try_hardlink_or_copy(r.transcript_zh_hant, dest / "transcripts" / "transcript_zh-Hant.txt")
        if r.transcript_en:
            _try_hardlink_or_copy(r.transcript_en, dest / "transcripts" / "transcript_en.txt")
        if r.summary_or_analysis:
            _try_hardlink_or_copy(r.summary_or_analysis, dest / "notes" / r.summary_or_analysis.name)

        title = (r.title or "").replace("|", " ").strip()
        index_lines.append(
            f"| {r.video_id or ''} | {title} | "
            f"`{out_dir.as_posix()}/final/library/by_video_id/{vid}/{r.run_name}/` | {r.run_name} |"
        )

    (final / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    (output_base / "_latest_run.txt").write_text(run_id + "\n", encoding="utf-8")
    (intermediate / "run_meta.txt").write_text(
        "\n".join([
            f"RUN_ID={run_id}",
            f"SOURCE={source_dir.as_posix()}",
            f"OUTPUT={out_dir.as_posix()}",
            f"ASSETS_TSV={assets_tsv.as_posix()}",
        ]) + "\n",
        encoding="utf-8",
    )
    print(f"OK: wrote index to {out_dir.as_posix()}")
    return out_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Helius-002 素材整理工具（继承 v1 downloads_organizer.py）"
    )
    parser.add_argument(
        "--source", "-s",
        default="workspace/inputs/",
        help="下载目录"
    )
    parser.add_argument(
        "--output-base", "-o",
        default="workspace/outputs",
        help="输出根目录"
    )
    parser.add_argument(
        "--run-id", "-r",
        default="",
        help="运行 ID（默认自动生成）"
    )
    parser.add_argument(
        "--apply-dedupe",
        action="store_true",
        help="移动重复字幕/JSON 到 _duplicates"
    )
    parser.add_argument(
        "--max-hash-mb",
        type=int,
        default=50,
        help="去重哈希最大 MB"
    )
    args = parser.parse_args()
    organize(
        source_dir=args.source,
        output_base=args.output_base,
        run_id=args.run_id.strip() or None,
        apply_dedupe=bool(args.apply_dedupe),
        max_hash_mb=int(args.max_hash_mb),
    )


if __name__ == "__main__":
    main()
