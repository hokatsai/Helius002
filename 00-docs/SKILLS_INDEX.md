# Skills 使用導航

這份索引用來回答一個問題：**現在這一步應該用哪個 skill？**

不要把所有 skill 平鋪理解。先判斷你處在哪個階段：採集、理解、創作、發布，還是維護。

## 最常用工作流

### 1. 參考視頻二創流程

用於：你有一個參考視頻或 `script.md`，想提煉要點，重寫一篇相關但不照抄的新腳本，再生成分鏡。

```text
video-download
→ transcription
→ reference-script-rewriter
→ humanizer-zh
→ long-video-storyboard
```

最常見輸出：
- `01-key-points.md`
- `02-rewritten-video-script.md`
- `02-rewritten-video-script-humanized.md`
- `03-storyboard.md`

### 2. 從零寫長視頻腳本流程

用於：你只有一個主題，想直接生成一篇長視頻口播稿。

```text
script-generator
→ humanizer-zh
→ long-video-storyboard
```

可選下游：

```text
content-repurposer
→ packaging-optimizer
```

### 3. 成片發布準備流程

用於：腳本和分鏡已經完成，準備做標題、封面、短視頻切片、圖文分發。

```text
long-video-storyboard
→ content-repurposer
→ packaging-optimizer
```

### 4. 視頻研究流程

用於：你想拆解一個視頻為什麼有效，而不是立刻重寫。

```text
video-download
→ transcription
→ video-content-analysis
```

如果是整個頻道或帳號策略：

```text
channel-analysis
→ topic-scorer
```

## 快速路由表

| 你想做什麼 | 優先用 | 典型輸入 | 典型輸出 | 常用度 |
|---|---|---|---|---|
| 下載 YouTube 視頻 | [video-download](../02-skills/video-download/SKILL.md) | URL | 視頻 / 字幕 | 常用 |
| 視頻轉文字 | [transcription](../02-skills/transcription/SKILL.md) | 視頻 / 音頻 / URL | transcript / subtitles | 常用 |
| 根據參考腳本重寫新腳本 | [reference-script-rewriter](../02-skills/reference-script-rewriter/SKILL.md) | `script.md` | 新腳本 / human / 分鏡 | 常用 |
| 從零生成長視頻腳本 | [script-generator](../02-skills/script-generator/SKILL.md) | 主題 / 指令 | 長視頻口播稿 | 常用 |
| 去 AI 味 / 口播自然化 | [humanizer-zh](../02-skills/humanizer-zh/SKILL.md) | 腳本 / 文案 | human 版本 | 常用 |
| 長視頻分鏡 / 剪映清單 | [long-video-storyboard](../02-skills/long-video-storyboard/SKILL.md) | 腳本 | 分鏡 / B-roll / 剪映提示 | 常用 |
| 一稿多發 | [content-repurposer](../02-skills/content-repurposer/SKILL.md) | 長腳本 | Shorts / 小紅書 / 推文 / Newsletter | 常用 |
| 標題封面包裝 | [packaging-optimizer](../02-skills/packaging-optimizer/SKILL.md) | 腳本 / 主題 | 標題 / 封面大字 / Hook | 常用 |
| 分析視頻內容結構 | [video-content-analysis](../02-skills/video-content-analysis/SKILL.md) | URL / transcript | 分析報告 | 偶爾用 |
| 分析頻道定位 | [channel-analysis](../02-skills/channel-analysis/SKILL.md) | 頻道 / 內容樣本 | 頻道策略 / 用戶畫像 | 偶爾用 |
| 選題打分排序 | [topic-scorer](../02-skills/topic-scorer/SKILL.md) | 選題列表 | 優先級 / 分數 | 偶爾用 |
| 發布後復盤 | [content-review-loop](../02-skills/content-review-loop/SKILL.md) | 後台數據 | 表現歸因 / 改進建議 | 偶爾用 |
| YouTube 下載故障排查 | [youtube-diagnostics](../02-skills/youtube-diagnostics/SKILL.md) | 錯誤信息 | 診斷方案 | 排障用 |

## 分層理解

### 採集層

| Skill | 用途 | 狀態 |
|---|---|---|
| [video-download](../02-skills/video-download/SKILL.md) | 下載 YouTube 或其他平台視頻素材 | 常用 |
| [transcription](../02-skills/transcription/SKILL.md) | 視頻/音頻轉文字、字幕提取 | 常用 |
| [materials-collector](../02-skills/materials-collector/SKILL.md) | 批量收集素材、熱點追蹤 | 偶爾用 |
| [materials-organizer](../02-skills/materials-organizer/SKILL.md) | 整理下載素材、索引、去重 | 偶爾用 |

### 理解層

| Skill | 用途 | 狀態 |
|---|---|---|
| [reference-script-rewriter](../02-skills/reference-script-rewriter/SKILL.md) | 從參考腳本提煉要點，重寫新腳本 | 常用 |
| [video-content-analysis](../02-skills/video-content-analysis/SKILL.md) | 拆解視頻內容、結構、創作方法 | 偶爾用 |
| [video-analysis](../02-skills/video-analysis/SKILL.md) | 偏短視頻/視覺規劃/14 鏡頭方案 | 偶爾用 |
| [channel-analysis](../02-skills/channel-analysis/SKILL.md) | 頻道定位、競品、用戶畫像、內容邊界 | 偶爾用 |
| [topic-scorer](../02-skills/topic-scorer/SKILL.md) | 選題分數和優先級 | 偶爾用 |
| [youtube-diagnostics](../02-skills/youtube-diagnostics/SKILL.md) | yt-dlp、cookie、字幕、下載故障診斷 | 排障用 |

### 創作層

| Skill | 用途 | 狀態 |
|---|---|---|
| [script-generator](../02-skills/script-generator/SKILL.md) | 從主題生成長視頻/短視頻腳本 | 常用 |
| [humanizer-zh](../02-skills/humanizer-zh/SKILL.md) | 去 AI 感、讓口播更自然 | 常用 |
| [long-video-storyboard](../02-skills/long-video-storyboard/SKILL.md) | 6-10 分鐘長視頻分鏡、剪映執行清單 | 常用 |
| [tts](../02-skills/tts/SKILL.md) | 文字轉語音、AI 配音 | 需要配音時用 |

### 風格模板層

這些更像「風格素材」或「腳本模板」，通常不直接單獨調用，而是被 `script-generator` 使用。

| Skill | 用途 | 狀態 |
|---|---|---|
| [triangle-narrative](../02-skills/triangle-narrative/SKILL.md) | 認知反差 + 理性證據 + 情感共鳴 | 底層模板 |
| [dankoe](../02-skills/dankoe/SKILL.md) | Dan Koe / P3 框架 / 個人品牌方向 | 底層模板 |
| [renzhi-convenience-store](../02-skills/renzhi-convenience-store/) | 認知便利店M 中文長視頻解說風格 | 底層模板 |

### 發布層

| Skill | 用途 | 狀態 |
|---|---|---|
| [content-repurposer](../02-skills/content-repurposer/SKILL.md) | 長視頻轉 Shorts、小紅書、推文、Newsletter | 常用 |
| [packaging-optimizer](../02-skills/packaging-optimizer/SKILL.md) | 標題、封面大字、前 3 秒 Hook | 常用 |
| [content-review-loop](../02-skills/content-review-loop/SKILL.md) | 發布後數據復盤和歸因 | 偶爾用 |

### 系統/調度層

| Skill | 用途 | 狀態 |
|---|---|---|
| [ai-runner](../02-skills/ai-runner/SKILL.md) | 多模型任務調度、AI 任務執行 | 進階用 |

## 常用命令與觸發詞

| 指令 / 說法 | 對應 Skill | 用途 |
|---|---|---|
| `根據這個 script.md 重寫一篇相關視頻腳本` | `reference-script-rewriter` | 參考腳本二創 |
| `human 這個文件` / `去 AI 感` | `humanizer-zh` | 生成自然口播版本 |
| `生成長視頻分鏡` / `剪映操作清單` | `long-video-storyboard` | 腳本轉分鏡 |
| `/money [主題]` | `script-generator` | 三角結構長視頻腳本 |
| `/dankoe [主題]` | `script-generator` | Dan Koe 風格腳本 |
| `/renzhi [主題]` | `script-generator` | 認知便利店風格腳本 |
| `/hook [主題]` | `script-generator` | 標題和開場 |
| `/short [主題]` | `script-generator` | 30/60/90 秒短視頻 |
| `/repurpose [腳本]` | `content-repurposer` | 一稿多發 |
| `/package [腳本]` | `packaging-optimizer` | 標題封面包裝 |
| `/score [選題]` | `topic-scorer` | 選題評分 |
| `/review [數據]` | `content-review-loop` | 發布後復盤 |

## 什麼時候不要用某些 Skill

- 不要用 `long-video-storyboard` 來重寫參考視頻腳本；先用 `reference-script-rewriter`。
- 不要用 `video-analysis` 做 6-10 分鐘長視頻分鏡；優先用 `long-video-storyboard`。
- 不要直接用 `triangle-narrative`、`dankoe`、`renzhi-convenience-store`，除非你明確要研究這個風格本身；一般通過 `script-generator` 調用。
- 不要用 `content-repurposer` 寫主腳本；它適合主腳本完成後拆分平台版本。
- 不要在普通創作流程裡先用 `ai-runner`；它更適合多模型調度或複雜自動化。

## 暫時不用刪的原因

目前不建議刪 skill。更好的做法是先用這份導航分流：

- `常用`：高頻創作鏈路，優先維護。
- `偶爾用`：特定情況有價值，先保留。
- `底層模板`：不常直接調用，但可能支撐腳本風格。
- `排障用 / 進階用`：平時不用，出問題或做自動化時再用。

等使用一段時間後，如果某個 skill 長期沒有被觸發，再考慮合併或淘汰。

## 配置

全局配置集中在：

`02-skills/_core/config.yaml`

常見配置區：
- `video_download.*`：下載質量和 yt-dlp 參數
- `transcription.*`：字幕/轉錄參數
- `script_generator.*`：腳本引擎和多風格配置
- `tts.*`：語音合成參數
- `channel_analysis.*`：頻道分析和策略參數
