import asyncio
import csv
from os.path import exists
import datetime
import time
from pyppeteer import launch

headers = ['date', 'store', 'product name', 'current price', 'reference price', 'url']

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

        #await self.page.select('select[name="COUNTPERPAGE"', '0')
        await self.page.waitForSelector('div.js-product-list')
        # this gets every product information on the page

        products_nodes = await self.page.querySelectorAll('div.product-container > div.product')

        for product_node in products_nodes:
            # p_i = product_node.evaluate("""(n) => {
            #     let ob = {}
            #     ob.name = n.querySelector(".productname").innerText
            #     if (n.querySelector(".reference")) {
            #         ob.price_reference = Number(n.querySelector(".reference").innerText.replace(",", ".").replace(/€\xa0/g, ""))
            #         ob.price_current = Number(n.querySelector(".current").innerText.replace(",", ".").replace(/€\xa0/g, ""))
            #     } else {
            #         let price = Number(n.querySelector(".current").innerText.replace(",", ".").replace(/€\xa0/g, ""))
            #         ob.price_reference = price
            #         ob.price_current = price
            #     }
            #     return ob
            # }
            # """)
            await self.page.screenshot({'path' : str(time.time_ns()) + '.png', 'clip': await product_node.boundingBox()})

        products = await self.page.querySelectorAllEval('div.product-container > div.product', """(nodes => nodes.map(n => {
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
        #await self.page.screenshot({'path': str(time.time_ns()) + '.png', 'fullPage': True})
        today = datetime.date.today()
        if not exists(self.filename):
            with open(self.filename, 'x+') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(headers)
        with open(self.filename, 'a+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for product in products:
                csv_writer.writerow([today, 'vandenborre', product['name'], product['price_current'], product['price_reference'], self.url])




async def main():
    """Crates a new scraper (Vandenborre here) and starts scraping it
    """
    # launches the browser
    browser = await launch()
    vdb = await VandenborreScraper.create(browser, "https://www.vandenborre.be/fr/gsm-smartphone/smartphone")
    r = await vdb.scrape()
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
