import network
import time
import urequests as requests  # MicroPython's urequests for HTTP
import machine
import json
from ultrasonic_sensor import UltrasonicSensor
from plant_profile import PlantProfile

# Wi-Fi Credentials
ssid = "Chelsea's S23 Ultra"
password = 'forfssake'

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait until connected
while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print('IP Address:', wlan.ifconfig()[0])

# HTTP endpoint (replace with your server URL)
server_url = 'http://192.168.0.179:8000/receive_data'  # Example URL where the server receives data

# Plant profiles with sensor pins
plants = [
    PlantProfile(name="Basil", water_needs=2, pump_pin=6,
                 sensor_pin=28, img_source='https://i.imgur.com/w8xuEfx.gif'),
    PlantProfile(name="Aloe", water_needs=1, pump_pin=7,
                 sensor_pin=27, img_source='https://i.imgur.com/e9EikGU.gif'),
    PlantProfile(name="Begonia", water_needs=3, pump_pin=8,
                 sensor_pin=26, img_source='https://i.imgur.com/phBFJkd.gif')
]

# Initialize ultrasonic sensor
ultrasonic_sensor = UltrasonicSensor(trigger_pin_num=0, echo_pin_num=1)

# Initialize onboard LED
led = machine.Pin(25, machine.Pin.OUT)

# Function to read soil moisture and ultrasonic sensor
def read_sensors():
    readings = {}

    # Turn on the onboard LED
    led.value(1)

    # Read soil moisture sensors
    plant_data = [
        {
            "name": plant.get_name(),
            "water_needs": plant.get_water_needs(),
            "current_water_level": plant.get_current_water_level(),
            "img_source": plant.get_img_source()
        }
        for plant in plants
    ]
    
    readings["plants"] = plant_data

    try:
        distance = ultrasonic_sensor.read_distance()
        percentage = ultrasonic_sensor.convert_sonic_reading_to_percentage(distance)
        readings["level"] = percentage
        
    except Exception as e:
        print("Error reading ultrasonic sensor:", e)
        readings["level"] = None
        
    # Turn off the onboard LED
    led.value(0)

    return readings

# Function to send sensor data via HTTP POST
def send_sensor_data():
    data = read_sensors()

    # Prepare JSON message
    json_data = json.dumps(data)

    # Send HTTP POST request
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(server_url, data=json_data, headers=headers)
        print('HTTP POST Status:', response.status_code)
        response.close()
    except Exception as e:
        print("Error sending HTTP POST request:", e)

# Send sensor data periodically
while True:
    send_sensor_data()
    time.sleep(10)  # Delay between readings
