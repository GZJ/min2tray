from abc import ABC, abstractmethod
from typing import Optional


class BaseWindowIdentifier(ABC):

    def __init__(self, title: Optional[str] = None, process_id: Optional[int] = None):
        self.title = title
        self.process_id = process_id

    @abstractmethod
    def __repr__(self) -> str:
        pass


class BaseWindowManager(ABC):

    def __init__(self, identifier: BaseWindowIdentifier):
        self.identifier = identifier
        self.is_visible = True
        self._platform_handle = None

    @abstractmethod
    def find_window(self) -> bool:
        pass

    @abstractmethod
    def hide(self):
        pass

    @abstractmethod
    def show(self):
        pass

    def toggle(self):
        if self.is_visible:
            self.hide()
        else:
            self.show()
