import asyncio
from playwright.async_api import async_playwright

CDP_URL = "http://localhost:9222"

async def navigate(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]        # <-- no () here
        page = context.pages[0]              # <-- same here
        await page.goto(url)
        title = await page.title()
        await browser.close()
        return f"Navigated to {url} (title: {title})"

async def click_text(text: str):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]
        await page.click(f"text={text}")
        await browser.close()
        return f"Clicked element with text '{text}'"

async def type_into(selector: str, text: str):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]
        await page.fill(selector, text)
        await browser.close()
        return f"Typed '{text}' into {selector}"

async def get_accessibility_tree():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]
        snapshot = await page.accessibility.snapshot()
        await browser.close()
        return snapshot

# ----------------------------
# Test sequence
# ----------------------------
# async def main():
#     print(await navigate("https://example.com"))
#     print(await click_text("More information"))
#     print(await navigate("https://google.com"))
#     print(await type_into("textarea[name=q]", "hello world"))
#     ax_tree = await get_accessibility_tree()
#     print("Accessibility snapshot keys:", ax_tree.keys())
#
# asyncio.run(main())
