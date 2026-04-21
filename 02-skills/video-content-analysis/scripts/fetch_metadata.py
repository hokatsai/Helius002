#!/usr/bin/env python3
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ctx = ssl._create_unverified_context()


def extract_video_id(url: str) -> str:
    patterns = [
        r"v=([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return ""


def youtube_oembed(url: str):
    api = "https://www.youtube.com/oembed?url=" + urllib.parse.quote(url, safe="") + "&format=json"
    return json.loads(urllib.request.urlopen(api, context=ctx, timeout=20).read().decode("utf-8", "ignore"))


def youtube_description(url: str):
    html = urllib.request.urlopen(url, context=ctx, timeout=20).read().decode("utf-8", "ignore")
    patterns = [r'"shortDescription":"(.*?)"', r'<meta name="description" content="(.*?)">']
    for p in patterns:
        m = re.search(p, html)
        if m:
            return m.group(1).replace("\\n", "\n")
    return ""


def main():
    if len(sys.argv) < 2:
        print("usage: fetch_metadata.py <url>", file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    video_id = extract_video_id(url)
    out = {
        "url": url,
        "platform": "youtube" if "youtube.com" in url or "youtu.be" in url else "unknown",
        "video_id": video_id,
    }
    try:
        data = youtube_oembed(url)
        out.update({
            "title": data.get("title", ""),
            "creator": data.get("author_name", ""),
            "thumbnail_url": data.get("thumbnail_url", ""),
        })
    except Exception as e:
        out["oembed_error"] = str(e)
    try:
        out["description"] = youtube_description(url)
    except Exception as e:
        out["description_error"] = str(e)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
