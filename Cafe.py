import mainCameraPY as MC
import cv2
import zbar
import datetime
from PIL import Image
import time
import os
import pyttsx3
import MySQLdb

os.system("cls")
capVideo = cv2.VideoCapture(0)

engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')

db = MySQLdb.connect("localhost","root","","cafepro")
now = datetime.datetime.now()

def MealApp():
    global QRCode
    global isEaten

    while True:
        isEaten = 0
        now = datetime.datetime.now()
        if (now.hour >= 16 and now.hour < 18) or (now.hour >= 0 and now.hour <= 5) or (now.hour >= 4 and now.hour < 8):
            isQrDetected = False
            frame = MC.readCamera()
	    cv2.rectangle(frame,(1200,500),(500,730),(100,70,0),-2)
	    cv2.putText(frame,"Current Date : "+str(now.year)+"-"+str(now.month)+"-"+str(now.day),(550,550),MC.font, 1,(70,0,100),2)
	    cv2.putText(frame,"BreakFast Eaten User : "+str(MC.BreakfastEaten),(600,600),MC.font, 0.8,(255, 255, 255),2)
	    cv2.putText(frame,"    Lunch Eaten User : "+str(MC.LunchEaten),(600,630),MC.font, 0.8,(255, 255, 255),2)
	    cv2.putText(frame,"    Dinner Eaten User : "+str(MC.DinnerEaten),(600,660),MC.font, 0.8,(255, 255, 255),2)
            cv2.imshow("Face Recognition Cafe Monitering System",frame)
            cv2.waitKey(1)


            if MC.isDetected == True:
                i = 0;
                while i < 10:
                    frame = MC.readCamera()
                    cv2.imshow("Face Recognition Cafe Monitering System",frame)
                    cv2.waitKey(1)
                    i = i + 1
                    blackImage = MC.blackImage
		cv2.rectangle(blackImage,(1200,500),(500,730),(100,70,0),-2)
		cv2.putText(frame,"Current Date : "+str(now.year)+"-"+str(now.month)+"-"+str(now.day),(550,550),MC.font, 1,(70,0,100),2)
		cv2.putText(blackImage,"BreakFast Eaten User : "+str(MC.BreakfastEaten),(600,600),MC.font, 0.8,(255, 255, 255),2)
		cv2.putText(blackImage,"    Lunch Eaten User : "+str(MC.LunchEaten),(600,630),MC.font, 0.8,(255, 255, 255),2)
		cv2.putText(blackImage,"    Dinner Eaten User : "+str(MC.DinnerEaten),(600,660),MC.font, 0.8,(255, 255, 255),2)

                QRDetect = False
                while QRDetect == False:
                    now1 = datetime.datetime.now()   
                    ret, img = capVideo.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    image = Image.fromarray(gray)
                    width, height = image.size
                    zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

                    scanner = zbar.ImageScanner()
                    scanner.scan(zbar_image)
                    for decoded in zbar_image:
                        if decoded.data is not None:
                            QRCode = decoded.data
                            QRDetect = True


                    rows = 480
                    cols = 640
                    channels = 3

                    roi = blackImage[0:rows, 0:cols ]
                    ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
                    mask_inv = cv2.bitwise_not(mask)

                    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
                    img2_fg = cv2.bitwise_and(img,img,mask = mask)

                    dst = cv2.add(img1_bg,img2_fg)
                    blackImage[0:rows, 725:cols+725 ] = dst


                    CurrTime = str(now1.hour)+":"+str(now1.minute)+":"+str(now1.second)
                    cv2.putText(blackImage,'Position Your QRCode Correctly',(750,50),MC.font, 0.5,(70,0,100),2)
                    cv2.putText(blackImage,CurrTime,(1250,50), MC.font, 0.5,(70,0,100),2)
                    
                    if QRDetect == True:
                        try:
                            if int(QRCode) <= 0 and int(QRCode) >= 9999:
                                QRDetect = False
                                engine.say('You Entered Invalid Meal Card Code')
                                engine.runAndWait()
                            else:
                                engine.say('Meal Card Detected')
                                engine.runAndWait()
                        except:
                            QRDetect = False
                            engine.say('You Entered Invalid Meal Card Code')
                            engine.runAndWait()
                            
                    cv2.imshow("Face Recognition Cafe Monitering System",blackImage)
                    cv2.waitKey(1)


                cv2.imshow("Face Recognition Cafe Monitering System",blackImage)
                cv2.waitKey(1)

                cv2.putText(blackImage,'Position Your QRCode Correctly('+ QRCode +')',(750,50),MC.font, 0.5,(70,0,100),2)
                isEaten = MC.checkUser(QRCode)

                if isEaten == 1 or isEaten == 2:
                    cursor = db.cursor()
                    sql = "SELECT * FROM cafeuser WHERE QrNum="+QRCode
                    cursor.execute(sql)
                    db.commit()  
                    row = cursor.fetchone()
                    cursor.close()

                    mealType = MC.mealTypeCheck()

                    if isEaten == 1:
                        engine.say('Hello '+row[1]+' '+row[2]+' Have A Good '+mealType)
                        engine.runAndWait()

                    else:
                        engine.say(row[1]+' '+row[2]+' You Are Cheating')
                        engine.runAndWait()

                elif isEaten == 3:
                    engine.say('You Have Stolen Other Persons Meal Card')
                    engine.runAndWait()

                elif isEaten == 4:
                    engine.say('You Are Using Invalid Meal Card')
                    engine.runAndWait()

                elif isEaten == 5:
                    engine.say('You Meal Card is Disabled Please ReEnabled it Again')
                    engine.runAndWait()

        else :
            ImageNotOpened = cv2.imread("BlackImage.jpg")
            CurrTime = "Cafe is Closed "
            cv2.putText(ImageNotOpened,CurrTime,(300,400), MC.font, 2,(25,255,255),2)
            CurrTime = "Current Time "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)
            cv2.putText(ImageNotOpened,CurrTime,(400,500), MC.font, 2,(25,255,255),2)

            MC.readCamera()
            if MC.isDetected == True:
                engine.say('Dear User The Cafe is Still Closed')
                engine.runAndWait()

            cv2.imshow("Face Recognition Cafe Monitering System",ImageNotOpened)
            cv2.waitKey(1)

MealApp()
