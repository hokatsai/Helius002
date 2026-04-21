# Skills 索引

## 全部 Skills

| Skill | 触发词 | 核心功能 | 状态 |
| --- | --- | --- | --- |
| [video-download](../02-skills/video-download/SKILL.md) | 下载视频、下载YouTube | yt-dlp 下载，Chrome Cookie，AVC 优先 | ✅ 就绪 |
| [transcription](../02-skills/transcription/SKILL.md) | 转录、字幕、转写 | 字幕下载 + Whisper API 转录 + 清理 | ✅ 就绪 |
| [materials-organizer](../02-skills/materials-organizer/SKILL.md) | 整理素材、整理下载 | 扫描 + 去重 + library 构建 | ✅ 就绪 |
| [materials-collector](../02-skills/materials-collector/SKILL.md) | 收集素材、热点追踪 | 多源收集 + 周报 + trend_score | ✅ 就绪 |
| [channel-analysis](../02-skills/channel-analysis/SKILL.md) | 频道分析、账号战略、用户画像 | 8支柱 + Topic Filter + **Strategy 模式** | ⬆️ 已升级 |
| [video-content-analysis](../02-skills/video-content-analysis/SKILL.md) | 视频拆解、内容分析 | v2.1 Pipeline: metadata→字幕→分析→报告 | ✅ 就绪 |
| [video-analysis](../02-skills/video-analysis/SKILL.md) | 分镜、剪辑节奏、视觉规划 | 14镜头 + B-roll + **Visual Plan 模式** | ⬆️ 已升级 |
| [long-video-storyboard](../02-skills/long-video-storyboard/SKILL.md) | 长视频分镜、导演分镜、节奏设计 | 6-10分钟长视频分镜 + 节奏波形 + 认知负担控制 | ✅ 新建完成 |
| [script-generator](../02-skills/script-generator/SKILL.md) | /money、/hook、/dankoe、/renzhi、/short | **多风格脚本引擎** + 短视频协议 | ⬆️ 已升级 |
| [tts](../02-skills/tts/SKILL.md) | 配音、TTS、AI配音 | OpenAI/ElevenLabs + 情绪对齐 | ✅ 就绪 |
| [triangle-narrative](../02-skills/triangle-narrative/SKILL.md) | 三角结构、/money | 三角脚本 + 14镜头 + 8支柱 + 标题公式 | ✅ 就绪 |
| [dankoe](../02-skills/dankoe/SKILL.md) | Dan Koe、P3框架 | P3框架 + 2小时生态 + 内容瀑布流 | ✅ 就绪 |
| [renzhi-convenience-store](../02-skills/renzhi-convenience-store/) | 認知便利店M | 中文长视频解说风格 + 视频生成 | ✅ 就绪 |
| [ai-runner](../02-skills/ai-runner/SKILL.md) | AI执行、AI任务 | Codex/Gemini/Tavily 多模型调度 | ✅ 就绪 |
| [youtube-diagnostics](../02-skills/youtube-diagnostics/SKILL.md) | YouTube诊断 | runtime/cookie/字幕/下载 故障诊断 | ✅ 就绪 |
| [topic-scorer](../02-skills/topic-scorer/SKILL.md) | 选题评分、/score、选题排序 | 五维度评分 + 阶段自适应权重 + 周报联动 | ✅ 新建完成 |
| [humanizer-zh](../02-skills/humanizer-zh/SKILL.md) | 去AI感、/humanize | 基于维基百科规则去AI痕迹，增加文本灵魂 | ✅ 新建完成 |
| [packaging-optimizer](../02-skills/packaging-optimizer/SKILL.md) | 包装优化、/package | 10+标题变体 + 大字封面 + 前3秒Hook + 平台适配 | ✅ 新建完成 |
| [content-repurposer](../02-skills/content-repurposer/SKILL.md) | 一稿多发、/repurpose | 长视频切Shorts/改写图文/提炼推文及Newsletter | ✅ 新建完成 |
| [content-review-loop](../02-skills/content-review-loop/SKILL.md) | 数据复盘、/review | 分析高表现与低表现归因并回流系统配置 | ✅ 新建完成 |


## Skill 关系图

```
输入 (URL / 主题 / 素材)
    │
    ▼
┌──────────────────┐
│  video-download  │ ──► 03-inputs/
└────────┬─────────┘
         │
    ┌────┴────────────────┐
    ▼                     ▼
┌──────────────┐   ┌──────────────────┐
│ materials-   │   │  youtube-        │
│ organizer    │   │  diagnostics     │
└──────┬───────┘   └──────────────────┘
       │
  ┌────┴────────┐
  ▼             ▼
┌──────────┐  ┌──────────────────┐
│ trans-   │  │ video-content-   │
│ cription │  │ analysis (v2.1)  │
└────┬─────┘  └────────┬─────────┘
     │                 │
     │    ┌────────────┤
     ▼    ▼            ▼
┌────────────────┐  ┌─────────────────┐
│ channel-       │  │ Creator Skills  │
│ analysis       │  │  ├ moneyxyz     │
│ ├ Analysis     │  │  ├ dankoe       │
│ └ Strategy ⬆️  │  │  └ renzhi-*     │
└───────┬────────┘  └────────┬────────┘
        │                    │
        └──────────┬─────────┘
                   ▼
         ┌──────────────────┐
         │ script-generator │  ← 多风格脚本引擎 ⬆️
         │ /money /dankoe   │
         │ /renzhi /short   │
         └────────┬─────────┘
                  │
            ┌─────┴──────┐
            ▼            ▼
     ┌────────────┐  ┌───────┐
     │ video-     │  │  tts  │
     │ analysis   │  └───────┘
     │ ├ Storyboard│
     │ └ Visual   │
     │   Plan ⬆️  │
     └────────────┘
             │
             ▼
     ┌───────────────────┐
     │ long-video-       │
     │ storyboard        │
     │ 6-10min rhythm    │
     │ + attention design│
     └───────────────────┘

     ┌─────────────────────────────────┐
     │ materials-collector (独立定时)   │
     │ ai-runner (统一调度)             │
     └─────────────────────────────────┘
```

## 斜杠指令

| 指令 | Skill | 功能 |
| --- | --- | --- |
| `/money [主题]` | script-generator | MoneyXYZ 五步结构完整脚本 |
| `/dankoe [主题]` | script-generator | Dan Koe P3 框架脚本 ⬆️ |
| `/renzhi [主题]` | script-generator | 認知便利店M 深度解说脚本 ⬆️ |
| `/hook [主题]` | script-generator | 5 个爆款标题 + 开场白 |
| `/hooks [主题]` | script-generator | 多风格开场变体 ⬆️ |
| `/short [主题]` | script-generator | 30s/60s/90s 短视频脚本 ⬆️ |
| `/refine [文本]` | script-generator | 降维类比优化 + 情感锚点 |
| `/humanize [文本]` | humanizer-zh | 大幅降低文字中的AI机翻感 ⬆️ |
| `/package [脚本]` | packaging-optimizer | 一键生成：10标题+5封面文案+3Hook ⬆️ |
| `/repurpose [脚本]` | content-repurposer | 一键生成 Shorts / 图文 / 推文 / EDM 多版本 |
| `/toshort [脚本]` | content-repurposer | 专门提炼并输出竖屏短视频脚本格式 |
| `/review [数据]` | content-review-loop | 进行基于后台发行表现的数据复盘及破局诊断 |
| `/check [脚本]` | script-generator | 自检：权威引用 + 说教感 + 逻辑闭环 |

## 配置

所有配置集中在 `02-skills/_core/config.yaml`：

- `video_download.*` — 下载质量参数
- `transcription.*` — 字幕/转录参数
- `script_generator.*` — 脚本引擎参数（含多风格配置）
- `tts.*` — 语音合成参数
- `channel_analysis.*` — 8 大支柱 + 标题公式 + Strategy 参数
