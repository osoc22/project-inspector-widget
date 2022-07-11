import asyncio
import csv
from os.path import exists
import datetime
import time
from pyppeteer import launch

OUTPUT_PATH = 'output/'

headers = ['date', 'store', 'product name', 'current price', 'reference price', 'image']

class GenericScraper:
    """A GenericScaper is some kind of interface that specific webshop scrapers
    will implement the methods of
    """

    @classmethod
    async def create(cls, browser, url):
        """Creates a scraper from a browser instance and url

        Args:
            browser (Browser): a Browser after launch from pyppeteer has been called
            url (str): a string for the url of the starting point of the scraper

        Returns:
            GenericScraper: an instance of a GenericScaper
        """
        self = cls()
        self.page = await browser.newPage()
        self.url = url
        return self

    async def go_to_page(self, url):
        """Sets the Page to the given url

        Args:
            url (str): the url the browser will go to
        """
        await self.page.goto(url)

    async def scrape(self):
        """Scrapes the product informations and does a screenshot of the website
        """
        pass

    async def close(self):
        """Closes the Page
        """
        await self.page.close()


class VandenborreScraper(GenericScraper):
    """A scraper made for the Vandenborre website
    """

    @classmethod
    async def create(cls, browser, url):
        self = cls()
        self.url = url
        par = await super().create(browser, url)
        self.page = par.page
        self.filename = "vandenborre.csv"
        print(self.url)
        return self

    async def go_to_page(self, url):
        await super().go_to_page(url)

    async def scrape(self):
        await self.go_to_page(self.url)
        # this clicks the "OK" button on the popup asking us for cookies
        await self.page.evaluate("""() => {
            document.getElementById("onetrust-accept-btn-handler").dispatchEvent(new MouseEvent("click", {
                bubbles: true,
                cancelable: true,
                view: window
            }));
        }""")

        # await self.page.select('select[name="COUNTPERPAGE"', '0')
        await self.page.waitForSelector('div.js-product-list')
        # this gets every product information on the page

        products_nodes = await self.page.querySelectorAll('div.product-container > div.product')

        product_informations = []

        for product_node in products_nodes:
            p_i = await self.page.evaluate("""(n) => {
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
            }
            """, product_node)
            timestamp = str(time.time_ns())
            # user's excel language need to be english for this to work?
            p_i['image'] = "=HYPERLINK(\"" + timestamp + '.png' + "\";\"Image\")"
            product_informations.append(p_i)
            # print(await product_node.boundingBox())
            # await self.page.screenshot({'path': 'ttt.png', 'fullPage': True})
            await self.page.screenshot({'path' : OUTPUT_PATH+timestamp + '.png', 'clip': await product_node.boundingBox()})

        today = datetime.date.today()
        if not exists(OUTPUT_PATH+self.filename):
            with open(OUTPUT_PATH+self.filename, 'x+') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow(headers)
        with open(OUTPUT_PATH+self.filename, 'a+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            for product in product_informations:
                csv_writer.writerow([today, 'vandenborre', product['name'], product['price_current'], product['price_reference'], product['image']])




async def main():
    """Crates a new scraper (Vandenborre here) and starts scraping it
    """
    # launches the browser
    browser = await launch()
    vdb = await VandenborreScraper.create(browser, "https://www.vandenborre.be/fr/gsm-smartphone/smartphone")
    r = await vdb.scrape()
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
