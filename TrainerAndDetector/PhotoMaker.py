import numpy as np
import cv2

FaceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
EyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

sampleNumber = 0

while sampleNumber < 100:
    ret, DetectFace = cap.read()
    GrayColor = cv2.cvtColor(DetectFace, cv2.COLOR_BGR2GRAY)    
    Faces = FaceDetect.detectMultiScale(DetectFace, 1.3, 5)    
    for (x,y,w,h) in Faces:
        GrayFace = cv2.resize((GrayColor[y: y+h, x: x+w]), (110, 110))
        Eyes = EyeCascade.detectMultiScale(GrayFace)
        for (ex, ey, ew, eh) in Eyes:
            sampleNumber = sampleNumber+1;
            cv2.line(GrayColor, (x, y), (x + (w/5) ,y), (255,255,255), 2)
            cv2.line(GrayColor, (x+((w/5)*4), y), (x+w, y), (255,255,255), 2)
            cv2.line(GrayColor, (x, y), (x, y+(h/5)), (255,255,255), 2)
            cv2.line(GrayColor, (x+w, y), (x+w, y+(h/5)), (255,255,255), 2)
            cv2.line(GrayColor, (x, (y+(h/5*4))), (x, y+h), (255,255,255), 2)
            cv2.line(GrayColor, (x, (y+h)), (x + (w/5) ,y+h), (255,255,255), 2)
            cv2.line(GrayColor, (x+((w/5)*4), y+h), (x + w, y + h), (255,255,255), 2)
            cv2.line(GrayColor, (x+w, (y+(h/5*4))), (x+w, y+h), (255,255,255), 2)
            cv2.imwrite('FLSPhoto/User.9999.'+str(sampleNumber)+'.png',GrayColor[y:y+h, x:x+w])  
        cv2.waitKey(1);
    cv2.imshow('Face and Eye Detector',GrayColor)