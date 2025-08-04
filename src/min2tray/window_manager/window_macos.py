import subprocess
from typing import Optional

from .window_base import BaseWindowManager, BaseWindowIdentifier
from ..utils import PLATFORM


class MacOSIdentifier(BaseWindowIdentifier):

    def __init__(self, title: Optional[str] = None,
                 process_id: Optional[int] = None,
                 window_number: Optional[int] = None):
        super().__init__(title, process_id)
        self.window_number = window_number

    def __repr__(self):
        return f"MacOSIdentifier(title={self.title}, process_id={self.process_id}, window_number={self.window_number})"


class MacOSWindowManager(BaseWindowManager):

    def __init__(self, identifier: MacOSIdentifier):
        super().__init__(identifier)

    def find_window(self) -> bool:
        if PLATFORM != "darwin":
            return False

        try:
            from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID  # type: ignore

            windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)

            for window in windows:
                if self.identifier.title and window.get('kCGWindowName') == self.identifier.title:
                    self._platform_handle = window
                    return True

                if isinstance(self.identifier, MacOSIdentifier) and self.identifier.window_number and window.get('kCGWindowNumber') == self.identifier.window_number:
                    self._platform_handle = window
                    return True

                if self.identifier.process_id and window.get('kCGWindowOwnerPID') == self.identifier.process_id:
                    self._platform_handle = window
                    return True

            return False

        except ImportError:
            print("Warning: macOS-specific libraries not available")
            return False
        except Exception:
            return False

    def hide(self):
        if self._platform_handle and self.is_visible:
            try:
                app_name = self._platform_handle.get('kCGWindowOwnerName', '')
                if app_name:
                    script = f'tell application "{app_name}" to set visible to false'
                    subprocess.run(["osascript", "-e", script], check=True)
                    self.is_visible = False
            except subprocess.CalledProcessError:
                pass

    def show(self):
        if self._platform_handle and not self.is_visible:
            try:
                app_name = self._platform_handle.get('kCGWindowOwnerName', '')
                if app_name:
                    script = f'tell application "{app_name}" to set visible to true'
                    subprocess.run(["osascript", "-e", script], check=True)
                    subprocess.run(["osascript", "-e", f'tell application "{app_name}" to activate'], check=True)
                    self.is_visible = True
            except subprocess.CalledProcessError:
                pass
