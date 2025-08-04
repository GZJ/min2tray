import os
from typing import Optional, Callable

import pystray
from PIL import Image, ImageDraw

from .utils import IconLoadError


class TrayIcon:

    def __init__(self, name: str = "Min2Tray", title: str = "Application"):
        self.name = name
        self.title = title
        self.icon = None
        self._menu_items = []
        self._running = False

    def create_default_image(self, width: int = 64, height: int = 64,
                           color1: str = "black", color2: str = "white") -> Image.Image:
        image = Image.new("RGB", (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
        dc.rectangle((0, height // 2, width // 2, height), fill=color2)
        return image

    def load_icon(self, icon_path: Optional[str] = None) -> Image.Image:
        if icon_path and os.path.exists(icon_path):
            try:
                return Image.open(icon_path)
            except Exception as e:
                raise IconLoadError(f"Failed to load icon from {icon_path}: {e}")
        else:
            return self.create_default_image()

    def add_menu_item(self, text: str, action: Callable, default: bool = False):
        self._menu_items.append(pystray.MenuItem(text, action, default=default))

    def start(self, icon_path: Optional[str] = None):
        icon_image = self.load_icon(icon_path)

        if not any(item.text == "Exit" for item in self._menu_items):
            self.add_menu_item("Exit", self.stop)

        self.icon = pystray.Icon(
            self.name,
            icon=icon_image,
            title=self.title,
            menu=pystray.Menu(*self._menu_items)
        )

        self._running = True
        self.icon.run()

    def stop(self):
        if self.icon:
            self._running = False
            self.icon.stop()
