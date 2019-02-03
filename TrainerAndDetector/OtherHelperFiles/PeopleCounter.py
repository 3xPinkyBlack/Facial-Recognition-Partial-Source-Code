import cv2
import numpy as np

DetectFace = cv2.imread("User.1622.2.png")

ret, thresh1 = cv2.threshold(DetectFace,127,255,cv2.THRESH_BINARY)
kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(DetectFace,kernel,iterations = 1)
dilation = cv2.dilate(DetectFace,kernel,iterations = 1)
cv2.imwrite('Erosion Image Example.jpg',erosion)
cv2.imwrite('Dilation Image Example.jpg',dilation)

kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
cv2.imwrite("letters_closing.png",closing)
cv2.imwrite("letters_opening.png",opening)
