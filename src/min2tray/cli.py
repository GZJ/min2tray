import argparse
import sys
from .core import minimize_to_tray

def main():
    parser = argparse.ArgumentParser(description="Minimize window to system tray.")
    parser.add_argument("-c", "--command", metavar="", help="The process command.")
    parser.add_argument(
        "-w", "--window_title", metavar="", help="Title of the window to minimize."
    )
    parser.add_argument(
        "-i",
        "--icon_image",
        metavar="",
        help="The path to the icon image that will be displayed in the system tray.",
    )
    parser.add_argument(
        "-k",
        "--hotkey",
        metavar="",
        help="The hotkey combination to trigger the minimize action.",
    )
    parser.add_argument(
        "-m",
        "--start_minimized",
        action="store_true",
        help="Starts the application in a minimised state.",
    )

    args = parser.parse_args()

    if not args.window_title:
        print("Error: Window title is required")
        sys.exit(1)

    try:
        minimize_to_tray(
            window_title=args.window_title,
            command=args.command,
            icon_path=args.icon_image,
            hotkey=args.hotkey,
            start_hidden=args.start_minimized
        )
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
