import numpy as np
import cv2
import os
import shutil
import time

FaceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
EyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

WHITE = [125,30,255]
sampleNumber = 0;

userIDNum = None

def isPathExist(path):
    a = 0
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        a = 1
    return a

b = 0

aa = 0
while aa == 0:
    while b == 0:
        os.system("cls")
        userIDNum = input("Enter The User Identification Number: ")
        
        path = "UserData/"+str(userIDNum)+"/"
        if isPathExist(path) == 1:
            break
            b = 1
        else:
            print("The User is Already Registered")
        time.sleep(1)

    print("Capturing User Face For Registration")
    os.system("cls")

    while sampleNumber < 300:
        ret, DetectFace = cap.read()
        GrayColor = cv2.cvtColor(DetectFace, cv2.COLOR_BGR2GRAY)    
        Faces = FaceDetect.detectMultiScale(DetectFace, 1.3, 5)    
        for (x,y,w,h) in Faces:
            GrayFace = cv2.resize((GrayColor[y: y+h, x: x+w]), (110, 110))
            Eyes = EyeCascade.detectMultiScale(GrayFace)
            for (ex, ey, ew, eh) in Eyes:
                sampleNumber = sampleNumber+1;
                cv2.line(GrayColor, (x, y), (x + (w/5) ,y), WHITE, 2)
                cv2.line(GrayColor, (x+((w/5)*4), y), (x+w, y), WHITE, 2)
                cv2.line(GrayColor, (x, y), (x, y+(h/5)), WHITE, 2)
                cv2.line(GrayColor, (x+w, y), (x+w, y+(h/5)), WHITE, 2)
                cv2.line(GrayColor, (x, (y+(h/5*4))), (x, y+h), WHITE, 2)
                cv2.line(GrayColor, (x, (y+h)), (x + (w/5) ,y+h), WHITE, 2)
                cv2.line(GrayColor, (x+((w/5)*4), y+h), (x + w, y + h), WHITE, 2)
                cv2.line(GrayColor, (x+w, (y+(h/5*4))), (x+w, y+h), WHITE, 2)

                r = 280.0 / GrayColor[y:y+h, x:x+w].shape[1]
                dim = (280, int(GrayColor[y:y+h, x:x+w].shape[0] * r))
                
                # perform the actual resizing of the image and show it
                resized = cv2.resize(GrayColor[y:y+h, x:x+w], dim, interpolation = cv2.INTER_AREA)

                cv2.imwrite('UserData/'+str(userIDNum)+'/User.'+str(userIDNum)+'.'+str(sampleNumber)+'.png',resized)  
        cv2.imshow('Face and Eye Detector',GrayColor)
        cv2.waitKey(1);
    print("Please Wait A Moment")

    imgNum = 1
    while imgNum <= 200:
        if userIDNum != 1622:
            FileName1 = "False/User.9999."+str(imgNum)+".png"
        else:
            FileName1 = "FLS/User.9999."+str(imgNum)+".png"
        
        FileName2 = "UserData/"+str(userIDNum)+"/User.9999."+str(imgNum)+".png"
        shutil.copyfile(FileName1, FileName2)
        imgNum = imgNum + 1

    print("The User Face Captured Sucessfully")
    print("Pease Register The User To The Cafe System")

cap.release()
cv2.destroyAllWindows()
