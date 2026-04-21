---
name: tts
description: 触发词：配音、TTS、文字转语音、AI配音、语音合成。当你需要为视频生成旁白配音或语音时使用。
---

# TTS Skill

## 功能说明
本 Skill 为 Helius-002 视频创作系统提供核心音频动力。它将文本内容转化为符合系统审美风格的语音旁白，深度适配 Helius-002 的"清醒、孤独、克制、带一点希望"的情绪基调。

## 核心能力
- 多引擎支持（OpenAI TTS + ElevenLabs）
- 精准语速控制（0.5x - 2.0x）
- 情绪对齐（克制、自然、呼吸感）
- 自动化输出到 `workspace/temp/`

## 输入/输出规范
### 输入
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 需要转换的文本（建议单次 ≤500 字） |
| provider | string | 否 | openai（默认）/ elevenlabs |
| voice | string | 否 | OpenAI: alloy/echo/fable/onyx/nova/shimmer; ElevenLabs: Voice ID |
| speed | float | 否 | 语速 0.25-4.0，默认 1.0 |
| output_filename | string | 否 | 输出文件名，默认 tts_[timestamp].mp3 |

### 输出
| 参数 | 类型 | 说明 |
|------|------|------|
| success | bool | 执行状态 |
| audio_path | string | 生成音频的绝对路径 |
| metadata | object | 时长、字符数、消耗估算 |

## 执行流程
1. 验证文本长度（分段处理超长文本）
2. 根据 provider 调用对应 TTS API
3. 匹配语速与 BGM 风格
4. 输出到 `workspace/temp/`
5. 返回音频路径和元数据

## 错误处理
### 错误类型与降级方案
| 错误类型 | 降级方案 | 重试机制 |
|----------|----------|----------|
| OpenAI API 超时/失败 | 回退到 ElevenLabs | 3 次重试 |
| ElevenLabs 也失败 | 使用本地备选 TTS 或返回错误 | 3 次重试 |
| 文本超长 | 自动分段处理 | 不重试 |
| 磁盘空间不足 | 清理 temp 后重试 | 不重试 |

### 错误日志
所有错误自动记录到 `workspace/logs/tts/YYYY-MM-DD.log`

## 与其他 Skill 协作
- **依赖**: script-generator（获取脚本文本）
- **被依赖**: video-analysis（使用配音生成视频）
- **依赖**: env_checker（检查 TTS API keys）

## 使用示例
### 示例1：默认 OpenAI 旁白
```bash
helius.py tts --text "在这个寂静的深夜，我们与孤独达成和解，却从未放弃寻找那一抹微光。" --voice "onyx" --speed 0.9
```

### 示例2：ElevenLabs 高级合成
```bash
sag tts --provider elevenlabs --text "希望，是破碎后的重塑。" --voice "Josh" --output_filename "hope_narration.mp3"
```

## 依赖
- **API Keys**: OPENAI_API_KEY 或 ELEVENLABS_API_KEY
- **工具链**: sag 命令行工具（可选）
- **BGM 建议**: 参见 VideoMachine-Agent.toml 的 BPM 推荐

## 情绪指南
- **避免**: 夸张播音腔、导购音
- **推荐**: 呼吸感停顿、低沉平稳、内在张力
