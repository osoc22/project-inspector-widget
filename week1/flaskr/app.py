try:
    from  __init__ import create_app                          
except ImportError:
    from . import create_app

try:
   from src.models import Product, WebShop, Screenshot, Scraper                 
except ImportError:
   from .src.models import Product, WebShop, Screenshot, Scraper
from io import BytesIO
import json
from datetime import datetime
import tldextract
from flask import Response, request
from threading import Thread
import os
import queue
from base64 import b64decode
import csv
from io import BytesIO, StringIO
import json
import zipfile
import enum

q = queue.Queue()

def scraping_queue(ctx):
     def worker(ctx):
          with ctx.app_context():
               while True:
                    scraper_id = q.get()
                    scraper = Scraper.find_by_id(scraper_id)
                    if scraper:
                         try:
                              scraper.status = Status.running.value
                              scraper.save_to_db()
                              os.system(f'python scraper.py {scraper.url} {scraper.id}')
                         except:
                              print(f'there was an error while scraping {scraper.url}')
                              scraper.status = Status.error.value
                         else:
                              scraper.status = Status.done.value
                         finally:
                              scraper.save_to_db()
                    else:
                         print("there was no scraper with that id, lets remove it from the queue")
                    q.task_done()
     Thread(target=worker, daemon=True, args=[ctx]).start()
     q.join()

class Status(enum.Enum):
    running = 'RUNNING'
    done = 'DONE'
    error = 'ERROR'

app = create_app()
Thread(target=scraping_queue, args=[app]).start()
@app.route('/') 
def index():  
     return "Welcome to the backend server"

def start_scraper_cmd(url):
     cmd = f'python scraper.py {url}'
     os.system(cmd)


@app.route('/start-scraper/<id>')
def start_scraper_by_id(id):
     scraper = Scraper.find_by_id(id)

     if not scraper:
          return json.dumps({'success': False, 'messsage': 'Could not find scraper'}), 400, {'ContentType':'application/json'}
     q.put(id)
     return "added scraper to the queue"
     # try:
     #      Thread(target=start_scraper_cmd, args=(scraper.url,), daemon=True).start()
     #      scraper.status = Status.running.value
     #      scraper.save_to_db()
     # except BaseException as err:
     #      return json.dumps({'success': False, 'messsage': f"Unexpected {err=}, {type(err)=}"}), 500, {'ContentType':'application/json'}
     

     # return json.dumps({'success': True, 'messsage': 'Scraper ran succesfully'}), 200, {'ContentType':'application/json'}



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

     # try:
     #      scraper.save_to_db()
     #      # Start the scraper
     #      Thread(target=start_scraper_cmd, args=(scraper.url,), daemon=True).start()
     # except BaseException as err:
     #      return json.dumps({'success': False, 'messsage': f"Unexpected {err=}, {type(err)=}"}), 500, {'ContentType':'application/json'}
     
     return json.dumps({'success': True, 'data': scraper.serialize()}), 201, {'ContentType':'application/json'}


@app.route('/scrapers', methods=["GET"]) 
def get_scrapers():
     scrapers = []

     for scraper in Scraper.find_all():
          s = scraper.serialize()
          scrapers.append(s)
     
     print(scrapers)
     return json.dumps(scrapers)

@app.route('/scrapers/<id>', methods=["GET"]) 
def get_scraper(id):
     scraper = Scraper.find_by_id(id)
     if not scraper:
          return json.dumps({'success': False, 'message': 'Scraper not found'}), 400, {'ContentType':'application/json'}
     else:
          return json.dumps({'success': True, 'data': scraper.serialize()}), 200, {'ContentType':'application/json'}

@app.route('/scrapers/<id>', methods=["DELETE"])
def delete_scraper(id):
     scraper = Scraper.find_by_id(id)
     if not scraper:
          return json.dumps({'success': False, 'message': 'Scraper not found'}), 400, {'ContentType':'application/json'}
     scraper.delete_from_db()
     return json.dumps({'success': True, 'message': 'Scraper succesfully deleted'}), 200, {'ContentType':'application/json'}

@app.route('/scrapers/<id>/results') 
def get_scraper_results(id):
     products = []
     scraper = Scraper.find_by_id(id)
 
     if not scraper:
          return json.dumps({'success': False, 'messsage': 'Could not find scraper'}), 400, {'ContentType':'application/json'}
     
     for product in scraper.products:
          p = product.serialize()
          products.append(p)
     
     return json.dumps(products)


@app.route('/scrapers/<id>/export') 
def export_scraper_to_file(id):
     scraper = Scraper.find_by_id(id)

     if not scraper:
          return json.dumps({'success': False, 'messsage': 'Could not find scraper'}), 400, {'ContentType':'application/json'}
     
     products = scraper.products

     file_object = BytesIO()


     with zipfile.ZipFile(file_object, 'w') as zip_file:
          csv_output = StringIO()
          csv_header = ['product name', 'current price', 'reference price', 'date', 'image']
          csv_writer = csv.writer(csv_output, delimiter=';')
          csv_writer.writerow(csv_header)
          for product in products:
               csv_writer.writerow([product.name, product.price_current, product.price_reference, product.date, "=HYPERLINK(\"" + product.screenshot.name + '.png' + "\";\"Image\")"])
               img_buffer = BytesIO(b64decode(product.screenshot.screenshot_file))
               zip_file.writestr(product.screenshot.name + '.png', img_buffer.read())
          csv_output.seek(0)

          zip_file.writestr('results.csv', csv_output.read())
     
     file_object.seek(0)
     filename = '%s_%s.zip' % (scraper.name.replace(' ', '_'), scraper.last_scanned.strftime("%Y%m%d-%H%M%S"))
    
     return Response(
          file_object,
          mimetype="application/zip",
          headers={"Content-disposition":
                    f"attachment; filename={filename}"})

@app.route('/products', methods=["POST"]) # This endpoint will be called inside scraper, change name of route
def add_products():
    scraper = None 
    products = json.loads(request.json)

    for product in products:
          scraper = Scraper.query.filter_by(url=product['url']).first()
        
          p = Product.query.filter_by(
               name = product['product_name'],
               scraper = scraper).order_by(Product.date.desc()).first()
  
          if not p or p.price_current != product['price_current'] or p.price_reference != product['price_reference']:
              screenshot = Screenshot(name=str(product['screenshot_id']), screenshot_file=product['screenshot'])
              screenshot.save_to_db()
              product['screenshot'] = screenshot
              p = Product(name=product['product_name'], price_current=product['price_current'], price_reference=product['price_reference'], screenshot=product['screenshot'], webshop=scraper.webshop, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), scraper=scraper)
              p.save_to_db()
                   
    
    if scraper: # Delete if statement
          scraper.status = Status.done.value
          scraper.last_scanned = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          scraper.save_to_db()
  
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