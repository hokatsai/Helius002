---
name: video-download
description: 触发词：下载视频、下载YouTube、获取视频素材。当你需要从YouTube或其他平台下载视频作为素材时使用。
---

# Video Download Skill

## 功能说明
此 Skill 旨在为 Helius-002 系统提供稳定、高质量的视频素材下载能力。它基于 `yt-dlp` 的 Python 实现，继承并增强了 v1 版本 PowerShell 脚本的核心逻辑。

### 核心特性
- **多平台支持**：支持 YouTube 及数百个主流视频平台的视频下载。
- **编码优先逻辑**：强制优先选择 **AVC (H.264)** 视频编码和 **M4A** 音频编码。这种组合提供了最佳的剪辑软件兼容性（如 Premiere Pro, CapCut），避免转码开销。
- **质量控制**：最高支持 **1080p 60fps**，在保证清晰度的同时优化存储与处理速度。
- **身份验证**：自动从 **Chrome 浏览器** 读取 Cookie 以处理会员内容或年龄限制视频；若浏览器提取失败，支持回退至指定的 `cookies.txt` 文件。
- **极致稳定性**：启用 8 线程并发下载（`concurrent-fragments`），并配置无限重试机制以应对不稳定网络。
- **自动化输出**：所有素材统一存放至 `workspace/inputs/` 目录。

## 核心能力
- 多平台视频下载（YouTube, Bilibili 等）
- AVC/H.264 编码优先 + M4A 音频
- 1080p60fps 最高质量
- Cookie/浏览器认证
- 8 线程并发 + 无限重试

## 输入/输出规范
### 输入
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | 视频的完整 URL |
| cookie_path | string | 否 | 备用 cookies.txt 路径 |
| output_name | string | 否 | 自定义文件名，默认为视频标题 |

### 输出
| 参数 | 类型 | 说明 |
|------|------|------|
| file_path | string | 下载完成后的本地绝对路径 |
| metadata | object | 包含标题、时长、分辨率等元数据 |

## 执行流程
1. 解析 URL，识别平台
2. 构建 yt-dlp 下载命令（AVC 编码优先）
3. 执行下载（带重试机制）
4. 验证文件完整性
5. 返回文件路径和元数据

## 错误处理
### 错误类型与降级方案
| 错误类型 | 降级方案 | 重试机制 |
|----------|----------|----------|
| 网络超时/断开 | 无限重试直到成功 | 间隔 3s |
| 平台反爬虫 | 回退到 cookies.txt 认证 | 1 次 |
| 视频不可用/已删除 | 返回友好错误，不阻塞后续流程 | 不重试 |
| 磁盘空间不足 | 返回明确错误信息 | 不重试 |

### 错误日志
所有错误自动记录到 `workspace/logs/video-download/YYYY-MM-DD.log`

## 与其他 Skill 协作
- **被依赖**: transcription（需要视频路径进行转录）
- **被依赖**: materials-organizer（整理下载的素材）
- **依赖**: env_checker（检查 yt-dlp/ffmpeg 是否安装）

## 使用示例
### 示例1：基础下载
```bash
helius.py download "https://www.youtube.com/watch?v=xxxx"
```

### 示例2：带 Cookie 认证
```python
import subprocess

cmd = [
    "python", "-m", "yt_dlp",
    "--format", "bestvideo[vcodec^=avc1][height<=1080][fps<=60]+bestaudio[ext=m4a]/best",
    "--merge-output-format", "mp4",
    "--cookies-from-browser", "chrome",
    "--concurrent-fragments", "8",
    "--retries", "infinite",
    "https://www.youtube.com/watch?v=xxxx"
]
subprocess.run(cmd, check=True)
```

## 依赖
- **Python**: 3.8+
- **yt-dlp**: 核心下载引擎（建议定期 `pip install -U yt-dlp`）
- **FFmpeg**: 用于音视频流的合并与封装
- **Chrome Browser**: 用于 cookies-from-browser 功能
