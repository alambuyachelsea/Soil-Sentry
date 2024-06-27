from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HTML_FILE = 'html_files/index.html'

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            try:
                # Open and read index.html file
                with open(HTML_FILE, 'rb') as file:
                    content = file.read()

                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)

            except FileNotFoundError:
                # Handle file not found
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'index.html not found')

        else:
            # Handle other GET requests
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'File not found')

    def do_POST(self):
        if self.path == '/receive_data':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)

                json_data = json.loads(post_data.decode('utf-8'))
                print('Received sensor data:', json_data)

                # Process data as needed (store in database, etc.)

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

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting HTTP server on port 8000...')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print('Server stopped.')

if __name__ == '__main__':
    run_server()
