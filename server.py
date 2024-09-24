import logging
import http.server
import cgi
import json

from helper import write_to_temp, upload_images
from driver import main as gcn
from plot import plot


class GCNHttpRequestHandler(http.server.BaseHTTPRequestHandler):

    def _safe_write(self, data):
        """Safely write to the client, checking if wfile is still open."""
        if not self.wfile.closed:
            try:
                self.wfile.write(data.encode('utf-8'))
                self.wfile.flush()
            except (BrokenPipeError, ValueError) as e:
                logging.error(f"Failed to write to wfile: {e}")

    def _close_stream(self):
        """Close the event stream properly."""
        if not self.wfile.closed:
            try:
                self._safe_write("event: close\n\n")
            except (BrokenPipeError, ValueError) as e:
                logging.error(f"Failed to close stream: {e}")
            finally:
                self.finish()  # Gracefully close the connection    
    
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

                # Start streaming logs to the client
                self.send_response(200)
                self.send_header('Content-type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Connection', 'keep-alive')
                self.end_headers()

                # Handle the uploaded file
                try:
                    # Perform operations
                    self._safe_write(f"data: 'Starting process...'\n\n")
                    gcn()

                    self._safe_write(f"data: 'Plotting...'\n\n")
                    plot()

                    list_url = upload_images()

                except Exception as e:
                    logging.error('Error processing file:', exc_info=True)
                    self._safe_write(f"data: ERROR: {str(e)}\n\n")

                # Send a response back to the client
                self._safe_write(f"data: Process complete\n\n")
                self._safe_write(f"data: {json.dumps(list_url)}\n\n")

                # Close the connection
                self._close_stream()

            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self._safe_write("Bad request. No data found in the request.")


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
