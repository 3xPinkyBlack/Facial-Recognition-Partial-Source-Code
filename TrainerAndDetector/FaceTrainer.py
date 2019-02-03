import os
import cv2
import numpy as np
from PIL import Image
import MySQLdb
import datetime
import time

FaceRecognizer = cv2.face.LBPHFaceRecognizer_create()

def isPathExist(path,UserIDNum):
    a = 0
    dir = os.path.dirname(path)
    if os.path.exists(dir):
        tPath = "../TrainingData/"+str(UserIDNum)+"/"
        tDir = os.path.dirname(tPath)
        if not os.path.exists(tDir):
            os.makedirs(tDir)
            a = 1
        else:
            a = 2
    return a

def getUserImage(UserDataPath) :
    UserImagePath = [os.path.join(UserDataPath, f) for f in os.listdir(UserDataPath)]
    UserFaces = []
    UserIDs = []
    for ImagePath in UserImagePath :
        UserFaceImage = Image.open(ImagePath).convert('L')
        FaceNp = np.array(UserFaceImage, 'uint8')
        ID = int(os.path.split(ImagePath)[-1].split('.')[1])
        UserFaces.append(FaceNp)
        UserIDs.append(ID)
        cv2.waitKey(10)
    return np.array(UserIDs), UserFaces

conReg = 1

while conReg == 1:
    while True:
        #os.system("cls")
        global UserDataPath
        global UserIDNum
        UserIDNum = input("Enter The User QRCode Number: ")
        UserDataPath = 'UserData/'+str(UserIDNum)+"/"
        
        if isPathExist(UserDataPath,UserIDNum) == 1:
            break
        elif isPathExist(UserDataPath,UserIDNum) == 2:
            print("The User Is Already Registered")
        else:
            print("Please Take User A Photo Before Training")
        time.sleep(1)

    FName = str(raw_input("Enter The First Name  : "))
    MName = str(raw_input("Enter The Middle Name : "))
    LName = str(raw_input("Enter Last Name       : "))

    UserIDs, UserFaces = getUserImage(UserDataPath)
    print("Please Wait Until The User Registered")

    try:
        FaceRecognizer.train(UserFaces, np.array(UserIDs))
        FaceRecognizer.save('../TrainingData/'+str(UserIDNum)+'/'+str(UserIDNum)+'.yml')
        print("Sucessfully Saved Trained Data")

        db = MySQLdb.connect("localhost","root","","cafepro")
        cursor = db.cursor()
        now = datetime.datetime.now()

        sql = "INSERT INTO cafeuser(QrNum,FName,MName,LName,userMonth,userDate,Breakfast,Lunch,Dinner,Disabled) VALUES("+str(UserIDNum)+",'"+FName+"','"+MName+"','"+LName+"',"+str(now.month)+","+str(now.day)+",0,0,0,0)"
        cursor.execute(sql)
        db.commit()  
        cursor.close()
        print("The User Is Already Registered")
        print("He Can Use Cafe From Now")
    except :
        print("Error Occured Try To Register Again")
