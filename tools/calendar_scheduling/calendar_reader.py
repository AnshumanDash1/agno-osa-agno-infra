"""Calendar reading and scheduling placeholders."""
from typing import Dict

from agno.tools import Toolkit

from tools.common import not_implemented


def calendar_list_events(timeframe: str = "today") -> Dict[str, str]:
    """List events for the requested timeframe (today/tomorrow/this week)."""
    if timeframe not in {"today", "tomorrow", "this_week"}:
        raise ValueError("timeframe must be 'today', 'tomorrow', or 'this_week'")
    return not_implemented(
        feature="calendar_list_events",
        integration_hint=(
            "Connect to Google Calendar API or automate the Calendar UI to extract upcoming meetings."
        ),
    )


def calendar_create_event(natural_language_request: str) -> Dict[str, str]:
    """Create an event from a natural language description."""
    if not natural_language_request:
        raise ValueError("natural_language_request is required")
    return not_implemented(
        feature="calendar_create_event",
        integration_hint=(
            "Use a natural language to structured event parser plus Calendar API insert calls."
        ),
    )


def calendar_reschedule_event(event_id: str, new_time: str) -> Dict[str, str]:
    """Reschedule an existing event to a new time."""
    if not event_id:
        raise ValueError("event_id is required")
    if not new_time:
        raise ValueError("new_time is required")
    return not_implemented(
        feature="calendar_reschedule_event",
        integration_hint="Call Calendar API events.patch with parsed RFC3339 timestamps.",
    )


def calendar_cancel_event(event_id: str) -> Dict[str, str]:
    """Cancel an existing event."""
    if not event_id:
        raise ValueError("event_id is required")
    return not_implemented(
        feature="calendar_cancel_event",
        integration_hint="Invoke Calendar API events.delete or automate UI cancellation.",
    )


def calendar_join_meeting(meeting_url: str) -> Dict[str, str]:
    """Open a video conference link from the calendar."""
    if not meeting_url:
        raise ValueError("meeting_url is required")
    return not_implemented(
        feature="calendar_join_meeting",
        integration_hint="Automate Chrome to open the meeting URL and handle pre-join dialogs.",
    )


def calendar_travel_time(event_id: str) -> Dict[str, str]:
    """Fetch travel time reminders linked to a calendar event."""
    if not event_id:
        raise ValueError("event_id is required")
    return not_implemented(
        feature="calendar_travel_time",
        integration_hint=(
            "Pull location metadata from the event and query Google Maps Distance Matrix API."
        ),
    )


class CalendarToolkit(Toolkit):
    """Calendar and scheduling automation placeholders."""

    def __init__(self) -> None:
        super().__init__(name="calendar")
        self.register(calendar_list_events)
        self.register(calendar_create_event)
        self.register(calendar_reschedule_event)
        self.register(calendar_cancel_event)
        self.register(calendar_join_meeting)
        self.register(calendar_travel_time)

    def instructions(self) -> str:
        return (
            "Calendar tooling summarizes required API permissions (Google Calendar, Maps) "
            "and highlights where UI automation may fill gaps."
        )


CALENDAR_TOOLKIT = CalendarToolkit()

__all__ = ["CalendarToolkit", "CALENDAR_TOOLKIT"]
