from agno.agent import Agent
from agno.models.google import Gemini
from agno.os import AgentOS
from dotenv import load_dotenv
from agno.models.ollama import Ollama

from computer_use_tool import (
    list_recent_emails_tool as list_recent_emails,
    open_chrome_url_tool as open_chrome_url,
    read_email_body_tool as read_email_body,
)

# model=Ollama(id="llama3.2:1b"),
# model=Gemini(id="gemini-2.0-flash-lite"),
load_dotenv()

assistant = Agent(
    name="Assistant",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=["""
    You are a helpful AI assistant who controls the user's browser and inbox.

    ## URL Handling
    Always provide fully qualified URLs starting with https://. Infer and correct malformed URLs before using `open_chrome_url`.

    ## Gmail Workflow
    1. Call `open_chrome_url` with https://mail.google.com to ensure Gmail is active when needed.
    2. Use `list_recent_emails(limit=...)` to provide subjects, senders, snippets, and include the `thread_id` so the user can choose a message.
    3. When the user requests details, call `read_email_body(thread_id=...)` with the selected identifier. Mention that the result corresponds to the Gmail thread and relay the message body clearly.
    4. If Gmail is not ready or requires login, inform the user and pause.

    ## Searches
    When users ask for general information, infer whether they want to open a site or perform a Google search. For searches, visit https://www.google.de/search?q=QUERY with spaces replaced by '+'.
    """],
    tools=[open_chrome_url, list_recent_emails, read_email_body],
    markdown=True,
)

test_assistant = Agent(
    name="Assistant",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=["You are a helpful assistant"],
    markdown=True,
)

agent_os = AgentOS(
    os_id="my-first-os",
    description="My first AgentOS",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="my_os:app", reload=True)
