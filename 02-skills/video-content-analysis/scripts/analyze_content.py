#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


def find_hooks(text: str, limit: int = 5):
    lines = [x.strip() for x in re.split(r"[\n]+", text) if x.strip()]
    strong = []
    for line in lines:
        if any(k in line for k in ["为什么", "其实", "你以为", "How", "What if", "Stop", "Most people"]):
            strong.append(line)
    return strong[:limit] or lines[:limit]


def simple_report(meta, text):
    hooks = find_hooks(text)
    key_lines = [x.strip() for x in re.split(r"[\n]+", text) if len(x.strip()) > 30][:10]
    confidence = "high" if len(text) > 1200 else "medium" if len(text) > 200 else "low"
    return {
        "basic_info": meta,
        "confidence": confidence,
        "core_topic": meta.get("title", "Unknown video"),
        "click_logic": [
            "Check title for contrast/conflict",
            "Look for promised result or curiosity gap",
            "Map identity or anxiety trigger",
        ],
        "structure_breakdown": {
            "hook": hooks[:2],
            "setup": key_lines[:2],
            "reframe": key_lines[2:4],
            "proof_or_examples": key_lines[4:7],
            "close_or_cta": key_lines[7:10],
        },
        "hooks": hooks,
        "key_lines": key_lines,
        "cta_candidates": [x for x in key_lines if any(k.lower() in x.lower() for k in ["join", "subscribe", "download", "sign up", "课程", "订阅", "关注"])][:3],
        "style_guess": "unknown",
        "helius_angles": [
            "Turn this into 3 Chinese short-video titles",
            "Extract a reusable hook and CTA",
            "Map to MoneyXYZ / Dan Koe / 認知便利店 if relevant",
        ],
    }


def to_markdown(report):
    meta = report["basic_info"]
    lines = []
    lines.append(f"# {meta.get('title','Untitled')}\n")
    lines.append(f"- Creator: {meta.get('creator','Unknown')}")
    lines.append(f"- Platform: {meta.get('platform','Unknown')}")
    lines.append(f"- URL: {meta.get('url','')}")
    lines.append(f"- Confidence: {report.get('confidence','low')}\n")
    lines.append("## Core topic")
    lines.append(report.get("core_topic", ""))
    lines.append("\n## Hooks")
    for h in report.get("hooks", []):
        lines.append(f"- {h}")
    lines.append("\n## Key lines")
    for k in report.get("key_lines", []):
        lines.append(f"- {k}")
    lines.append("\n## Helius angles")
    for a in report.get("helius_angles", []):
        lines.append(f"- {a}")
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 3:
        print("usage: analyze_content.py <meta.json> <clean_transcript.md>", file=sys.stderr)
        sys.exit(1)
    meta = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    text = Path(sys.argv[2]).read_text(encoding="utf-8", errors="ignore")
    report = simple_report(meta, text)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
