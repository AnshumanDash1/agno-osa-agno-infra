"""Browser navigation helpers leveraging Chrome AppleScript bridge."""
from typing import Dict

from agno.tools import Toolkit

from computer_use_tool import execute_javascript, open_chrome_url


def browser_open_url(url: str) -> Dict[str, str]:
    """Open a fully-qualified URL in Chrome and focus the tab."""
    if not url or not url.startswith("http"):
        raise ValueError("Provide a fully-qualified URL starting with http or https")
    open_chrome_url(url=url)
    return {"status": "ok", "url": url}


def browser_google_search(query: str, market: str = "us") -> Dict[str, str]:
    """Open a Google search for the provided query."""
    if not query:
        raise ValueError("query is required")
    domain = "google.com" if market == "us" else f"google.{market}"
    encoded = query.replace(" ", "+")
    url = f"https://www.{domain}/search?q={encoded}"
    open_chrome_url(url=url)
    return {"status": "ok", "url": url}


def browser_go_back() -> Dict[str, str]:
    """Navigate back in the active Chrome tab history."""
    execute_javascript("window.history.back(); return 'back';")
    return {"status": "ok", "action": "back"}


def browser_go_forward() -> Dict[str, str]:
    """Navigate forward in the active Chrome tab history."""
    execute_javascript("window.history.forward(); return 'forward';")
    return {"status": "ok", "action": "forward"}


def browser_scroll(direction: str = "down", amount: int = 600) -> Dict[str, str]:
    """Scroll the current page by the requested amount."""
    if direction not in {"up", "down"}:
        raise ValueError("direction must be 'up' or 'down'")
    delta = amount if direction == "down" else -amount
    execute_javascript(f"window.scrollBy(0, {delta}); return window.scrollY.toString();")
    return {"status": "ok", "direction": direction, "amount": amount}


class BrowserNavigationToolkit(Toolkit):
    """Toolkit for simple browser navigation primitives."""

    def __init__(self) -> None:
        super().__init__(name="browser_navigation")
        self.register(browser_open_url)
        self.register(browser_google_search)
        self.register(browser_go_back)
        self.register(browser_go_forward)
        self.register(browser_scroll)

    def instructions(self) -> str:
        return (
            "Use these navigation primitives to load pages, perform searches, and adjust scroll "
            "position without scripting complex flows."
        )


BROWSER_NAVIGATION_TOOLKIT = BrowserNavigationToolkit()

__all__ = [
    "BROWSER_NAVIGATION_TOOLKIT",
    "BrowserNavigationToolkit",
    "browser_open_url",
    "browser_google_search",
    "browser_go_back",
    "browser_go_forward",
    "browser_scroll",
]
