import network
import usocket as socket
from plant_profile import PlantProfile

# Wi-Fi credentials
SSID = 'YourSSID'
PASSWORD = 'YourPassword'

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print('IP address:', wlan.ifconfig()[0])

# Initialize a sample plant profile with the pump connected 
# to GPIO pin 15 and sensor to ADC pin 26
basil = PlantProfile(name="Fern", water_needs=2, pump_pin=6, sensor_pin=20)
aloe = PlantProfile(name="Aloe", water_needs=1, pump_pin=7, sensor_pin=19)
begonia = PlantProfile(name="Begonia", water_needs=3, pump_pin=8,
                       sensor_pin=18)

# Function to handle incoming client connections


def handle_client(client_socket):
    request = client_socket.recv(1024)
    request_str = request.decode('utf-8')
    print("Request:")
    print(request_str)

    # Parse the first line of the HTTP request
    request_line = request_str.split('\n')[0]
    request_file = request_line.split(' ')[1]

    if request_file == '/':
        request_file = '/index.html'
    elif request_file == '/script.js':
        request_file = '/script.js'
    elif request_file == '/styles.css':
        request_file = '/styles.css'
    elif request_file == '/plant_info':
        response = f'{{"name": "{plant.get_name()}", "water_needs": {plant.get_water_needs(
        )}, "current_water_level": {plant.get_current_water_level()}}}'
        client_socket.send("HTTP/1.1 200 OK\n")
        client_socket.send("Content-Type: application/json\n")
        client_socket.send("Connection: close\n\n")
        client_socket.sendall(response)
        client_socket.close()
        return

    try:
        # remove the leading '/' from the filename
        with open(request_file[1:], 'r') as f:
            response = f.read()
        if request_file.endswith('.html'):
            content_type = 'text/html'
        elif request_file.endswith('.js'):
            content_type = 'application/javascript'
        elif request_file.endswith('.css'):
            content_type = 'text/css'
        else:
            content_type = 'text/plain'

        client_socket.send("HTTP/1.1 200 OK\n")
        client_socket.send("Content-Type: {}\n".format(content_type))
        client_socket.send("Connection: close\n\n")
        client_socket.sendall(response)
    except OSError:
        client_socket.send("HTTP/1.1 404 Not Found\n")
        client_socket.send("Connection: close\n\n")

    # Handle plant profile actions
    if b"GET /water" in request:
        plant.water_plant(100)  # Water the plant by 100ml

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
