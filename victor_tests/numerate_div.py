import asyncio
from pyppeteer import launch

async def main():
    # launches the browser
    browser = await launch()

    # creates a new "Page" in the browser
    page = await browser.newPage()

    # navigates to the given URL
    await page.goto("https://www.vandenborre.be/fr/gsm-smartphone/smartphone")

    # basically clicks the "OK" on the cookie popup
    await page.evaluate(f"""() => {{
        document.getElementById("onetrust-accept-btn-handler").dispatchEvent(new MouseEvent("click", {{
            bubbles: true,
            cancelable: true,
            view: window
        }}));
    }}""")


    ratings = await page.evaluate('document.getElementsByTagName("strong").value')
    print(ratings)
    await page.screenshot({'path': 'test.png', 'fullPage': True})


    


    
    await page.close()
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())