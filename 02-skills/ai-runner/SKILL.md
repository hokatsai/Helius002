---
name: ai-runner
description: 触发词：AI执行、AI任务、自动选择模型、AI工作流。当你需要执行AI任务、生成内容、分析数据时使用此技能，它会自动选择最适合的模型。
---

# AI Runner - 通用 AI 执行层

## 核心概念

不绑定具体模型，自动选择最合适的执行方式：
- **Codex** → 代码生成、文件修改、调试
- **Gemini CLI** → 搜索研究、长文本分析、知识整理
- **Tavily** → 实时网络搜索
- **Helius-002 Skills** → 特定领域的结构化任务

## 模型选择策略

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 代码生成/修改 | Codex | 原生代码能力最强 |
| 内容创作/脚本 | Codex 或 Gemini | 两者皆可 |
| 网络搜索/研究 | Gemini + Tavily | 实时信息 |
| 长文档分析 | Gemini | 超长上下文 |
| 结构化任务 | Codex | 工具调用强 |
| 快速问答 | Gemini | 响应快 |

## 自动选择规则

```
if "代码" in task or "script" in task or "生成" in task:
    → Codex
elif "搜索" in task or "研究" in task or "分析" in task:
    → Gemini CLI + Tavily
elif "脚本" in task or "文案" in task or "内容" in task:
    → Codex (生成) + Gemini (优化)
else:
    → Codex (默认)
```

## 使用方式

### 方式一：自动选择（推荐）
```
把任务描述发给我，我自动选择最合适的模型执行
```

### 方式二：手动指定
```
@Codex: 生成一个视频标题
@Gemini: 搜索最新的AI工具
```

### 方式三：直接调用 Skill
```
helius.py skill video-download --url "xxx"
helius.py skill script-generator --topic "降维打击"
```

## 执行示例

### 示例 1：内容创作
```
用户: 帮我写一个关于"降维打击"的视频脚本
Runner: 
  1. 选择 Codex 生成脚本
  2. 用 Gemini 优化结构
  3. 输出完整脚本
```

### 示例 2：竞品分析
```
用户: 分析 MoneyXYZ 频道
Runner:
  1. Tavily 搜索最新信息
  2. Gemini 分析内容策略
  3. Codex 生成报告
```

### 示例 3：自动化工作流
```
用户: 收集本周热点素材
Runner:
  1. Tavily 搜索多个主题
  2. Gemini 整理分类
  3. Codex 生成周报
  4. materials-collector 保存
```

## API Key 配置

自动读取已有 Key：
- Codex: `OPENAI_API_KEY`
- Gemini CLI: `GEMINI_API_KEY`
- Tavily: `~/.openclaw/secrets/tavily_api_key`

## 依赖

| 工具 | 状态 | 用途 |
|------|------|------|
| Codex | ✅ 已安装 | 代码/脚本生成 |
| Gemini CLI | ✅ 已安装 | 搜索/分析 |
| Tavily | ✅ 已配置 | 实时搜索 |
| Helius Skills | ✅ 已安装 | 结构化任务 |

## 与 Helius-002 的关系

AI Runner 是 Helius-002 的「执行引擎」：

```
用户请求 → AI Runner 分析 → 选择模型 → 执行 Skill → 返回结果
```

所有 Helius-002 Skills 都通过 AI Runner 统一调度。
