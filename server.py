from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/receive_data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
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
