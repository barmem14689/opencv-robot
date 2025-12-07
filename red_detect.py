import cv2
import numpy as np
import time 
import serial

def zov(x,in_min,in_max,out_min,out_max):
    z = (x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    y = int(z)
    return y

ser = serial.Serial('COM5',9600,timeout=1)

cap = cv2.VideoCapture(0)

FinalCoordinat = 0 #питон ебанное дерьмо ненавижу сука

while True:
    res,frame = cap.read()
    if not res:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0,120,70])
    upper_red1 = np.array([10,255,255])
    lower_red2 = np.array([170,120,70])
    upper_red2 = np.array([180,255,255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1+mask2
    
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area > 500:
            x, y, w, h = cv2.boundingRect(largest)
            cv2.rectangle(frame,(x,y),(x + w, y + h), (0,255,0),2)

            cx = x + w // 2
            cy = y + h // 2
            cv2.circle(frame, (cx, cy), 5, (255,0,0), -1)
            ccx = zov(cx,20,627,0,255)
            cv2.putText(img=frame,text=str(ccx),org=(x,w),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=1,color=(0,255,0),thickness=1)
            FinalCoordinat = ccx
        else:
            FinalCoordinat = 0        
    ser.write(bytes([FinalCoordinat]))
    print(FinalCoordinat)

    cv2.imshow("Red Tracker", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()


