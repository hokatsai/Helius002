---
name: skill-name
description: 触发词（触发这个skill的关键词/短语）
---

# Skill 名称

## 功能说明
简明扼要地描述这个skill做什么

## 核心能力
- 能力1
- 能力2

## 输入/输出规范
### 输入
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| param1 | string | 是 | 参数说明 |

### 输出
| 参数 | 类型 | 说明 |
|------|------|------|
| result | string | 返回值说明 |

## 执行流程
1. 步骤1
2. 步骤2

## 错误处理
### 错误类型与降级方案
| 错误类型 | 降级方案 | 重试机制 |
|----------|----------|----------|
| 网络超时 | 使用缓存或返回友好错误 | 重试3次，间隔2s |
| API 失败 | 回退到备用 API 或本地处理 | 重试3次 |

### 错误日志
所有错误自动记录到 `workspace/logs/{skill-name}/YYYY-MM-DD.log`

## 与其他 Skill 协作
- **依赖**: skill-name-1（用于xxx）
- **被依赖**: skill-name-2（为其提供xxx）

## 使用示例
### 示例1
```bash
helius.py skill-name --arg1 value1
```

### 示例2
> 触发词：xxx
> 执行结果：xxx

## 依赖
- **API Keys**: `OPENAI_API_KEY`
- **其他Skill**: skill-name-1
- **环境**: Python 3.8+, yt-dlp
