import webview
import threading
import time
import sys
import os
from pathlib import Path
from typing import List, Dict

from min2tray import WindowToTray
from min2tray.window_manager import WindowIdentifier
from min2tray.tray import TrayIcon


def get_tray_icon_path():
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    icon_path = project_root / "assets" / "tray.png"

    if icon_path.exists():
        return str(icon_path)
    else:
        print(f"⚠️ Warning: Custom tray icon not found at {icon_path}, using default icon")
        return None


class MultiWindowTrayManager:

    def __init__(self, tray_name: str = "Multi-Window Manager"):
        self.tray_name = tray_name
        self.windows: Dict[str, WindowToTray] = {}
        self.webview_windows: List = []
        self.tray_icon = TrayIcon(tray_name, "Multi-Window Manager")
        self.is_running = False

        self._setup_tray_menu()

    def _setup_tray_menu(self):
        self.tray_icon.add_menu_item("🔄 Toggle All Windows", self._toggle_all_windows, default=True)
        self.tray_icon.add_menu_item("👁️ Show All Windows", self._show_all_windows)
        self.tray_icon.add_menu_item("🙈 Hide All Windows", self._hide_all_windows)

    def create_demo_windows(self):
        print("🏗️ Creating multiple demo windows...")

        control_html = self._create_control_panel_html()
        window1 = webview.create_window(
            'Main Control Panel',
            html=control_html,
            width=600,
            height=500,
            x=100,
            y=100,
            resizable=True
        )
        self.webview_windows.append(window1)

        data_html = self._create_data_panel_html()
        window2 = webview.create_window(
            'Data Panel',
            html=data_html,
            width=500,
            height=400,
            x=750,
            y=100,
            resizable=True
        )
        self.webview_windows.append(window2)

        settings_html = self._create_settings_panel_html()
        window3 = webview.create_window(
            'Settings Panel',
            html=settings_html,
            width=450,
            height=350,
            x=100,
            y=650,
            resizable=True
        )
        self.webview_windows.append(window3)

        return [window1, window2, window3]

    def _create_control_panel_html(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Main Control Panel</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                    box-sizing: border-box;
                }
                .panel {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 25px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                }
                h1 {
                    text-align: center;
                    margin-bottom: 30px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                }
                .control-group {
                    margin: 20px 0;
                    padding: 15px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    border-left: 4px solid #4CAF50;
                }
                button {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 16px;
                    margin: 5px;
                    transition: background 0.3s;
                    width: 100%;
                }
                button:hover {
                    background: #45a049;
                }
                .status {
                    background: rgba(76, 175, 80, 0.2);
                    padding: 15px;
                    border-radius: 8px;
                    margin: 20px 0;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="panel">
                <h1>🎮 Multi-Window Main Control Panel</h1>
                <div class="status">
                    ✅ Multi-window management system activated
                </div>
                <div class="control-group">
                    <h3>🎯 Hotkey Functions</h3>
                    <p>• <strong>Ctrl+Alt+1</strong> - Toggle Main Control Panel</p>
                    <p>• <strong>Ctrl+Alt+2</strong> - Toggle Data Panel</p>
                    <p>• <strong>Ctrl+Alt+3</strong> - Toggle Settings Panel</p>
                    <p>• <strong>Ctrl+Alt+H</strong> - Hide/Show All Windows</p>
                </div>
                <div class="control-group">
                    <h3>🖱️ System Tray Functions</h3>
                    <p>• Right-click the tray icon to see the multi-window menu</p>
                    <p>• Control the visibility of each window individually</p>
                    <p>• Support for one-click show/hide all windows</p>
                </div>
                <div class="control-group">
                    <button onclick="alert('This is a test button for the Main Control Panel')">Test Function</button>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_data_panel_html(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Panel</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                    min-height: 100vh;
                    box-sizing: border-box;
                }
                .panel {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 25px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                }
                h1 {
                    text-align: center;
                    margin-bottom: 30px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                }
                .data-item {
                    display: flex;
                    justify-content: space-between;
                    padding: 10px;
                    margin: 10px 0;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                }
                .data-value {
                    font-weight: bold;
                    color: #FFE082;
                }
            </style>
        </head>
        <body>
            <div class="panel">
                <h1>📊 Data Panel</h1>
                <div class="data-item">
                    <span>Number of Windows:</span>
                    <span class="data-value">3</span>
                </div>
                <div class="data-item">
                    <span>Tray Status:</span>
                    <span class="data-value">Active</span>
                </div>
                <div class="data-item">
                    <span>Hotkeys:</span>
                    <span class="data-value">Registered</span>
                </div>
                <div class="data-item">
                    <span>Runtime:</span>
                    <span class="data-value" id="runtime">00:00</span>
                </div>
                <div class="data-item">
                    <span>Memory Usage:</span>
                    <span class="data-value">Normal</span>
                </div>
            </div>
            <script>
                let startTime = Date.now();
                setInterval(() => {
                    const elapsed = Math.floor((Date.now() - startTime) / 1000);
                    const minutes = Math.floor(elapsed / 60);
                    const seconds = elapsed % 60;
                    document.getElementById('runtime').textContent =
                        `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                }, 1000);
            </script>
        </body>
        </html>
        """

    def _create_settings_panel_html(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Settings Panel</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    min-height: 100vh;
                    box-sizing: border-box;
                }
                .panel {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 25px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                }
                h1 {
                    text-align: center;
                    margin-bottom: 30px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                }
                .setting-item {
                    margin: 15px 0;
                    padding: 15px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    border-left: 4px solid #2196F3;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                }
                input, select {
                    width: 100%;
                    padding: 8px;
                    border: none;
                    border-radius: 4px;
                    background: rgba(255, 255, 255, 0.9);
                    color: #333;
                }
            </style>
        </head>
        <body>
            <div class="panel">
                <h1>⚙️ Settings Panel</h1>
                <div class="setting-item">
                    <label>Tray Icon Theme:</label>
                    <select>
                        <option>Default</option>
                        <option>Dark</option>
                        <option>Color</option>
                    </select>
                </div>
                <div class="setting-item">
                    <label>Hotkey Trigger Delay (ms):</label>
                    <input type="number" value="100">
                </div>
                <div class="setting-item">
                    <label>Auto-hide Time (seconds):</label>
                    <input type="number" value="0" placeholder="0 = disabled">
                </div>
                <div class="setting-item">
                    <label>Window Animation:</label>
                    <select>
                        <option>Enabled</option>
                        <option>Disabled</option>
                    </select>
                </div>
            </div>
        </body>
        </html>
        """

    def setup_tray_integration(self):
        def setup_multi_tray():
            time.sleep(3)

            try:
                window_configs = [
                    ("Main Control Panel", "<ctrl>+<alt>+1"),
                    ("Data Panel", "<ctrl>+<alt>+2"),
                    ("Settings Panel", "<ctrl>+<alt>+3")
                ]

                for window_title, hotkey in window_configs:
                    print(f"🔧 Setting up window management for: {window_title}")

                    window_identifier = WindowIdentifier(title=window_title)

                    window_to_tray = WindowToTray(
                        window_identifier=window_identifier,
                        tray_name=f"Hidden-{window_title}",
                        tray_title=window_title
                    )

                    window_to_tray.setup_window()

                    window_to_tray.register_hotkey(hotkey)

                    self.windows[window_title] = window_to_tray

                    self.tray_icon.add_menu_item(
                        f"🔄 Toggle {window_title}",
                        lambda title=window_title: self._toggle_single_window(title)
                    )

                self.tray_icon.add_menu_item("------", lambda: None)

                from min2tray.hotkey import HotkeyManager
                self.hotkey_manager = HotkeyManager()
                self.hotkey_manager.register("<ctrl>+<alt>+h", self._toggle_all_windows)

                icon_path = get_tray_icon_path()

                if icon_path:
                    print(f"🎨 Using custom tray icon: {icon_path}")
                    threading.Thread(target=lambda: self.tray_icon.start(icon_path), daemon=True).start()
                else:
                    threading.Thread(target=self.tray_icon.start, daemon=True).start()

                print("✅ Multi-window tray integration setup complete")
                print("💡 Use the following hotkeys to control windows:")
                print("   • Ctrl+Alt+1 - Main Control Panel")
                print("   • Ctrl+Alt+2 - Data Panel")
                print("   • Ctrl+Alt+3 - Settings Panel")
                print("   • Ctrl+Alt+H - All Windows")

            except Exception as e:
                print(f"❌ Error setting up multi-window tray integration: {e}")
                import traceback
                traceback.print_exc()

        threading.Thread(target=setup_multi_tray, daemon=True).start()

    def _toggle_single_window(self, window_title: str):
        try:
            if window_title in self.windows:
                self.windows[window_title].window_manager.toggle()
                print(f"🔄 Toggled window: {window_title}")
        except Exception as e:
            print(f"❌ Error toggling window {window_title}: {e}")

    def _toggle_all_windows(self):
        print("🔄 Toggling all windows")
        for window_title, window_to_tray in self.windows.items():
            try:
                window_to_tray.window_manager.toggle()
            except Exception as e:
                print(f"❌ Error toggling window {window_title}: {e}")

    def _show_all_windows(self):
        print("👁️ Showing all windows")
        for window_title, window_to_tray in self.windows.items():
            try:
                window_to_tray.window_manager.show()
            except Exception as e:
                print(f"❌ Error showing window {window_title}: {e}")

    def _hide_all_windows(self):
        print("🙈 Hiding all windows")
        for window_title, window_to_tray in self.windows.items():
            try:
                window_to_tray.window_manager.hide()
            except Exception as e:
                print(f"❌ Error hiding window {window_title}: {e}")

    def _quit_app(self):
        print("👋 Exiting multi-window application...")

        for window_to_tray in self.windows.values():
            try:
                window_to_tray.stop()
            except Exception as e:
                print(f"❌ Error stopping window manager: {e}")

        if hasattr(self, 'hotkey_manager'):
            try:
                self.hotkey_manager.stop()
            except Exception as e:
                print(f"❌ Error stopping hotkey manager: {e}")

        if self.tray_icon:
            self.tray_icon.stop()

        for window in self.webview_windows:
            try:
                window.destroy()
            except:
                pass

    def run(self):
        print("🚀 Starting multi-window tray demo...")

        self.create_demo_windows()

        self.setup_tray_integration()

        self.tray_icon.add_menu_item("❌ Exit", self._quit_app)

        try:
            webview.start(debug=False)
        except KeyboardInterrupt:
            print("\n👋 User interrupted, exiting...")
            self._quit_app()


def main():
    print("=" * 70)
    print("🎯 Min2Tray Multi-Window Management Demo")
    print("=" * 70)
    print("📝 This demo shows how to use the min2tray library to manage multiple windows")
    print("🔧 Features:")
    print("   • Manage 3 independent PyWebView windows simultaneously")
    print("   • Each window has its own hotkey control")
    print("   • Unified system tray interface to manage all windows")
    print("   • Supports individual and batch control of window visibility")
    print("   • Uses custom tray icon (assets/tray.png)")
    print("")
    print("🎮 Hotkey Guide:")
    print("   • Ctrl+Alt+1 - Toggle Main Control Panel")
    print("   • Ctrl+Alt+2 - Toggle Data Panel")
    print("   • Ctrl+Alt+3 - Toggle Settings Panel")
    print("   • Ctrl+Alt+H - Toggle All Windows")
    print("=" * 70)

    try:
        app = MultiWindowTrayManager()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 User interrupted, exiting...")
    except Exception as e:
        print(f"❌ Error during runtime: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
