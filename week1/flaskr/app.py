from . import create_app
from .src.models import Product, WebShop, Screenshot, Scraper
import json
import tldextract
from flask import request
import os

app = create_app()


@app.route('/') 
def index():  
     return "Welcome to the backend server"


output = []

@app.route('/start-scraper', methods=["POST"]) 
def start_scraper():
     data = json.loads(request.data)
     url = data['url']
     cmd = f'python scraper.py {url}'
     os.system(cmd)

     return json.dumps(output)

@app.route('/scrapers/<id>')
def start_scraper_by_id(id):
     scraper = Scraper.find_by_id(id)

     if not scraper:
          pass
          # if scraper not found throw, scraper not found error

     url = scraper.url
     cmd = f'python scraper.py {url}'
     os.system(cmd)

@app.route('/scrapers', methods=["POST"]) 
def add_scraper():
     data = json.loads(request.data)
     ext = tldextract.extract(data['url'])
     
     webshop_name = ext.domain
     webshop = WebShop.find_by_name(webshop_name)

     if not webshop:
          webshop = WebShop(name=webshop_name)
          webshop.save_to_db()
     
     scraper = Scraper(name=data['name'], url=data['url'], webshop=webshop, start_date=data['start_date'], end_date=data['end_date'])
     scraper.save_to_db()

     return json.dumps({'success': True}), 201, {'ContentType':'application/json'}



@app.route('/scrapers', methods=["GET"]) 
def get_scrapers():
     scrapers = []

     for scraper in Scraper.find_all():
          s = scraper.serialize()
          scrapers.append(s)
     
     return json.dumps(scrapers)

@app.route('/products', methods=["POST"]) # This endpoint will be called inside scraper
def add_products():
    products = json.loads(request.json)

    for product in products:
         webshop_name = product['webshop']
         webshop = WebShop.find_by_name(webshop_name)
         if not webshop:
               webshop = WebShop(name=webshop_name)
               webshop.save_to_db()
               
         screenshot_name = str(product['screenshot_id'])
         screenshot = Screenshot.find_by_name(screenshot_name)

         if not screenshot:
               screenshot = Screenshot(name=screenshot_name, screenshot_file=product["screenshot"])
               screenshot.save_to_db()
          
         product['webshop'] = webshop
         product['screenshot'] = screenshot
      

         p = Product.query.filter_by(
               name = product['product_name'],
               webshop = product['webshop']).first()
         
         if not p:
              p = Product(name=product['product_name'], price_current=product['price_current'], price_reference=product['price_reference'], screenshot=product['screenshot'], webshop=product['webshop'], date="2022-07-13 11:13:20")
              p.save_to_db()
          
         output.append(p.serialize())

    return json.dumps({'success': True}), 201, {'ContentType':'application/json'}


@app.route('/products', methods=["GET"])
def get_products():
     products = []

     for product in Product.find_all():
          p = product.serialize()
          products.append(p)
     
     return json.dumps(products)

if __name__ == '__main__': 
     app.run(debug=True)