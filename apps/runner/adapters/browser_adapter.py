import asyncio
from pathlib import Path
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False
from PIL import Image, ImageDraw

class BrowserAdapter:
    def __init__(self, profile: str | None = None):
        self.profile = profile or '.profiles/x'

    async def screenshot(self, url: str, out_path: Path):
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if PLAYWRIGHT_AVAILABLE:
            async with async_playwright() as p:
                browser = await p.chromium.launch_persistent_context(self.profile, headless=True)
                page = await browser.new_page()
                await page.goto(url)
                await asyncio.sleep(1.0)
                await page.screenshot(path=str(out_path))
                await browser.close()
        else:
            # Mock screenshot
            img = Image.new('RGB', (800, 600), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.text((10,10), f"Screenshot mock\n{url}", fill=(255,255,0))
            img.save(out_path)
