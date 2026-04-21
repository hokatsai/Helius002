#!/usr/bin/env python3
"""
AI Runner - 通用 AI 执行层
自动选择 Codex 或 Gemini CLI 执行任务
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# API Keys
def get_openai_key():
    try:
        keys_file = Path.home() / "Desktop/Helius-001/01-system/configs/apis/API-Keys.md"
        if keys_file.exists():
            content = keys_file.read_text()
            for line in content.split('\n'):
                if 'OPENAI_API_KEY' in line:
                    return line.split('=')[1].strip()
    except:
        pass
    return os.getenv("OPENAI_API_KEY", "")

def get_gemini_key():
    try:
        keys_file = Path.home() / "Desktop/Helius-001/01-system/configs/apis/API-Keys.md"
        if keys_file.exists():
            content = keys_file.read_text()
            for line in content.split('\n'):
                if 'GEMINI_API_KEY' in line:
                    return line.split('=')[1].strip()
    except:
        pass
    return os.getenv("GEMINI_API_KEY", "")

# 执行 Codex
def run_codex(task, sandbox="workspace-write"):
    openai_key = get_openai_key()
    if not openai_key:
        return "❌ OPENAI_API_KEY 未配置"
    
    cmd = [
        "codex", "exec",
        "--sandbox", sandbox,
        "--skip-git-repo-check",
        f"--system-prompt", "You are a helpful AI assistant focused on content creation and productivity."
    ]
    
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = openai_key
    
    try:
        result = subprocess.run(
            cmd + [task],
            capture_output=True,
            text=True,
            timeout=120,
            env=env
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "❌ Codex 执行超时"
    except Exception as e:
        return f"❌ Codex 错误: {e}"

# 执行 Gemini CLI
def run_gemini(task, use_tavily=False):
    gemini_key = get_gemini_key()
    if not gemini_key:
        # 尝试用 Tavily 搜索
        if use_tavily:
            return run_tavily(task)
        return "❌ GEMINI_API_KEY 未配置"
    
    env = os.environ.copy()
    env["GEMINI_API_KEY"] = gemini_key
    
    cmd = ["gemini", "-p", task, "--approval-mode", "yolo"]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            env=env
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "❌ Gemini 执行超时"
    except Exception as e:
        return f"❌ Gemini 错误: {e}"

# 执行 Tavily 搜索
def run_tavily(query, max_results=5):
    try:
        tavily_key_file = Path.home() / ".openclaw/secrets/tavily_api_key"
        if tavily_key_file.exists():
            tavily_key = tavily_key_file.read_text().strip()
        else:
            return "❌ Tavily API Key 未配置"
        
        import urllib.request
        import json
        import ssl
        
        data = {
            "api_key": tavily_key,
            "query": query,
            "max_results": max_results,
            "include_answer": True
        }
        
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"}
        )
        
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            result = json.loads(resp.read())
            items = result.get("results", [])
            output = f"🔍 搜索结果: {query}\n\n"
            for i, item in enumerate(items, 1):
                output += f"{i}. {item.get('title', '')}\n"
                output += f"   {item.get('url', '')}\n"
                if item.get('content'):
                    output += f"   {item.get('content')[:100]}...\n"
            return output
    except Exception as e:
        return f"❌ Tavily 错误: {e}"

# 智能路由
def route_task(task):
    """根据任务类型自动选择模型"""
    task_lower = task.lower()
    
    # 代码相关 → Codex
    if any(k in task_lower for k in ["代码", "script", "python", "写代码", "调试", "修复"]):
        print("🎯 选择: Codex (代码能力强)")
        return run_codex(task)
    
    # 搜索研究 → Gemini + Tavily
    elif any(k in task_lower for k in ["搜索", "研究", "分析", "查找", "查询"]):
        print("🔍 选择: Gemini + Tavily (搜索能力强)")
        return run_gemini(task, use_tavily=True)
    
    # 内容创作 → Codex
    elif any(k in task_lower for k in ["创作", "生成", "写", "制作", "内容"]):
        print("✍️ 选择: Codex (内容生成)")
        return run_codex(task)
    
    # 默认 → Codex
    else:
        print("🤖 选择: Codex (默认)")
        return run_codex(task)

# 主函数
def main():
    parser = argparse.ArgumentParser(description="AI Runner - 通用 AI 执行层")
    parser.add_argument("--task", "-t", help="任务描述")
    parser.add_argument("--model", "-m", choices=["codex", "gemini", "tavily", "auto"], 
                       default="auto", help="指定模型")
    parser.add_argument("--search", "-s", help="快速搜索")
    parser.add_argument("--sandbox", default="workspace-write", 
                       choices=["read-only", "workspace-write", "danger-dangerously-bypass-approvals-and-sandbox"],
                       help="Codex 沙箱模式")
    args = parser.parse_args()
    
    if args.search:
        print(f"🔍 搜索: {args.search}")
        print(run_tavily(args.search))
        return
    
    if args.task:
        if args.model == "auto":
            print(route_task(args.task))
        elif args.model == "codex":
            print(run_codex(args.task, args.sandbox))
        elif args.model == "gemini":
            print(run_gemini(args.task))
        elif args.model == "tavily":
            print(run_tavily(args.task))
    else:
        print("AI Runner - 通用 AI 执行层")
        print("\n用法:")
        print("  --task/-t <任务>     执行 AI 任务（自动选择模型）")
        print("  --search/-s <查询>   快速搜索")
        print("  --model/-m <模型>   手动指定模型 (codex/gemini/tavily/auto)")
        print("  --sandbox <模式>    Codex 沙箱模式")
        print("\n示例:")
        print("  ai_runner.py -t '帮我写一个视频脚本'")
        print("  ai_runner.py -s '最新AI工具'")
        print("  ai_runner.py -t '分析这个代码' -m codex")

if __name__ == "__main__":
    main()
