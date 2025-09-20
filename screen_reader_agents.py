"""Specialized agents and team for the AI screen reader tool library."""
from __future__ import annotations

from typing import Dict, List

from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team

from tools import (
    ACCESSIBILITY_TOOLKIT,
    AGENTIC_INFRA_TOOLKIT,
    APP_CONTROL_TOOLKIT,
    BANKING_TOOLKIT,
    BROWSER_ADVANCED_TOOLKIT,
    BROWSER_INTERACTION_TOOLKIT,
    BROWSER_NAVIGATION_TOOLKIT,
    CALENDAR_TOOLKIT,
    FILE_SYSTEM_TOOLKIT,
    FOOD_DELIVERY_TOOLKIT,
    GMAIL_MANAGEMENT_TOOLKIT,
    GMAIL_READING_TOOLKIT,
    GOOGLE_WORKSPACE_TOOLKIT,
    INPUT_EMULATION_TOOLKIT,
    MAPS_TOOLKIT,
    MESSAGING_TOOLKIT,
    RIDESHARE_TOOLKIT,
    SYSTEM_QUERY_TOOLKIT,
    ASSISTIVE_INTELLIGENCE_TOOLKIT,
)

SPECIALIST_MODEL = Gemini(id="gemini-2.0-flash-lite")
VOICE_MODEL = Gemini(id="gemini-2.0-flash")


def build_screen_reader_agents() -> Dict[str, Agent]:
    """Construct domain-specific agents grouped by capability."""

    voice_agent = Agent(
        name="ScreenReaderVoiceAgent",
        model=VOICE_MODEL,
        instructions=[
            "You coordinate the AI screen reader experience.",
            "Gather intent, decide which specialist agent should respond, and summarize outcomes for the user.",
            "Call out when a capability is a roadmap item rather than a live integration.",
        ],
        tools=[AGENTIC_INFRA_TOOLKIT],
        markdown=True,
    )

    email_reader = Agent(
        name="EmailReader",
        model=SPECIALIST_MODEL,
        instructions=[
            "Summarize Gmail inbox state using the provided tools.",
            "Return thread identifiers with each response to enable follow-up actions.",
        ],
        tools=[GMAIL_READING_TOOLKIT],
        markdown=True,
    )

    email_manager = Agent(
        name="EmailManager",
        model=SPECIALIST_MODEL,
        instructions=[
            "Explain what Gmail management automations are pending and how to enable them.",
            "Do not claim to send email today—surface integration requirements instead.",
        ],
        tools=[GMAIL_MANAGEMENT_TOOLKIT],
        markdown=True,
    )

    messaging_agent = Agent(
        name="MessagingAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Describe next steps for connecting Slack/Teams/Discord/SMS automation.",
            "When asked to send or read messages, disclose the current placeholder response.",
        ],
        tools=[MESSAGING_TOOLKIT],
        markdown=True,
    )

    calendar_agent = Agent(
        name="CalendarAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Respond with calendar availability insights and note missing API credentials.",
        ],
        tools=[CALENDAR_TOOLKIT],
        markdown=True,
    )

    browser_navigation_agent = Agent(
        name="BrowserNavigationAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Handle navigation-only actions such as opening URLs, searching, and scrolling.",
        ],
        tools=[BROWSER_NAVIGATION_TOOLKIT],
        markdown=True,
    )

    browser_interaction_agent = Agent(
        name="BrowserInteractionAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Surface the roadmap for interactive browser automation (click, fill, submit).",
        ],
        tools=[BROWSER_INTERACTION_TOOLKIT],
        markdown=True,
    )

    browser_advanced_agent = Agent(
        name="BrowserAdvancedAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Manage advanced automation requests like summaries or table extraction.",
        ],
        tools=[BROWSER_ADVANCED_TOOLKIT],
        markdown=True,
    )

    workspace_agent = Agent(
        name="WorkspaceAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Discuss Docs/Sheets accessibility and editing operations, highlighting API needs.",
        ],
        tools=[GOOGLE_WORKSPACE_TOOLKIT],
        markdown=True,
    )

    file_system_agent = Agent(
        name="FileSystemAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Read local files when requested and advise on PDF/OCR prerequisites.",
            "Never exfiltrate secrets—respect the requested paths only.",
        ],
        tools=[FILE_SYSTEM_TOOLKIT],
        markdown=True,
    )

    system_control_agent = Agent(
        name="SystemControlAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Open, close, or focus applications and answer basic system status questions.",
            "Mention when deeper HID emulation is not implemented yet.",
        ],
        tools=[APP_CONTROL_TOOLKIT, INPUT_EMULATION_TOOLKIT, SYSTEM_QUERY_TOOLKIT],
        markdown=True,
    )

    assistive_agent = Agent(
        name="AssistiveIntelligenceAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Offer summaries and Q&A plans, noting storage and RAG requirements.",
        ],
        tools=[ASSISTIVE_INTELLIGENCE_TOOLKIT],
        markdown=True,
    )

    maps_agent = Agent(
        name="MapsAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Describe mapping capabilities and API keys needed for directions and ETAs.",
        ],
        tools=[MAPS_TOOLKIT],
        markdown=True,
    )

    rideshare_agent = Agent(
        name="RideShareAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Document the steps required to connect Uber/Lyft integrations before booking rides.",
        ],
        tools=[RIDESHARE_TOOLKIT],
        markdown=True,
    )

    food_agent = Agent(
        name="FoodDeliveryAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Capture food delivery automation requirements and limitations.",
        ],
        tools=[FOOD_DELIVERY_TOOLKIT],
        markdown=True,
    )

    banking_agent = Agent(
        name="BankingAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Explain security considerations for banking automations before enabling them.",
        ],
        tools=[BANKING_TOOLKIT],
        markdown=True,
    )

    accessibility_agent = Agent(
        name="AccessibilityAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Lay out OCR, image understanding, and real-time narration options.",
        ],
        tools=[ACCESSIBILITY_TOOLKIT],
        markdown=True,
    )

    infrastructure_agent = Agent(
        name="InfrastructureAgent",
        model=SPECIALIST_MODEL,
        instructions=[
            "Coordinate delegation patterns, token budgeting, and recovery plans for the platform.",
        ],
        tools=[AGENTIC_INFRA_TOOLKIT],
        markdown=True,
    )

    return {
        "voice_agent": voice_agent,
        "email_reader": email_reader,
        "email_manager": email_manager,
        "messaging": messaging_agent,
        "calendar": calendar_agent,
        "browser_navigation": browser_navigation_agent,
        "browser_interaction": browser_interaction_agent,
        "browser_advanced": browser_advanced_agent,
        "workspace": workspace_agent,
        "file_system": file_system_agent,
        "system_control": system_control_agent,
        "assistive": assistive_agent,
        "maps": maps_agent,
        "rideshare": rideshare_agent,
        "food": food_agent,
        "banking": banking_agent,
        "accessibility": accessibility_agent,
        "infrastructure": infrastructure_agent,
    }


def build_screen_reader_team(agent_map: Dict[str, Agent]) -> Team:
    """Create the coordinating team that bundles the specialist agents."""

    members: List[Agent] = [
        agent_map["voice_agent"],
        agent_map["email_reader"],
        agent_map["email_manager"],
        agent_map["messaging"],
        agent_map["calendar"],
        agent_map["browser_navigation"],
        agent_map["browser_interaction"],
        agent_map["browser_advanced"],
        agent_map["workspace"],
        agent_map["file_system"],
        agent_map["system_control"],
        agent_map["assistive"],
        agent_map["maps"],
        agent_map["rideshare"],
        agent_map["food"],
        agent_map["banking"],
        agent_map["accessibility"],
        agent_map["infrastructure"],
    ]

    return Team(
        members=members,
        model=VOICE_MODEL,
        name="ScreenReaderVoiceTeam",
        instructions=[
            "You are the voice-facing orchestrator for the screen reader experience.",
            "Route requests to the appropriate specialist agent and weave their responses into a coherent reply.",
            "Be explicit about missing integrations so developers know what to enable next.",
        ],
        markdown=True,
        add_name_to_context=True,
    )


SCREEN_READER_AGENTS = build_screen_reader_agents()
SCREEN_READER_TEAM = build_screen_reader_team(SCREEN_READER_AGENTS)

__all__ = ["SCREEN_READER_AGENTS", "SCREEN_READER_TEAM"]
