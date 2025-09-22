import serial
import time

SERIAL_PORT = '/dev/cu.usbserial-1110' 
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) 

    print(f"Connected to Arduino on {SERIAL_PORT}")
    print("Use keys to control your robot. Press 'f' to exit the program.")
    print("Commands:")
    print("  w: Move forward")
    print("  s: Move backward")
    print("  a: Arm upward")
    print("  d: Arm downward")
    print("  z: Claw open")
    print("  x: Claw close")
    print("  u: Servo 2 (up)")
    print("  j: Servo 2 (down)")
    print("  h: Servo 1 (left)")
    print("  k: Servo 1 (right)")
    print("  q: Stop all motors")
    print("  f: Exit program")

    while True:
        command = input("Enter command: ").strip().lower()

        if command == 'f':
            print("Exiting program...")
            break
        elif command in ('w', 's', 'a', 'd', 'z', 'x', 'u', 'j', 'h', 'k', 'q'):
            ser.write(command.encode('utf-8'))
            print(f"Sent command: {command}")
        else:
            print("Invalid command. Please enter one of the listed keys.")

except serial.SerialException as e:
    print(f"Error: Could not open serial port {SERIAL_PORT}. Details: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")