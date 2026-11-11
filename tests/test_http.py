import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import pytest
from xyzapp.__main__ import Handler


def test_health_and_not_found():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}"
    try:
        with urllib.request.urlopen(url + "/health", timeout=3) as response:
            assert response.status == 200
            data = json.load(response)
            assert data["status"] == "ok"
            assert data["version"] == "1.0.0"
            assert "release" in data
        with pytest.raises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(url + "/missing", timeout=3)
        assert error.value.code == 404
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
