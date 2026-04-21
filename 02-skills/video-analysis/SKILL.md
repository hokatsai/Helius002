---
name: video-analysis
description: 触发词：视频分析、分镜、剪辑节奏、B-roll、视觉规划、镜头表、画面设计。当你需要分析视频结构、设计分镜、规划剪辑节奏、生成完整视觉方案时使用。
---

# Video Analysis & Visual Planner Skill

## 功能说明
本 Skill 承载 Helius-002 核心的视频内容建模与视觉规划逻辑。它具备两大模式：
1. **分镜模式（Storyboard）**：将脚本拆解为 14 个标准镜头，生成分镜表与 AI 指令
2. **视觉规划模式（Visual Plan）**：基于脚本生成完整的可执行视觉方案，含时间轴、素材清单、AI配图

---

## 核心能力

### 分镜能力（原有）
- 14 镜头标准分镜模板
- 剪辑节奏规则引擎
- B-roll 智能建议（语义补偿 + 情绪渲染）
- 多平台适配（TikTok/Bilibili/YouTube）

### 视觉规划能力（新增 ⬆️）
- **A-roll / B-roll 时间轴切分**：精确标注每秒的画面类型
- **关键画面节点标记**：情感高点 / 论证转折 / CTA 触发点
- **板书 / 打字机片段规划**：typewriter-video 段落建议
- **AI 配图精细化 prompt**：区分实拍风 / 插画风 / 数据图表 / 文字屏
- **脚本段落映射**：镜头与脚本段落的一一对应关系

---

## 输入/输出规范

### 输入
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| topic | string | 是 | 视频主题或原始文案 |
| script | string | 否 | 完整脚本文本（来自 script-generator）|
| target_platform | string | 否 | TikTok/Bilibili/YouTube（默认 YouTube）|
| duration_limit | int | 否 | 期望时长秒数（默认 45-60s）|
| mode | string | 否 | `storyboard`（默认）/ `visual-plan` / `full` |

### 输出 — Storyboard 模式（原有）
| 参数 | 类型 | 说明 |
|------|------|------|
| storyboard | list | 14 镜头分镜表（含画面/旁白/Prompt）|
| clip_plan | object | 剪辑指导方案（BGM/音效/转场）|
| ai_prompts | list | AI 视觉生成指令清单 |

### 输出 — Visual Plan 模式（新增 ⬆️）
| 参数 | 类型 | 说明 |
|------|------|------|
| shot_timeline | json | 时间轴级镜头表 |
| broll_list | markdown | 带来源建议的 B-roll 清单 |
| ai_image_prompts | markdown | 精细化 AI 配图 prompt |
| typewriter_segments | markdown | 打字机视频片段建议 |
| key_moments | json | 关键画面节点标记 |
| script_mapping | json | 脚本段落 ↔ 镜头映射 |

---

## Visual Plan 模式详细说明（新增 ⬆️）

### 时间轴镜头表 `shot_timeline.json`

每个镜头包含：

```json
{
  "shot_id": 1,
  "start_time": "0:00",
  "end_time": "0:03",
  "duration_sec": 3,
  "type": "A-roll",
  "sub_type": "talking_head",
  "script_section": "Hook",
  "script_text": "你以为省钱是财富自由的钥匙？",
  "visual_description": "正面中景，轻微摇头，表情克制",
  "overlay_text": null,
  "broll_alternative": "stock: 存钱罐碎裂慢动作",
  "energy_level": "high",
  "is_key_moment": true,
  "key_moment_type": "hook"
}
```

### A-roll / B-roll 切分规则

| 类型 | 占比建议 | 使用场景 |
|------|----------|----------|
| **A-roll（主画面）** | 40-60% | 说话人出镜、核心论点阐述 |
| **B-roll（辅助画面）** | 20-35% | 数据展示、案例图片、情绪渲染 |
| **Text Screen（文字屏）** | 10-20% | 关键数字、核心金句、名言引用 |
| **Typewriter（打字机）** | 5-15% | 代码展示、逐字呈现、过程演示 |

### 关键画面节点 `key_moments.json`

```json
[
  {
    "time": "0:00",
    "type": "hook",
    "label": "开场钩子",
    "visual_requirement": "高能量，快速吸引注意力",
    "suggested_technique": "快剪 + 大字幕 + 音效"
  },
  {
    "time": "1:30",
    "type": "emotional_turn",
    "label": "情感反转",
    "visual_requirement": "节奏放缓，画面留白",
    "suggested_technique": "慢推镜头 + 降低BGM + 停顿"
  },
  {
    "time": "3:00",
    "type": "cta_trigger",
    "label": "行动号召",
    "visual_requirement": "明确指引，视觉聚焦",
    "suggested_technique": "文字屏 + 箭头指引 + 订阅动画"
  }
]
```

### Typewriter 片段规划 `typewriter_segments.md`

适用场景：
- 代码/命令行展示
- 重要概念逐字呈现
- 清单/步骤逐条展示
- "打字机效果"增加观看沉浸感

每个片段输出：
```
## Typewriter Segment #1
- 位置：1:20 - 1:35
- 关联脚本段：Core Argument - Point 1
- 内容：
  1. 反脆弱 ≠ 不怕打击
  2. 反脆弱 = 从打击中变强
  3. 反脆弱 = 波动是养分
- 字体建议：等宽字体，深色背景
- 动画速度：中速（每行 2 秒）
```

### AI 配图 Prompt 精细化 `ai_image_prompts.md`

每个 prompt 标注风格类型：

| 风格 | 适用场景 | Prompt 模式 |
|------|----------|-------------|
| 📸 **实拍风** | 案例、故事、人物 | "cinematic photo of..., natural lighting, shallow DOF" |
| 🎨 **插画风** | 概念、抽象、比喻 | "minimalist flat illustration of..., muted colors, clean lines" |
| 📊 **数据图表** | 统计、对比、趋势 | "infographic showing..., dark background, accent color #xxx" |
| 📝 **文字屏** | 金句、名言、关键数字 | "text card: '[内容]', font: bold sans-serif, bg: gradient" |

---

## 14 镜头标准分镜模板（原有，保留）

| 镜头# | 时长 | 类型 | 内容要点 |
|-------|------|------|---------|
| 1 | 0-3s | **开场Hook** | 反直觉陈述 |
| 2 | 3-10s | **问题引入** | 观众痛点 |
| 3 | 10-20s | **过渡** | 预告内容 |
| 4 | 20-40s | **故事1** | 权威引用 |
| 5 | 40-60s | **Point 1** | 核心观点1 |
| 6 | 60-80s | **过渡** | 连接词 |
| 7 | 80-100s | **故事2** | 案例引用 |
| 8 | 100-120s | **Point 2** | 核心观点2 |
| 9 | 120-130s | **过渡** | 连接词 |
| 10 | 130-150s | **故事3** | 个人经历 |
| 11 | 150-170s | **Point 3** | 核心观点3 |
| 12 | 170-180s | **Emotion** | 情感共鸣 |
| 13 | 180-190s | **总结** | Point回顾 |
| 14 | 190-200s | **CTA** | 微行动 |

---

## 执行流程

### Storyboard 模式
1. 解析 topic（如果是脚本则提取关键信息）
2. 应用 14 镜头模板生成分镜结构
3. 计算剪辑节奏点（黄金 3 秒/痛点/高潮等）
4. 生成 B-roll 建议（语义 + 情绪双维度）
5. 输出 AI Prompt 清单
6. 生成剪辑指导方案

### Visual Plan 模式（新增 ⬆️）
1. 接收完整脚本（优先从 script-generator 获取）
2. 将脚本拆分为段落，建立段落 ↔ 镜头映射
3. 对每个段落分配 A-roll / B-roll / Text / Typewriter 类型
4. 生成时间轴级镜头表 `shot_timeline.json`
5. 标记关键画面节点 `key_moments.json`
6. 生成 B-roll 清单（含素材来源建议）
7. 为需要 AI 配图的镜头生成精细化 prompt
8. 识别适合 typewriter 效果的段落并生成规划
9. 输出完整视觉方案到 `04-outputs/visual-plans/`

### Full 模式
依次执行 Storyboard → Visual Plan，合并输出

---

## 错误处理
### 错误类型与降级方案
| 错误类型 | 降级方案 | 重试机制 |
|----------|----------|----------|
| 脚本过长 | 自动截断或分段处理 | 不重试 |
| 主题模糊 | 返回通用模板 + 建议明确主题 | 不重试 |
| LLM 生成失败 | 回退到预设模板填充 | 3 次重试 |
| 无脚本输入（Visual Plan） | 提示先用 script-generator 生成脚本 | 不重试 |

### 错误日志
所有错误自动记录到 `06-logs/video-analysis/YYYY-MM-DD.log`

## 与其他 Skill 协作
- **依赖**: script-generator（获取脚本文案 — Visual Plan 模式强依赖）
- **依赖**: tts（使用配音时长校准节奏）
- **被依赖**: 视频剪辑工具（使用分镜和视觉方案）
- **依赖**: env_checker（检查 LLM API 可用性）

## 使用示例

### 示例1：分镜生成（Storyboard 模式）
> "帮我分析'个人生产力工具'主题，生成 14 个分镜并规划剪辑节奏"

### 示例2：完整视觉方案（Visual Plan 模式，新增 ⬆️）
> "我用 /money 生成了一个关于'反脆弱'的脚本，帮我生成完整视觉方案，包含时间轴、B-roll 清单和 AI 配图 prompt"

### 示例3：Short 视频分镜
> "对这个脚本进行分镜设计，目标平台 TikTok，时长 45s"

### 示例4：Typewriter 规划（新增 ⬆️）
> "这个脚本里有 3 个核心概念适合用打字机效果呈现，帮我规划 typewriter 片段"

## 依赖
- **Content-Generator**: script-generator 提供文案
- **Visual-Standard**: AI Prompt 美学标准
- **API Keys**: OPENAI_API_KEY（LLM 生成）
