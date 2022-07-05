import asyncio
from pyppeteer import launch

async def main(someClass):
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
    
    # selects "show all products"
    await page.select('select[name="COUNTPERPAGE"', '0')
    # waits for the entire product list to be loaded
    await page.waitForSelector('div.js-product-list')

    products = await page.querySelectorAll('div.js-product-container')
    # screenshots the entire page without size limitations
    await page.screenshot({'path': 'test.png', 'fullPage': True})
    await page.close()
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())