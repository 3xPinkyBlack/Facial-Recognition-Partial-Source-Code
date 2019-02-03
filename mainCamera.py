import numpy as np
import cv2
import datetime
import MySQLdb
import zbar
from PIL import Image
import os
import pyttsx3
import sys

FaceDetect = cv2.CascadeClassifier('HaarCascade/haarcascade_frontalface_default.xml')
EyeCascade = cv2.CascadeClassifier('HaarCascade/haarcascade_eye.xml')  
FaceRecognizer = cv2.face.LBPHFaceRecognizer_create()

isDetected = False
WHITE = [255, 255, 255]
capVideo = cv2.VideoCapture(1)  
font = cv2.FONT_HERSHEY_SIMPLEX

NormalGrayFace = None
NewBlackImage = cv2.imread("BlackImage.jpg")

def readCamera():
    global blackImage
    global isDetected
    global GrayFace
    global GrayColorImage
    global FullChImage

    blackImage = cv2.imread("BlackImage.jpg")
    now1 = datetime.datetime.now()                   #Get All Current Day Values 
    
    isDetected = False
    ret, DetectFace = capVideo.read()                #Split Video In To Frames
    GrayColor = cv2.cvtColor(DetectFace, cv2.COLOR_BGR2GRAY)        #Make The Frame Gray
    FullChImage = GrayColor
    Faces = FaceDetect.detectMultiScale(GrayColor, 1.3, 5)          #Detect Faces
    
    for (x,y,w,h) in Faces:
        GrayFace = cv2.resize((GrayColor[y: y+h, x: x+w]), (110, 110))
        GrayColorImage = GrayColor[y:y+h, x:x+w]
        Eyes = EyeCascade.detectMultiScale(GrayFace)
        for (ex, ey, ew, eh) in Eyes:
            isDetected = True
            NAME = "Face Detected"
            drawRectangle(DetectFace,x,y,w,h,NAME)
            
    cv2.putText(DetectFace,'Position Your Face Correctly',(10,50),font, 0.5,(70,0,100),2)
    rows = 480
    cols = 640
    channels = 3

    roi = blackImage[0:rows, 0:cols ]
    ret, mask = cv2.threshold(GrayColor, 0, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

    img2_fg = cv2.bitwise_and(DetectFace,DetectFace,mask = mask)

    dst = cv2.add(img1_bg,img2_fg)
    blackImage[0:rows, 0:cols ] = dst

    CurrTime = str(now1.hour)+":"+str(now1.minute)+":"+str(now1.second)
    cv2.putText(blackImage,CurrTime,(500,50), font, 0.5,(70,0,100),2)

    
    ret, jpeg = cv2.imencode(".jpg", blackImage)
    
    return jpeg.tobytes()

def checkUser(QRCode):
    userDir = "TrainingData/"+QRCode+"/"+QRCode+".yml"
    try:
        FaceRecognizer.read(userDir)
        r = 280.0 / , GrayColorImage.shape[1]
        dim = (280, int(GrayColorImage.shape[0] * r))
                
        resized = cv2.resize(GrayColorImage, dim, interpolation = cv2.INTER_AREA)
        userQRCode, conf = FaceRecognizer.predict(resized)

        if userQRCode == int(QRCode):
            isEaten = checkMeal(QRCode)
        else :
            useOtherMealCard(QRCode)
            isEaten = 3

        return isEaten
    except:
        print(sys.exc_info()[0])
        return 4
    
def mealTimeCheck():
    now = datetime.datetime.now()
    mealTime = 0

    if now.hour >= 19 and now.hour < 21: 
        mealTime = 6
    elif now.hour >= 0 and now.hour <= 5:
        mealTime = 7
    elif now.hour >= 6 and now.hour < 8:
        mealTime = 8
    
    return mealTime

def mealTypeCheck():
    now = datetime.datetime.now()
    mealType = ""

    if now.hour >= 19 and now.hour < 21: 
        mealType = "Breakfast"
    elif now.hour >= 0 and now.hour <= 5:
        mealType = "Lunch"
    elif now.hour >= 6 and now.hour < 8:
        mealType = "Dinner"
    
    return mealType

def checkMeal(QRCode):
    db = MySQLdb.connect("localhost","root","","cafepro")
    cursor = db.cursor()
    now = datetime.datetime.now()

    sql = "SELECT * FROM cafeuser WHERE QrNum="+QRCode+" and userMonth="+str(now.month)+" and userDate="+str(now.day)
    cursor.execute(sql)
    db.commit()  
    row = cursor.fetchone()
    cursor.close()

    mealTime = mealTimeCheck()

    if row is not None:
        if row[9] == 0:
            if row[mealTime] == 1:
                triedMoreTimes(QRCode)
                isEaten = 2
            else :
                updateToAte(QRCode)
                isEaten = 1
        else:
            isEaten = 5
    else :
        if row[9] == 0:
            updateToAte(QRCode)
            isEaten = 1
        else:
            isEaten = 5
    
    return isEaten

def NotMealType(mealType):
    Breakfast = "Breakfast"
    Lunch = "Lunch"
    Dinner = "Dinner"

    if mealType == Breakfast:
        return Lunch, Dinner
    elif mealType == Lunch:
        return Breakfast, Dinner
    else:
        return Breakfast, Lunch

def triedMoreTimes(QRCode):
    now = datetime.datetime.now()
    mealType = mealTypeCheck()
    mealTime = mealTimeCheck()

    db = MySQLdb.connect("localhost","root","","cafepro")

    chNum = 1
    chDir = "CheaterImage/"+str(now.year)+str(now.month)+str(now.day)

    cursor = db.cursor()
    selectFromCheater = "SELECT * FROM cheateruser WHERE userMonth="+str(now.month)+" AND userDate="+str(now.day)
    cursor.execute(selectFromCheater)
    db.commit()
    rowcount = cursor.rowcount
    cursor.close()

    if not os.path.exists(chDir):
        os.makedirs(chDir)

    chNum = int(rowcount) + 1

    imgName = str(now.year)+str(now.month)+str(now.day)+str(chNum)
    imgDir = chDir+"/"+imgName+".png"

    cv2.imwrite(imgDir,FullChImage)

    mealType2, mealType3 = NotMealType(mealType)

    cursor = db.cursor()
    TriedUser = "INSERT INTO cheateruser(QrNum,userMonth,userDate,ImageName,"+mealType+","+mealType2+","+mealType3+",Tried,OtherMeal,Disabled) VALUES("+QRCode+","+str(now.month)+","+str(now.day)+","+imgName+",1,0,0,1,0,0)"
    cursor.execute(TriedUser)
    db.commit()
    cursor.close()

def useOtherMealCard(QRCode):
    now = datetime.datetime.now()

    mealType = mealTypeCheck()
    mealTime = mealTimeCheck()

    db = MySQLdb.connect("localhost","root","","cafepro")

    chNum = 1
    chDir = "CheaterImage/"+str(now.year)+str(now.month)+str(now.day)

    cursor = db.cursor()
    selectFromCheater = "SELECT * FROM cheateruser WHERE userMonth="+str(now.month)+" AND userDate="+str(now.day)
    cursor.execute(selectFromCheater)
    db.commit()
    rowcount = cursor.rowcount
    cursor.close()

    if not os.path.exists(chDir):
        os.makedirs(chDir)

    chNum = int(rowcount) + 1

    imgName = str(now.year)+str(now.month)+str(now.day)+str(chNum)
    imgDir = chDir+"/"+imgName+".png"

    cv2.imwrite(imgDir,FullChImage)

    mealType2, mealType3 = NotMealType(mealType)

    cursor = db.cursor()
    OtherPersonMeal = "INSERT INTO cheateruser(QrNum,userMonth,userDate,ImageName,"+mealType+","+mealType2+","+mealType3+",Tried,OtherMeal,Disabled) VALUES("+QRCode+","+str(now.month)+","+str(now.day)+","+imgName+",1,0,0,0,1,0)"
    cursor.execute(OtherPersonMeal)
    db.commit()
    cursor.close()



def updateToAte(QRCode):
    now = datetime.datetime.now()

    mealType = mealTypeCheck()
    mealTime = mealTimeCheck()

    db = MySQLdb.connect("localhost","root","","cafepro")

    cursor = db.cursor()
    UpdateCafeUser = "UPDATE cafeuser SET userMonth="+str(now.month)+",userDate="+str(now.day)+","+mealType+"=1 WHERE QrNum="+QRCode
    cursor.execute(UpdateCafeUser)
    db.commit()
    cursor.close()

    cursor = db.cursor()
    selectFromMealDate = "SELECT * FROM mealtime WHERE mealMonth="+str(now.month)+" AND mealDate="+str(now.day)
    cursor.execute(selectFromMealDate)
    db.commit()  
    row = cursor.fetchone()
    cursor.close()

    mealTime = mealTime - 4 

    numUser = 0
    if row is not None:
        numUser = row[mealTime] + 1

        cursor = db.cursor()
        UpdateMealDate = "UPDATE mealtime SET "+mealType+"="+str(numUser)+" WHERE mealMonth="+str(now.month)+" AND mealDate="+str(now.day)
        cursor.execute(UpdateMealDate)
        db.commit()
        cursor.close()
    else:
        cursor = db.cursor()
        UpdateMealDate = "INSERT INTO mealtime (mealMonth, mealDate, Breakfast, Lunch, Dinner) Values("+str(now.month)+","+str(now.day)+",0,0,0)"
        cursor.execute(UpdateMealDate)
        db.commit()
        cursor.close()

        cursor = db.cursor()
        UpdateMealDate = "UPDATE mealtime SET "+mealType+"=1 WHERE mealMonth="+str(now.month)+" AND mealDate="+str(now.day)
        cursor.execute(UpdateMealDate)
        db.commit()
        cursor.close()

def drawRectangle(GrayColor,x,y,w,h,NAME):
    NamePosY = y - 10
    NamePosX = x + w/2 - (len(NAME)*7/2)

    if NamePosX < 0:
        NamePosX = 0
    elif (NamePosX +10 + (len(NAME) * 7) > GrayColor.shape[1]):
        NamePosX= NamePosX - (NamePosX +10 + (len(NAME) * 7) - (GrayColor.shape[1]))
    if NamePosY < 0:
        NamePosY = NamePosY = y + h + 10

    cv2.line(GrayColor, (x, y), (x + (w/5) ,y), WHITE, 2)
    cv2.line(GrayColor, (x+((w/5)*4), y), (x+w, y), WHITE, 2)
    cv2.line(GrayColor, (x, y), (x, y+(h/5)), WHITE, 2)
    cv2.line(GrayColor, (x+w, y), (x+w, y+(h/5)), WHITE, 2)
    cv2.line(GrayColor, (x, (y+(h/5*4))), (x, y+h), WHITE, 2)
    cv2.line(GrayColor, (x, (y+h)), (x + (w/5) ,y+h), WHITE, 2)
    cv2.line(GrayColor, (x+((w/5)*4), y+h), (x + w, y + h), WHITE, 2)
    cv2.line(GrayColor, (x+w, (y+(h/5*4))), (x+w, y+h), WHITE, 2)

    cv2.rectangle(GrayColor, (NamePosX-10, NamePosY-25), (NamePosX +10 + (len(NAME) * 7), NamePosY-1), (100,0,70), -2)
    cv2.rectangle(GrayColor, (NamePosX-10, NamePosY-25), (NamePosX +10 + (len(NAME) * 7), NamePosY-1), WHITE, 1) 
    cv2.putText(GrayColor, NAME, (NamePosX, NamePosY - 10), cv2.FONT_HERSHEY_DUPLEX, .4, WHITE)  

    return GrayColor
