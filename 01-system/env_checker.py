#!/usr/bin/env python3
"""
Helius-002 环境检查工具
检查 API keys、依赖安装、网络连接等环境配置
输出诊断报告
"""

import os
import sys
import subprocess
import socket
import shutil
from pathlib import Path
from datetime import datetime

WORKSPACE_ROOT = Path(__file__).parent.parent


class EnvChecker:
    """环境检查器"""

    def __init__(self):
        self.workspace = WORKSPACE_ROOT
        self.results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "checks": {},
            "summary": {"passed": 0, "failed": 0, "warnings": 0}
        }

    def check_api_keys(self) -> dict:
        """检查 API Keys 配置"""
        print("\n[1/4] 检查 API Keys...")
        api_keys = {
            "OPENAI_API_KEY": "OpenAI (GPT/Whisper/TTS)",
            "ELEVENLABS_API_KEY": "ElevenLabs (TTS)",
            "YOUTUBE_API_KEY": "YouTube Data API",
        }

        status = {}
        for key, service in api_keys.items():
            value = os.environ.get(key)
            if value:
                # 只显示前4位和后4位
                masked = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
                print(f"  ✅ {key} ({service}): {masked}")
                status[key] = {"service": service, "status": "configured", "masked": masked}
            else:
                print(f"  ⚠️  {key} ({service}): 未配置")
                status[key] = {"service": service, "status": "missing"}

        self.results["checks"]["api_keys"] = status
        return status

    def check_dependencies(self) -> dict:
        """检查依赖是否安装"""
        print("\n[2/4] 检查依赖安装...")
        deps = {
            "python": ("python", ["--version"]),
            "yt-dlp": ("yt-dlp", ["--version"]),
            "ffmpeg": ("ffmpeg", ["-version"]),
            "git": ("git", ["--version"]),
        }

        status = {}
        for name, (cmd, args) in deps.items():
            path = shutil.which(cmd)
            if path:
                try:
                    result = subprocess.run(
                        [cmd] + args,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    version_line = result.stdout.split("\n")[0] if result.stdout else "unknown"
                    print(f"  ✅ {name}: {version_line}")
                    status[name] = {"status": "installed", "path": path, "version": version_line}
                except Exception as e:
                    print(f"  ⚠️  {name}: 已找到但无法获取版本 ({e})")
                    status[name] = {"status": "warning", "path": path}
            else:
                print(f"  ❌ {name}: 未安装")
                status[name] = {"status": "missing"}

        self.results["checks"]["dependencies"] = status
        return status

    def check_network(self) -> dict:
        """检查网络连接"""
        print("\n[3/4] 检查网络连接...")
        hosts = {
            "openai.com": 443,
            "youtube.com": 443,
            "api.together.xyz": 443,
        }

        status = {}
        for host, port in hosts.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                sock.close()
                if result == 0:
                    print(f"  ✅ {host}:{port} - 可达")
                    status[host] = {"status": "reachable", "port": port}
                else:
                    print(f"  ⚠️  {host}:{port} - 连接失败")
                    status[host] = {"status": "unreachable", "port": port}
            except Exception as e:
                print(f"  ❌ {host}:{port} - {e}")
                status[host] = {"status": "error", "error": str(e)}

        self.results["checks"]["network"] = status
        return status

    def check_workspace(self) -> dict:
        """检查 Workspace 目录结构"""
        print("\n[4/4] 检查 Workspace 结构...")
        dirs = {
            "workspace/inputs": WORKSPACE_ROOT / "workspace" / "inputs",
            "workspace/outputs": WORKSPACE_ROOT / "workspace" / "outputs",
            "workspace/temp": WORKSPACE_ROOT / "workspace" / "temp",
            "workspace/logs": WORKSPACE_ROOT / "workspace" / "logs",
            "skills": WORKSPACE_ROOT / "skills",
            "tools": WORKSPACE_ROOT / "tools",
        }

        status = {}
        for name, path in dirs.items():
            abs_path = Path(path).expanduser()
            if abs_path.exists():
                file_count = len(list(abs_path.rglob("*"))) if abs_path.is_dir() else 1
                print(f"  ✅ {name}: {abs_path} ({file_count} 项)")
                status[name] = {"status": "exists", "path": str(abs_path), "items": file_count}
            else:
                print(f"  ⚠️  {name}: {abs_path} (不存在，将自动创建)")
                status[name] = {"status": "missing", "path": str(abs_path)}

        self.results["checks"]["workspace"] = status
        return status

    def run_all(self) -> dict:
        """运行所有检查"""
        print("=" * 50)
        print("Helius-002 环境诊断报告")
        print("=" * 50)
        print(f"时间: {self.results['timestamp']}")
        print(f"工作区: {self.workspace}")

        self.check_api_keys()
        self.check_dependencies()
        self.check_network()
        self.check_workspace()

        # 生成摘要
        all_checks = []
        for category in self.results["checks"].values():
            all_checks.extend(category.values())

        self.results["summary"]["passed"] = sum(
            1 for c in all_checks if c.get("status") in ("configured", "installed", "exists", "reachable")
        )
        self.results["summary"]["failed"] = sum(
            1 for c in all_checks if c.get("status") in ("missing", "error")
        )
        self.results["summary"]["warnings"] = sum(
            1 for c in all_checks if c.get("status") in ("warning",)
        )

        print("\n" + "=" * 50)
        print("摘要")
        print("=" * 50)
        print(f"  ✅ 通过: {self.results['summary']['passed']}")
        print(f"  ❌ 失败: {self.results['summary']['failed']}")
        print(f"  ⚠️  警告: {self.results['summary']['warnings']}")

        if self.results["summary"]["failed"] > 0:
            print("\n[建议] 请安装缺失的依赖或配置 API Keys")
        elif self.results["summary"]["warnings"] > 0:
            print("\n[建议] 部分功能可能受限，建议解决警告项")
        else:
            print("\n[状态] 环境配置良好!")

        return self.results

    def save_report(self, path: Path = None) -> Path:
        """保存诊断报告到文件"""
        import json
        if path is None:
            path = WORKSPACE_ROOT / "workspace" / "logs" / f"env-check-{datetime.now().strftime('%Y-%m-%d')}.json"

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n[报告] 诊断报告已保存到: {path.relative_to(WORKSPACE_ROOT)}")
        return path


def main():
    checker = EnvChecker()
    checker.run_all()
    checker.save_report()

    # 如果有严重缺失，返回非零退出码
    if checker.results["summary"]["failed"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
