# min2tray

min2tray is a program designed to minimize the window of a running program to the system tray and offer a shortcut for easy access. (Windows only, current version))

## Features

- Minimize running program windows to the system tray with a custom icon.
- Restore program windows from the system tray using a keyboard shortcut.

## Quick Start

The following command provides a quick demonstration of how to utilize `min2tray` for minimizing a running program window to the system tray, all while configuring a keyboard shortcut and specifying a custom icon:

```
min2tray -c="alacritty.exe --working-directory . -t  alacritty"  -w="alacritty"  -i="icon.png" -k='<ctrl>+<alt>+a'
```

In this example:
- `-c` specifies the command to execute the program (`alacritty.exe --working-directory . -t alacritty`).
- `-w` identifies the program window by its title (`alacritty`).
- `-i` designates a custom icon (`icon.png`).
- `-k` sets the keyboard shortcut to `<ctrl>+<alt>+a`.

Feel free to customize the command, window title, icon, and keyboard shortcut to match your specific application's needs. This command snippet exemplifies how to enhance the usability and accessibility of your program with `min2tray`.
