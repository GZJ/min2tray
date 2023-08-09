from setuptools import setup

setup(
    name="min2tray",
    version="0.1.0",
    url=[
        "https://github.com/gzj/min2tray", 
        "https://git.sr.ht/~gzj/min2tray"
    ],
    author="gzj",
    author_email="gzj00@outlook.com",
    description="Minimize program to system tray",
    long_description="Minimize program to system tray",
    long_description_content_type="text/markdown",
    py_modules=["min2tray"],
    install_requires=["pystray", "pynput", "Pillow"],
    entry_points={
        "console_scripts": [
            "min2tray = min2tray:main",
        ],
    },
)
