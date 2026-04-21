# Helius-002 平台化 Demo 搭建提示詞

> 用途：直接給 Coding AI 讀取並開始搭建平台版 Demo
> 時間目標：4 月 11 日前可上台演示

---

## 一、任務目標

你現在不是在做一個「開發者工具集合」，而是在做一個 **面向創作者的 AI 內容工作流平台 Demo**。

一句話定位：

**Helius-002 是一個把「看內容」變成「做內容」的 AI 創作者工作流平台。**

目標不是做完整 SaaS，而是做一個：
- 有產品感
- 能上台展示
- 能跑通一條核心工作流
- UI 簡潔漂亮
- 背後可接 Helius-002 現有能力

---

## 二、核心原則

### 1. 不做大而全
不要做：
- 多賬號系統
- 發布排程
- 權限管理
- 複雜 BI 數據看板
- 一堆做不完的假功能

### 2. 只做一條核心工作流
主工作流必須是：

**輸入一個 YouTube 視頻連結 / 一段文本素材**  
→ 提取內容  
→ 分析核心觀點  
→ 爆款結構拆解  
→ 生成符合創作者風格的新腳本  
→ 輸出可用內容資產

### 3. UI 必須像產品
觀眾要覺得這是：
- 一個創作者平台
- 一個內容工作台
- 一個產品

而不是：
- 工具殼子
- 技術後台
- CLI 面板

---

## 三、這次只做 4 個模塊

### 1. Dashboard
首頁，負責展示平台定位與入口。

內容：
- 產品標題：Helius-002
- 副標：把「看內容」變成「做內容」的 AI 創作者工作流平台
- 主 CTA：開始一次內容拆解
- 三張價值卡片：
  - 導入素材
  - AI 分析爆款結構
  - 生成腳本與內容資產

### 2. Import
素材導入頁。

功能：
- 粘貼 YouTube / B站連結
- 粘貼文本內容
- 預留 PDF 上傳入口（可先做 placeholder）
- 開始分析按鈕

要求：
- 有 loading 狀態
- 點了有反應
- 能把任務送進下一步

### 3. Analysis
內容分析頁。

展示：
- 摘要
- 3~5 條核心觀點
- 爆款結構分析
- 為什麼值得研究

要求：
- 用卡片 / 區塊展示
- 不要直接輸出原始 JSON
- 看起來像分析工作台

### 4. Script
腳本生成頁。

展示：
- 3 個標題備選
- 完整腳本
- 結構標記：
  - Hook
  - Evidence
  - Core Argument
  - Twist
  - CTA

要求：
- 有「複製腳本」按鈕
- 有「保存到素材庫」按鈕

### 5. Library
素材庫 / 任務沉澱頁。

展示：
- 本次任務名稱
- 輸入來源
- 摘要
- 核心觀點
- 腳本
- 建立時間

用途：
- 讓觀眾感受到這個平台可以沉澱內容資產

---

## 四、整體頁面結構

左側導航只保留：
- Dashboard
- Import
- Analysis
- Script
- Library

不要再加其他頁。

---

## 五、Demo 必須跑通的流程

### Demo Flow
1. 打開 Dashboard
2. 進入 Import
3. 輸入一個 YouTube 連結或粘貼一段文本
4. 點「開始分析」
5. 跳到 Analysis 頁面
6. 顯示摘要 / 核心觀點 / 爆款拆解
7. 點「生成腳本」
8. 跳到 Script 頁面
9. 顯示標題 + 腳本
10. 點「保存到素材庫」
11. 在 Library 裡看到本次產出

這條流程必須閉環。

---

## 六、技術要求

### 前端
可用：
- Next.js / React
- Tailwind CSS

### UI 風格
要求：
- 白色 / 淺灰基調
- 極簡、有產品感
- 參考：Notion / Linear / Arc / 現代 SaaS 平台
- 卡片式布局
- 乾淨留白
- 有 hover 狀態

禁止：
- 深色黑客風
- 開發者後台感太重
- 頁面擁擠
- 原始 JSON 裸奔

### 後端 / 數據策略
優先保證 Demo 跑通。

允許：
- mock data
- fallback data
- 單一成功案例預置

不要求：
- 這一版完全接通所有真實 API
- 完整商業級後端能力

但是：
- 畫面要像真的產品
- 任務狀態要完整
- 不要讓觀眾看出是假的

---

## 七、每次任務至少輸出這些內容

### Analysis Output
- summary
- 3~5 key insights
- viral structure analysis
- why this content works

### Script Output
- 3 title ideas
- full script
- section labels:
  - hook
  - evidence
  - core argument
  - emotional twist
  - CTA

### Library Output
- task name
- source input
- created time
- analysis snapshot
- script snapshot

---

## 八、產品感細節（必須有）

一定要有：
- loading spinner / skeleton
- 任務狀態（processing / done）
- 清楚的區塊標題
- 按鈕 hover
- 複製按鈕
- 保存成功提示
- 頁面之間有明確操作路徑

不能有：
- 點了沒反應
- 一堆 TODO
- 頁面空白
- 流程斷頭
- 工程名詞直接暴露給用戶

---

## 九、優先級

### P0（必做）
- 平台外殼完成
- 4 個模塊頁面完成
- 1 條核心工作流跑通
- Analysis → Script → Library 閉環
- UI 有產品感

### P1（有時間再做）
- PDF 入口做成可用
- 增加頻道分析入口
- 任務歷史列表
- 更多腳本風格選擇

### P2（這次先別做）
- 多賬號
- 團隊協作
- 數據中台
- 發布排程
- 權限管理

---

## 十、成功標準

做完後，觀眾應該能在 30 秒內理解：

**「這是一個把內容拆解、分析、重組、生成腳本的 AI 創作者工作台。」**

而不是：

**「這人做了一堆 AI 工具，但不知道哪個最重要。」**

---

## 十一、交付要求

請先交付：
1. 可演示的 Dashboard
2. Import / Analysis / Script / Library 四頁
3. 一條可跑通的 demo flow
4. 一版漂亮的白色簡潔 UI

完成後，交給 QA（Helius）測試驗收。
