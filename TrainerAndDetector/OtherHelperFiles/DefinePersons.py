import numpy as np
import cv2
import time
import Person

cap = cv2.VideoCapture(0) #Open video file
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True) #Create the background substractor
kernelOp = np.ones((3,3),np.uint8)
kernelCl = np.ones((11,11),np.uint8)
areaTH = 1500

while(cap.isOpened()):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame) 
    try:
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        mask = cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        break
    _, contours0, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours0:
        cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cnt)
        print area
        if area > areaTH:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            new = True
            for i in persons:
                if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
                    new = False
                    i.updateCoords(cx,cy) #actualiza coordenadas en el objeto and resets age
                    break
            if new == True:
                p = Person.MyPerson(pid,cx,cy, max_p_age)
                persons.append(p)
                pid += 1
                
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

            for i in persons:
                if len(i.getTracks()) >= 2:
                    pts = np.array(i.getTracks(), np.int32)
                    pts = pts.reshape((-1,1,2))
                    frame = cv2.polylines(frame,[pts],False,i.getRGB())
                if i.getId() == 9:
                    print str(i.getX()), ',', str(i.getY())
                    cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)

    cv2.imshow('Frame',frame)

    k = cv2.waitKey(30)
    if k == 'q':
        break
cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows
