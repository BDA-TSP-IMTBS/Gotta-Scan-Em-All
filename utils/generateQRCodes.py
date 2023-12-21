import json
import random, string
import pyqrcode
from pyqrcode import QRCode
from PIL import Image, ImageDraw

# This program generates QR codes from slugs

DEFAULT_URL = "http://marchedenoel-bda-tmsp.h.minet.net:5000/"

with open("../app/items.json", "r") as f:
  data = json.load(f)

for i in range(len(data['items'])):
  dest = DEFAULT_URL + data['items'][i]['slug']
  myQR = QRCode(dest)
  myQR.png('qrcode'+str(i+1)+'.png', scale=8)
  
  myQR_img = Image.open('qrcode'+str(i+1)+'.png')
  draw = ImageDraw.Draw(myQR_img)

  text_width, text_height = draw.textsize(str(data['items'][i]['id']))
  text_position = ((myQR_img.width - text_width) // 2, myQR_img.height - text_height - 10) # Position pour placer le texte en bas de l'image
  draw.text(text_position, str(data['items'][i]['id']), fill="black") # Ajout du texte à l'image
  myQR_img.save('qrcode'+str(i+1)+'.png')

dest = DEFAULT_URL
myQR = QRCode(dest)
myQR.png('qrcodeBASE.png', scale=8)

myQR_img = Image.open('qrcodeBASE.png')
draw = ImageDraw.Draw(myQR_img)
text_width, text_height = draw.textsize(DEFAULT_URL)
text_position = ((myQR_img.width - text_width) // 2, myQR_img.height - text_height - 10) # Position pour placer le texte en bas de l'image
draw.text(text_position, DEFAULT_URL, fill="black") # Ajout du texte à l'image
myQR_img.save('qrcodeBASE.png')


