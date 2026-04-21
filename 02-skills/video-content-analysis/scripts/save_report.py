#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path.home() / "Desktop/Helius-002/workspace/video-analysis/reports"


def main():
    if len(sys.argv) < 4:
        print("usage: save_report.py <video_id> <meta.json> <analysis.json> [clean_transcript]", file=sys.stderr)
        sys.exit(1)
    video_id = sys.argv[1]
    meta = Path(sys.argv[2])
    analysis = Path(sys.argv[3])
    clean = Path(sys.argv[4]) if len(sys.argv) > 4 else None

    target = BASE / video_id
    target.mkdir(parents=True, exist_ok=True)

    (target / "meta.json").write_text(meta.read_text(encoding="utf-8"), encoding="utf-8")
    (target / "analysis.json").write_text(analysis.read_text(encoding="utf-8"), encoding="utf-8")
    if clean and clean.exists():
        (target / "clean_transcript.md").write_text(clean.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")

    report = json.loads(analysis.read_text(encoding="utf-8"))
    md = [f"# {report['basic_info'].get('title', video_id)}", ""]
    md.append(f"- Creator: {report['basic_info'].get('creator','Unknown')}")
    md.append(f"- URL: {report['basic_info'].get('url','')}")
    md.append(f"- Confidence: {report.get('confidence','low')}")
    md.append("")
    if report.get('transcript_source'):
        md.append(f"- Transcript source: {report.get('transcript_source')}")
    if report.get('pipeline_confidence_note'):
        md.append(f"- Pipeline note: {report.get('pipeline_confidence_note')}")
    md.append("")
    md.append("## Hooks")
    for x in report.get("hooks", []):
        md.append(f"- {x}")
    md.append("")
    md.append("## Structure")
    for k, vals in report.get("structure_breakdown", {}).items():
        md.append(f"- {k}:")
        for v in vals:
            md.append(f"  - {v}")
    md.append("")
    md.append("## Key lines")
    for x in report.get("key_lines", []):
        md.append(f"- {x}")
    md.append("")
    md.append("## CTA candidates")
    for x in report.get("cta_candidates", []):
        md.append(f"- {x}")
    md.append("")
    md.append("## Helius angles")
    for x in report.get("helius_angles", []):
        md.append(f"- {x}")
    (target / "analysis_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(str(target))


if __name__ == "__main__":
    main()
