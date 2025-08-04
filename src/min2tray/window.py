from .window_manager import WindowIdentifier, create_window_manager
from .utils import WindowNotFoundError


class WindowManager:

    def __init__(self, window_title: str):
        self.identifier = WindowIdentifier(title=window_title)
        self.manager = create_window_manager(self.identifier)
        self.window_title = window_title
        self.is_visible = True
        self._find_window()

    def _find_window(self):
        if not self.manager.find_window():
            raise WindowNotFoundError(f"Window with title '{self.window_title}' not found")

    def hide(self):
        self.manager.hide()
        self.is_visible = self.manager.is_visible

    def show(self):
        self.manager.show()
        self.is_visible = self.manager.is_visible

    def toggle(self):
        self.manager.toggle()
        self.is_visible = self.manager.is_visible


class FlexibleWindowManager:

    def __init__(self, identifier: WindowIdentifier):
        self.identifier = identifier
        self.manager = create_window_manager(identifier)
        self.is_visible = True
        self._find_window()

    def _find_window(self):
        if not self.manager.find_window():
            raise WindowNotFoundError(f"Window not found with identifier: {self.identifier}")

    def hide(self):
        self.manager.hide()
        self.is_visible = self.manager.is_visible

    def show(self):
        self.manager.show()
        self.is_visible = self.manager.is_visible

    def toggle(self):
        self.manager.toggle()
        self.is_visible = self.manager.is_visible
