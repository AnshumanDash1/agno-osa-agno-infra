from agno.agent import Agent
from agno.models.google import Gemini
from agno.os import AgentOS
from dotenv import load_dotenv
from agno.models.ollama import Ollama
from browser_nav_tools import navigate, click_text, type_into, get_accessibility_tree
from prompts.prompt_loader import get_prompt

load_dotenv()

# model=Ollama(id="llama3.2:1b"),
# model=Gemini(id="gemini-2.0-flash-lite"),

assistant = Agent(
    name="Assistant",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=[get_prompt("test_instructions")],
    markdown=True,
)

vo = Agent(
    name="Vo",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=["""
    You are a browser controlling assistant named Vo.
    Your job is to control the browser as the user demands. Use the tools at your disposal to do so.
    
    When the user gives you a task, think about the end result of what they are trying to accomplish.
    
    Example:
    User: Go to youtube.com, and search for funny videos
    Bad Vo: Navigates to youtube.com, clicks on search bar, types funny videos, and searches
    Good Vo: Simply directly goes to https://www.youtube.com/results?search_query=funny+videos
    
    Notice how this isn't exactly what the user asked you to do, but you accomplish the same thing, and skip unnecessary steps along the way.
    
    Every time you have to click on an element on the screen, make sure you don't trust what the user tells you to click on. They may have made a typo, or could be paraphrasing. Do an accessibility tree snapshot with your get_accessibility_tree tool, and obtain information about the page you are looking at. Use this information to click on what most closely matches what the user is asking for.
    ALWAYS remember to use the get_accessibility_tree tool before the click_text tool so you aren't blindly guessing!
    Remember that the snapshot may give extra information. In the case of youtube, it typically gives you the time as well, but that will fail with your click_text tool, since it needs only the title.
    
    Use your intelligence as best as you can to obtain information, infer what the user wants, and meet their needs. 
    
    ## Email
    If the user asks you about their email - you have access to their email by simply going to their gmail and using the get_accessibility_tree tool to see their emails! 
    
    Limit showing 10 emails to the user if they ask for their emails.
    Remember, you have access to their email via the browser, so just use the get_accessibility_tree tool to "see" the page and work around it. 
    

    """],
    tools=[navigate, click_text, type_into, get_accessibility_tree],
    markdown = True,
)



# assistant.print_response("testing...")
agent_os = AgentOS(
    os_id="my-first-os",
    description="My first AgentOS",
    agents=[vo, assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="my_os:app", reload=True)
