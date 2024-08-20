import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import matplotlib.pyplot as plt
import csv

# GPIO Mode (BOARD / BCM) I Used BCM >> Check The DataSheet For the BCM
GPIO.setmode(GPIO.BCM)

# Define GPIO Pins
TRIG = 23
ECHO = 24
TEMP_SENSOR_PIN = 17  # For DHT11
DHT_SENSOR = Adafruit_DHT.DHT11

# Set GPIO direction (IN / OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to read distance from the ultrasonic sensor
def read_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    
    while GPIO.input(ECHO) == 1:
        end_time = time.time()
    
    duration = end_time - start_time
    distance = (duration * 34300) / 2  # Distance in cm
    return distance

# Function to read temperature from the DHT11 sensor
def read_temperature():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, TEMP_SENSOR_PIN)
    return temperature

# Function to log sensor data to a CSV file
def log_data(distance, temperature):
    with open('sensor_log.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), distance, temperature])

# Function to generate a plot of the sensor data
def generate_plot():
    times, distances, temperatures = [], [], []
    with open('sensor_log.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            times.append(row[0])
            distances.append(float(row[1]))
            temperatures.append(float(row[2]))
    
    plt.figure(figsize=(10, 5))
    plt.plot(times, distances, label="Distance (cm)", color='b')
    plt.plot(times, temperatures, label="Temperature (°C)", color='r')
    plt.xlabel('Time')
    plt.ylabel('Sensor Readings')
    plt.title('Sensor Data Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('sensor_data_plot.png')
    plt.show()

# Main function to run the sensor reading loop
if _name_ == "_main_":
    try:
        # Create and initialize the log file
        with open('sensor_log.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Distance(cm)", "Temperature(C)"])

        # Continuous loop to read sensors and log data
        while True:
            distance = read_distance()
            temperature = read_temperature()
            log_data(distance, temperature)
            print(f"Distance: {distance:.2f} cm, Temperature: {temperature:.2f} C")
            time.sleep(2)
    
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO settings on exit
        generate_plot()  # Generate the plot when the loop ends
