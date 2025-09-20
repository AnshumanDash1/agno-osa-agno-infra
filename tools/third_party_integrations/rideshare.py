"""Ride share integrations placeholders."""
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def rideshare_order(service: str, pickup: str, dropoff: str) -> Dict[str, str]:
    """Order a ride on Uber or Lyft."""
    if not service:
        raise ValueError("service is required")
    if not pickup:
        raise ValueError("pickup is required")
    if not dropoff:
        raise ValueError("dropoff is required")
    return not_implemented(
        feature="rideshare_order",
        integration_hint=(
            f"Integrate with the {service} API (OAuth scopes) or automate mobile/desktop flows for ride booking."
        ),
    )


def rideshare_status(service: str, ride_id: str) -> Dict[str, str]:
    """Check ride status."""
    if not service:
        raise ValueError("service is required")
    if not ride_id:
        raise ValueError("ride_id is required")
    return not_implemented(
        feature="rideshare_status",
        integration_hint=f"Use {service} APIs to poll ride status and driver ETA.",
    )


class RideShareToolkit(Toolkit):
    """Toolkit summarizing rideshare integrations."""

    def __init__(self) -> None:
        super().__init__(name="rideshare")
        self.register(rideshare_order)
        self.register(rideshare_status)

    def instructions(self) -> str:
        return "Rideshare tooling requires OAuth credentials and compliance with platform policies."


RIDESHARE_TOOLKIT = RideShareToolkit()

__all__ = ["RIDESHARE_TOOLKIT", "RideShareToolkit"]
