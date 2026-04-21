# Helius-002 快速入门

## 环境准备

```bash
# 1. 安装依赖
pip install yt-dlp openai

# 2. 安装 FFmpeg（用于音视频处理）
# macOS
brew install ffmpeg
# Ubuntu
sudo apt install ffmpeg

# 3. 配置 API Keys
# 编辑 02-skills/_core/config.yaml
```

## 典型工作流

### 1. 下载视频素材

```bash
# 基础下载（Chrome Cookie）
python3 01-system/download.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 使用本地 Cookie 文件
python3 01-system/download.py "URL" --cookies cookies.txt

# 指定输出目录
python3 01-system/download.py "URL" -o 03-inputs/
```

### 2. 整理素材

```bash
# 扫描并生成索引
python3 01-system/organize.py --source 03-inputs/ --output-base 04-outputs/

# 启用去重
python3 01-system/organize.py --source 03-inputs/ --apply-dedupe
```

### 3. 下载字幕/转录

```bash
# 下载字幕（VTT/SRT）
python3 01-system/transcribe.py download "https://www.youtube.com/watch?v=VIDEO_ID"

# 清理为纯文本
python3 01-system/transcribe.py clean 05-temp/transcription/video.vtt

# Whisper API 转录
python3 01-system/transcribe.py transcribe 05-temp/audio.m4a -k YOUR_API_KEY
```

### 4. 生成脚本

在 Agent 中使用斜杠指令：

```
/money 为什么努力不一定有回报

/hook AI时代如何保持竞争力

/refine [粘贴已有文案]

/check [粘贴脚本]
```

### 5. 频道分析

```
分析频道 https://www.youtube.com/@channel

根据 8 大内容支柱诊断定位问题
```

## Skill 调用方式

| 需求 | 触发词 | 输出 |
| --- | --- | --- |
| 下载视频 | "下载视频"、"下载YouTube" | 03-inputs/*.mp4 |
| 字幕/转录 | "转录"、"视频转文字" | 05-temp/*.txt |
| 整理素材 | "整理素材"、"生成索引" | 04-outputs/*/index.md |
| 频道分析 | "频道分析"、"竞品分析" | 定位/选题/标题报告 |
| 脚本生成 | "/money"、"写脚本" | 完整视频制作包 |
| 视频分析 | "分镜"、"剪辑节奏" | 14 镜头分镜表 |
| TTS | "配音"、"AI配音" | 05-temp/*.mp3 |

## 输出产物

每个完整视频项目会产出：

```
04-outputs/{run_id}/
├── final/
│   └── library/by_video_id/{video_id}/
│       ├── video/named.mp4
│       ├── captions/zh-Hant.vtt
│       ├── captions/en.vtt
│       └── transcripts/transcript_zh-Hant.txt
└── intermediate/
    ├── youtube_assets.tsv
    ├── duplicates.tsv
    └── actions_taken.tsv
```
