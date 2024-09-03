import serial
import RPi.GPIO as GPIO
import time

# Setup serial connection to Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

# Setup GPIO pin for alert (e.g., LED or alarm)
ALERT_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALERT_PIN, GPIO.OUT)

def process_data(data):
    # Split the incoming data by comma
    data_parts = data.split(',')
    sensor_values = {}

    # Parse each part to extract the sensor values
    for part in data_parts:
        key, value = part.split(':')
        sensor_values[key.strip()] = int(value.strip())

    return sensor_values

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(data)
            
            sensor_values = process_data(data)
            print(f"Accelerometer X: {sensor_values['AcX']}, Y: {sensor_values['AcY']}, Z: {sensor_values['AcZ']}")
            print(f"Gyroscope X: {sensor_values['GyX']}, Y: {sensor_values['GyY']}, Z: {sensor_values['GyZ']}")
            
            # Example alert condition based on threshold values
            if abs(sensor_values['AcX']) > 20000 or abs(sensor_values['AcY']) > 20000 or abs(sensor_values['AcZ']) > 20000:
                GPIO.output(ALERT_PIN, GPIO.HIGH)  # Turn on alert (e.g., LED)
                time.sleep(1)  # Adjust this duration as needed
                GPIO.output(ALERT_PIN, GPIO.LOW)   # Turn off alert
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    ser.close()
