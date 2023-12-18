import json
import random, string
import pyqrcode
from pyqrcode import QRCode

# This program generates QR codes from slugs

DEFAULT_URL = "http://157.159.195.109:5000/"

with open("../app/items.json", "r") as f:
  data = json.load(f)

for i in range(len(data['items'])):
  dest = DEFAULT_URL + data['items'][i]['slug']
  myQR = QRCode(dest)
  myQR.png('qrcode'+str(i+1)+'.png', scale=8)
  
dest = DEFAULT_URL
myQR = QRCode(dest)
myQR.png('qrcodeBASE.png', scale=8)
    


