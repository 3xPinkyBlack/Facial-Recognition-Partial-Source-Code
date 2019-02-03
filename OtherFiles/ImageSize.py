import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
GrayColor = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cv2.imwrite("HabibEndrisMohammed.png", frame)

img = cv2.imread("HabibEndrisMohammed.png")

print(img.shape)
