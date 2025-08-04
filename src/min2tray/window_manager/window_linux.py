import subprocess
from typing import Optional

from .window_base import BaseWindowManager, BaseWindowIdentifier
from ..utils import PLATFORM


class LinuxIdentifier(BaseWindowIdentifier):

    def __init__(self, title: Optional[str] = None,
                 process_id: Optional[int] = None,
                 window_id: Optional[int] = None):
        super().__init__(title, process_id)
        self.window_id = window_id

    def __repr__(self):
        return f"LinuxIdentifier(title={self.title}, process_id={self.process_id}, window_id={self.window_id})"


class LinuxWindowManager(BaseWindowManager):

    def __init__(self, identifier: LinuxIdentifier):
        super().__init__(identifier)

    def find_window(self) -> bool:
        if PLATFORM != "linux":
            return False

        try:
            if isinstance(self.identifier, LinuxIdentifier) and self.identifier.window_id:
                self._platform_handle = str(self.identifier.window_id)
                return True

            if self.identifier.title:
                result = subprocess.run(
                    ["xdotool", "search", "--name", self.identifier.title],
                    capture_output=True, text=True
                )
                if result.returncode == 0 and result.stdout.strip():
                    self._platform_handle = result.stdout.strip().split('\n')[0]
                    return True

            if self.identifier.process_id:
                result = subprocess.run(
                    ["xdotool", "search", "--pid", str(self.identifier.process_id)],
                    capture_output=True, text=True
                )
                if result.returncode == 0 and result.stdout.strip():
                    self._platform_handle = result.stdout.strip().split('\n')[0]
                    return True

            return False

        except Exception:
            return False

    def hide(self):
        if self._platform_handle and self.is_visible:
            try:
                subprocess.run(["xdotool", "windowunmap", str(self._platform_handle)], check=True)
                self.is_visible = False
            except subprocess.CalledProcessError:
                pass

    def show(self):
        if self._platform_handle and not self.is_visible:
            try:
                subprocess.run(["xdotool", "windowmap", str(self._platform_handle)], check=True)
                subprocess.run(["xdotool", "windowactivate", str(self._platform_handle)], check=True)
                self.is_visible = True
            except subprocess.CalledProcessError:
                pass
