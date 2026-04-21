#!/usr/bin/env python3
import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

ctx = ssl._create_unverified_context()


def extract_video_id(url: str) -> str:
    for p in [r"v=([A-Za-z0-9_-]{11})", r"youtu\.be/([A-Za-z0-9_-]{11})", r"youtube\.com/shorts/([A-Za-z0-9_-]{11})"]:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return ""


def fetch_caption_tracks(url: str):
    html = urllib.request.urlopen(url, context=ctx, timeout=20).read().decode("utf-8", "ignore")
    m = re.search(r'"captions":(\{.*?\}),"videoDetails"', html)
    if not m:
        return []
    data = json.loads(m.group(1))
    return data.get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])


def main():
    if len(sys.argv) < 2:
        print("usage: get_transcript.py <url>", file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    out = {"url": url, "video_id": extract_video_id(url), "status": "partial", "tracks": []}
    try:
        tracks = fetch_caption_tracks(url)
        out["tracks"] = [
            {
                "languageCode": t.get("languageCode"),
                "name": (t.get("name", {}).get("simpleText") or (t.get("name", {}).get("runs") or [{}])[0].get("text", "")),
                "baseUrl": t.get("baseUrl", ""),
            }
            for t in tracks
        ]
        out["status"] = "found" if tracks else "unavailable"
    except Exception as e:
        out["error"] = str(e)
        out["status"] = "error"
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
