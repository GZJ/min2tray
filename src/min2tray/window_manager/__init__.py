from .window_base import BaseWindowManager, BaseWindowIdentifier
from .window_windows import WindowsWindowManager, WindowsIdentifier
from .window_linux import LinuxWindowManager, LinuxIdentifier
from .window_macos import MacOSWindowManager, MacOSIdentifier
from .window_factory import (
    WindowIdentifier,
    create_window_manager,
    by_title,
    by_process_id,
    by_window_id,
    by_handle
)

__all__ = [
    "BaseWindowManager",
    "BaseWindowIdentifier",
    "WindowsWindowManager",
    "WindowsIdentifier",
    "LinuxWindowManager",
    "LinuxIdentifier",
    "MacOSWindowManager",
    "MacOSIdentifier",
    "WindowIdentifier",
    "create_window_manager",
    "by_title",
    "by_process_id",
    "by_window_id",
    "by_handle"
]
