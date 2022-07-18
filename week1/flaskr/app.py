from . import create_app
from .src.models import Product, WebShop, Screenshot
import json
from flask import request, Response
import os


app = create_app()

@app.route('/') 
def index():  
     return "Welcome to the backend server"

@app.route('/start-scraper') 
def start_scraper():
     test = main()
     
     return "It worked"

@app.route('/products', methods=["POST"]) # This function will be called inside scraper
def add_products():
    products = request.json

    for product in products:
         webshop_name = product['webshop']
         webshop = WebShop.find_by_name(webshop_name)
         if not webshop:
               webshop = WebShop(name=webshop_name)
               webshop.save_to_db()
               
         screenshot_name = str(product['screenshot'])
         screenshot = Screenshot.find_by_name(screenshot_name)

         if not screenshot:
               screenshot = Screenshot(name=screenshot_name, screenshot_file="This is a test")
               screenshot.save_to_db()
          
         product['webshop'] = webshop
         product['screenshot'] = screenshot


          # check if p is today
         p = Product.query.filter_by(
               name = product['name'],
               webshop = product['webshop']).first()
         
         if not p:
              p = Product(**product)
              p.save_to_db()

    return json.dumps({'success': True}), 201, {'ContentType':'application/json'}


@app.route("/get-csv")
def get_csv():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    csv = ''

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=mytest.csv"})


app.run(debug=True)


@app.route('/products', methods=["GET"]) # this function will be called on start scraper requesy
def get_products():
     products = []

     for product in Product.find_all():
          p = product.serialize()
          products.append(p)
     
     return json.dumps(products)

if __name__ == '__main__': 
     app.run(debug=True)