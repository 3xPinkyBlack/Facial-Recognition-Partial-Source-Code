import cv2
import zbar
from PIL import Image

img = cv2.imread("QRDatas/0050.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
image = Image.fromarray(gray)
width, height = image.size
zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

scanner = zbar.ImageScanner()
scanner.scan(zbar_image)
for decoded in zbar_image:
	if decoded.data is not None:
		print decoded.data