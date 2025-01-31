
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Utilisation de la camera
camera = cv2.VideoCapture(0)

def image():
    while True:
        # Lire une image de la camera
        success, frame = camera.read()  
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # classifier le visage
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            # Détectection des visages
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            # encadrement des visages detectés par de rectangle
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Encoder l'image en JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(image(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
