# import csv
# import json

# file_name = 'vandenborre'

# products = {} # Retrieved information from database



# headers = ['category', 'product name', 'url', 'image path', 'date', 'reference price']

# file = open('data.json')

# products = json.load(file)


# def create_csv_from_products(products):

#     with open("{}.csv".format(file_name), 'w') as csv_file:

#         writer = csv.writer(csv_file)

#         writer.writerow(headers)
   
#         for product in products:

#             writer.writerow([product['category'], product['name'], product['url'], product['url'], product['date'], product['reference price']])

# create_csv_from_products(products)

from datetime import datetime

PRODUCTS = [
    {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "webshop": "Farrell",
        "name": "smartphone super cool",
        "price_current": 1,
        "price_reference": 20,
        "screenshot": 111100011242
    },
    {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "webshop": "Farrell",
        "name": "smartphone super cool",
        "price_current": 1,
        "price_reference": 20,
        "screenshot": 111100011242
    },
    {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "webshop": "Farrell",
        "name": "smartphone super cool",
        "price_current": 1,
        "price_reference": 20,
        "screenshot": 111100011242
    }
]

dt = datetime.fromtimestamp(1658141410673083800)
print(dt.strftime("%d/%m/%Y %H:%M:%S"))