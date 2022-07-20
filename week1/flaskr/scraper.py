import asyncio
import base64
import csv
import json
import os
from os.path import exists
import datetime
import time
from io import BytesIO
from PIL import Image
from pyppeteer import launch
import click
from price_parser import Price
import requests

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
                ob.product_name = n.querySelector(".productname").innerText
                if (n.querySelector(".reference")) {
                    ob.price_reference = n.querySelector(".reference").innerText
                    ob.price_current = n.querySelector(".current").innerText
                } else {
                    let price = n.querySelector(".current").innerText
                    ob.price_reference = price
                    ob.price_current = price
                }
                return ob
            }
            """, product_node)
            timestamp = str(time.time_ns())
            p_i['price_reference'] = Price.fromstring(p_i['price_reference']).amount_float
            p_i['price_current'] = Price.fromstring(p_i['price_current']).amount_float
            p_i['webshop'] = 'vandenborre'
            # user's excel language need to be english for this to work?
            p_i['image'] = "=HYPERLINK(\"" + timestamp + '.png' + "\";\"Image\")"
            coords = await product_node.boundingBox()
            p_i['coords'] = (coords['x'], coords['y'], coords['x']+coords['width'], coords['y']+coords['height'])
            p_i['timestamp'] = timestamp
            p_i['url'] = self.url
            product_informations.append(p_i)
        get_products_from_screenshot(OUTPUT_PATH+'ttt.png', product_informations, False)
        output_data_to_file(self.filename, product_informations)
        res = requests.post(os.environ.get('APP_URL') + "/products", json=json.dumps(product_informations))
        return product_informations

class X2OScraper(GenericScraper):
    """A scraper for the X2O webshop
    """

    @classmethod
    async def create(cls, browser, url):
        self = cls()
        self.url = url
        par = await super().create(browser, url)
        self.page = par.page
        self.filename = "X20.csv"
        print(self.url)
        return self

    async def go_to_page(self, url):
        await super().go_to_page(url)

    async def scrape(self):
        product_informations = []
        await self.page.setViewport({
            'width': 1920,
            'height': 5000
        })
        await self.go_to_page(self.url)
        page_nbr = 0
        next_page_nbr = 1
        while (page_nbr < next_page_nbr):
            await asyncio.sleep(5)
            page_nbr = next_page_nbr
            await self.page.waitForSelector('div[class^="gallery-root-"]')
            await self.page.screenshot({'path': OUTPUT_PATH+'tttt{}.png'.format(page_nbr)})
            product_nodes = await self.page.querySelectorAll('div.gallery-item')
            for product_node in product_nodes:
                p_i = await self.page.evaluate("""(n) => {
                    let ob = {}
                    ob.product_name = n.querySelector('a[class^="item-nameWrapper-"]').innerText
                    ob.price_current = n.querySelector('span[class^="price-"]').innerText
                    if (n.querySelector('p[class^="PromoAdvantageEuro-oldPrice-"]')) {
                        ob.price_reference = n.querySelector('p[class^="PromoAdvantageEuro-oldPrice-"]').innerText
                    } else {
                        ob.price_reference = ob.price_current
                    }
                    return ob
                }""", product_node)
                timestamp = str(time.time_ns())
                p_i['price_reference'] = Price.fromstring(p_i['price_reference']).amount_float
                p_i['price_current'] = Price.fromstring(p_i['price_current']).amount_float
                p_i['webshop'] = 'x2o'
                # user's excel language need to be english for this to work?
                p_i['image'] = "=HYPERLINK(\"" + timestamp + '.png' + "\";\"Image\")"
                coords = await product_node.boundingBox()
                p_i['coords'] = (coords['x'], coords['y'], coords['x']+coords['width'], coords['y']+coords['height'])
                p_i['timestamp'] = timestamp
                p_i['url'] = self.url
                product_informations.append(p_i)
            get_products_from_screenshot(OUTPUT_PATH+'tttt{}.png'.format(page_nbr), product_informations[len(product_nodes)*-1:], False)
            output_data_to_file(self.filename, product_informations)
            arrows = await self.page.querySelectorAll('a[class^=navButton-buttonArrow]')
            for arrow in arrows:
                nbr = await self.page.evaluate("""(a) => {
                    return Number(a.href.match(/=(\d+$)/)[1])
                }
                """, arrow)
                next_page_nbr = nbr if next_page_nbr < nbr else next_page_nbr
            if page_nbr < next_page_nbr:
                await self.page.evaluate("""() => {
                    let arrows = document.querySelectorAll('a[class^=navButton-buttonArrow]')
                    arrows[arrows.length - 1].dispatchEvent(new MouseEvent("click", {bubbles: true, view: window, cancelable: true}))
                }""")
        res = requests.post(os.environ.get('APP_URL') + "/products", json=json.dumps(product_informations))
        return product_informations

def output_data_to_endpoint(shop, data):
    today = datetime.date.today()
    for d in data:
        data["date"] = today
        data["image"] = data.pop("timestamp")
        data["webshop"] = shop
    res = requests.post("http://localhost:8500/products", json=json.dumps(data))
    
def output_screenshot_to_endpoint(img_source, product_data):
    payload = []
    try:
        with Image.open(img_source) as im:
            for product in product_data:
                buffer = BytesIO()
                region = im.crop(product['coords'])
                region.save(buffer, fomart="PNG")
                buffer.seek(0)
                payload.append({"id":product_data["timestamp"], "image": base64.b64encode(buffer).decode()})
        res = requests.post("http://localhost:8500/products", json=json.dumps(payload))
    except OSError:
        print("oh oh")
        pass


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
            csv_writer.writerow([today, 'vandenborre', product['product_name'], product['price_current'], product['price_reference'], product['image']])


def get_products_from_screenshot(img_source, product_data, saveImg=True):
    """Cuts each individual product from the big screenshot of the page.

    Args:
        img_source (str): path to the image to cut.
        product_data (list): information about the products so that we can cut accordingly.
    """
    try:
        with Image.open(img_source) as im:
            for product in product_data:
                region = im.crop(product['coords'])
                if saveImg:
                    region.save(OUTPUT_PATH+product['timestamp']+'.png')
                else:
                    buffer = BytesIO()
                    region.save(buffer, format="PNG")
                    buffer.seek(0)
                    product["screenshot"] = base64.b64encode(buffer.getvalue()).decode()
                    product["screenshot_id"] = product["timestamp"]
    except OSError:
        print("oh oh")
        pass




async def main(url):
    """Creates an appropriate scraper from the url given and starts scraping away.

    Args:
        url (str): the url of the webshop to scrape.
    """
    browser = await launch({
        'autoClose': False,
        'executablePath': '/usr/bin/google-chrome-stable',
        'args': ["--no-sandbox"],
    })

    scraper = None
    if ('vandenborre.be' in url):
        scraper = await VandenborreScraper.create(browser, url)
        print("yes")
    elif ('x2o.be' in url):
        scraper = await X2OScraper.create(browser, url)
    else:
        print('webshop not supported')
        await browser.close()
        exit(0)
    ret = await scraper.scrape()
    await browser.close()
    return ret

@click.command()
@click.argument('url')
def start(url):
    asyncio.run(main(url))

if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    start()