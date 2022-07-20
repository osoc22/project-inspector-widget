import asyncio
import base64
import csv
import json
import logging
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
        self.generic_eval = """(n) => {{
                    let ob = {{
                        "product_name" : null,
                        "price_current": null,
                        "price_reference": null,
                        "product_code": null
                    }}
                    if (n.querySelector('{0}')) {{
                        ob.product_name = n.querySelector('{0}').innerText
                    }}
                    if (n.querySelector('{1}')) {{
                        ob.price_current = n.querySelector('{1}').innerText
                    }}
                    if (n.querySelector('{2}')) {{
                        ob.price_reference = n.querySelector('{2}').innerText
                    }}
                    if (ob.price_reference == null) {{
                        ob.price_reference = ob.price_current
                    }}
                    return ob
                }}"""
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
        self.webshop = "x2o"
        self.price_current_field = '.current'
        self.price_reference_field = '.reference'
        self.product_name_field = '.productname'
        self.eval_fct = par.generic_eval.format(self.product_name_field, self.price_current_field, self.price_reference_field)
        return self

    async def go_to_page(self, url):
        await super().go_to_page(url)

    async def scrape(self):
        product_informations = []
        await self.go_to_page(self.url)
        # this clicks the "OK" button on the popup asking us for cookies
        await self.page.evaluate("""() => {
            document.getElementById("onetrust-accept-btn-handler").dispatchEvent(new MouseEvent("click", {
                cancelable: true,
                view: window,
                bubbles: true
            }));
        }""")
        await asyncio.sleep(3)
        #await self.page.select('select[name="COUNTPERPAGE"', '0')
        await self.page.waitForSelector('div.js-product-list')
        
        # this closes the weird "hey need help" thing on the website if it pops up
        if await self.page.querySelector('body[class*="no-scroll"]'):
            await self.page.evaluate("""() => {
                document.querySelector("div[class*='js-open-whisbi']").dispatchEvent(new MouseEvent("click", {
                    cancelable: true,
                    bubbles: true,
                    view: window
                }));
            }""")
            
        big_image = BytesIO(await self.page.screenshot({'type': 'png', 'fullPage': True}))
        product_nodes = await self.page.querySelectorAll('div.product-container > div.product')

        for product_node in product_nodes:
            product_info = await extract_data_from_node(self.webshop, self.page, self.eval_fct, product_node)
            if product_info is not None:
                product_informations.append(product_info)
        get_products_from_screenshot(big_image, product_informations, True)
        # res = requests.post("http://localhost:8500/products", json=json.dumps(product_informations))
        print(product_informations)

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
        self.webshop = "x2o"
        self.price_current_field = 'span[class^="price-"]'
        self.price_reference_field = 'p[class^="PromoAdvantageEuro-oldPrice-"]'
        self.product_name_field = 'a[class^="item-nameWrapper-"]'
        self.eval_fct = par.generic_eval.format(self.product_name_field, self.price_current_field, self.price_reference_field)
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
                product_info = await extract_data_from_node(self.webshop, self.page, self.eval_fct, product_node)
                if product_info is not None:
                    product_informations.append(product_info)
            get_products_from_screenshot(OUTPUT_PATH+'{0}{1}.png'.format(self.webshop, page_nbr), product_informations[len(product_nodes)*-1:], False)
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
        #res = requests.post("http://localhost:8500/products", json=json.dumps(product_informations))
        return product_informations

async def extract_data_from_node(webshop, page, eval_fct, node):
    p_i = await page.evaluate(eval_fct, node)
    if not p_i['product_name'] or not p_i['price_current'] or not p_i['price_reference']:
        return None
    p_i["screenshot_id"] = str(time.time_ns())
    p_i['price_reference'] = Price.fromstring(p_i['price_reference']).amount_float
    p_i['price_current'] = Price.fromstring(p_i['price_current']).amount_float
    p_i['webshop'] = webshop
    coords = await node.boundingBox()
    p_i['coords'] = (coords['x'], coords['y'], coords['x']+coords['width'], coords['y']+coords['height'])
    #p_i['image'] = "=HYPERLINK(\"" + timestamp + '.png' + "\";\"Image\")"
    return p_i
    

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
                    region.save(OUTPUT_PATH+product['screenshot_id']+'.png')
                else:
                    buffer = BytesIO()
                    region.save(buffer, format="PNG")
                    buffer.seek(0)
                    product["screenshot"] = base64.b64encode(buffer.getvalue()).decode()
    except OSError:
        print("oh oh")
        pass




async def main(url):
    """Creates an appropriate scraper from the url given and starts scraping away.

    Args:
        url (str): the url of the webshop to scrape.
    """
    # hopefully this gets the chrome service's IP, because chrome debug doesn't allow access via hostname
    try:
        CHROME_IP = socket.getaddrinfo('chrome',0)[0][4][0]
    except socket.gaierror:
        CHROME_IP = '127.0.0.1'
    pyppeteer.DEBUG = True
    browser = await pyppeteer.connect(browserURL=f'http://{CHROME_IP}:9222', logLevel=logging.DEBUG)
    context = await browser.createIncognitoBrowserContext()
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
    await context.close()
    await browser.disconnect()
    return ret

@click.command()
@click.argument('url')
def start(url):
    asyncio.run(main(url))

if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    start()