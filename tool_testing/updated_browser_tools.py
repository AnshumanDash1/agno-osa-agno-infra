import asyncio
from playwright.async_api import async_playwright

# Connect to your existing Chrome (started with --remote-debugging-port=9222)
CDP_URL = "http://localhost:9222"


# -------------------------
# NAVIGATE
# -------------------------
async def navigate(url: str):
    """
    Tool: navigate
    Description: Navigate the active Chrome tab to a given URL.

    Args:
        url (str): The full URL to visit (e.g. "https://google.com").

    Returns:
        str: A confirmation message including the URL and the page title.
    """
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]

        await page.goto(url)
        title = await page.title()

        await browser.close()
        return f"Navigated to {url} (title: {title})"


# -------------------------
# GET ACCESSIBLE ACTIONS
# -------------------------
async def get_actions():
    """
    Tool: get_actions
    Description: Retrieve all actionable elements from the page's accessibility tree.

    Args:
        None

    Returns:
        list[dict]: A list of elements with role and name, e.g.
            [{"role": "button", "name": "Search"}, {"role": "link", "name": "Sign in"}].
        These represent buttons, links, textboxes, and menu items that can be interacted with.
    """
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]

        snapshot = await page.accessibility.snapshot()
        await browser.close()

        def extract_actions(node):
            actions = []
            if "role" in node and "name" in node:
                if node["role"] in ["button", "link", "textbox", "menuitem"]:
                    actions.append({"role": node["role"], "name": node["name"]})
            for child in node.get("children", []):
                actions.extend(extract_actions(child))
            return actions

        return extract_actions(snapshot)


# -------------------------
# CLICK BY ROLE + NAME
# -------------------------
async def click_role_name(role: str, name: str):
    """
    Tool: click_role_name
    Description: Click an element by its accessibility role and accessible name.

    Args:
        role (str): The role of the element (e.g. "button", "link", "textbox").
        name (str): The accessible name or label of the element (e.g. "Search", "Compose").

    Returns:
        str: A confirmation message if successful, or an error message if the click fails.
    """
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]

        try:
            locator = page.get_by_role(role, name=name)
            await locator.first.click(timeout=5000)
            await browser.close()
            return f"Clicked {role} with name '{name}'"
        except Exception as e:
            await browser.close()
            return f"Failed to click {role} '{name}': {e}"


# -------------------------
# TYPE INTO INPUTS
# -------------------------
async def type_into(selector: str, text: str):
    """
    Tool: type_into
    Description: Type text into an input field by CSS selector.

    Args:
        selector (str): The CSS selector for the input (e.g. "input[name=q]", "#search").
        text (str): The text to type into the input field.

    Returns:
        str: A confirmation message if successful, or an error message if typing fails.
    """
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]

        try:
            await page.fill(selector, text)
            await browser.close()
            return f"Typed '{text}' into {selector}"
        except Exception as e:
            await browser.close()
            return f"Failed typing into {selector}: {e}"


# -------------------------
# TEST HARNESS
# -------------------------
async def main():
    print(await navigate("https://youtube.com"))

    actions = await get_actions()
    print("First 10 actions:", actions[:10])

    # Example: try clicking YouTube's search button
    print(await click_role_name("button", "Search"))

    # Example: type into search field
    print(await type_into("input#search", "Accessibility videos"))


if __name__ == "__main__":
    asyncio.run(main())
