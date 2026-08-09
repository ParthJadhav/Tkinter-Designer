"""Dependency boundary for the optional desktop entry point."""

import sys


def load_app():
    from .app import main

    return main


def main():
    try:
        app_main = load_app()
    except ModuleNotFoundError as exc:
        if exc.name not in {"tkinter", "_tkinter"}:
            raise
        print(
            "error: Tkinter is not available in this Python installation. "
            "Install Python with Tk support (for example, python3-tk on Linux) "
            "and recreate the virtual environment.",
            file=sys.stderr,
        )
        return 1
    return app_main()


if __name__ == "__main__":
    raise SystemExit(main())
