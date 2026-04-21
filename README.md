# Helius-002 视频内容创作系统

> 模块化升级版 — 从 Helius-001 演进而来，现已全面应用 `00 - 05` 生命流水线架构！

## 概述

Helius-002 是新一代视频内容创作系统，采用模块化 Skill 架构。每个 Skill 专注单一能力，通过标准化的输入/输出接口串联成完整的内容生产线。现已对齐最先进的操作架构标准。

## 🗂 目录树与工作流水线

全系统采用以下顺序结构，高度可视化从文件下载到生成的流动过程：

```
Helius-002/
├── 00-docs/             # 系统文档与索引
│   ├── QUICKSTART.md
│   └── SKILLS_INDEX.md
├── 01-system/           # 底层系统与工具箱 (原 tools/)
│   ├── download.py
│   ├── transcribe.py
│   └── organize.py
├── 02-skills/           # AI 智能体/技能模块存放区 (原 skills/)
│   ├── _core/
│   │   └── config.yaml  # 全局配置文件
│   ├── 01_获取类：video-download / materials-collector...
│   ├── 02_分析类：transcription / video-analysis / channel-analysis...
│   ├── 03_生成类：script-generator / tts...
│   └── 05_风格类：moneyxyz / dankoe...
├── 03-inputs/           # 输入库 (原 workspace/inputs/) — 存放下载好的源素材
├── 04-outputs/          # 输出库 (原 workspace/outputs/) — 存放最终结构化打包好的内容
├── 05-temp/             # 临时与运行站 (临时转码、日志文件存放)
└── helius.py            # 主程序唯一交互入口 (`python3 helius.py`)
```

> **♻️ 数据流转逻辑**:
> 数据从网络上被下载到 **`03-inputs`** -> 通过 **`01-system`** 底层组件或 **`02-skills`** 处理加工（过程中利用 **`05-temp`** 周转）-> 最终沉淀在 **`04-outputs`** 形成高度干净的素材库。

## 核心哲学：MoneyXYZ 三角结构

所有脚本生成遵循三大原则：

1. **认知反差 (Contrarian Truth)** — 从大众认知反面切入
2. **理性证据 (Rational Evidence)** — 引用权威数据/书籍
3. **感性共鸣 (Emotional Resonance)** — 朋友般的坦诚聊天

## 快速开始

详见 [QUICKSTART.md](00-docs/QUICKSTART.md)

## Skill 索引

详见 [SKILLS_INDEX.md](00-docs/SKILLS_INDEX.md)

## 依赖
- Python 3.8+
- yt-dlp (`pip install yt-dlp`)
- FFmpeg
- OpenAI API Key（用于 Whisper / TTS）
