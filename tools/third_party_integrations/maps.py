"""Maps integrations placeholders."""
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def maps_get_directions(origin: str, destination: str, mode: str = "driving") -> Dict[str, str]:
    """Get directions between two points."""
    if not origin:
        raise ValueError("origin is required")
    if not destination:
        raise ValueError("destination is required")
    return not_implemented(
        feature="maps_get_directions",
        integration_hint="Call Google Maps Directions API and include travel mode options.",
    )


def maps_eta(origin: str, destination: str, mode: str = "driving") -> Dict[str, str]:
    """Get estimated travel time."""
    if not origin:
        raise ValueError("origin is required")
    if not destination:
        raise ValueError("destination is required")
    return not_implemented(
        feature="maps_eta",
        integration_hint="Use Google Maps Distance Matrix API to retrieve ETAs and delays.",
    )


class MapsToolkit(Toolkit):
    """Toolkit for mapping helpers."""

    def __init__(self) -> None:
        super().__init__(name="maps")
        self.register(maps_get_directions)
        self.register(maps_eta)

    def instructions(self) -> str:
        return "Maps tooling depends on Google Maps APIs and appropriate billing configuration."


MAPS_TOOLKIT = MapsToolkit()

__all__ = ["MAPS_TOOLKIT", "MapsToolkit"]
