"""System query helpers for status checks."""
import subprocess
from datetime import datetime
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def _read_battery_status() -> str:
    try:
        output = subprocess.check_output(["pmset", "-g", "batt"], text=True)
        return output.strip()
    except Exception as exc:  # pragma: no cover - platform dependent fallback
        return f"Unable to read battery information: {exc}"


def system_get_status(metric: str) -> Dict[str, str]:
    """Report system status like battery, wifi, time, or volume."""
    if not metric:
        raise ValueError("metric is required")
    metric = metric.lower()
    if metric == "time":
        return {
            "status": "ok",
            "metric": metric,
            "value": datetime.now().isoformat(timespec="seconds"),
        }
    if metric == "battery":
        return {
            "status": "ok",
            "metric": metric,
            "value": _read_battery_status(),
        }
    return not_implemented(
        feature=f"system_get_status:{metric}",
        integration_hint="Add platform-specific commands for Wi-Fi, volume, and notifications.",
    )


class SystemQueryToolkit(Toolkit):
    """Toolkit for system status checks."""

    def __init__(self) -> None:
        super().__init__(name="system_queries")
        self.register(system_get_status)

    def instructions(self) -> str:
        return "System queries currently support time and battery. Extend with Wi-Fi, notifications, and audio state."


SYSTEM_QUERY_TOOLKIT = SystemQueryToolkit()

__all__ = [
    "SYSTEM_QUERY_TOOLKIT",
    "SystemQueryToolkit",
]
