#!/usr/bin/env python3
"""
認知便利店M 风格视频创作助手

用法:
    python generate_video.py --topic "你的话题"
    python generate_video.py --topic "降维打击" --format json
"""

import argparse
import json
import sys
from pathlib import Path

# 标题模板
TITLE_TEMPLATES = [
    "「你以为{common}，其实{counterintuitive}」",
    "「为什么有钱人Y，而不是你X」",
    "「90%的人不知道的{topic}」",
    "「{topic}背后的{principle}」",
]

# Hook模板
HOOK_TEMPLATES = [
    "你是不是也这样——{problem}",
    "为什么有人能{success}，而你却{struggle}？",
    "今天告诉你一个关于{topic}的真相...",
]

# 反直觉开场
COUNTERINTUITIVE_TEMPLATES = [
    "但真正的答案是：{answer}",
    "其实，这背后是一个{principle}",
    "这就是为什么：{insight}",
]

def generate_script(topic: str, style: str = "便利店") -> dict:
    """生成视频脚本"""
    
    script = {
        "topic": topic,
        "title": f"「你以为{topic}很简单，其实高手都懂这个原理」",
        "hook": f"你是不是也这样——每次看到{topic}都觉得头大？",
        "counterintuitive": f"但真正的答案是：高手从来不从{topic}入手",
        "main_content": f"""第一段 (痛点):
- {topic} 是很多人都会遇到的困惑
- 常见的误区是...

第二段 (反直觉):
- {topic} 背后其实是一个经典的心理原理
- 宜家的1元冰淇淋就是这个原理的最佳案例

第三段 (行动):
- 所以下次遇到{topic}，试试这个方法...
- 金句结尾：{topic}不是目的，而是手段
""",
        "duration": "90-120秒",
        "ai_prompts": {
            "visual_1": "手绘白板风，一个人物剪影在思考，背景简洁",
            "visual_2": "关键词「{topic}」放大，周围有思维导图",
            "visual_3": "一个生活中常见的场景，解释{topic}原理"
        },
        "tts_params": {
            "voice": "onyx",
            "speed": 0.9,
            "style": "克制、内敛、有深度"
        }
    }
    
    return script

def main():
    parser = argparse.ArgumentParser(description="認知便利店M 风格视频创作助手")
    parser.add_argument("--topic", required=True, help="视频主题")
    parser.add_argument("--format", default="text", choices=["text", "json"], help="输出格式")
    args = parser.parse_args()
    
    script = generate_script(args.topic)
    
    if args.format == "json":
        print(json.dumps(script, ensure_ascii=False, indent=2))
    else:
        print(f"📺 主题: {script['topic']}")
        print(f"\n🎯 标题:")
        print(f"   {script['title']}")
        print(f"\n🪝 Hook:")
        print(f"   {script['hook']}")
        print(f"\n🔄 反直觉开场:")
        print(f"   {script['counterintuitive']}")
        print(f"\n📝 正文内容:")
        print(script['main_content'])
        print(f"\n⏱️ 时长: {script['duration']}")
        print(f"\n🎨 AI画面提示词:")
        for k, v in script['ai_prompts'].items():
            print(f"   [{k}]: {v}")

if __name__ == "__main__":
    main()
