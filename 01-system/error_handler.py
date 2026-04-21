#!/usr/bin/env python3
"""
Helius-002 错误处理工具
提供统一的错误处理、重试和降级机制
"""

import time
import traceback
from pathlib import Path
from datetime import datetime
from functools import wraps
from typing import Callable, Any, Optional, Tuple

WORKSPACE_ROOT = Path(__file__).parent.parent
LOGS_DIR = WORKSPACE_ROOT / "workspace" / "logs"


class ErrorHandler:
    """统一错误处理器"""

    def __init__(self, max_retries: int = 3, retry_delay: float = 2.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._ensure_logs_dir()

    def _ensure_logs_dir(self):
        """确保日志目录存在"""
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    def with_retry(
        self,
        func: Callable,
        *args,
        retry_on: Tuple[type, ...] = (Exception,),
        **kwargs
    ) -> Any:
        """
        重试逻辑装饰器/包装器

        Args:
            func: 要执行的函数
            *args: 函数位置参数
            retry_on: 需要重试的异常类型元组
            **kwargs: 函数关键字参数

        Returns:
            函数返回值

        Raises:
            最后一次重试仍然失败的异常
        """
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except retry_on as e:
                last_error = e
                if attempt < self.max_retries:
                    print(f"  [RETRY] {func.__name__} 失败 ({attempt}/{self.max_retries}), {self.retry_delay}s 后重试...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"  [FAIL] {func.__name__} 最终失败")
                    self.log_error(last_error, {"func": func.__name__, "args": str(args)})
        raise last_error

    def with_fallback(
        self,
        primary_func: Callable,
        fallback_func: Callable,
        context: str = ""
    ) -> Any:
        """
        降级逻辑包装器

        Args:
            primary_func: 主方法（不接受参数）
            fallback_func: 备用方法（不接受参数）
            context: 上下文描述

        Returns:
            成功执行的方法的返回值
        """
        try:
            return primary_func()
        except Exception as e:
            print(f"  [FALLBACK] {context} 主方法失败，尝试降级方案...")
            self.log_error(e, {"context": context, "method": "primary"})
            try:
                return fallback_func()
            except Exception as e2:
                print(f"  [FATAL] {context} 降级方案也失败")
                self.log_error(e2, {"context": context, "method": "fallback"})
                raise e2

    def log_error(self, error: Exception, context: dict = None) -> Path:
        """
        记录错误到 workspace/logs/

        Args:
            error: 异常对象
            context: 额外的上下文信息

        Returns:
            日志文件路径
        """
        self._ensure_logs_dir()
        log_file = LOGS_DIR / f"helius-{datetime.now().strftime('%Y-%m-%d')}.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ctx_str = "\n".join(f"  {k}: {v}" for k, v in (context or {}).items())
        log_entry = (
            f"[{timestamp}] ERROR\n"
            f"  Type: {type(error).__name__}\n"
            f"  Message: {error}\n"
            + (f"  Context:\n{ctx_str}\n" if context else "")
            + f"  Traceback:\n{traceback.format_exc()}\n"
            + "-" * 50 + "\n"
        )
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"  [LOG] 错误已记录到 {log_file.relative_to(WORKSPACE_ROOT)}")
        return log_file

    def retry_decorator(self, retry_on: Tuple[type, ...] = (Exception,)):
        """重试装饰器工厂"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return self.with_retry(func, *args, retry_on=retry_on, **kwargs)
            return wrapper
        return decorator


def with_retry_decorator(max_retries: int = 3, retry_delay: float = 2.0, retry_on: Tuple[type, ...] = (Exception,)):
    """独立重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = ErrorHandler(max_retries=max_retries, retry_delay=retry_delay)
            return handler.with_retry(func, *args, retry_on=retry_on, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    # 测试错误处理工具
    handler = ErrorHandler(max_retries=3, retry_delay=1.0)

    def flaky_function(fail_count: int = 2):
        """测试用：前N次调用失败的函数"""
        flaky_function.call_count = getattr(flaky_function, 'call_count', 0) + 1
        if flaky_function.call_count <= fail_count:
            raise RuntimeError(f"模拟失败 ({flaky_function.call_count}/{fail_count})")
        return "成功!"

    # 测试重试
    print("测试重试逻辑:")
    result = handler.with_retry(flaky_function, fail_count=2)
    print(f"  结果: {result}")

    # 测试降级
    print("\n测试降级逻辑:")
    def primary_fail():
        raise RuntimeError("主方法失败")

    def fallback_success():
        return "降级方案成功!"

    result = handler.with_fallback(primary_fail, fallback_success, "测试降级")
    print(f"  结果: {result}")

    print("\n所有测试通过!")
