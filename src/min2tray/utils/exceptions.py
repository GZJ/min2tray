"""
Custom exceptions for Min2Tray library
"""


class TrayError(Exception):
    """Base exception for tray-related errors"""
    pass


class WindowNotFoundError(TrayError):
    """Raised when the specified window cannot be found"""
    pass


class IconLoadError(TrayError):
    """Raised when the icon image cannot be loaded"""
    pass


class HotkeyRegistrationError(TrayError):
    """Raised when hotkey registration fails"""
    pass
