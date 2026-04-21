# _示例_run 输出目录

此目录用于存放示例运行后的整理结果。

## 输出结构

```
_示例_run/
├── intermediate/
│   ├── youtube_assets.tsv          # 素材索引表
│   └── deduplication_report.json   # 去重报告（如启用）
└── final/
    └── library/
        └── by_video_id/
            └── {video_id}/         # 按视频 ID 组织的素材包
                ├── {video_id}.mp4
                ├── {video_id}.zh-Hant.vtt
                └── {video_id}.en.vtt
```

## 说明

- **intermediate/**：中间产物，供人工审核
- **final/**：结构化素材库，可供剪辑工具直接使用
- **index.md**：由 materials-organizer 自动生成的可视化清单

## 相关命令

```bash
python helius.py organize   # 整理 workspace/inputs/ 中的所有素材
python helius.py list       # 查看当前输入/输出状态
```
