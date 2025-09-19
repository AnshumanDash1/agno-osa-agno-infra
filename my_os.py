from agno.agent import Agent
from agno.models.google import Gemini
from agno.os import AgentOS
from dotenv import load_dotenv
from computer_use_tool import open_chrome_url, get_unread_emails
from agno.models.ollama import Ollama

load_dotenv()

# model=Ollama(id="llama3.2:1b"),
# model=Gemini(id="gemini-2.0-flash-lite"),

assistant = Agent(
    name="Assistant",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=["""
    You are a helpful AI assistant who takes user querys and controls the web browser for them.
    For any urls, make sure to put https:// before the url. 
    Make sure the argument you give is an actual url.
    If the user gives a non-working url, infer the meaning and make it into an actual url.
    Example:
    User: Open youtube.com
    Assistant: Call tool with argument: https://youtube.com
    
    User: Open htt;/youtube.co
    Assistant: Call tool with argument: https://youtube.com
    
    You should infer the meaning instead of needing an exact match.
    
    ## Searching
    If the user wants to search for something on google, use the url:
    https://www.google.de/search?q=THEIR_SEARCH_QUERY_HERE
    
    This will go to the results page for the google search. Make sure you infer the user's desire for search.
    
    Example:
    Sear fo netf;ix
    Infer -> search for netflix -> the user needs netflix.com, not a google search for netflix
    go to https://netflix.com
    
    Example:
    Searchh fir infornatin on gmos
    Infer -> User wants information on gmos -> do a google search for gmo's
    go to https://www.google.de/search?q=facts+on+genetically+modified+organisms
    
    Example: 
    Wha arw som ni ce plaves to eat around Aloharetta?
    Infer -> User wants information on restaurants near a specific location -> do a google search for restaurants near me
    go to https://www.google.de/search?q=restaurants+in+alpharetta
    
    
    """],
    tools=[open_chrome_url, get_unread_emails],
    markdown=True,
)

test_assistant = Agent(
    name="Assistant",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=["You are a helpful assistant"],
    markdown = True,
)

# assistant.print_response("testing...")
agent_os = AgentOS(
    os_id="my-first-os",
    description="My first AgentOS",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="my_os:app", reload=True)
