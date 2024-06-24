import network
import usocket as socket
import json
from plant_profile import PlantProfile
import time
from soil_sensor import SoilSensor

# Wi-Fi credentials
SSID = "Chelsea's S23 Ultra"
PASSWORD = 'forfssake'

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print('IP address:', wlan.ifconfig()[0])

# Initialize plant profiles and add them to a global list
plants = [
    PlantProfile(name="Basil", water_needs=2, pump_pin=6, sensor_pin=28, img_source='https://i.imgur.com/w8xuEfx.gif'),
    PlantProfile(name="Aloe", water_needs=1, pump_pin=7, sensor_pin=27, img_source='https://i.imgur.com/e9EikGU.gif'),
    PlantProfile(name="Begonia", water_needs=3, pump_pin=8, sensor_pin=26, img_source='https://i.imgur.com/phBFJkd.gif')
]


# Function to handle incoming client connections
def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print("Request:")
    print(request)

    # Split the request to get the HTTP method and path
    request_lines = request.split('\n')
    request_line = request_lines[0].strip()
    method, path, _ = request_line.split(' ')

    # If the path is '/', serve index.html
    if path == '/':
        path = '/index.html'

    # Handle different request paths
    try:
        if path.endswith('.html') or path.endswith('.js') or path.endswith('.css'):
            with open(path[1:], 'r') as f:
                response = f.read()
            if path.endswith('.html'):
                content_type = 'text/html'
            elif path.endswith('.js'):
                content_type = 'application/javascript'
            elif path.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/plain'

            client_socket.send("HTTP/1.1 200 OK\n")
            client_socket.send("Content-Type: {}\n".format(content_type))
            client_socket.send("Connection: close\n\n")
            client_socket.sendall(response.encode('utf-8'))

        elif path == '/plants':
            response_data = [
                {
                    "name": plant.get_name(),
                    "water_needs": plant.get_water_needs(),
                    "current_water_level": plant.get_current_water_level(),
                    "img_source": plant.img_source  # Include img_source in response
                }
                for plant in plants
            ]
            response = json.dumps(response_data)

            client_socket.send("HTTP/1.1 200 OK\n")
            client_socket.send("Content-Type: application/json\n")
            client_socket.send("Connection: close\n\n")
            client_socket.sendall(response.encode('utf-8'))

        else:
            client_socket.send("HTTP/1.1 404 Not Found\n")
            client_socket.send("Connection: close\n\n")

    except OSError:
        client_socket.send("HTTP/1.1 404 Not Found\n")
        client_socket.send("Connection: close\n\n")

    client_socket.close()

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 80))
server_socket.listen(5)

print('Listening on port 80...')

# Main loop to accept client connections
while True:
    client_socket, addr = server_socket.accept()
    print('Got a connection from', addr)
    handle_client(client_socket)