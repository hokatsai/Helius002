#!/usr/bin/env python3
"""
素材自动收集系统
自动收集认知升级、AI运用、效率提升、自我提升相关素材
"""

import json
import os
import sys
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# 添加 Helius-002 到路径
BASE_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

# API Key
TAVILY_API_KEY = Path.home() / ".openclaw/secrets/tavily_api_key"
if TAVILY_API_KEY.exists():
    TAVILY_API_KEY = TAVILY_API_KEY.read_text().strip()
else:
    TAVILY_KEY = os.getenv("TAVILY_API_KEY", "")

# 素材保存路径
MATERIALS_DIR = Path.home() / "Desktop/Helius-002/workspace/materials"
TRENDING_DIR = MATERIALS_DIR / "trending"
SNAPSHOTS_DIR = MATERIALS_DIR / "snapshots"
REPORTS_DIR = MATERIALS_DIR / "reports"
STATE_FILE = MATERIALS_DIR / "state.json"

# 收集主题
TOPICS = [
    "认知升级 心理学 思维模型 2026",
    "AI工具 ChatGPT Claude 使用技巧 2026",
    "效率提升 生产方法论 深度工作 2026",
    "个人成长 自我提升 副业 2026",
    "注意力经济 专注力 习惯养成 2026",
]

def load_state():
    """加载状态"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_collect": None, "items": []}

def save_state(state):
    """保存状态"""
    MATERIALS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

def search_tavily(query, max_results=5):
    """搜索 Tavily"""
    import urllib.request
    import ssl
    
    if not TAVILY_API_KEY:
        print("⚠️  Tavily API Key 未配置")
        return []
    
    ssl_context = ssl._create_unverified_context()
    
    data = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "include_answer": True,
        "include_raw_content": False
    }
    
    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
            result = json.loads(response.read())
            return result.get("results", [])
    except Exception as e:
        print(f"搜索错误: {e}")
        return []

def categorize(query):
    """分类素材"""
    query_lower = query.lower()
    if any(k in query_lower for k in ["ai", "gpt", "claude", "工具", "prompt", "chatgpt"]):
        return "AI运用"
    elif any(k in query_lower for k in ["效率", "生产力", "工作", "专注", "深度工作"]):
        return "效率提升"
    elif any(k in query_lower for k in ["成长", "个人", "职业", "副业", "自我"]):
        return "自我提升"
    else:
        return "认知升级"

def collect_topic(topic):
    """收集单个主题"""
    print(f"📡 搜索: {topic}")
    results = search_tavily(topic, max_results=5)
    
    items = []
    for r in results:
        item = {
            "id": f"{int(time.time())}_{len(items)}",
            "title": r.get("title", ""),
            "summary": r.get("content", "")[:200],
            "source": r.get("url", "").split("/")[2] if r.get("url") else "unknown",
            "url": r.get("url", ""),
            "category": categorize(topic),
            "tags": topic.split()[:3],
            "collected_at": datetime.now().isoformat(),
            "trend_score": r.get("score", 0),
            "why_important": r.get("answer", "")[:100] if r.get("answer") else ""
        }
        items.append(item)
    
    time.sleep(1)  # 避免API限流
    return items

def collect_all():
    """收集所有主题"""
    print("🚀 开始素材收集...")
    all_items = []
    
    for topic in TOPICS:
        items = collect_topic(topic)
        all_items.extend(items)
        print(f"   ✓ {topic}: {len(items)} 条")
    
    # 保存原始素材
    TRENDING_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    snapshot_file = SNAPSHOTS_DIR / f"snapshot_{today}.json"
    snapshot_file.write_text(json.dumps(all_items, ensure_ascii=False, indent=2))
    
    # 更新状态
    state = load_state()
    state["last_collect"] = datetime.now().isoformat()
    state["items"] = all_items
    save_state(state)
    
    print(f"\n✅ 收集完成! 共 {len(all_items)} 条素材")
    print(f"📁 保存至: {snapshot_file}")
    
    return all_items

def generate_report():
    """生成周报"""
    state = load_state()
    items = state.get("items", [])
    
    if not items:
        print("⚠️ 没有素材，请先运行收集")
        return
    
    # 按分类统计
    categories = {}
    for item in items:
        cat = item.get("category", "其他")
        categories[cat] = categories.get(cat, 0) + 1
    
    # 生成报告
    week_num = datetime.now().isocalendar()[1]
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# 📰 素材周报 {today}

> 自动收集 | 共 {len(items)} 条素材

## 📊 分类统计

| 分类 | 数量 |
|------|------|
"""
    
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        report += f"| {cat} | {count} |\n"
    
    report += f"""
## 🔥 Top 10 素材

"""
    
    # 按热度排序
    sorted_items = sorted(items, key=lambda x: x.get("trend_score", 0), reverse=True)
    
    for i, item in enumerate(sorted_items[:10], 1):
        report += f"""### {i}. {item['title']}
- 📂 分类: {item['category']}
- 🏷️ 来源: {item['source']}
- 📝 摘要: {item['summary'][:100]}...
- 🔗 [查看原文]({item['url']})
- 💡 重要性: {item.get('why_important', 'N/A')[:80]}

---
"""
    
    report += f"""
## 💡 本周趋势洞察

基于本周收集的素材，以下主题值得关注：

"""
    
    # 生成洞察
    top_cats = sorted(categories.items(), key=lambda x: -x[1])[:3]
    for cat, _ in top_cats:
        report += f"- **{cat}**: 本周最热，共 {categories[cat]} 条相关素材\n"
    
    report += f"""
---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
*数据来源: Tavily 实时搜索*
"""
    
    # 保存报告
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / f"week_report_{today}.md"
    report_file.write_text(report)
    
    print(f"📄 报告已生成: {report_file}")
    return report_file

def list_materials(category=None):
    """列出素材"""
    state = load_state()
    items = state.get("items", [])
    
    if category:
        items = [i for i in items if i.get("category") == category]
    
    print(f"\n📚 素材库 (共 {len(items)} 条)"
    if category:
        print(f"   分类: {category}")
    print()
    
    for i, item in enumerate(items, 1):
        print(f"{i}. 【{item['category']}】{item['title']}")
        print(f"   来源: {item['source']} | 热度: {item.get('trend_score', 0):.2f}")
        print(f"   链接: {item['url']}")
        print()

def search_materials(keyword):
    """搜索素材"""
    state = load_state()
    items = state.get("items", [])
    
    results = [i for i in items if keyword.lower() in i.get("title", "").lower() or keyword.lower() in i.get("summary", "").lower()]
    
    print(f"\n🔍 搜索结果: '{keyword}' ({len(results)} 条)")
    for i, item in enumerate(results, 1):
        print(f"{i}. 【{item['category']}】{item['title']}")
        print(f"   {item['summary'][:80]}...")

def main():
    parser = argparse.ArgumentParser(description="素材自动收集系统")
    parser.add_argument("--collect", action="store_true", help="执行素材收集")
    parser.add_argument("--report", action="store_true", help="生成周报")
    parser.add_argument("--list", action="store_true", help="列出所有素材")
    parser.add_argument("--search", type=str, help="搜索素材")
    parser.add_argument("--category", type=str, help="按分类筛选")
    parser.add_argument("--weekly", action="store_true", help="执行每周收集+报告")
    args = parser.parse_args()
    
    if args.collect or args.weekly:
        collect_all()
    
    if args.report or args.weekly:
        generate_report()
    
    if args.list:
        list_materials(args.category)
    
    if args.search:
        search_materials(args.search)
    
    if not any([args.collect, args.report, args.list, args.search, args.weekly]):
        parser.print_help()

if __name__ == "__main__":
    main()
