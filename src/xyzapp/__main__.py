import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/health"):
            self.send_error(404)
            return
        body = json.dumps({"status": "ok", "app": "xyz", "version": "1.0.0",
                           "release": os.environ.get("RELEASE_ID", "local")}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    # B104: enlace interno del contenedor, publicado solo en localhost por Compose.
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()  # nosec B104
