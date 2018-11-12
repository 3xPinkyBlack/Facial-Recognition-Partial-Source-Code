import mainCamera as MC
from flask import Flask, render_template, Response
import cv2
import zbar
import datetime
from PIL import Image
import time
import os
import pyttsx3
import MySQLdb

os.system("cls")
capVideo = cv2.VideoCapture(1)

engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')

db = MySQLdb.connect("localhost","root","","cafepro")
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    global QRCode
    global isEaten

    while True:
        isEaten = 0
        now = datetime.datetime.now()
        if (now.hour >= 19 and now.hour < 21) or (now.hour >= 0 and now.hour < 2) or (now.hour >= 6 and now.hour < 8):
            isQrDetected = False
            frame = MC.readCamera()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            if MC.isDetected == True:
                engine.say('Position Your Face Correctly')
                engine.runAndWait()
                fDet = 0
                while fDet <= 10:
                    fDet = fDet + 1
                    frame = MC.readCamera()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') 

                    blackImage = MC.blackImage

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
                            engine.say('You Entered Invalid Meal Card Code')
                            engine.runAndWait()

                        ret, jpeg = cv2.imencode('.jpg', blackImage)
                        jpeg = jpeg.tobytes()

                    ret, jpeg = cv2.imencode('.jpg', blackImage)
                    jpeg = jpeg.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n') 

                ret, jpeg = cv2.imencode('.jpg', blackImage)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n') 

                isEaten = MC.checkUser(QRCode, MC.GrayColorImage)

                UserState = None

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
                        engine.say(row[1]+' '+row[2]+' You Are Cheating On Me')
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

            ret, frame = cv2.imencode('.jpg', ImageNotOpened)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/admin/')
def admin():
    return render_template('admin/index.html')

@app.route('/admin/illAct/')
def cheaters():
    return render_template('admin/illAct/index.html')

@app.route('/admin/nonCafe/')
def nonCafe():
    return render_template('admin/nonCafe/index.html')

@app.route('/admin/todayAct/')
def toDayAct():
    return render_template('admin/todayAct/index.html')

@app.route('/admin/userStat/')
def userStat():
    return render_template('admin/userStat/index.html')

@app.route('/admin/regUser/')
def regUser():
    return render_template('admin/regUser/index.html')

if __name__ == '__main__':
    app.run()
