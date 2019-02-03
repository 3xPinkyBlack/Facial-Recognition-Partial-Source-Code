import numpy as np
import cv2

WHITE = [255, 255, 255]

class VideoCamera(object):
    def __init__(self):
        self.FaceDetect = cv2.CascadeClassifier('HaarCascade/haarcascade_frontalface_default.xml')
        self.EyeCascade = cv2.CascadeClassifier('HaarCascade/haarcascade_eye.xml')
        self.video = cv2.VideoCapture(1)        
        
        self.FaceRecognizer = cv2.face.LBPHFaceRecognizer_create()
        self.FaceRecognizer.read('TrainingData/TrainingData.yml')
        self.UserID = 0;
        self.font = cv2.FONT_HERSHEY_SIMPLEX
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, DetectFace = self.video.read()   
        GrayColor = cv2.cvtColor(DetectFace, cv2.COLOR_BGR2GRAY) 
        Faces = self.FaceDetect.detectMultiScale(GrayColor, 1.3, 5)

        for (x,y,w,h) in Faces:
            GrayFace = cv2.resize((GrayColor[y: y+h, x: x+w]), (110, 110))
            Eyes = self.EyeCascade.detectMultiScale(GrayFace)
            for (ex, ey, ew, eh) in Eyes:
                self.UserID, conf = self.FaceRecognizer.predict(GrayFace)

                if self.UserID != 0:
                    if self.UserID == 1622:
                        NAME = 'Cafe User - Habib Endris'
                    elif self.UserID == 1162:
                        NAME = 'Cafe User - Elyas Abate'
                    elif self.UserID == 99999:
                        self.UserID = 0
                        NAME = 'UnRecognized User'
                else :
                    self.UserID = 0
                    NAME = 'UnRecognized User'

                Name_y_pos = y - 10
                Name_X_pos = x + w/2 - (len(NAME)*7/2)

                if Name_X_pos < 0:
                    Name_X_pos = 0
                elif (Name_X_pos +10 + (len(NAME) * 7) > GrayColor.shape[1]):
                    Name_X_pos= Name_X_pos - (Name_X_pos +10 + (len(NAME) * 7) - (GrayColor.shape[1]))
                if Name_y_pos < 0:
                    Name_y_pos = Name_y_pos = y + h + 10

                cv2.line(GrayColor, (x, y), (x + (w/5) ,y), WHITE, 2)
                cv2.line(GrayColor, (x+((w/5)*4), y), (x+w, y), WHITE, 2)
                cv2.line(GrayColor, (x, y), (x, y+(h/5)), WHITE, 2)
                cv2.line(GrayColor, (x+w, y), (x+w, y+(h/5)), WHITE, 2)
                cv2.line(GrayColor, (x, (y+(h/5*4))), (x, y+h), WHITE, 2)
                cv2.line(GrayColor, (x, (y+h)), (x + (w/5) ,y+h), WHITE, 2)
                cv2.line(GrayColor, (x+((w/5)*4), y+h), (x + w, y + h), WHITE, 2)
                cv2.line(GrayColor, (x+w, (y+(h/5*4))), (x+w, y+h), WHITE, 2)
    
                cv2.rectangle(GrayColor, (Name_X_pos-10, Name_y_pos-25), (Name_X_pos +10 + (len(NAME) * 7), Name_y_pos-1), (0,0,0), -2)           # Draw a Black Rectangle over the face frame
                cv2.rectangle(GrayColor, (Name_X_pos-10, Name_y_pos-25), (Name_X_pos +10 + (len(NAME) * 7), Name_y_pos-1), WHITE, 1) 
                cv2.putText(GrayColor, NAME, (Name_X_pos, Name_y_pos - 10), cv2.FONT_HERSHEY_DUPLEX, .4, WHITE)  

        ret, jpeg = cv2.imencode('.jpg', GrayColor)
        return jpeg.tobytes()
