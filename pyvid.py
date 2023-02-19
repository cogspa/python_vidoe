import cv2
from flask import Flask, Response

app = Flask(__name__)

def gen_frames():
    """Function to capture frames from webcam"""
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Web page that streams webcam video"""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
