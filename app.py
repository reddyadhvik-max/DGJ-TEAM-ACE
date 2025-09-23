import time
import threading
import cv2
from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO

from gpiozero import Button, MotionSensor
import adafruit_dht
import board

app = Flask(__name__)
data_lock = threading.Lock() 

latest_sensor_data = {
    'flame': 'No Flame',
    'motion': 'No Motion',
    'tilt': 'Upright',
    'temperature': 'N/A',
    'humidity': 'N/A',
    'person_detected': False
}
latest_image_data = None
last_capture_time = 0


FLAME_PIN = 17
PIR_PIN = 27
TILT_PIN = 22
DHT_PIN = board.D4 

flame_sensor = Button(FLAME_PIN, pull_up=True)
pir_sensor = MotionSensor(PIR_PIN)
tilt_sensor = Button(TILT_PIN, pull_up=True)

try:
    dht_device = adafruit_dht.DHT11(DHT_PIN)
except RuntimeError as error:
    print(f"DHT11 sensor initialization failed: {error.args[0]}")
    exit()

def read_sensors_periodically():
    global latest_sensor_data
    while True:
        with data_lock:
            latest_sensor_data['flame'] = "🔥 Flame Detected!" if flame_sensor.is_pressed else "No Flame"
            latest_sensor_data['motion'] = "🚶 Motion Detected!" if pir_sensor.motion_detected else "No Motion"
            latest_sensor_data['tilt'] = "🔴 Tilted" if tilt_sensor.is_pressed else "🟢 Upright"
            
            try:
                temperature = dht_device.temperature
                humidity = dht_device.humidity
                if temperature is not None and humidity is not None:
                    latest_sensor_data['temperature'] = f"{temperature:.1f}°C"
                    latest_sensor_data['humidity'] = f"{humidity:.1f}%"
                else:
                    latest_sensor_data['temperature'] = "N/A"
                    latest_sensor_data['humidity'] = "N/A"
            except RuntimeError:
                pass

        print(f"Sensor Data: {latest_sensor_data}")
        time.sleep(1)


sensor_thread = threading.Thread(target=read_sensors_periodically, daemon=True)
sensor_thread.start()


camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

model = YOLO('yolov8n.pt')

last_yolo_process_time = 0
YOLO_PROCESS_INTERVAL = 1 

def generate_frames():
    global latest_sensor_data, latest_image_data, last_capture_time, last_yolo_process_time
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        frame = cv2.flip(frame, 1)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        

        current_time = time.time()
        if (current_time - last_yolo_process_time) > YOLO_PROCESS_INTERVAL:
            
            results = model(frame, verbose=False)
            person_detected_flag = False
            
            for r in results:
                for box in r.boxes:
                    label = model.names[int(box.cls[0])]
                    if label == 'person':
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        confidence = float(box.conf[0])
                        
                        if confidence > 0.5:
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                            person_detected_flag = True

            with data_lock:
                latest_sensor_data['person_detected'] = person_detected_flag
                
                if person_detected_flag and (current_time - last_capture_time) > 3:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    latest_image_data = buffer.tobytes()
                    last_capture_time = time.time()
            
            last_yolo_process_time = current_time

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/sensor_data')
def sensor_data():
    with data_lock:
        return jsonify(latest_sensor_data)

@app.route('/captured_image')
def captured_image():
    with data_lock:
        if latest_image_data:
            return Response(latest_image_data, mimetype='image/jpeg')
        return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

    ## cd my_rover_project
##source venv/bin/activate