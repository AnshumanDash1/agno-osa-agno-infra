"""Common helpers for screen reader toolkits."""
from typing import Dict


def not_implemented(feature: str, integration_hint: str) -> Dict[str, str]:
    """Return a consistent payload for unimplemented features."""
    return {
        "status": "not_implemented",
        "feature": feature,
        "details": (
            f"The capability '{feature}' is not implemented yet. {integration_hint} "
            "Configure the necessary integration or extend the toolkit to enable it."
        ),
    }
