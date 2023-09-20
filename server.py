import logging
import http.server
import cgi
import json

from helper import write_to_temp, upload_images
from driver import main as gcn
from plot import plot


class GCNHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_type, _ = cgi.parse_header(self.headers.get('content-type'))

        if content_type == 'multipart/form-data':
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'},
            )

            if 'data' in form_data:
                npz_file = form_data['data']

                # Save the uploaded file to the server
                write_to_temp(npz_file)

                # Handle the uploaded file
                try:
                    # Perform operations
                    gcn()
                    plot()
                    list_url = upload_images()
                except Exception as e:
                    logging.error('Error loading file:', str(e))

                # Send a response back to the client
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(list_url).encode(encoding='utf_8'))

            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(
                    "Bad request. Incorrect file found in the request.".encode())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='logfile.log',
                        format='%(asctime)s %(levelname)s:%(message)s')

    webServer = http.server.HTTPServer(
        ("localhost", 5000), GCNHttpRequestHandler)
    logging.info("Server started http://localhost:5000.")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    logging.info("Server stopped.")
