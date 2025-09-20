"""Keyboard and mouse emulation placeholders."""
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def system_type_text(text: str) -> Dict[str, str]:
    """Type text via keyboard emulation."""
    if text is None:
        raise ValueError("text is required")
    return not_implemented(
        feature="system_type_text",
        integration_hint="Use AppleScript keystroke or a HID automation library to type characters.",
    )


def system_click_target(target: str) -> Dict[str, str]:
    """Click on a UI element by description."""
    if not target:
        raise ValueError("target is required")
    return not_implemented(
        feature="system_click_target",
        integration_hint="Integrate with accessibility API or Playwright MCP for coordinate clicks.",
    )


class InputEmulationToolkit(Toolkit):
    """Toolkit capturing keyboard and mouse emulation roadmap."""

    def __init__(self) -> None:
        super().__init__(name="system_input_emulation")
        self.register(system_type_text)
        self.register(system_click_target)

    def instructions(self) -> str:
        return "These tools highlight the need for HID-level automation to emit keystrokes and clicks."


INPUT_EMULATION_TOOLKIT = InputEmulationToolkit()

__all__ = [
    "INPUT_EMULATION_TOOLKIT",
    "InputEmulationToolkit",
]
