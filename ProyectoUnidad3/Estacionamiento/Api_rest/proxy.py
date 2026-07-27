import http.server
import threading
import urllib.request

ESP32_URL = "http://192.168.1.8/api/estacionamiento"
PROXY_PORT = 8765

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/estacionamiento":
            try:
                req = urllib.request.Request(ESP32_URL, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = resp.read()
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self.send_response(503)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error":"ESP32 no accesible","plazas":[]}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        pass

_proxy_server = None
_proxy_thread = None

def iniciar_proxy():
    global _proxy_server, _proxy_thread
    if _proxy_server is not None:
        return
    _proxy_server = http.server.HTTPServer(("127.0.0.1", PROXY_PORT), ProxyHandler)
    _proxy_thread = threading.Thread(target=_proxy_server.serve_forever, daemon=True)
    _proxy_thread.start()
