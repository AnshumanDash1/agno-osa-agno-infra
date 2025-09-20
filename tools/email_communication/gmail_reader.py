"""Gmail reading helpers built on top of the existing Chrome automation."""
from typing import Any, Dict, List

from agno.tools import Toolkit

from computer_use_tool import (
    GMAIL_BASE_URL,
    list_recent_emails,
    open_chrome_url,
    read_email_body,
)


def gmail_list_unread(limit: int = 5) -> Dict[str, Any]:
    """Return unread Gmail threads with metadata for quick scanning."""
    if limit <= 0:
        raise ValueError("limit must be positive")
    open_chrome_url(url=GMAIL_BASE_URL)
    emails: List[Dict[str, Any]] = list_recent_emails(limit=limit)
    return {"threads": emails, "count": len(emails)}


def gmail_read_summaries(limit: int = 3) -> Dict[str, Any]:
    """Produce lightweight summaries of recent Gmail threads."""
    if limit <= 0:
        raise ValueError("limit must be positive")
    open_chrome_url(url=GMAIL_BASE_URL)
    emails = list_recent_emails(limit=limit)
    summaries = []
    for entry in emails:
        subject = entry.get("subject", "(no subject)")
        sender = entry.get("sender", "Unknown sender")
        snippet = entry.get("snippet", "").strip()
        summaries.append(
            {
                "thread_id": entry.get("thread_id"),
                "summary": f"{sender}: {subject} — {snippet}",
            }
        )
    return {"summaries": summaries, "count": len(summaries)}


def gmail_open_thread(thread_id: str, message_index: int = 0) -> Dict[str, Any]:
    """Open a Gmail thread by id and return the requested message payload."""
    if not thread_id:
        raise ValueError("thread_id is required")
    open_chrome_url(url=GMAIL_BASE_URL)
    message = read_email_body(thread_id=thread_id, message_index=message_index)
    return {"thread": message}


class GmailReadingToolkit(Toolkit):
    """Toolkit exposing read-only Gmail utilities."""

    def __init__(self) -> None:
        super().__init__(name="gmail_reading")
        self.register(gmail_list_unread)
        self.register(gmail_read_summaries)
        self.register(gmail_open_thread)

    def instructions(self) -> str:
        return (
            "Use these tools to keep the Gmail inbox in focus, list unread messages, "
            "and surface conversational context when a user requests email details."
        )


GMAIL_READING_TOOLKIT = GmailReadingToolkit()

__all__ = [
    "GmailReadingToolkit",
    "GMAIL_READING_TOOLKIT",
    "gmail_list_unread",
    "gmail_read_summaries",
    "gmail_open_thread",
]
