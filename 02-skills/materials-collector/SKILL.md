---
name: materials-collector
description: 触发词：收集素材、自动收集、热点追踪、素材库更新。当你需要定期收集认知升级、AI运用、效率提升、自我提升相关的热点内容和素材时使用此技能。
---

# 素材自动收集系统

## 功能概述

自动收集以下领域的热点内容和素材：
- 认知升级（心理学、思维模型）
- AI运用（工具、prompt、趋势）
- 效率提升（方法论、生产力工具）
- 自我提升（个人成长、职业发展）

## 收集策略

### 触发条件
| 触发方式 | 说明 |
|---------|------|
| **每周定时** | 每周一自动执行 |
| **热点触发** | 检测到重大AI/认知类新闻时立即收集 |
| **手动触发** | 说「收集本周素材」|

### 收集来源
| 来源 | 内容类型 |
|------|---------|
| Tavily搜索 | 实时热点新闻 |
| YouTube Trending | 热门视频主题 |
| Twitter/X | 热门话题讨论 |
| Reddit | 讨论热度高的帖子 |
| 微信公众号 | 中文优质内容 |

## 素材格式

每个素材保存为JSON：
```json
{
  "id": "素材ID",
  "title": "标题",
  "summary": "100字摘要",
  "source": "来源",
  "url": "原文链接",
  "category": "认知升级/AI运用/效率提升/自我提升",
  "tags": ["标签1", "标签2"],
  "collected_at": "2026-04-02T18:37:00Z",
  "trend_score": 8.5,
  "why_important": "为什么值得收藏"
}
```

## 报告生成

每周生成一份 `week_report_YYYY-WXX.md`：
- 本周Top10素材
- 各分类数量统计
- 趋势分析
- 推荐关注点

## 使用方式

```bash
# 手动执行收集
python3 tools/materials_collector.py --collect

# 生成周报
python3 tools/materials_collector.py --report

# 查看素材库
python3 tools/materials_collector.py --list

# 搜索素材
python3 tools/materials_collector.py --search "AI写作"
```

## 依赖

- Tavily API Key（已有）
- Python 3.9+
- requests库
