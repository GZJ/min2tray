"""
Utility modules for Min2Tray library
"""

from .platform import PLATFORM, get_platform, is_windows, is_linux, is_macos
from .exceptions import TrayError, WindowNotFoundError, IconLoadError, HotkeyRegistrationError

__all__ = [
    "PLATFORM",
    "get_platform",
    "is_windows", 
    "is_linux",
    "is_macos",
    "TrayError",
    "WindowNotFoundError",
    "IconLoadError", 
    "HotkeyRegistrationError"
]
