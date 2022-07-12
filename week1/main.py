import asyncio
import csv
from os.path import exists
import datetime
import time
from PIL import Image
from pyppeteer import launch
import click

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
                cancelable: true,
                view: window
            }));
        }""")

        await self.page.select('select[name="COUNTPERPAGE"', '0')
        await self.page.waitForSelector('div.js-product-list')
        # this gets every product information on the page
        await self.page.screenshot({'path': OUTPUT_PATH+'ttt.png', 'fullPage': True})
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
            coords = await product_node.boundingBox()
            p_i['coords'] = (coords['x'], coords['y'], coords['x']+coords['width'], coords['y']+coords['height'])
            p_i['timestamp'] = timestamp
            product_informations.append(p_i)        
        get_products_from_screenshot(OUTPUT_PATH+'ttt.png', product_informations)
        output_data_to_file(self.filename, product_informations)       


def output_data_to_file(filename, data):
    """Writes scraped product data to an csv file.

    Args:
        filename (str): filename to output the data to.
        data (list): basically everything that is supposed to go into the file
    """
    today = datetime.date.today()
    if not exists(OUTPUT_PATH+filename):
        with open(OUTPUT_PATH+filename, 'x+', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow(headers)
    with open(OUTPUT_PATH+filename, 'a+', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        for product in data:
            csv_writer.writerow([today, 'vandenborre', product['name'], product['price_current'], product['price_reference'], product['image']])


def get_products_from_screenshot(img_source, product_data):
    """Cuts each individual product from the big screenshot of the page.

    Args:
        img_source (str): path to the image to cut.
        product_data (list): information about the products so that we can cut accordingly.
    """
    try:
        with Image.open(img_source) as im:
            for product in product_data:
                region = im.crop(product['coords'])
                region.save(OUTPUT_PATH+product['timestamp']+'.png')
    except OSError:
        print("oh oh")
        pass



async def main(url):
    """Creates an appropriate scraper from the url given and starts scraping away.

    Args:
        url (str): the url of the webshop to scrape.
    """
    browser = await launch()
    scraper = None
    if ('vandenborre.be' in url):
        scraper = await VandenborreScraper.create(browser, url)
    else:
        print('webshop not supported')
        await browser.close()
        exit(0)
    await scraper.scrape()
    await browser.close()

@click.command()
@click.argument('url')
def start(url):
    asyncio.run(main(url))

if __name__ == '__main__':
    start()
