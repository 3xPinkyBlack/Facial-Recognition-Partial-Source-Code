import numpy as np
import cv2

FaceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
EyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

WHITE = [125,30,255]

FaceRecognizer = cv2.face.LBPHFaceRecognizer_create()
FaceRecognizer.read('../TrainingData/1622/1622.yml')

UserID = '';  
font = cv2.FONT_HERSHEY_SIMPLEX
while True :  
    ret, DetectFace = cap.read()
    GrayColor = cv2.cvtColor(DetectFace, cv2.COLOR_BGR2GRAY)    
    Faces = FaceDetect.detectMultiScale(DetectFace, 1.3, 5,cv2.CASCADE_FIND_BIGGEST_OBJECT)    
    for (x,y,w,h) in Faces:
        GrayFace = cv2.resize((DetectFace[y: y+h, x: x+w]), (110, 110))
        Eyes = EyeCascade.detectMultiScale(GrayFace)
        for (ex, ey, ew, eh) in Eyes:
            r = 280.0 / GrayColor[y:y+h, x:x+w].shape[1]
            dim = (280, int(GrayColor[y:y+h, x:x+w].shape[0] * r))
                
            resized = cv2.resize(GrayColor[y:y+h, x:x+w], dim, interpolation = cv2.INTER_AREA)
            UserID, conf = FaceRecognizer.predict(resized)
            cv2.line(DetectFace, (x, y), (x + (w/5) ,y), WHITE, 2)
            cv2.line(DetectFace, (x+((w/5)*4), y), (x+w, y), WHITE, 2)
            cv2.line(DetectFace, (x, y), (x, y+(h/5)), WHITE, 2)
            cv2.line(DetectFace, (x+w, y), (x+w, y+(h/5)), WHITE, 2)
            cv2.line(DetectFace, (x, (y+(h/5*4))), (x, y+h), WHITE, 2)
            cv2.line(DetectFace, (x, (y+h)), (x + (w/5) ,y+h), WHITE, 2)
            cv2.line(DetectFace, (x+((w/5)*4), y+h), (x + w, y + h), WHITE, 2)
            cv2.line(DetectFace, (x+w, (y+(h/5*4))), (x+w, y+h), WHITE, 2)
            if UserID == 1622:
                UserID = "Habib Endris"
            # el
            # if UserID == 1163:
            #     UserID = "Elyas Abate"
            else:
                UserID = "Unknown Person"
        
        cv2.putText(DetectFace, str(UserID), (x,y+h), font, 2,(100,200,100), 5, cv2.LINE_AA)
        #elif UserID == 1162 :
        #    UserID = 'Elyas'

      
    cv2.imshow('Face and Eye Detector',DetectFace)
    k = cv2.waitKey(1);
    if k == ord('q') :
        break

cap.release()
cv2.destroyAllWindows()
