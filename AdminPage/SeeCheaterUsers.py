import cv2
import os
import MySQLdb
import datetime

db = MySQLdb.connect("localhost","root","","cafepro")
now = datetime.datetime.now()
img = cv2.imread("AdminBackground.png")

while True:
	try:
		sql = "SELECT * FROM cheateruser WHERE userMonth="+str(now.month)+" AND userDate="+str(now.day)
		cursor = db.cursor()
		cursor.execute(sql)
		db.commit()
		rowcount = cursor.rowcount
		row = cursor.fetchall()
		cursor.close()

		imgNum = int(rowcount)
		while imgNum > 0:
			imgName = "../CheaterImage/"+str(now.year)+str(now.month)+str(now.day)+"/"+str(now.year)+str(now.month)+str(now.day)+str(imgNum)+".png"
			chImage = cv2.imread(imgName, 0)
			chNum = "Cheater Number: "+str(imgNum)
			cv2.imshow(chNum, chImage)
			imgNum = imgNum - 1

		if rowcount == 0:
			cv2.putText(img,'No One Was Cheating ToDay',(100,200),cv2.FONT_HERSHEY_SIMPLEX, 1,(70,0,100),2)
			cv2.imshow("Cheater Number: None",img)
			cv2.waitKey(1)

	except:
		cv2.putText(img,'Something is Not Right',(100,200),cv2.FONT_HERSHEY_SIMPLEX, 1,(70,0,100),2)
		cv2.imshow("Cheater Number: None",img)
		cv2.waitKey(1)