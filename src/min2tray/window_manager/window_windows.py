from typing import Optional
from .window_base import BaseWindowManager, BaseWindowIdentifier
from ..utils import PLATFORM


class WindowsIdentifier(BaseWindowIdentifier):

    def __init__(self, title: Optional[str] = None,
                 process_id: Optional[int] = None,
                 handle: Optional[int] = None):
        super().__init__(title, process_id)
        self.handle = handle

    def __repr__(self):
        return f"WindowsIdentifier(title={self.title}, process_id={self.process_id}, handle={self.handle})"


class WindowsWindowManager(BaseWindowManager):

    def __init__(self, identifier: WindowsIdentifier):
        super().__init__(identifier)

    def find_window(self) -> bool:
        if PLATFORM != "windows":
            return False

        try:
            import win32gui
            import win32process

            if isinstance(self.identifier, WindowsIdentifier) and self.identifier.handle:
                self._platform_handle = self.identifier.handle
                return bool(win32gui.IsWindow(self._platform_handle))

            if self.identifier.title:
                handle = win32gui.FindWindow(None, self.identifier.title)
                if handle:
                    self._platform_handle = handle
                    return True

            if self.identifier.process_id:
                found_handles = []

                def enum_windows_proc(hwnd, lParam):
                    if win32gui.IsWindowVisible(hwnd):
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        if pid == self.identifier.process_id:
                            found_handles.append(hwnd)
                    return True

                win32gui.EnumWindows(enum_windows_proc, 0)
                if found_handles:
                    self._platform_handle = found_handles[0]
                    return True

            return False

        except ImportError:
            print("Warning: Windows-specific libraries not available")
            return False
        except Exception:
            return False

    def hide(self):
        if self._platform_handle and self.is_visible:
            try:
                import win32gui
                import win32con
                win32gui.ShowWindow(self._platform_handle, win32con.SW_HIDE)
                self.is_visible = False
            except ImportError:
                print("Warning: Windows-specific libraries not available")

    def show(self):
        if self._platform_handle and not self.is_visible:
            try:
                import win32gui
                import win32con
                import pywintypes

                win32gui.ShowWindow(self._platform_handle, win32con.SW_RESTORE)

                try:
                    win32gui.SetForegroundWindow(self._platform_handle)
                except pywintypes.error as e:
                    print(f"Warning: SetForegroundWindow failed: {e}")
                    try:
                        win32gui.SetWindowPos(
                            self._platform_handle,
                            win32con.HWND_TOPMOST,
                            0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                        )
                        win32gui.SetWindowPos(
                            self._platform_handle,
                            win32con.HWND_NOTOPMOST,
                            0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                        )
                    except pywintypes.error as e2:
                        print(f"Warning: Alternative window activation failed: {e2}")

                self.is_visible = True
            except ImportError:
                print("Warning: Windows-specific libraries not available")
