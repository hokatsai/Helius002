# Helius-002 MiniMax 2.7 接入提示词（先跑通版）

> 用途：给 Coding AI 直接读取，优先把真实 AI 主链路跑通  
> 目标：先让平台用 MiniMax 2.7 正常完成 `文本输入 → Analysis → Script`，不要先做复杂多模型系统

---

## 一、任务目标

当前情况：
- 平台前端已经完成
- `/api/analyze` 和 `/api/script` 已经开始接真实 AI
- 但当前写法依赖 `OPENAI_API_KEY`
- 用户没有 OpenAI API key，只有 MiniMax 2.7 的 key

### 本轮目标
不要做完整多模型中台，
先做一个**能跑起来的 MiniMax 版本**：

## 让以下流程可用
**文本输入 → Analysis → Script**

并保证：
- 前端结构不改
- demo flow 不改
- 失败时仍可 fallback 到 mock

---

## 二、这轮不要做什么

### 不要做
- 不要做完整 provider 抽象系统
- 不要同时接 OpenAI / Gemini / MiniMax 三套
- 不要改大前端结构
- 不要扩展到视频下载 / 频道分析
- 不要重写平台逻辑

### 这轮只做
- 把现有依赖 `OPENAI_API_KEY` 的文本 AI 流程
- 改成先支持 `MINIMAX_API_KEY` 或兼容 MiniMax 的调用方式
- 跑通 `/api/analyze` 和 `/api/script`

---

## 三、当前核心问题

当前后端报错是：
```json
{"error":"analyze_failed","detail":"missing OPENAI_API_KEY"}
```

这说明：
- API 路由已经存在
- 但后端把模型调用写死在 OpenAI 上了
- 现在不是前端问题，而是后端模型接入层问题

---

## 四、实现目标

## 1. 新环境变量
请支持读取：

```env
MINIMAX_API_KEY=
```

如果项目里已有 `.env.example`，请补上：

```env
MINIMAX_API_KEY=your_minimax_key_here
```

同时保留未来可扩展空间，但当前优先 MiniMax。

---

## 2. `/api/analyze` 改成使用 MiniMax

### 输入
```json
{
  "text": "用户输入的一段文本"
}
```

### 输出目标
```json
{
  "summary": "...",
  "keyInsights": ["...", "...", "..."],
  "viralStructure": [
    { "title": "Hook", "detail": "..." },
    { "title": "Evidence", "detail": "..." },
    { "title": "Argument", "detail": "..." },
    { "title": "Twist + CTA", "detail": "..." }
  ],
  "whyItWorks": "..."
}
```

### 要求
- 调用 MiniMax 2.7 或你当前最接近的 MiniMax 文本模型
- 输出必须是结构化 JSON
- 如果模型返回内容不可解析，做一次修正或 fallback

---

## 3. `/api/script` 改成使用 MiniMax

### 输入
```json
{
  "analysis": { ... },
  "styleKey": "rational"
}
```

### 输出目标
```json
{
  "titles": ["...", "...", "..."],
  "styleKey": "rational",
  "styleLabel": "理性拆解风",
  "sections": {
    "hook": "...",
    "evidence": "...",
    "coreArgument": "...",
    "emotionalTwist": "...",
    "cta": "..."
  }
}
```

### 要求
- 将当前风格选择真正传进 prompt
- 不同 styleKey 至少体现在：
  - 标题语气
  - Hook 语气
  - CTA 语气
  - 整体表达气质

---

## 五、推荐实现策略

## 策略：不要全局大改，先做最小替换

### 做法
在现有 `/api/analyze` 和 `/api/script` 里：
- 把 OpenAI 写死逻辑替换为 MiniMax 调用
- 或新建一个很轻的 `llmClient` 文件，先只支持 minimax

例如：
```js
const provider = 'minimax';
const apiKey = process.env.MINIMAX_API_KEY;
```

### 重点
不是现在把系统设计到很完美，
而是：

**先把一条真实 AI 主链路跑通。**

---

## 六、错误处理必须保留

这一轮最重要的一点：

## 即使 MiniMax 调用失败，也不能让 Demo 死

### 必须保留 fallback
如果：
- key 缺失
- 请求超时
- 返回 JSON 解析失败
- 模型报错

则：
- 返回错误提示
- 或自动 fallback 到 mock analysis/script
- 前端流程仍然可继续

### 目标体验
最好：真实 AI 跑通  
最差：仍然能走完整 demo flow

---

## 七、前端改动限制

### Import
- 文本输入优先走真实 AI
- 链接输入继续保留 demo/mock 逻辑

### Analysis
- 不改结构
- 只让它接真实返回

### Script
- 不改结构
- 风格切换继续保留，并真正作用于脚本生成

### Library
- 保存逻辑不改
- 能保存真实 AI 结果即可

---

## 八、MiniMax 接入完成后的成功标准

完成后，平台应该满足：

### 文本测试流程
1. 用户粘贴一段中文文本
2. 点击“开始分析”
3. `/api/analyze` 返回真实分析结果
4. Analysis 页面展示真实 summary / keyInsights / structure / whyItWorks
5. 点击“生成脚本”
6. `/api/script` 返回真实脚本结果
7. Script 页面展示真实 titles / sections
8. 可保存到 Library

### 异常情况
如果 MiniMax 调用失败：
- 有错误提示
- 或 fallback 到 mock
- 不让平台断掉

---

## 九、这一轮的最终目的

不是做一个“完美的多模型架构”，
而是：

## 先让 Helius-002 真的拥有第一条可用的 AI 能力

也就是：

**文本输入 → 真 Analysis → 真 Script**

只要这条跑通，11 号的 demo 质量就会上一个台阶。

---

## 十、交付要求

请完成：
1. 支持 `MINIMAX_API_KEY`
2. `/api/analyze` 改为可用的 MiniMax 调用
3. `/api/script` 改为可用的 MiniMax 调用
4. 保留 fallback 到 mock
5. 前端主流程不变
6. 完成后交给 QA（Helius）继续测试

---

## 十一、一句话提醒

这一轮不要想太多，
先做一件最重要的事：

**让 MiniMax 2.7 真正把文本变成分析和脚本。**
