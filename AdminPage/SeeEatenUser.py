import cv2
import os
import MySQLdb
import datetime

db = MySQLdb.connect("localhost","root","","cafepro")
now = datetime.datetime.now()
img = cv2.imread("AdminBackground.png")

while True:
	try:
		print("h3110")
		sql = "SELECT * FROM mealtime WHERE mealMonth="+str(now.month)+" AND mealDate="+str(now.day)
		cursor = db.cursor()
		cursor.execute(sql)
		db.commit()
		row = cursor.fetchone()
		cursor.close()
		
		if row is not None:
			usText = 'Breakfast     Lunch    Dinner'
			cv2.putText(img,usText,(70,200),cv2.FONT_HERSHEY_SIMPLEX, 1,(100,70,0),2)

			usText = '------    ----    ----'
			cv2.putText(img,usText,(70,215),cv2.FONT_HERSHEY_SIMPLEX, 1,(70,0,100),2)

			usText = '  '+str(row[2])+'            '+str(row[3])+'        '+str(row[4])
			cv2.putText(img,usText,(70,250),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)

			cv2.imshow("Number Of ToDay Eater",img)
			cv2.waitKey(1)
		else:
			cv2.putText(img,'No One Ate There Meal To Day',(100,200),cv2.FONT_HERSHEY_SIMPLEX, 1,(70,0,100),2)
			cv2.imshow("Number Of ToDay Eater",img)
			cv2.waitKey(1)

	except:
		cv2.putText(img,'No One Ate There Meal To Day',(100,200),cv2.FONT_HERSHEY_SIMPLEX, 1,(70,0,100),2)
		cv2.imshow("Number Of ToDay Eater",img)
		cv2.waitKey(1)