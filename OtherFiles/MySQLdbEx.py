import MySQLdb
import datetime

db = MySQLdb.connect("localhost","root","","cafepro")
cursor = db.cursor()

now = datetime.datetime.now()
QRCode = "1622"

# sql = "SELECT * FROM cafeuser WHERE QrNum='1622' and userMonth="+str(now.month)+" and userDate="+str(now.day)
# cursor.execute(sql)
# db.commit()  
# row = cursor.fetchone()

# if len(row) != 0:
# 	print("Congratulation The Row is Not Empty")
# 	print("There Are ",len(row)," Rows Detected")
# else:
# 	print("Oh! Error No Row is Detected")

def mealTimeCheck():
    now = datetime.datetime.now()
    mealTime = 0

    if now.hour >= 6 and now.hour <= 8: 
        mealTime = 6
    elif now.hour >= 11 and now.hour <= 13:
        mealTime = 7
    elif now.hour >= 17 and now.hour <= 19:
        mealTime = 8
    
    return mealTime

sql = "SELECT * FROM cheateruser WHERE userMonth="+str(now.month)+" AND userDate="+str(now.day)
cursor.execute(sql)
db.commit()  
row = cursor.rowcount

mealtime = mealTimeCheck() - 4

numUser = 0

if int(row) != 0:
    print "Someone Found in The Database"
    print str(int(row) + 2)+" Rows Detected"
    # print row[mealtime]
else :
	print "You Are Not Lucky No One is in The Database"