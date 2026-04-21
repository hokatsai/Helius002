import sys
import os

print("Checking faster-whisper dependency...")
try:
    from faster_whisper import WhisperModel
except ImportError:
    print("Installing faster-whisper (this is a one-time setup and takes about 1 minute)...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "faster-whisper"], stdout=subprocess.DEVNULL)
    from faster_whisper import WhisperModel

import re

# Model selection
model_size = "base"
print(f"Loading '{model_size}' model for local transcription...")
# int8 is best for CPU
model = WhisperModel(model_size, device="cpu", compute_type="int8")

video_path = r"C:\Users\MSS\Desktop\Helius-002\03-inputs\Gemini_AI-v19Tzzbq0c0\Gemini如何史詩級反超ChatGPT？你不知道的Google Gemini誕生真實故事！揭秘Google AI戰爭中的致勝武器：TPU晶片+超長記憶力｜名人商業解密-v19Tzzbq0c0.mp4"

print("Starting transcription (this may take a few minutes)...")
segments, info = model.transcribe(video_path, beam_size=5, language="zh")

print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")

text_lines = []
for segment in segments:
    text_lines.append(segment.text)
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

# Post processing for clean Markdown formatting
full_text = "".join(text_lines)
sentences = re.split(r'([。！？!?])', full_text)

paragraphs = []
current_p = ""
# Group sentences by punctuation
if len(sentences) > 1:
    for i in range(0, len(sentences)-1, 2):
        current_p += sentences[i] + sentences[i+1]
        # break paragraph at around 150 chars
        if len(current_p) > 150:
            paragraphs.append(current_p.strip())
            current_p = ""
    if current_p:
        paragraphs.append(current_p.strip())
else:
    paragraphs.append(full_text)

final_md = "# Gemini如何史詩級反超ChatGPT？ Google Gemini誕生真實故事\n\n" + "\n\n".join(paragraphs)

out_path = r"C:\Users\MSS\Desktop\Helius-002\03-inputs\Gemini_AI-v19Tzzbq0c0\script.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(final_md)

print("Transcription Complete. Clean script saved to", out_path)
