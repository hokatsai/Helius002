---
name: editing-execution-planner
description: 剪輯執行計劃、粗剪精剪、A-roll 挑段、B-roll 落位、字幕樣式、音樂音效、導出檢查、剪映/CapCut 操作清單。當你需要把腳本、分鏡、A-roll 拍攝素材和 B-roll 建議轉成完整剪輯工作清單時使用。
---

# Editing Execution Planner Skill

## 功能說明
把腳本、分鏡、拍攝計劃或素材清單轉成可執行的剪輯流程。它比 `long-video-storyboard` 更靠近落地剪輯：管理 A-roll 挑段、粗剪、精剪、B-roll、字幕、音效、導出和發布前 QA。

## 適用場景
- A-roll 已拍完，需要剪輯順序。
- 已有分鏡，需要轉成剪映/CapCut 執行清單。
- 需要明確區分粗剪、精剪、字幕、音效和導出。
- 想避免剪輯時邊想邊做，導致返工。

## 輸入
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| script_or_storyboard | string | 是 | 腳本、分鏡或視頻方向稿 |
| aroll_plan | string | 否 | A-roll 拍攝計劃或素材列表 |
| editing_tool | string | 否 | 默認 `CapCut / 剪映` |
| platform | string | 否 | 默認 `YouTube / Bilibili` |
| output_dir | string | 否 | 默認寫入對應 `04-outputs/{中文主題包}/` |

## 輸出
默認輸出：

1. `05-editing-execution-plan.md`
   - 項目設置
   - 素材整理
   - 粗剪清單
   - A-roll 挑段規則
   - 精剪補充
   - B-roll 落位
   - 字幕樣式
   - 音樂/音效
   - 導出檢查
   - 發布前 QA

## 工作流程

### Step 1：建立剪輯工程
輸出項目設置：
- 畫幅
- 幀率
- 分辨率
- 音頻規格
- 文件夾結構
- 素材命名規則

### Step 2：A-roll 粗剪
先保證主線可看。

只做：
- 刪停頓
- 刪重複
- 刪口頭禪
- 刪講錯重說
- 挑最好的一版 take
- 保留必要停頓

### Step 3：結構檢查
確認：
- 開頭 15 秒是否有衝突
- 每段是否推進觀點
- 是否有消化段
- 是否有重複說理
- 結尾是否收束到主張

### Step 4：精剪
加入：
- 重點句放大
- 節奏變化
- B-roll
- 圖示
- 關鍵詞字幕
- 必要音效

### Step 5：字幕與文字層
字幕規則：
- 自動字幕保留完整口播
- 手動強調字幕只放 2-8 字
- 每次只強調一個概念
- 不遮擋臉和主要 B-roll

### Step 6：音頻和音樂
檢查：
- 人聲音量穩定
- 背景音樂不搶話
- 音效只用於段落轉折和重點提示
- 不用過多花哨音效

### Step 7：導出與 QA
必須檢查：
- 字幕是否錯字
- B-roll 是否擋臉/擋字
- 音量是否忽大忽小
- 開頭是否能留人
- 結尾是否乾淨
- 導出規格是否符合平台

## 質量檢查
- 是否先粗剪再精剪？
- 是否避免在粗剪階段堆效果？
- 是否把 B-roll 落到具體段落？
- 是否有字幕和音頻規則？
- 是否包含導出 QA？

## 與其他 Skill 協作
- **上游**: `long-video-storyboard`
- **上游**: `aroll-shooting-planner`
- **下游**: `packaging-optimizer`
- **下游**: `content-repurposer`

