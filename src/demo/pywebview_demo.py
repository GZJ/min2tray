import webview
import threading
import time
import sys
import os
from pathlib import Path

from min2tray import WindowToTray
from min2tray.window_manager import WindowIdentifier


def get_tray_icon_path():
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    icon_path = project_root / "assets" / "tray.png"

    if icon_path.exists():
        return str(icon_path)
    else:
        print(f"⚠️ Warning: Custom tray icon not found at {icon_path}, using default icon")
        return None


class WebViewTrayApp:

    def __init__(self):
        self.webview_window = None
        self.tray_app = None
        self.is_running = False

    def create_webview(self):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Min2Tray PyWebView Demo</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                    box-sizing: border-box;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 30px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                }
                h1 {
                    text-align: center;
                    margin-bottom: 30px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                }
                .feature {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 10px;
                    border-left: 4px solid #4CAF50;
                }
                .hotkey {
                    background: rgba(255, 255, 255, 0.2);
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-family: 'Courier New', monospace;
                    font-weight: bold;
                }
                .status {
                    text-align: center;
                    padding: 15px;
                    background: rgba(76, 175, 80, 0.2);
                    border-radius: 8px;
                    margin: 20px 0;
                }
                button {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 16px;
                    margin: 10px;
                    transition: background 0.3s;
                }
                button:hover {
                    background: #45a049;
                }
                .info {
                    background: rgba(33, 150, 243, 0.2);
                    padding: 15px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 4px solid #2196F3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Min2Tray PyWebView Demo</h1>

                <div class="status">
                    ✅ PyWebView window created, Min2Tray system tray function activated
                </div>

                <div class="feature">
                    <h3>🎯 Hotkey Function</h3>
                    <p>Press <span class="hotkey">Ctrl+Alt+h</span> to hide/show the window</p>
                    <p>After hiding, the window will be minimized to the system tray. Click the tray icon to show it again.</p>
                </div>

                <div class="feature">
                    <h3>🎮 System Tray Function</h3>
                    <p>• Right-click the tray icon to see the menu</p>
                    <p>• Left-click to toggle window visibility</p>
                    <p>• Supports running completely hidden in the background</p>
                </div>

                <div class="info">
                    <h3>📋 Instructions</h3>
                    <p>1. This demo shows how to use the pywebview library with min2tray</p>
                    <p>2. The application will automatically identify the current pywebview window and manage it in the system tray</p>
                    <p>3. Supports global hotkeys that work even when the window is not in the foreground</p>
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <button onclick="pywebview.api.minimize_window()">Minimize to Tray</button>
                    <button onclick="pywebview.api.show_info()">Show Info</button>
                </div>
            </div>

            <script>
                window.addEventListener('DOMContentLoaded', function() {
                    console.log('PyWebView Demo loaded');
                });
            </script>
        </body>
        </html>
        """

        self.webview_window = webview.create_window(
            'Min2Tray PyWebView Demo',
            html=html_content,
            width=900,
            height=700,
            resizable=True,
            minimized=False
        )

        return self.webview_window

    def setup_tray_integration(self):
        def setup_tray():
            time.sleep(2)

            try:
                window_identifier = WindowIdentifier(title="Min2Tray PyWebView Demo")

                self.tray_app = WindowToTray(
                    window_identifier=window_identifier,
                    tray_name="PyWebView Demo",
                    tray_title="Min2Tray PyWebView Demo"
                )

                self.tray_app.setup_window()

                self.tray_app.register_hotkey("<ctrl>+<alt>+h")

                self.tray_app.tray_icon.add_menu_item("Show Info", self._show_info)
                self.tray_app.tray_icon.add_menu_item("About", self._show_about)
                self.tray_app.tray_icon.add_menu_item("Exit", self._quit_app)

                icon_path = get_tray_icon_path()

                if icon_path:
                    print(f"🎨 Using custom tray icon: {icon_path}")
                    threading.Thread(target=lambda: self.tray_app.tray_icon.start(icon_path), daemon=True).start()
                else:
                    threading.Thread(target=self.tray_app.tray_icon.start, daemon=True).start()

                print("✅ System tray integration setup complete")
                print("💡 Use Ctrl+Alt+h to hide/show the window")

            except Exception as e:
                print(f"❌ Error setting up tray integration: {e}")

        threading.Thread(target=setup_tray, daemon=True).start()

    def _show_info(self):
        print("📊 Min2Tray PyWebView Demo - Current status is normal")

    def _show_about(self):
        print("ℹ️ Min2Tray PyWebView Demo v1.0 - A demo application integrating pywebview and system tray functionality")

    def _quit_app(self):
        print("👋 Exiting application...")
        if self.tray_app:
            self.tray_app.stop()
        if webview.windows:
            webview.windows[0].destroy()

    def run(self):
        print("🚀 Starting Min2Tray PyWebView Demo...")

        self.create_webview()

        self.setup_tray_integration()

        class Api:
            def __init__(self, app_instance):
                self.app = app_instance

            def minimize_window(self):
                if hasattr(self.app, 'tray_app') and self.app.tray_app and self.app.tray_app.window_manager:
                    self.app.tray_app.window_manager.hide()
                    print("🔽 Window hidden to tray")

            def show_info(self):
                print("📋 This is an integration demo of PyWebView + Min2Tray")
                return "Info has been displayed in the console"

        webview.start(Api(self), debug=True)


def main():
    print("=" * 60)
    print("🎯 Min2Tray PyWebView Demo")
    print("=" * 60)
    print("📝 This demo shows how to use the pywebview library with min2tray")
    print("🔧 Features:")
    print("   • Create modern web UI with PyWebView")
    print("   • Min2Tray provides system tray and hotkey functionality")
    print("   • Global hotkey Ctrl+Alt+h to control window show/hide")
    print("   • Supports tray icon interaction")
    print("   • Uses custom tray icon (assets/tray.png)")
    print("=" * 60)

    try:
        app = WebViewTrayApp()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 User interrupted, exiting...")
    except Exception as e:
        print(f"❌ Error during runtime: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
