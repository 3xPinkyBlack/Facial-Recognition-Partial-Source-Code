import numpy as np
import cv2

img = np.zeros((768,1366,1), np.uint8)
cv2.imwrite('Black Image.jpg',img)
