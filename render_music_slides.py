import asyncio
import os
from playwright.async_api import async_playwright

FRAMES_DIR = r"c:\books\08_acoustic_resonance_audio_forensics\video_assets\frames"
os.makedirs(FRAMES_DIR, exist_ok=True)
SLIDES_URL = "file:///" + os.path.abspath(r"c:\books\08_acoustic_resonance_audio_forensics\video_assets\slides.html").replace("\\", "/")

async def render_all_slides():
    print("Launching Microsoft Edge via Playwright for 1920x1080 rendering...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        for i in range(1, 7):
            url = f"{SLIDES_URL}#slide-{i}"
            await page.goto(url)
            await page.wait_for_timeout(1000)  # wait for fonts and CSS to settle
            out_img = os.path.join(FRAMES_DIR, f"slide_{i}.png")
            await page.screenshot(path=out_img)
            print(f"  [OK] Rendered slide {i} -> {out_img}")

        await browser.close()
        print("All 6 presentation slides rendered successfully in 1080p!")

if __name__ == "__main__":
    asyncio.run(render_all_slides())
