from flask import Flask, render_template,Response
import serial
import cv2

app = Flask(__name__)

try:
    ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
except:
    ser = None
    print("Error,Cant find port")

try:
    cap = cv2.VideoCapture(1)
except:
    cap = None
    print("Error, Cant find camera, try to change cv2.VideoCapture(from 1 to 0)")

def genereate_frames():
    while True:
        res,frame = cap.read()
        if not res:
            break
        ret,buffer = cv2.imencode(' .jpg',frame)
        frame_bytes = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cmd/<command>')
def cmd(command):
    if ser and ser.is_open:
        ser.write(command.encode())
    return 'OK'

@app.route('/video_feed')
def video_feed():
    return Response(genereate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8080)

