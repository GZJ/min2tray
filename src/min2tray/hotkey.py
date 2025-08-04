from typing import Callable

from pynput import keyboard

from .utils import HotkeyRegistrationError


class HotkeyManager:

    def __init__(self):
        self.listener = None
        self.hotkeys = {}

    def register(self, key_combination: str, callback: Callable):
        try:
            hotkey = keyboard.HotKey(keyboard.HotKey.parse(key_combination), callback)
            self.hotkeys[key_combination] = hotkey

            if self.listener:
                self.listener.stop()

            temp_listener = keyboard.Listener(on_press=lambda k: None, on_release=lambda k: None)

            def for_canonical(f):
                return lambda k: f(temp_listener.canonical(k))

            self.listener = keyboard.Listener(
                on_press=for_canonical(self._on_press),
                on_release=for_canonical(self._on_release)
            )
            self.listener.start()

        except Exception as e:
            raise HotkeyRegistrationError(f"Failed to register hotkey '{key_combination}': {e}")

    def _on_press(self, key):
        for hotkey in self.hotkeys.values():
            hotkey.press(key)

    def _on_release(self, key):
        for hotkey in self.hotkeys.values():
            hotkey.release(key)

    def stop(self):
        if self.listener:
            self.listener.stop()
