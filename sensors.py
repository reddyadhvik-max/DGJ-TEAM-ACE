import RPi.GPIO as GPIO
import time
import adafruit_dht
import board


FLAME_PIN = 17
PIR_PIN = 27
TILT_PIN = 22
DHT_PIN = board.D4 


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(FLAME_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


GPIO.setup(TILT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    dht_device = adafruit_dht.DHT11(DHT_PIN)
except RuntimeError as error:
    print(f"DHT11 sensor initialization failed: {error.args[0]}")
    exit()


try:
    print("Reading sensor data... (Press Ctrl+C to exit) 🚀")
    while True:
        
        if not GPIO.input(FLAME_PIN): 
            print("🔥 Flame Detected!")
        else:
            print("No Flame")
        
        if GPIO.input(PIR_PIN): 
            print("🚶 Motion Detected!")
        else:
            print("No Motion")

        
        if not GPIO.input(TILT_PIN): 
            print("🔴 Tilt Sensor: Tilted")
        else:
            print("🟢 Tilt Sensor: Upright")
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            
            if temperature is not None and humidity is not None:
                print(f"🌡️ Temp: {temperature:.1f}°C | 💧 Humidity: {humidity:.1f}%")
            else:
                print("DHT11 sensor reading failed. Retrying...")
        except RuntimeError as error:
        
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            

            dht_device.exit()
            raise error

        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting program. 👋")
    
finally:
    GPIO.cleanup() 
    dht_device.exit() 
