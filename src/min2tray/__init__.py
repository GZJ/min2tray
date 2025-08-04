from .core import WindowToTray, minimize_to_tray, minimize_to_tray_flexible
from .tray import TrayIcon
from .window import WindowManager, FlexibleWindowManager
from .hotkey import HotkeyManager
from .process import ProcessManager, ProcessEvent
from .window_manager import WindowIdentifier, create_window_manager, by_title, by_process_id, by_window_id, by_handle
from .utils import PLATFORM
from .utils import WindowNotFoundError, TrayError, IconLoadError, HotkeyRegistrationError
from .cli import main

__version__ = "0.2.0"
__author__ = "gzj"
__email__ = "gzj00@outlook.com"

__all__ = [
    "WindowToTray",
    "TrayIcon",
    "WindowManager",
    "FlexibleWindowManager",
    "HotkeyManager",
    "ProcessManager",
    "ProcessEvent",
    "minimize_to_tray",
    "minimize_to_tray_flexible",
    "WindowIdentifier",
    "create_window_manager",
    "by_title",
    "by_process_id",
    "by_window_id",
    "by_handle",
    "PLATFORM",
    "WindowNotFoundError",
    "TrayError",
    "IconLoadError",
    "HotkeyRegistrationError",
    "main",
]
