# _示例_run 输入目录

此目录用于存放示例运行时的原始下载素材。

## 预期文件

将视频下载至此目录后，系统会按以下流程处理：

1. **下载**：`python helius.py download <url>` → 文件落入此目录
2. **转录**：`python helius.py transcribe <url>` → 音频发送至 Whisper
3. **整理**：`python helius.py organize` → 素材迁移至 `workspace/outputs/_示例_run/`

## 文件规范

建议包含：
- `.mp4` / `.mkv` 视频文件
- `.info.json` YouTube 元数据（如有）
- `.vtt` 字幕文件（如有）

## 示例命令

```bash
cd ~/Desktop/Helius-002
python helius.py download "https://www.youtube.com/watch?v=EXAMPLE"
python helius.py organize
python helius.py list
```
