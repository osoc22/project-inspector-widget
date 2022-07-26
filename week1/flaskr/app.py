try:
    from  __init__ import create_app                          
except ImportError:
    from . import create_app

try:
   from src.models import Product, WebShop, Screenshot, Scraper, User, TokenBlocklist     
except ImportError:
   from .src.models import Product, WebShop, Screenshot, Scraper, User, TokenBlocklist
from werkzeug.security import generate_password_hash, check_password_hash
from io import BytesIO
import json
from datetime import datetime, timedelta, timezone
import tldextract
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, jwt_required, set_access_cookies
from flask_jwt_extended import create_refresh_token
from flask import Response, request, jsonify
from threading import Thread
import os
from base64 import b64decode
import csv
from io import BytesIO, StringIO
import json
import zipfile
import enum


class Status(enum.Enum):
    running = 'RUNNING'
    done = 'DONE'
    error = 'ERROR'

app = create_app()

@app.route('/') 
def index():  
     return "Welcome to the backend server"

def start_scraper_cmd(url):
     cmd = f'python scraper.py {url}'
     os.system(cmd)


@app.route('/start-scraper/<id>')
@jwt_required()
def start_scraper_by_id(id):
     scraper = Scraper.find_by_id(id)

     if not scraper:
          return json.dumps({'success': False, 'messsage': 'Could not find scraper'}), 400, {'ContentType':'application/json'}
     
     try:
          Thread(target=start_scraper_cmd, args=(scraper.url,), daemon=True).start()
          scraper.status = Status.running.value
          scraper.save_to_db()
     except BaseException as err:
          return json.dumps({'success': False, 'messsage': f"Unexpected {err=}, {type(err)=}"}), 500, {'ContentType':'application/json'}
     

     return json.dumps({'success': True, 'messsage': 'Scraper ran succesfully'}), 200, {'ContentType':'application/json'}



@app.route('/scrapers', methods=["POST"])
@jwt_required()
def add_scraper():
     data = json.loads(request.data)
     ext = tldextract.extract(data['url'])
     
     webshop_name = ext.domain
     webshop = WebShop.find_by_name(webshop_name)

     if not webshop:
          webshop = WebShop(name=webshop_name)
          webshop.save_to_db()
     
     current_user_id = get_jwt_identity()
     user = User.find_by_public_id(current_user_id) 

     scraper = Scraper(name=data['name'], url=data['url'], webshop=webshop, start_date=data['start_date'], end_date=data['end_date'], user=user)

     try:
          scraper.save_to_db()
          # Start the scraper
          Thread(target=start_scraper_cmd, args=(scraper.url,), daemon=True).start()
     except BaseException as err:
          return json.dumps({'success': False, 'messsage': f"Unexpected {err=}, {type(err)=}"}), 500, {'ContentType':'application/json'}
     
     return json.dumps({'success': True, 'data': scraper.serialize()}), 201, {'ContentType':'application/json'}


@app.route('/scrapers', methods=["GET"])
@jwt_required()
def get_scrapers():
     scrapers = []

     for scraper in Scraper.find_all():
          s = scraper.serialize()
          scrapers.append(s)
     
     return json.dumps(scrapers)

@app.route('/scrapers/<id>', methods=["GET"])
@jwt_required()
def get_scraper(id):
     scraper = Scraper.find_by_id(id)
     if not scraper:
          return json.dumps({'success': False, 'message': 'Scraper not found'}), 400, {'ContentType':'application/json'}
     else:
          return json.dumps({'success': True, 'data': scraper.serialize()}), 200, {'ContentType':'application/json'}

@app.route('/scrapers/<id>', methods=["DELETE"])
@jwt_required()
def delete_scraper(id):
     scraper = Scraper.find_by_id(id)
     if not scraper:
          return json.dumps({'success': False, 'message': 'Scraper not found'}), 400, {'ContentType':'application/json'}
     scraper.delete_from_db()
     return json.dumps({'success': True, 'message': 'Scraper succesfully deleted'}), 200, {'ContentType':'application/json'}

@app.route('/scrapers/<id>/results')
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def get_products():
     products = []

     for product in Product.find_all():
          p = product.serialize()
          products.append(p)
     
     return json.dumps(products)

# Put this in separate class, get scrapers from each user, adding and deleting scraper only if jwt is required

# Using an `after_request` callback, we refresh any token that is within 30 minutes
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@app.route('/register', methods=["POST"]) 
def register_user():
     # todo: validate object
     data = json.loads(request.data)

     if not data:
          return json.dumps({'succes': False, 'message': 'Please provide user details.'}), 400, {'ContentType':'application/json'}

     # Check if user already exists
     user = User.find_by_email(data['email'])

     if not user:
          try:
               password = generate_password_hash(data['password'])
               user = User(email=data['email'], username=data['username'], password=password) 
               user.save_to_db()

               return json.dumps({'success': True, 'messsage': 'Succesfully registered'}), 201, {'ContentType':'application/json'}
          
          except BaseException as err:
               return json.dumps({'success': False, 'messsage': f"Unexpected {err=}, {type(err)=}"}), 401, {'ContentType':'application/json'}
     else:
          return json.dumps({'succes': False, 'message': 'User already exists. Please Log in.'}), 400, {'ContentType':'application/json'}
 
@app.route('/login', methods=["POST"])
def login_user():
     data = json.loads(request.data)

     if not data:
          return json.dumps({'succes': False, 'message': 'Please provide user details.'}), 400, {'ContentType':'application/json'}

     user = User.find_by_username(data['username'])

     if not user:
          return json.dumps({'succes': False, 'message': 'Bad username or password.'}), 401, {'ContentType':'application/json'}

       
     if check_password_hash(user.password, data["password"]):
           # create a new token with the user public id
          access_token = create_access_token(identity=user.public_id, fresh=True)
          refresh_token = create_refresh_token(identity=user.public_id)
          user.authenticated = True
          user.save_to_db()
          return jsonify({ "access_token": access_token, "refresh_token": refresh_token, "user_id": user.public_id })
 
     return json.dumps({'success': False, 'messsage': 'Invalid data'}), 401, {'ContentType':'application/json'}

@app.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
     # Get current user
    current_user_id = get_jwt_identity()
    user = User.find_by_public_id(current_user_id)
    user.authenticated = False
    user.save_to_db()

    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    TokenBlocklist(jti=jti, created_at=now).save_to_db()

    return json.dumps({'success': True, 'messsage': 'Access token revoked'}), 200, {'ContentType':'application/json'}
   
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return json.dumps({ "access_token": access_token })

@app.route("/user", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.find_by_public_id(current_user_id)
    
    return json.dumps({"id": str(user.public_id), "email": user.email, "username": user.username }), 200

@app.route("/scrapers/user", methods=["GET"])
@jwt_required()
def get_scrapers_of_current_user():
    current_user_id = get_jwt_identity()
    user = User.find_by_public_id(current_user_id) 
    scrapers = []

    for scraper in user.scrapers:
          s = scraper.serialize()
          scrapers.append(s)
     
    return json.dumps(scrapers)

if __name__ == '__main__': 
     app.run(debug=True)