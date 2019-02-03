import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","","kiot" )

cursor = db.cursor()

FN = ''
LN = ''
UID = 0
ST = 0

#sql = """CREATE TABLE cafe (
#         FName  CHAR(20) NOT NULL,
#         LName  CHAR(20),
#         Stat  int)"""

#qur = """INSERT INTO cafe(Fname, LName, stat)VALUES('Elyas', 'Abate', 0)"""

sel = """SELECT * FROM cafeuser WHERE UserID=1162"""

cursor.execute(sel)
db.commit()

results = cursor.fetchall()
for row in results:
    if row[3] == 0 :
        Stat = 'Welcome To Your Meal'
    else :
        Stat = 'You Have Eaten Before'
            
    print(row[1]+" "+row[2]+" "+Stat)

FN = ''
LN = ''
UID = 0
ST = 0


db.close()
