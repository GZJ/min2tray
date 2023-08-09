import argparse
import atexit
import pystray
import win32gui
import win32con
import subprocess
import threading
import time
import os
import sys

from pynput import keyboard
from PIL import Image, ImageDraw

#----------------------------------- window ---------------------------------------------------
window_handle = None
is_window_visible = True

def hide_window(window_handle):
    win32gui.ShowWindow(window_handle, win32con.SW_HIDE)

def show_window(window_handle):
    x, y, width, height = window_rect = win32gui.GetWindowRect(window_handle)
    win32gui.SetWindowPos(window_handle, 0, x, y, width, height, win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
    
def get_window_handle(window_title):
    window_handle = win32gui.FindWindow(None, window_title)
    return window_handle

def init_window_handle(title):
    global window_handle
    window_title = title

    window_handle = get_window_handle(window_title)

def toggle_window_visibility():
    global is_window_visible
    if is_window_visible:
        hide_window(window_handle)
        is_window_visible = not is_window_visible
        print("Toggle window hiding")
    else:
        show_window(window_handle)
        is_window_visible = not is_window_visible
        print("Toggle window showing")

# ----------------------------------- subprocess ---------------------------------------------------
process = None

def run_cmd(cmd):
    global process
    process = subprocess.Popen(cmd)

    time.sleep(1)

def cmd_wait():
    while process.poll() is None:
        pass

    print(f"cmd over, return code: {process.returncode}")

# ----------------------------------- tray ---------------------------------------------------
icon = None

def create_default_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def iconRun(icon_image_path):

    global icon
    icon_image = None

    if icon_image_path:
        icon_image = Image.open(icon_image_path)
    else:
        icon_image = create_default_image(64, 64, 'black', 'white')


    icon = pystray.Icon(
        'test name',
        icon=icon_image,
        title="Example",
        menu=pystray.Menu(
            pystray.MenuItem(text="toggle_window_visibility",action=toggle_window_visibility,default=True),
            pystray.MenuItem("exit", lambda: (icon.stop(), process.terminate()))
        )
    )

    icon.run()

# ----------------------------------- hotkey ---------------------------------------------------
listener = None

def register_global_hotkey(key):
    global listener
    def for_canonical(f):
        return lambda k: f(listener.canonical(k))

    hotkey = keyboard.HotKey(
            keyboard.HotKey.parse(key),
            toggle_window_visibility)

    listener = keyboard.Listener(
                on_press=for_canonical(hotkey.press),
                on_release=for_canonical(hotkey.release))

    listener.start()

# ----------------------------------- main ---------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Minimize window to system tray.')
    parser.add_argument('-c', '--command', metavar='', help='The process command.')
    parser.add_argument('-w', '--window_title', metavar='', help='Title of the window to minimize.')
    parser.add_argument('-i', '--icon_image', metavar='', help='The path to the icon image that will be displayed in the system tray.')
    parser.add_argument('-k', '--hotkey', metavar='',  help='The hotkey combination to trigger the minimize action.')
    args = parser.parse_args()

    register_global_hotkey(args.hotkey)
    run_cmd(args.command)
    init_window_handle(args.window_title)

    thread_cmd = threading.Thread(target=cmd_wait)
    thread_icon = threading.Thread(target=iconRun, args=(args.icon_image,))

    thread_cmd.start()
    thread_icon.start()

    thread_cmd.join()
    icon.stop()
    listener.stop()

if __name__ == "__main__":
    main()
