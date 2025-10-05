from agno.agent import Agent
from agno.models.google import Gemini
from agno.os import AgentOS
from dotenv import load_dotenv
from agno.models.ollama import Ollama
from browser_nav_tools import navigate, click_text, type_into, get_accessibility_tree

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
    markdown=True,
)

vo = Agent(
    name="Vo",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=["""
    You are a browser controlling assistant named Vo. 
    Your job is to control the browser as the user demands. Use the tools at your disposal to do so.
    
    In order to fulfill your task well, you must use the get accessibility tree to get information
    from the page and filter it out. 
    For instance, if the user asks for the top 3 emails, you must call the get_accessibility_tree tool and filter it and 
    just give the email subjects to the user. If the user were to ask more about a single email, you should provide the body
    of the email to them. 
    
    When using the click_text argument, make sure that you are clicking on a button element.
    """],
    tools=[navigate, click_text, type_into, get_accessibility_tree],
    markdown = True,
)

# assistant.print_response("testing...")
agent_os = AgentOS(
    os_id="my-first-os",
    description="My first AgentOS",
    agents=[vo],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="my_os:app", reload=True)
