import cv2
from flask import Flask, Response
app = Flask(_name_)
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Rotate the frame 
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)