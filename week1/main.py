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
    
    # selects "show all products"
    # await page.select('select[name="COUNTPERPAGE"', '0')
    # waits for the entire product list to be loaded
    await page.waitForSelector('div.js-product-list')

    # t will contain an array of dict with the following values
    # name : the name of the product
    # price_reference : the "base" price of a discounted product, or the price of a product if there is no discount
    # price_current : the current discounted price of a product, or the price of a product if there is no discount
    t = await page.querySelectorAllEval('div.product-container > div.product', """(nodes => nodes.map(n => 
    {
        let ob = {}
        ob.name = n.querySelector(".productname").innerText
        if (n.querySelector(".reference")) {
            ob.price_reference = Number(n.querySelector(".reference").innerText.replace(",", ".").replace(/€\xa0/g, ""))
            ob.price_current = Number(n.querySelector(".current").innerText.replace(",", ".").replace(/€\xa0/g, ""))
        } else {
            let price = Number(n.querySelector(".current").innerText.replace(",", ".").replace(/€\xa0/g, ""))
            ob.price_reference = price
            ob.price_current = price
        }
        return ob
    }))""")
    # screenshots the entire page without size limitations
    await page.screenshot({'path': 'test.png', 'fullPage': True})
    await page.close()
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())