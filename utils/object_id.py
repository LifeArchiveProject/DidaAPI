"""ObjectId 辅助工具

用于生成与 MongoDB ObjectId 格式兼容的 24 位十六进制字符串。
滴答清单前端在构造番茄钟操作 ID 时使用相同格式，因此这里复刻生成规则：
- 前 4 字节为当前 Unix 时间戳（秒）
- 中间 5 字节为随机值
- 最后 3 字节为自增计数器
"""

from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class ObjectIdGenerator:
    """线程安全的 ObjectId 生成器"""

    _counter: int = field(init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    _rand_bytes: bytes = field(init=False)
    _COUNTER_MAX: ClassVar[int] = 0xFFFFFF

    def __post_init__(self) -> None:
        self._counter = int.from_bytes(os.urandom(3), "big")
        self._rand_bytes = os.urandom(5)

    def generate(self) -> str:
        """
        生成新的 ObjectId。

        Returns:
            str: 24 位十六进制字符串
        """
        timestamp = int(time.time())
        ts_bytes = timestamp.to_bytes(4, "big")

        with self._lock:
            counter = self._counter
            self._counter = (self._counter + 1) & self._COUNTER_MAX

        counter_bytes = counter.to_bytes(3, "big")
        object_id = ts_bytes + self._rand_bytes + counter_bytes
        return object_id.hex()


# 提供模块级默认生成器，避免频繁实例化
_DEFAULT_GENERATOR = ObjectIdGenerator()


def generate_object_id() -> str:
    """生成新的 ObjectId 字符串"""
    return _DEFAULT_GENERATOR.generate()

