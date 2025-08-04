# min2tray

Minimize any Windows program to the system tray.

## Description

`min2tray` is a utility that allows you to minimize any Windows application to the system tray instead of the taskbar. This helps keep your desktop clean while still being able to quickly access your applications.

## Features

-  Minimize any Windows application to system tray
-  Global hotkey support for quick toggle
-  Custom tray icon support
-  Start applications minimized
-  Lightweight and efficient
-  Simple command-line interface

## Installation

### Using pipx

```bash
pipx install min2tray
```

### Using uv (recommended)

```bash
# Install from source
git clone https://github.com/gzj/min2tray
cd min2tray
uv sync
```

## Usage

```bash
min2tray -c "notepad.exe" -w "Untitled - Notepad" -k "<ctrl>+<alt>+n" -m
```

### Command Line Options

- `-c, --command`: The command to start the application
- `-w, --window_title`: Title of the window to minimize to tray
- `-i, --icon_image`: Path to custom tray icon image (optional)
- `-k, --hotkey`: Global hotkey combination (e.g., "<ctrl>+<alt>+n")
- `-m, --start_minimized`: Start the application minimized to tray

### Example Usage

```bash
# Minimize Notepad with Ctrl+Alt+N hotkey
min2tray -c "notepad.exe" -w "Untitled - Notepad" -k "<ctrl>+<alt>+n"

# Start Calculator minimized with custom icon
min2tray -c "calc.exe" -w "Calculator" -i "calc_icon.png" -m

# Minimize Alacritty terminal
min2tray -c "alacritty.exe --working-directory . -t alacritty" -w "alacritty" -i "icon.png" -k "<ctrl>+<alt>+a"
```

### Hotkey Combinations

Hotkey combinations can include:

- `<ctrl>`, `<alt>`, `<shift>`
- Any letter or number
- Function keys (`<f1>`, `<f2>`, etc.)

Examples: `<ctrl>+<alt>+h`, `<shift>+<f1>`, `<ctrl>+<shift>+x`

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/gzj/min2tray
cd min2tray

# Install dependencies
uv sync

# Run the application
uv run min2tray --help
```

### Code Quality

```bash
# Format code
uv run black .

# Check formatting (without making changes)
uv run black --check .

# Sort imports
uv run isort .

# Check import sorting  
uv run isort --check-only .

# Lint code
uv run flake8 min2tray.py

# Type checking
uv run mypy min2tray.py --ignore-missing-imports

# Run tests
uv run pytest -v
```

### Building

```bash
# Build package
uv build

# Install development dependencies
uv sync

# Install production dependencies only
uv sync --no-dev

# Clean build artifacts
uv run python -c "import shutil; import os; [shutil.rmtree(d, ignore_errors=True) for d in ['build', 'dist', '__pycache__', '.pytest_cache', '.mypy_cache'] if os.path.exists(d)]"

# Run example
uv run min2tray -c "notepad.exe" -w "Untitled - Notepad" -k "<ctrl>+<alt>+n" -m
```

## Requirements

- Windows OS
- Python 3.9+
- Dependencies (automatically installed):
  - pystray
  - pynput  
  - Pillow
  - pywin32

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please file an issue on GitHub.
