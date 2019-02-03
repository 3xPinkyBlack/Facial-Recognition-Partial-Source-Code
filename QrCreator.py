import qrcode as qr

QRNum = 0
QRStr = ""
DirName = "QRDatas/0001 - 1000/"

while QRNum < 1000:
	QRNum = QRNum + 1
	QRStr = str(QRNum)
	if len(QRStr) == 1:
		QRStr = "000" + QRStr
	elif len(QRStr) == 2:
		QRStr = "00" + QRStr
	elif len(QRStr) == 3:
		QRStr = "0" + QRStr
		
	img = qr.make(QRStr)
	img.save(DirName + str(QRStr) + ".png")
