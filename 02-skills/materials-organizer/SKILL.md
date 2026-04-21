---
name: materials-organizer
description: 触发词：整理素材、整理下载、素材索引、去重。当你需要整理下载的视频素材、生成索引或去重时使用。
---

# Materials Organizer Skill

## 功能说明
Materials Organizer 是 Helius-002 系统的核心素材管理组件，承接自 v1 `downloads_organizer.py`。它负责将原始下载目录中的杂乱文件转化为结构化的、可供后续剪辑和分发的素材库。

## 核心能力
- 自动化扫描（.mp4/.mkv/.json/.vtt）
- 元数据解析（video_id 正则提取）
- SHA256 智能去重
- 多语言字幕检测（zh-Hant/en）
- 结构化库构建（intermediate + final 阶段）
- 导航生成（index.md）

## 输入/输出规范
### 输入
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source_dir | string | 否 | 下载目录，默认 workspace/inputs/ |
| run_id | string | 否 | 运行 ID，默认自动生成 |

### 输出
| 参数 | 类型 | 说明 |
|------|------|------|
| asset_index | string | youtube_assets.tsv 路径 |
| dedup_report | object | 去重报告 |
| library_structure | dict | final/library/ 组织结构 |

## 执行流程
1. 扫描下载目录，识别所有媒体文件
2. 提取 video_id，构建 RunAsset 数据
3. 读取 JSON 元数据（标题/上传者/日期）
4. SHA256 校验去重
5. 生成 intermediate/youtube_assets.tsv
6. 按 video_id 重组到 final/library/by_video_id/
7. 生成 index.md 导航文件

## 错误处理
### 错误类型与降级方案
| 错误类型 | 降级方案 | 重试机制 |
|----------|----------|----------|
| 目录为空/不存在 | 返回友好提示，不报错 | 不重试 |
| JSON 元数据解析失败 | 跳过该字段，继续处理其他文件 | 不重试 |
| 磁盘空间不足 | 停止并返回明确错误 | 不重试 |
| 文件权限问题 | 返回错误，提示检查权限 | 不重试 |

### 错误日志
所有错误自动记录到 `workspace/logs/materials-organizer/YYYY-MM-DD.log`

## 与其他 Skill 协作
- **依赖**: video-download（整理下载的视频）
- **被依赖**: video-analysis（使用整理后的素材）
- **依赖**: transcription（处理字幕文件）

## 使用示例
### 示例1：整理新下载的视频
```bash
helius.py organize
```

### 示例2：指定目录整理
```bash
python tools/organize.py --source workspace/inputs/my_videos --run_id "20260402_run1"
```

## 依赖
- **Python**: 3.8+
- **核心库**: hashlib, pathlib, re, json
- **数据结构**: RunAsset dataclass
