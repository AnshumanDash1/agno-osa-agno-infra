"""Application control helpers leveraging macOS automation."""
import subprocess
from typing import Dict

from agno.tools import Toolkit

from computer_use_tool import run_applescript


def system_open_app(app_name: str) -> Dict[str, str]:
    """Open an application by name."""
    if not app_name:
        raise ValueError("app_name is required")
    subprocess.run(["open", "-a", app_name], check=False)
    return {"status": "ok", "action": "open", "app": app_name}


def system_close_app(app_name: str) -> Dict[str, str]:
    """Close an application by name."""
    if not app_name:
        raise ValueError("app_name is required")
    script = f'tell application "{app_name}" to quit'
    try:
        run_applescript(script)
        status = "ok"
    except RuntimeError as exc:
        status = "error"
        return {"status": status, "app": app_name, "error": str(exc)}
    return {"status": status, "action": "close", "app": app_name}


def system_switch_window(app_name: str) -> Dict[str, str]:
    """Bring an application's front window to focus."""
    if not app_name:
        raise ValueError("app_name is required")
    script = f'tell application "{app_name}" to activate'
    run_applescript(script)
    return {"status": "ok", "action": "activate", "app": app_name}


class AppControlToolkit(Toolkit):
    """Toolkit for foreground application control."""

    def __init__(self) -> None:
        super().__init__(name="system_app_control")
        self.register(system_open_app)
        self.register(system_close_app)
        self.register(system_switch_window)

    def instructions(self) -> str:
        return "Use app control tools to open, close, or focus macOS applications via AppleScript bridge."


APP_CONTROL_TOOLKIT = AppControlToolkit()

__all__ = [
    "APP_CONTROL_TOOLKIT",
    "AppControlToolkit",
]
