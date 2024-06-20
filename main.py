import network
import usocket as socket
from machine import Pin

# Wi-Fi credentials
SSID = "Chelsea's S23 Ultra"
PASSWORD = 'forfssake'

# LED pin
# Change Pin(0) to the GPIO pin where your LED is connected
led_pin = Pin(0, Pin.OUT)

# Function to handle incoming client connections


def handle_client(client_socket):
    request = client_socket.recv(1024)
    request_str = request.decode('utf-8')
    print("Request:")
    print(request_str)

    # Parse the first line of the HTTP request
    request_line = request_str.split('\n')[0]
    request_file = request_line.split(' ')[1]

    # Determine which file to serve based on the request
    if request_file == '/':
        request_file = '/index.html'
    elif request_file == '/script.js':
        request_file = '/script.js'
    elif request_file == '/styles.css':
        request_file = '/styles.css'

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

    # Check if request is for /led endpoint
    if b"GET /led?state=on" in request:
        led_pin.value(1)  # Turn LED on
    elif b"GET /led?state=off" in request:
        led_pin.value(0)  # Turn LED off

    client_socket.close()


# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print('IP address:', wlan.ifconfig())

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
