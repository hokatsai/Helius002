# Helius-002 第一条真实 AI 接入提示词

> 用途：给 Coding AI 直接读取，开始接入第一条真实 AI 主链路  
> 目标：在不破坏现有 demo flow 的前提下，把“文本输入 → Analysis → Script”从 mock 升级为真实 AI 结果

---

## 一、任务目标

当前平台已经具备：
- 平台外壳
- Dashboard / Import / Analysis / Script / Library
- 可运行 demo flow
- Analysis 保存能力
- Script 风格选择能力
- 基本资产沉淀逻辑

现在要做的不是全量后端接入，
而是：

## 只接一条最关键、最稳、最适合演示的真实 AI 链路

### 第一条真实链路
**文本输入 → Analysis → Script**

也就是说：
- 用户在 Import 页粘贴文本
- 点击开始分析
- Analysis 页展示真实 AI 生成的摘要 / 核心观点 / 结构分析
- Script 页展示真实 AI 生成的标题与脚本
- 最后可保存到 Library

---

## 二、为什么先接这条

原因：
- 最稳
- 最适合演示
- 不依赖视频下载 / 字幕提取 / 外部复杂链路
- 最能体现 Helius-002 的核心价值
- 最容易在 11 号前做出稳定版本

### 现在不要优先接
- 视频下载全流程
- 自动转录
- 频道分析完整能力
- 复杂搜索 / 爬取 / 数据平台

这些都容易拖慢进度。

---

## 三、实现策略

### 原则
不要一上来推翻现有前端结构。  
在现有 demo flow 基础上，把 mock 生成替换为真实 AI 调用。

### 目标模式
当前：
- `buildMockAnalysis()`
- `buildMockScript()`

目标：
- 当用户输入文本时，调用真实 AI API
- 返回真实 analysis 数据结构
- 再调用真实 AI API 生成 script
- 如果失败，再 fallback 到 mock 数据

也就是：

**真实 AI 优先，mock 作为降级兜底。**

---

## 四、推荐实现方式

## 方案：先做一个最小后端 API

建议增加 2 个 API：

### 1. `/api/analyze`
输入：
```json
{
  "text": "用户输入的文本内容"
}
```

输出格式：
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

### 2. `/api/script`
输入：
```json
{
  "analysis": { ... },
  "styleKey": "rational"
}
```

输出格式：
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

---

## 五、模型与调用建议

### 优先要求
- 能稳定返回结构化结果
- 响应速度不要太慢
- 失败时可回退 mock

### 可以接受的方式
- 调用 OpenAI / MiniMax / Gemini 任一你当前最稳定的模型
- 只要能稳定输出 JSON 即可

### 最重要的不是模型多高级
而是：

**上台演示时，它能稳定出结果。**

---

## 六、风格选择的接入方式

当前 Script 已经有 style selector，
这一轮不要重做 UI，只要把 styleKey 真正接进 prompt。

例如：
- rational → 更理性、结构清晰
- friendly → 更像朋友聊天
- professional → 更冷静专业
- high-energy → 更强节奏感
- moneyxyz → 更强调认知反差 + 证据 + 情绪反转

### 要求
不同风格至少体现为：
- 标题语气不同
- Hook 不同
- CTA 不同
- 语言气质不同

---

## 七、降级策略（必须有）

这点非常重要。

### 如果真实 AI 失败
不要让平台报错崩掉。

必须做：
- try/catch
- loading 状态
- 错误提示
- 自动 fallback 到 mock 数据

### 正确体验
- 最佳情况：返回真实 AI 结果
- 最坏情况：仍然能走完整 demo flow（用 mock）

也就是说：

**即使后端失败，演示也不能死。**

---

## 八、前端改动要求

### Import 页
- 若输入的是文本，优先走真实 AI 链路
- 若输入的是 URL，可以暂时继续走 mock / 占位逻辑

### Analysis 页
- 优先展示真实分析结果
- 保存逻辑不变

### Script 页
- 优先展示真实脚本结果
- 风格切换可触发重新生成脚本
- 若真实调用失败，回退 mock script

### Library 页
- 结构不改
- 只需要能保存真实 analysis/script 结果

---

## 九、这轮不要做的事

### 不要扩展到这些内容
- 不要接视频下载全链路
- 不要接自动字幕/转录
- 不要接频道分析
- 不要接复杂外部搜索
- 不要做风格反推生成 skill
- 不要做视频分镜脚本

这一轮只做：

## 文本输入 → 真实 Analysis → 真实 Script

---

## 十、成功标准

完成后，这个平台应该达到：

### 演示场景下
1. 用户粘贴一段文本
2. 点击开始分析
3. Analysis 页显示真实 AI 结果
4. 点击生成脚本
5. Script 页显示真实 AI 结果
6. 可以保存到 Library
7. 若失败，仍可 fallback 跑通流程

### 观众感知
观众会感觉：

**这个平台不只是界面像产品，背后也真的开始有 AI 能力在工作。**

---

## 十一、交付要求

请交付：
1. 最小可用的 `/api/analyze`
2. 最小可用的 `/api/script`
3. 文本输入走真实 AI 链路
4. 风格选择接入 prompt
5. fallback 到 mock 的容错逻辑
6. 完成后交给 QA（Helius）测试

---

## 十二、一句话提醒

这一轮不是做“全平台后端”，
而是先把最关键的一条线做真：

**让文本输入真的能变成分析和脚本。**
