import threading
from typing import Optional, Union

from .window_manager import WindowIdentifier
from .tray import TrayIcon
from .window import FlexibleWindowManager
from .hotkey import HotkeyManager
from .process import ProcessManager, ProcessEvent


class WindowToTray:

    def __init__(self, window_title: Optional[str] = None,
                 window_identifier: Optional[WindowIdentifier] = None,
                 tray_name: str = "Min2Tray", tray_title: str = "Application"):
        if window_identifier:
            self.window_identifier = window_identifier
        elif window_title:
            self.window_identifier = WindowIdentifier(title=window_title)
        else:
            raise ValueError("Either window_title or window_identifier must be provided")

        self.window_manager = None
        self.tray_icon = TrayIcon(tray_name, tray_title)
        self.hotkey_manager = HotkeyManager()
        self.process_manager = ProcessManager()

        self.tray_icon.add_menu_item("Toggle Window", self._toggle_window, default=True)

    def _toggle_window(self):
        try:
            if self.window_manager:
                self.window_manager.toggle()
        except Exception as e:
            print(f"Error toggling window: {e}")
            try:
                self.setup_window()
                if self.window_manager:
                    self.window_manager.toggle()
            except Exception as e2:
                print(f"Failed to recover window manager: {e2}")

    def setup_window(self, window_identifier: Optional[WindowIdentifier] = None):
        identifier = window_identifier or self.window_identifier
        self.window_manager = FlexibleWindowManager(identifier)

    def register_hotkey(self, key_combination: str):
        self.hotkey_manager.register(key_combination, self._toggle_window)

    def run_command(self, command: Union[str, list], wait_time: float = 1.0):
        self.process_manager.add_hook(ProcessEvent.STARTED, self._on_process_started)
        self.process_manager.add_hook(ProcessEvent.EXITED, self._on_process_exited)
        self.process_manager.add_hook(ProcessEvent.ERROR, self._on_process_error)

        success = self.process_manager.run_command(command, wait_time)
        if not success:
            print("Failed to start process")

    def _on_process_started(self, process):
        print(f"Process started with PID: {process.pid}")

    def _on_process_exited(self, return_code):
        print(f"Process exited with return code: {return_code}")
        self.stop()

    def _on_process_error(self, exception):
        print(f"Process error: {exception}")
        self.stop()

    def start(self, icon_path: Optional[str] = None, start_hidden: bool = False):
        try:
            if start_hidden and self.window_manager:
                self.window_manager.hide()

            tray_thread = threading.Thread(target=self.tray_icon.start, args=(icon_path,))
            tray_thread.daemon = True
            tray_thread.start()

            if self.process_manager.is_running():
                self.process_manager.wait()
            else:
                try:
                    while True:
                        tray_thread.join(timeout=1.0)
                        if not tray_thread.is_alive():
                            break
                except KeyboardInterrupt:
                    print("\nReceived interrupt signal, stopping...")
                    self.stop()

        except Exception as e:
            print(f"Error during startup: {e}")
            self.stop()
            raise

    def stop(self):
        try:
            self.tray_icon.stop()
        except Exception as e:
            print(f"Error stopping tray icon: {e}")

        try:
            self.hotkey_manager.stop()
        except Exception as e:
            print(f"Error stopping hotkey manager: {e}")

        try:
            self.process_manager.terminate()
        except Exception as e:
            print(f"Error terminating process: {e}")


def minimize_to_tray(window_title: str, command: Optional[Union[str, list]] = None,
                    icon_path: Optional[str] = None, hotkey: Optional[str] = None,
                    start_hidden: bool = False, tray_name: str = "Min2Tray",
                    tray_title: str = "Application"):
    app = WindowToTray(window_title=window_title, tray_name=tray_name, tray_title=tray_title)

    if command:
        app.run_command(command)

    app.setup_window()

    if hotkey:
        app.register_hotkey(hotkey)

    app.start(icon_path, start_hidden)


def minimize_to_tray_flexible(window_identifier: WindowIdentifier,
                             command: Optional[Union[str, list]] = None,
                             icon_path: Optional[str] = None,
                             hotkey: Optional[str] = None,
                             start_hidden: bool = False,
                             tray_name: str = "Min2Tray",
                             tray_title: str = "Application"):
    app = WindowToTray(window_identifier=window_identifier, tray_name=tray_name, tray_title=tray_title)

    if command:
        app.run_command(command)

    app.setup_window()

    if hotkey:
        app.register_hotkey(hotkey)

    app.start(icon_path, start_hidden)
