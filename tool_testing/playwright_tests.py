import asyncio
import json
from playwright.async_api import Playwright, async_playwright, expect

CDP_URL = "http://localhost:9222"
async def run(playwright: Playwright) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]
        await page.goto("https://www.youtube.com/")
        await page.get_by_role("combobox", name="Search").click()
        await page.get_by_role("combobox", name="Search").fill("jaws screen reader tutorial")
        await page.get_by_role("button", name="Search", exact=True).click()
        await page.wait_for_load_state("networkidle")
        snapshot = await page.locator("body").aria_snapshot()
        print(snapshot)
        await page.get_by_text("A brief introduction to JAWS").click()


    # ---------------------
        await context.close()
        await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
