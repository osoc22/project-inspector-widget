from base64 import b64decode
import csv
from io import BytesIO, StringIO
import json
import zipfile

with open('data.json') as datafile:
    data = json.load(datafile)
    with zipfile.ZipFile('test.zip', 'w') as zip_file:
        csv_output = StringIO()
        csv_header = ['product name', 'current price', 'reference price', 'image']
        csv_writer = csv.writer(csv_output, delimiter=';')
        csv_writer.writerow(csv_header)
        for product in data:
            csv_writer.writerow([product['product_name'], product['price_current'], product['price_reference'], "=HYPERLINK(\"" + product['screenshot_id'] + '.png' + "\";\"Image\")"])
            img_buffer = BytesIO(b64decode(product['screenshot']))
            zip_file.writestr(product['screenshot_id']+'.png', img_buffer.read())
        csv_output.seek(0)
        zip_file.writestr('info.csv', csv_output.read())

