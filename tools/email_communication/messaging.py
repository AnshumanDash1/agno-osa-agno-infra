"""Placeholder messaging integrations (Slack, Teams, Discord, SMS, WhatsApp)."""
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def comm_read_channel(platform: str, channel: str) -> Dict[str, str]:
    """Read recent messages from a workspace or group channel."""
    if not platform:
        raise ValueError("platform is required")
    if not channel:
        raise ValueError("channel is required")
    return not_implemented(
        feature="comm_read_channel",
        integration_hint=(
            f"Connect to the {platform} API or automate its desktop app to fetch channel history "
            f"for '{channel}'."
        ),
    )


def comm_send_channel(platform: str, channel: str, message: str) -> Dict[str, str]:
    """Send a message to a workspace or group channel."""
    if not platform:
        raise ValueError("platform is required")
    if not channel:
        raise ValueError("channel is required")
    if not message:
        raise ValueError("message is required")
    return not_implemented(
        feature="comm_send_channel",
        integration_hint=(
            f"Use the {platform} SDK or desktop automation to deliver channel posts to '{channel}'."
        ),
    )


def comm_read_direct(platform: str, participant: str) -> Dict[str, str]:
    """Read direct or private messages with a single participant."""
    if not platform:
        raise ValueError("platform is required")
    if not participant:
        raise ValueError("participant is required")
    return not_implemented(
        feature="comm_read_direct",
        integration_hint=(
            f"Implement authenticated access to {platform} DM APIs or automate screen capture for {participant}."
        ),
    )


def comm_send_direct(platform: str, participant: str, message: str) -> Dict[str, str]:
    """Send a direct message through the specified platform."""
    if not platform:
        raise ValueError("platform is required")
    if not participant:
        raise ValueError("participant is required")
    if not message:
        raise ValueError("message is required")
    return not_implemented(
        feature="comm_send_direct",
        integration_hint=(
            f"Authenticate with the {platform} DM API or use UI automation to message {participant}."
        ),
    )


class MessagingToolkit(Toolkit):
    """Toolkit capturing the messaging integrations roadmap."""

    def __init__(self) -> None:
        super().__init__(name="messaging")
        self.register(comm_read_channel)
        self.register(comm_send_channel)
        self.register(comm_read_direct)
        self.register(comm_send_direct)

    def instructions(self) -> str:
        return (
            "These tools express the desired messaging coverage (Slack, Teams, Discord, SMS, WhatsApp). "
            "They currently surface integration requirements instead of performing live actions."
        )


MESSAGING_TOOLKIT = MessagingToolkit()

__all__ = [
    "MessagingToolkit",
    "MESSAGING_TOOLKIT",
    "comm_read_channel",
    "comm_send_channel",
    "comm_read_direct",
    "comm_send_direct",
]
