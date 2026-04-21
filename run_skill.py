import os
import re
import sys
import glob
import shutil
import subprocess

import sys

if len(sys.argv) > 1:
    video_id = sys.argv[1]
else:
    video_id = "4E49Net3-uA"
url = f"https://www.youtube.com/watch?v={video_id}"
base_dir = r"C:\Users\MSS\Desktop\Helius-002\03-inputs"

# 1. Download video & subs
temp_dir = os.path.join(base_dir, f"temp_{video_id}")
os.makedirs(temp_dir, exist_ok=True)

print(f"Downloading video {video_id} and checking for subtitles...")
dl_cmd = [
    "yt-dlp", 
    "-f", "bv*[vcodec^=avc1][height<=1080][fps<=60]+ba[ext=m4a]",
    "--merge-output-format", "mp4",
    "--write-subs",
    "--write-auto-subs",
    "--sub-langs", "zh-Hant,zh-TW,zh-Hans,zh-CN,zh",
    "-o", os.path.join(temp_dir, "%(title)s.%(ext)s"),
    url
]
subprocess.run(dl_cmd)

# 2. Directory structure
mp4_files = glob.glob(os.path.join(temp_dir, "*.mp4"))
if not mp4_files:
    print("Video download failed.")
    sys.exit(1)

video_path = mp4_files[0]
title = os.path.splitext(os.path.basename(video_path))[0]
clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
final_dir = os.path.join(base_dir, f"{clean_title}-{video_id}")
if os.path.exists(final_dir):
    shutil.rmtree(final_dir)
shutil.move(temp_dir, final_dir)

video_path_final = os.path.join(final_dir, os.path.basename(video_path))
vtt_files = glob.glob(os.path.join(final_dir, "*.vtt"))
script_md = os.path.join(final_dir, "script.md")

# 3. Process text
if vtt_files:
    print("Found official/auto VTT. Formatting native subtitles...")
    lines = []
    with open(vtt_files[0], "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("WEBVTT") or "-->" in line or line.startswith("Kind:") or line.startswith("Language:"):
                continue
            if re.search(r'[\u4e00-\u9fff]', line):
                line = re.sub(r'<[^>]+>', '', line)
                lines.append(line)
    raw_text = "".join(lines)
    
    sentences = re.split(r'([。！？!?])', raw_text)
    paragraphs = []
    curr = ""
    count = 0
    for i in range(0, len(sentences)-1, 2):
        if i+1 < len(sentences):
            curr += sentences[i] + sentences[i+1]
        count += 1
        if count >= 3 or len(curr) > 130:
            paragraphs.append(curr.strip())
            curr = ""
            count = 0
    if curr:
        paragraphs.append(curr.strip())
    
    final_output = f"# {title}\n\n" + "\n\n".join(paragraphs)

else:
    print("No VTT found. Booting up Faster-Whisper local AI transcription...")
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(video_path_final, beam_size=5, language="zh")
    text_lines = [seg.text for seg in segments]
    
    body = " ".join([l.strip() for l in text_lines])
    chunks = [c for c in body.split(' ') if c.strip()]
    
    paragraphs = []
    curr = []
    curr_len = 0
    for c in chunks:
        curr.append(c)
        curr_len += len(c)
        if curr_len > 120:
            paragraphs.append("，".join(curr) + "。")
            curr = []
            curr_len = 0
    if curr:
        paragraphs.append("，".join(curr) + "。")
    final_output = f"# {title}\n\n" + "\n\n".join(paragraphs)

with open(script_md, "w", encoding="utf-8") as f:
    f.write(final_output)

print(f"\n--- SUCCESS ---")
print(f"Data saved to: {final_dir}")
