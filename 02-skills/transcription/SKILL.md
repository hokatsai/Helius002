---
name: transcription
description: 触发词：转录、字幕、转写、视频转文字、提取脚本。当你需要把视频转成精美文字稿或字幕时使用。增强了免 API Key 的本地免费 AI 转录与智能长文自动排版能力。
---

# Transcription Skill

## 功能说明
本 Skill 负责将音视频媒体转化为可直接阅读、易于提取结构的精美文章资产。它不仅支持官方字幕抓取，还特别强化了**零 API Key 环境下的本地免费转录 (Faster-Whisper)**，并内建专门针对中文转录产物的**文章级优美排版算法 (Semantic Formatting)**。

最终，该 Skill 必须自动把影片、原始字幕、以及排版后的最终版 Markdown 脚本 (`script.md`) 收纳在独立的资产资料夹中，方便送给 `video-content-analysis` 或 `long-video-storyboard` 做下一步拆解。

## 核心工作流 (Auto-Pipeline)
当你收到「提取某影片脚本 / 转录影片」的请求时，请执行以下四步标准化流程：

### Step 1: 多源字幕获取 (yt-dlp)
- 首先使用内置或你的 `run_command` 利用 `yt-dlp` 尝试提取官方中文字幕 (.vtt)。
- 💡 如果成功抓到 `.vtt`：跳過 Step 2，直接進入 Step 3 的「原生標點排版法」。
- 💡 如果遇到 `TranscriptsDisabled` (沒有字幕) 且使用者無 OpenAI API Key：進入 Step 2。

### Step 2: 免費本地極速轉錄 (Faster-Whisper)
若判斷無法依賴 API 與現成字幕，請透過 Python 腳本在背景自動為使用者處理：
1. **靜默安裝**：`pip install faster-whisper`（由於其依賴 CTranslate2，不需下載肥大的 PyTorch，極度輕量且適合 CPU）。
2. **本地推論**：撰寫臨時 Python 腳本，呼叫 `WhisperModel("base", device="cpu", compute_type="int8")`，直接餵入目標 `.mp4` 音軌，抓取生成之 `segment.text` 原生無標點文本。

### Step 3: 文章級排版演算法 (The Reformatting Logic)
取得純文字稿後，你**必須**撰寫 Python 對文本進行重新排版，以消除所有「時間軸」與「文字磚塊感」，讓它看起來像一篇完整的專欄文章。針對來源有兩套邏輯：

👉 **針對原生 Whisper 文本 (利用空格分隔)**：
- 將 Whisper 的原生「空格」替換為「逗號 (，)」以還原人類停頓。
- 每累積約 120-150 字，強制插入「句號 (。)」，並輸出兩個換行符 (`\n\n`) 生成全新段落。

👉 **針對原生 VTT 文本 (已含標點)**：
- 剔除 HTML 標籤、時間軸數字與純英文翻譯軌，只抓出目標語言行。
- 透過正規表達式 `re.split(r'([。！？!?])')` 以句點精確斷句。
- 將短句合併，每 3 句話或 150 個字，強制進行一次段落切割 (`\n\n`)，確保版面透氣度。

### Step 4: 結構化資產與綜合標註 (Annotated Script)
最後一步，在 `03-inputs/` 底下自動為該影片建立**獨立資料夾**（推薦命名格式：`影片標題-VideoID`），然後將原檔與**合併標註後的最終腳本**歸檔入內：
1. 原片：`xxx.mp4`
2. 原始：`xxx.vtt` (若有)
3. 終稿：**`script.md`** 

**⚡重要：未來的 `script.md` 應直接包含「創作者深度分析與文本結構標註」**
你不需要再額外生成分開的 `analysis_report.md`。取而代之的是，在輸出的文本腳本中：
- 必須在最上方增加 `## 💡 創作者思路與借鑒指南`，點出其腳本優勢。
- 必須把文本內文拆分，並加上類似 `### 📌 [核心觀點一] 摧毀「時間=燃料」的錯覺` 這種小標註，為段落寫上一句短評。
- 讓使用者讀這份稿子的時候，就能順便理解大神的節奏架構！

## 異常與降級機制
- 如果 `faster-whisper` 模型下載過慢，可自動切換 `model_size = "tiny"` 來加速。
- 遇到非中文影片，請在 WhisperModel 中指定 `language="en"` 等對應參數，並適度切換全形標點(`。`)為半形(`.` )。

## 輸入與產出
- **輸入**: 影片網址 URL 或是本地 `workspace/inputs` / `03-inputs` 裡頭的 MP4 檔。
- **產出**: 一個完整獨立、包含 `script.md` 乾淨腳本內容的資產目錄。
