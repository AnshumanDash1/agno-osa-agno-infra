"""Food delivery integrations placeholders."""
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def food_order(service: str, restaurant: str, items: str) -> Dict[str, str]:
    """Order food via delivery services."""
    if not service:
        raise ValueError("service is required")
    if not restaurant:
        raise ValueError("restaurant is required")
    if not items:
        raise ValueError("items is required")
    return not_implemented(
        feature="food_order",
        integration_hint=(
            f"Integrate with {service} ordering APIs or automate the checkout flow via browser scripting."
        ),
    )


def food_reorder(service: str, order_id: str) -> Dict[str, str]:
    """Reorder a previous meal."""
    if not service:
        raise ValueError("service is required")
    if not order_id:
        raise ValueError("order_id is required")
    return not_implemented(
        feature="food_reorder",
        integration_hint=f"Use {service} reorder endpoints or saved carts via automation.",
    )


class FoodDeliveryToolkit(Toolkit):
    """Toolkit for food delivery automation."""

    def __init__(self) -> None:
        super().__init__(name="food_delivery")
        self.register(food_order)
        self.register(food_reorder)

    def instructions(self) -> str:
        return "Food delivery tooling depends on service-specific APIs and authentication tokens."


FOOD_DELIVERY_TOOLKIT = FoodDeliveryToolkit()

__all__ = ["FOOD_DELIVERY_TOOLKIT", "FoodDeliveryToolkit"]
