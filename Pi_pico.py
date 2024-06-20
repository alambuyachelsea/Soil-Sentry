import network
import usocket as socket
from machine import Pin

# Wi-Fi credentials
SSID = "Chelsea's S23 Ultra"
PASSWORD = 'forfssake'

# LED pin
led_pin = Pin(0, Pin.OUT)  
# Change Pin(0) to the GPIO pin where your LED is connected


# Function to handle incoming client connections
def handle_client(client_socket):
    request = client_socket.recv(1024)
    print("Request:")
    print(request)

    # Check if request is for /led endpoint
    if b"GET /led?state=on" in request:
        led_pin.value(1)  # Turn LED on
    elif b"GET /led?state=off" in request:
        led_pin.value(0)  # Turn LED off

    # Send HTTP response with the contents of index.html
    with open('t.html', 'r') as f:
        html_content = f.read()

    client_socket.send("HTTP/1.1 200 OK\n")
    client_socket.send("Content-Type: text/html\n")
    client_socket.send("Connection: close\n\n")
    client_socket.sendall(html_content)

    client_socket.close()


# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print('IP address:', wlan.ifconfig()[0])

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
