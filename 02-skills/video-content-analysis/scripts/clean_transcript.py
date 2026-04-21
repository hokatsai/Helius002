#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def clean_text(text: str) -> str:
    text = text.replace("\r", "")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(um|uh|啊|呃|就是|然后然后)+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*([。！？.!?])\s*", r"\1\n\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    if len(sys.argv) < 2:
        print("usage: clean_transcript.py <input-file>", file=sys.stderr)
        sys.exit(1)
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="ignore")
    print(clean_text(raw))


if __name__ == "__main__":
    main()
