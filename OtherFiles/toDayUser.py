import MySQLdb
import datetime

now = datetime.datetime.now()
db = MySQLdb.connect("localhost","root","","cafepro")
cursor = db.cursor()

def toDayUser():
    sel = "SELECT * FROM cafeuser WHERE userMonth="+str(now.month)+" and userDate="+str(now.day)

    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        totalMeal = int(row[6])+int(row[7])+int(row[8])
        print(row[0]+"\t"+row[1]+" "+row[2]+" "+row[3]+"\t"+str(totalMeal))
    
def breakfastUser():
    sel = "SELECT * FROM cafeuser WHERE Breakfast=1 and userMonth="+str(now.month)+" and userDate="+str(now.day)

    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        print(row[0]+"\t"+row[1]+" "+row[2]+" "+row[3]+"\tBreakFast")

def launchUser():
    sel = "SELECT * FROM cafeuser WHERE Launch=1 and userMonth="+str(now.month)+" and userDate="+str(now.day)

    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        print(row[0]+"\t"+row[1]+" "+row[2]+" "+row[3]+"\tLaunch")

def dinnerUser():
    sel = "SELECT * FROM cafeuser WHERE Dinner=1 and userMonth="+str(now.month)+" and userDate="+str(now.day)

    cursor.execute(sel)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        print(row[0]+"\t"+row[1]+" "+row[2]+" "+row[3]+"\tDinner")

print("User ID\tUser Full Name\t\tMeal Type")
print("---- --\t---- ---- ----\t\t---- ----")
toDayUser()