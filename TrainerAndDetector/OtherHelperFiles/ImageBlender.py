import cv2 as cv

BlackImage = cv.imread('BlackImage.jpg')
FaceImage = cv.imread('User.1622.2.png')


rows,cols,channels = FaceImage.shape
roi = BlackImage[0:rows, 0:cols ]

img2gray = cv.cvtColor(FaceImage,cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)

img1_bg = cv.bitwise_and(roi,roi,mask = mask_inv)

img2_fg = cv.bitwise_and(FaceImage,FaceImage,mask = mask)

dst = cv.add(img1_bg,img2_fg)
BlackImage[0:rows, 0:cols ] = dst

cv.imshow('Concatenated Images',BlackImage)
