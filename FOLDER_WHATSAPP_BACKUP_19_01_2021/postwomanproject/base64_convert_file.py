import base64
URL='C://Users//harshita.agarwal//Downloads//WhatsApp.jpeg'
data = open(URL, "rb").read()
encoded = base64.b64encode(data)
print(encoded)
f = open('image.txt', 'w')
f.write(str(encoded))
f.close()