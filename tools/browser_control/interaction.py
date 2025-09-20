"""Browser interaction placeholders for clicking and form editing."""
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def browser_click(label: str) -> Dict[str, str]:
    """Click a button or element identified by accessible label text."""
    if not label:
        raise ValueError("label is required")
    return not_implemented(
        feature="browser_click",
        integration_hint=(
            "Leverage Playwright MCP or Chrome accessibility tree to find elements by label and click."
        ),
    )


def browser_fill_form(field_label: str, value: str) -> Dict[str, str]:
    """Fill a form field identified by label text."""
    if not field_label:
        raise ValueError("field_label is required")
    return not_implemented(
        feature="browser_fill_form",
        integration_hint=(
            "Implement Playwright MCP routines to find inputs by label and populate values, including focus management."
        ),
    )


def browser_submit_form(form_label: str) -> Dict[str, str]:
    """Submit a form by name or button label."""
    if not form_label:
        raise ValueError("form_label is required")
    return not_implemented(
        feature="browser_submit_form",
        integration_hint="Use Playwright MCP to trigger form submissions or synthesize Enter key events.",
    )


def browser_copy_text(selector: str) -> Dict[str, str]:
    """Copy text from the page given a selector hint."""
    if not selector:
        raise ValueError("selector is required")
    return not_implemented(
        feature="browser_copy_text",
        integration_hint=(
            "Adopt query selector support through Playwright evaluate calls or Chrome's accessibility API."
        ),
    )


def browser_paste_text(selector: str, text: str) -> Dict[str, str]:
    """Paste provided text into an input control located by selector hint."""
    if not selector:
        raise ValueError("selector is required")
    if text is None:
        raise ValueError("text is required")
    return not_implemented(
        feature="browser_paste_text",
        integration_hint="Use clipboard automation or programmatic value assignment via Playwright.",
    )


class BrowserInteractionToolkit(Toolkit):
    """Toolkit describing desired browser interaction primitives."""

    def __init__(self) -> None:
        super().__init__(name="browser_interaction")
        self.register(browser_click)
        self.register(browser_fill_form)
        self.register(browser_submit_form)
        self.register(browser_copy_text)
        self.register(browser_paste_text)

    def instructions(self) -> str:
        return (
            "Interaction tools identify UI automation work. Implement them using Playwright MCP or AppleScript-based DOM access."
        )


BROWSER_INTERACTION_TOOLKIT = BrowserInteractionToolkit()

__all__ = [
    "BROWSER_INTERACTION_TOOLKIT",
    "BrowserInteractionToolkit",
]
