"""
Platform detection and utilities
"""

import platform

# Platform detection
PLATFORM = platform.system().lower()


def get_platform() -> str:
    """获取当前平台"""
    return PLATFORM


def is_windows() -> bool:
    """检查是否为Windows平台"""
    return PLATFORM == "windows"


def is_linux() -> bool:
    """检查是否为Linux平台"""
    return PLATFORM == "linux"


def is_macos() -> bool:
    """检查是否为macOS平台"""
    return PLATFORM == "darwin"
