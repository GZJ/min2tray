from .window_base import BaseWindowManager, BaseWindowIdentifier
from .window_windows import WindowsWindowManager, WindowsIdentifier
from .window_linux import LinuxWindowManager, LinuxIdentifier
from .window_macos import MacOSWindowManager, MacOSIdentifier
from ..utils import PLATFORM
from typing import Optional, Union


def by_title(title: str) -> 'WindowIdentifier':
    return WindowIdentifier(title=title)


def by_process_id(pid: int) -> 'WindowIdentifier':
    return WindowIdentifier(process_id=pid)


def by_window_id(window_id: int) -> 'WindowIdentifier':
    return WindowIdentifier(window_id=window_id)


def by_handle(handle: int) -> 'WindowIdentifier':
    return WindowIdentifier(handle=handle)


class WindowIdentifier:

    def __init__(self, title: Optional[str] = None,
                 window_id: Optional[int] = None,
                 process_id: Optional[int] = None,
                 handle: Optional[int] = None):
        self.title = title
        self.window_id = window_id
        self.process_id = process_id
        self.handle = handle

    def __repr__(self):
        return f"WindowIdentifier(title={self.title}, window_id={self.window_id}, process_id={self.process_id}, handle={self.handle})"

    def to_platform_specific(self) -> BaseWindowIdentifier:
        if PLATFORM == "windows":
            return WindowsIdentifier(
                title=self.title,
                process_id=self.process_id,
                handle=self.handle
            )
        elif PLATFORM == "linux":
            return LinuxIdentifier(
                title=self.title,
                process_id=self.process_id,
                window_id=self.window_id
            )
        elif PLATFORM == "darwin":
            return MacOSIdentifier(
                title=self.title,
                process_id=self.process_id,
                window_number=self.window_id
            )
        else:
            raise NotImplementedError(f"Platform {PLATFORM} is not supported")


def create_window_manager(identifier: 'WindowIdentifier') -> BaseWindowManager:
    platform_identifier = identifier.to_platform_specific()
    
    if PLATFORM == "windows":
        return WindowsWindowManager(platform_identifier)
    elif PLATFORM == "linux":
        return LinuxWindowManager(platform_identifier)
    elif PLATFORM == "darwin":
        return MacOSWindowManager(platform_identifier)
    else:
        raise NotImplementedError(f"Platform {PLATFORM} is not supported")


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
