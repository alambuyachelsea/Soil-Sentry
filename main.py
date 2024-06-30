import network
import time
import urequests as requests
import json
from ultrasonic_sensor import UltrasonicSensor
from plant_profile import PlantProfile

# Wi-Fi Credentials
ssid = "netwrok name"
password = 'network password'

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
# Change URL where the server receives data
server_url = 'http://serverURL:serverPortNumber/receive_data'

# Plant profiles with sensor pins
plants = [  # Change according to the number and needs of the plants
    PlantProfile(name="Basil", water_needs=2, pump_pin=14,
                 sensor_pin=28, img_source='https://i.imgur.com/w8xuEfx.gif'),
    PlantProfile(name="Aloe", water_needs=1, pump_pin=13,
                 sensor_pin=27, img_source='https://i.imgur.com/e9EikGU.gif'),
    PlantProfile(name="Pink Begonia", water_needs=3, pump_pin=15,
                 sensor_pin=26, img_source='https://i.imgur.com/phBFJkd.gif'),
]

# Initialize ultrasonic sensor
ultrasonic_sensor = UltrasonicSensor(trigger_pin_num=0, echo_pin_num=1)


# Function to read soil moisture and ultrasonic sensor
def water_plants():
    if get_reservoir_level() > 20:

        for plant in plants:
            print(plant.get_name(), plant.get_current_water_level(),
                  plant.get_water_needs())

            if plant.get_current_water_level() < plant.get_water_needs():
                plant.water_self()


def get_reservoir_level():

    distance = ultrasonic_sensor.read_distance()
    percentage = ultrasonic_sensor.convert_sonic_reading_to_percentage(
        distance)
    return percentage


# Function to read sensor data from all plants and ultrasonic sensor
def read_sensors():
    readings = {}

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

    try:  # Read ultrasonic sensor
        percentage = get_reservoir_level()
        readings["level"] = percentage

    except Exception as e:
        print("Error reading ultrasonic sensor:", e)
        readings["level"] = None

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

    # Water plants if reservoir level is above 20%
    water_plants()

    time.sleep(3600)  # Delay between readings in seconds
