import asyncio
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Playwright

CDP_URL = "http://localhost:9222"

@asynccontextmanager
async def get_playwright_context():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]
        try:
            yield p, browser, context, page
        finally:
            await p.stop()


async def navigate(url: str):
    async with get_playwright_context() as (_, browser, context, page):
        await page.goto(url)
        title = await page.title()
        return f"Navigated to {url} (title: {title})"


async def click_text(text: str):
    async with get_playwright_context() as (_, _, _, page):
        await page.get_by_text(text).click()
        return f"Clicked '{text}'"


async def type_into(selector: str, text: str):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]
        await page.fill(selector, text)
        return f"Typed '{text}' into {selector}"

async def get_accessibility_tree():
    async with get_playwright_context() as (_, _, _, page):
        return await page.locator("body").aria_snapshot()


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
