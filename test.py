import cv2

vid = cv2.VideoCapture(0)

while True:
	ret, img = vid.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)