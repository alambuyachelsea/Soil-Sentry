from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import asyncio
import websockets

# Global variable to store sensor data
sensor_data = {}


# HTTP request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/' or self.path == '/index.html':
                # Serve the index.html file
                with open('index.html', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(file.read())
            elif self.path == '/styles.css':
                # Serve the styles.css file
                with open('styles.css', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(file.read())
            elif self.path == '/script.js':
                # Serve the script.js file
                with open('script.js', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    self.wfile.write(file.read())
            elif self.path == '/plants':
                # Serve plants data
                if sensor_data:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(sensor_data['plants']).encode('utf-8'))
                else:
                    self.send_error(404, 'Sensor data not available')
            elif self.path == '/ultrasonic_reading':
                # Serve ultrasonic sensor data
                if sensor_data:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'level': sensor_data.get('level', 0)}, indent=4).encode())
                else:
                    self.send_error(404, 'Sensor data not available')
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
        except Exception as e:
            print('Error handling GET request:', e)
            self.send_error(500, 'Internal Server Error')

    def do_POST(self):
        if self.path == '/receive_data':
            print("here")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                json_data = json.loads(post_data.decode('utf-8'))
                print('Received sensor data:', json_data)

                # Store sensor data globally
                global sensor_data
                sensor_data = json_data

                # Send data to all connected WebSocket clients
                asyncio.run(send_data_to_clients(json_data))

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b"Data received successfully\r\n")
            except json.JSONDecodeError as e:
                print('Error decoding JSON:', e)
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Error: Invalid JSON data\r\n")
            except Exception as e:
                print('Error processing sensor data:', e)
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Error: Internal Server Error\r\n")
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Error: Unsupported request\r\n")


# WebSocket server handler
async def handle_websocket(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message from WebSocket client: {message}")

            if message == 'get_sensor_data':
                # Send current sensor data to WebSocket client
                global sensor_data
                await websocket.send(json.dumps(sensor_data))
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed")


# Function to send data to all WebSocket clients
async def send_data_to_clients(data):
    connected_clients = asyncio.all_tasks()
    for task in connected_clients:
        if isinstance(task, asyncio.Task) and task.get_coro() == handle_websocket:
            await task.get_coro()(data)


# Function to run the HTTP server
def run_http_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting HTTP server on port 8000...')
    try:
        httpd.serve_forever()
        print("server forever")
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('HTTP server stopped.')


# Function to run the WebSocket server
async def run_websocket_server():
    start_server = websockets.serve(handle_websocket, 'localhost', 8765)
    print('Starting WebSocket server on ws://localhost:8765...')


# Function to run both servers
def run_servers():
    http_thread = threading.Thread(target=run_http_server)
    http_thread.start()

    asyncio.run(run_websocket_server())

if __name__ == '__main__':
    run_servers()
