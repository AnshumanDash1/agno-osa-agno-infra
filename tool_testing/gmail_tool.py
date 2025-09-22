from agno.agent import Agent
from agno.tools.gmail import GmailTools
from agno.models.google import Gemini
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    tools=[GmailTools()],
    instructions="You help the user interact with their gmail."
    )
agent.print_response("Show me my latest 5 unread emails", markdown=True)