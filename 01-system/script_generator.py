#!/usr/bin/env python3
"""
script-generator 工具脚本
用法：
    python tools/script_generator.py --hook <主题>
    python tools/script_generator.py --money <主题>
    python tools/script_generator.py --refine <脚本文本>
    python tools/script_generator.py --check <脚本文本>
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

WORKSPACE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))


def get_client() -> OpenAI:
    if OpenAI is None:
        raise RuntimeError("openai package not installed. Run: pip install openai")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


SYSTEM_PROMPT = """你是一个专业的视频脚本创作助手，遵循 MoneyXYZ 三角哲学：
1. 认知反差（Contrarian Truth）- 提出反直觉观点，打破观众认知
2. 理性证据（Rational Evidence）- 提供书籍、学术论文、权威数据支撑
3. 感性共鸣（Emotional Resonance）- 创造情绪波动和代入感
4. 现实锚点（Concrete Cases）- 用真实案例、生活场景或高代入感的典型情境承接观点，避免假大空

输出格式要求：
- 标题钩子：5个选项，爆款风格
- 完整脚本：包含 hook(15s)、evidence(30s)、core_argument(45s)、twist(15s)、cta(5s)
- 语言：中文为主，证据部分可引用英文权威来源"""


HOOK_PROMPT = """为以下主题生成 5 个爆款标题钩子和开场白：

主题：{topic}

要求：
- 每个钩子包含：标题 + 3秒开场白
- 风格：反直觉、数字锚点、情绪冲击
- 格式：简洁有力，适合短视频开头
- 目标：3秒内抓住注意力"""

MONEY_PROMPT = """为以下主题生成 MoneyXYZ 风格的完整视频脚本：

主题：{topic}

要求：
- 时长：约 90 秒短片
- 结构：Hook(15s) → Evidence(30s) → Core Argument(45s) → Twist(15s) → CTA(5s)
- 三角哲学：必须体现认知反差、理性证据、感性共鸣
- 现实锚点：至少加入 1 个具体案例、人物故事或生活场景
- 案例优先级：优先用用户提供的真实经历；如果没有，就用公开真实案例；再不行就用“典型情境”式的小故事，但不要伪装成可核查的事实
- 写作要求：每讲一个抽象观点，尽量立刻补一个人、一个场景或一个事件
- 引用：至少 1 个书籍/学术/权威数据来源
- 输出完整脚本，包含分镜建议"""

REFINE_PROMPT = """优化以下视频脚本，提升传播力：

脚本：
{script}

要求：
1. 降维类比：用普通人能理解的比喻替换复杂概念
2. 情感锚点：强化情绪共鸣点
3. 节奏优化：调整句子长度，提升节奏感
4. 案例注入：如果原文太空，补入具体案例、生活场景或典型情境
5. 保留核心观点和证据引用"""

CHECK_PROMPT = """自检以下视频脚本：

脚本：
{script}

检查维度：
1. 权威引用：是否有真实可信的来源（书籍/学术/数据）？
2. 说教感：是否过于爹味？降低说教感，增加共情
3. 逻辑闭环：开头承诺的价值是否在结尾兑现？
4. 行动号召：CTA 是否具体、可操作？
5. 案例密度：是否至少有 1-2 个具体案例/场景承接观点？
6. 假大空风险：是否连续多段只讲道理，没有人物、事件或生活细节？

输出：问题列表 + 改进建议"""


def call_llm(prompt: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        max_tokens=2000,
    )
    return response.choices[0].message.content


def cmd_hook(topic: str) -> int:
    print(f"[script-generator] 生成标题钩子: {topic}\n")
    prompt = HOOK_PROMPT.format(topic=topic)
    result = call_llm(prompt)
    print(result)
    return 0


def cmd_money(topic: str) -> int:
    print(f"[script-generator] 生成完整脚本: {topic}\n")
    prompt = MONEY_PROMPT.format(topic=topic)
    result = call_llm(prompt)
    print(result)
    return 0


def cmd_refine(script: str) -> int:
    print(f"[script-generator] 优化脚本...\n")
    prompt = REFINE_PROMPT.format(script=script)
    result = call_llm(prompt)
    print(result)
    return 0


def cmd_check(script: str) -> int:
    print(f"[script-generator] 自检脚本...\n")
    prompt = CHECK_PROMPT.format(script=script)
    result = call_llm(prompt)
    print(result)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Helius-002 script-generator 工具")
    parser.add_argument("--hook", metavar="TOPIC", help="生成标题钩子")
    parser.add_argument("--money", metavar="TOPIC", help="生成完整脚本")
    parser.add_argument("--refine", metavar="TEXT", help="优化脚本")
    parser.add_argument("--check", metavar="TEXT", help="自检脚本")

    args = parser.parse_args()

    if args.hook:
        return cmd_hook(args.hook)
    elif args.money:
        return cmd_money(args.money)
    elif args.refine:
        return cmd_refine(args.refine)
    elif args.check:
        return cmd_check(args.check)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
