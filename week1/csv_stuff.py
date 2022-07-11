import csv
import json

file_name = 'vandenborre'

products = {} # Retrieved information from database



headers = ['category', 'product name', 'url', 'image path', 'date', 'reference price']

file = open('data.json')

products = json.load(file)


def create_csv_from_products(products):

    with open("{}.csv".format(file_name), 'w') as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow(headers)
   
        for product in products:

            writer.writerow([product['category'], product['name'], product['url'], product['url'], product['date'], product['reference price']])

create_csv_from_products(products)