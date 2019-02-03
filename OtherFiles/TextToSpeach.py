import pyttsx3
import MySQLdb
import datetime

engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_HAZEL_11.0')

db = MySQLdb.connect("localhost","root","","cafepro")
cursor = db.cursor()

def mealTypeCheck():
    now = datetime.datetime.now()
    mealType = ""
    mealTime = 0

    if now.hour >= 19 and now.hour < 21: 
        mealType = "Breakfast"
        mealTime = 6
    elif now.hour >= 0 and now.hour < 2:
        mealType = "Lunch"
        mealTime = 7
    elif now.hour >= 6 and now.hour < 8:
        mealType = "Dinner"
        mealTime = 8
    
    return mealTime, mealType

sql = "SELECT * FROM cafeuser WHERE QrNum=1622"
cursor.execute(sql)
db.commit()  
row = cursor.fetchone()
cursor.close()

mealTime, mealType = mealTypeCheck()

if row[mealTime] == 0:
    engine.say('Hello '+row[1]+' '+row[2]+' Have A Good '+mealType)
elif row[mealTime] == 1:
    engine.say(row[1]+' '+row[2]+' I Think You Are Cheating On Me')
elif mealTime == 0:
    engine.say('Dear '+row[1]+' '+row[2]+' The Cafe is Still Closed')

engine.runAndWait()
