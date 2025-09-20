"""Stubs for Gmail management actions pending deeper automation."""
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def gmail_compose_email(recipient: str, subject: str, body: str) -> Dict[str, str]:
    """Compose and send an email via Gmail (requires future API automation)."""
    if not recipient:
        raise ValueError("recipient is required")
    if not subject:
        raise ValueError("subject is required")
    if not body:
        raise ValueError("body is required")
    return not_implemented(
        feature="gmail_compose_email",
        integration_hint=(
            "Implement Chrome automation for the Gmail compose window or configure the "
            "Gmail API send scope."
        ),
    )


def gmail_search_inbox(query: str) -> Dict[str, str]:
    """Search Gmail for a query (sender, subject, or free text)."""
    if not query:
        raise ValueError("query is required")
    return not_implemented(
        feature="gmail_search_inbox",
        integration_hint="Use Gmail's search box automation or the Gmail API search endpoint.",
    )


def gmail_delete_thread(thread_id: str) -> Dict[str, str]:
    """Move a Gmail thread to trash."""
    if not thread_id:
        raise ValueError("thread_id is required")
    return not_implemented(
        feature="gmail_delete_thread",
        integration_hint="Drive Chrome keyboard shortcuts or Gmail API modify calls with trash label.",
    )


def gmail_archive_thread(thread_id: str) -> Dict[str, str]:
    """Archive a Gmail thread without deleting it."""
    if not thread_id:
        raise ValueError("thread_id is required")
    return not_implemented(
        feature="gmail_archive_thread",
        integration_hint="Use Gmail's archive button automation or apply the ARCHIVE label via API.",
    )


def gmail_mark_spam(thread_id: str) -> Dict[str, str]:
    """Mark a Gmail thread as spam."""
    if not thread_id:
        raise ValueError("thread_id is required")
    return not_implemented(
        feature="gmail_mark_spam",
        integration_hint="Invoke Gmail's spam action in the UI or Gmail API label modification.",
    )


class GmailManagementToolkit(Toolkit):
    """Toolkit exposing Gmail management placeholders awaiting automation."""

    def __init__(self) -> None:
        super().__init__(name="gmail_management")
        self.register(gmail_compose_email)
        self.register(gmail_search_inbox)
        self.register(gmail_delete_thread)
        self.register(gmail_archive_thread)
        self.register(gmail_mark_spam)

    def instructions(self) -> str:
        return (
            "These tools describe planned Gmail management flows. They currently report "
            "integration requirements so engineers can prioritize automation work."
        )


GMAIL_MANAGEMENT_TOOLKIT = GmailManagementToolkit()

__all__ = [
    "GmailManagementToolkit",
    "GMAIL_MANAGEMENT_TOOLKIT",
    "gmail_compose_email",
    "gmail_search_inbox",
    "gmail_delete_thread",
    "gmail_archive_thread",
    "gmail_mark_spam",
]
