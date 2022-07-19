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


    
    price = await page.evaluate("console.log(document.getElementById('current is-sale-price  '))")
    print(price)

    



    await page.close()
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())



