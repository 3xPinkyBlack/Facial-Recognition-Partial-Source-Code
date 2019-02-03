import MySQLdb
import datetime

now = datetime.datetime.now()
db = MySQLdb.connect("localhost","root","","cafepro")
cursor = db.cursor()

def toDayCheater():
    sel = "SELECT * FROM cheateruser WHERE userMonth="+str(now.month)+" and userDate="+str(now.day)

    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        print("User ID: "+row[0]+" and UserImageName: "+row[4])

def breakfastCheater():
    sel = "SELECT * FROM cheateruser WHERE breakfast=1 and userMonth="+str(now.month)+" and userDate="+str(now.day)

    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        print("User ID: "+row[0]+" and UserImageName: "+row[4])

def launchCheater():
    sel = "SELECT * FROM cheateruser WHERE launch=1 and userMonth="+str(now.month)+" and userDate="+str(now.day)
        
    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        print("User ID: "+row[0]+" and UserImageName: "+row[4])

def dinnerCheater():
    sel = "SELECT * FROM cheateruser WHERE dinner=1 and userMonth="+str(now.month)+" and userDate="+str(now.day)

    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        print("User ID: "+row[0]+" and UserImageName: "+row[4])

def thisMonthCheater():
    sel = "SELECT * FROM cheateruser WHERE userMonth="+str(now.month)

    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        print("User ID: "+row[0]+" and UserImageName: "+row[4])

def thisYearCheater():
    sel = "SELECT * FROM cheateruser"

    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        print("User ID: "+row[0]+" and UserImageName: "+row[4])
