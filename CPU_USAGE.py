import psutil
import time
from datetime import datetime
from gpiozero import LED

# Set up LEDs
green_led = LED(17)
yellow_led = LED(27)
red_led = LED(22)

def log_cpu_usage():
    with open("cpu_usage_log.txt", "a") as log_file:
        while True:
            # Getting the CPU usage percentage
            cpu_usage = psutil.cpu_percent(interval=1)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Log the usage with a timestamp
            log_file.write(f"{timestamp} - CPU Usage: {cpu_usage}%\n")
            log_file.flush()  # making sure the data is written to the file
            # Control LEDs based on CPU usage
            if cpu_usage < 50:
                green_led.on()
                yellow_led.off()
                red_led.off()
            elif cpu_usage < 80:
                green_led.off()
                yellow_led.on()
                red_led.off()
            else:
                green_led.off()
                yellow_led.off()
                red_led.on()
            
            time.sleep(5)

green_led.off()
yellow_led.off()
red_led.off()
