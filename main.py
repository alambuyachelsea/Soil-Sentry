import network
import usocket as socket
import json
from plant_profile import PlantProfile
from ultra_sonic_sensor import UltrasonicSensor
import time
import _thread

SSID = "Chelsea's S23 Ultra"
PASSWORD = 'forfssake'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print('IP address:', wlan.ifconfig()[0])

plants = [
    PlantProfile(name="Basil", water_needs=2, pump_pin=6, sensor_pin=28, img_source='https://i.imgur.com/w8xuEfx.gif'),
    PlantProfile(name="Aloe", water_needs=1, pump_pin=7, sensor_pin=27, img_source='https://i.imgur.com/e9EikGU.gif'),
    PlantProfile(name="Begonia", water_needs=3, pump_pin=8, sensor_pin=26, img_source='https://i.imgur.com/phBFJkd.gif')
]

# Create an instance of the UltrasonicSensor
ultrasonic_sensor = UltrasonicSensor(trigger_pin_num=0, echo_pin_num=1)

def update_soil_moisture():
    while True:
        for plant in plants:
            plant.get_current_water_level()
        time.sleep(10)

_thread.start_new_thread(update_soil_moisture, ())

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print("Request:", request)

        request_lines = request.split('\n')
        if len(request_lines) < 1:
            client_socket.send("HTTP/1.1 400 Bad Request\nConnection: close\n\n")
            client_socket.close()
            return

        request_line = request_lines[0].strip()
        parts = request_line.split(' ')
        if len(parts) < 3:
            client_socket.send("HTTP/1.1 400 Bad Request\nConnection: close\n\n")
            client_socket.close()
            return

        method, path, _ = parts
        if path == '/':
            path = '/index.html'

        if path.endswith('.html') or path.endswith('.js') or path.endswith('.css'):
            with open(path[1:], 'r') as f:
                response = f.read()
            content_type = 'text/html' if path.endswith('.html') else 'application/javascript' if path.endswith('.js') else 'text/css'
            client_socket.send("HTTP/1.1 200 OK\nContent-Type: {}\nConnection: close\n\n".format(content_type).encode('utf-8'))
            client_socket.sendall(response.encode('utf-8'))

        elif path == '/plants':
            response_data = [
                {
                    "name": plant.get_name(),
                    "water_needs": plant.get_water_needs(),
                    "current_water_level": plant.get_current_water_level(),
                    "img_source": plant.get_img_source()
                }
                for plant in plants
            ]
            response = json.dumps(response_data)
            client_socket.send("HTTP/1.1 200 OK\nContent-Type: application/json\nConnection: close\n\n".encode('utf-8'))
            client_socket.sendall(response.encode('utf-8'))
        
        elif path == '/ultrasonic_reading':
            distance = ultrasonic_sensor.read_distance()
            percentage = ultrasonic_sensor.convert_sonic_reading_to_percentage(distance)
            response_data = {"percentage": percentage}
            response = json.dumps(response_data)
            client_socket.send("HTTP/1.1 200 OK\nContent-Type: application/json\nConnection: close\n\n".encode('utf-8'))
            client_socket.sendall(response.encode('utf-8'))
            print(percentage)

        else:
            client_socket.send("HTTP/1.1 404 Not Found\nConnection: close\n\n".encode('utf-8'))

    except OSError as e:
        print("Error:", e)
        client_socket.send("HTTP/1.1 500 Internal Server Error\nConnection: close\n\n".encode('utf-8'))
    finally:
        client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 80))
server_socket.listen(5)

print('Listening on port 80...')

while True:
    client_socket, addr = server_socket.accept()
    print('Got a connection from', addr)
    handle_client(client_socket)
