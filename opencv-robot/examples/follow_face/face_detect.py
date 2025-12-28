import cv2
from time import sleep
import serial
import errors

def zov(x,in_min,in_max,out_min,out_max):
    z = (x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return int(z)

minimal_coordinate = 155
maximal_coordinate = 515

try:
    ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
except:
    ser = None
    print(errors.Serial_Error)    

try:
    cap = cv2.VideoCapture(1)
except:
    cap = None
    print(errors.Camera_Error)

cascade = cv2.CascadeClassifier('cascades/face.xml')

while True:
    result,frame = cap.read()
    if not result:
        break
    gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray_img,1.3,5)
    for(x,y,w,h) in faces:
        ox = x+w //2
    cx = zov(ox,minimal_coordinate,maximal_coordinate,0,255)
    print(cx)
    ser.write(bytes([cx]))

cap.release()
ser.write(bytes([0]))
cv2.destroyAllWindows
print(errors.Arrange_Error)