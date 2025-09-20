"""Browser control toolkits."""

from .navigation import BROWSER_NAVIGATION_TOOLKIT, BrowserNavigationToolkit
from .interaction import BROWSER_INTERACTION_TOOLKIT, BrowserInteractionToolkit
from .advanced import BROWSER_ADVANCED_TOOLKIT, BrowserAdvancedToolkit

__all__ = [
    "BROWSER_NAVIGATION_TOOLKIT",
    "BrowserNavigationToolkit",
    "BROWSER_INTERACTION_TOOLKIT",
    "BrowserInteractionToolkit",
    "BROWSER_ADVANCED_TOOLKIT",
    "BrowserAdvancedToolkit",
]
