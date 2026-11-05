import http.server
import json
import os
import mimetypes
import sys
from urllib.parse import urlparse, parse_qs
import engine

# Load .env file manually if present
def load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and not os.environ.get(key):
                        os.environ[key] = val

load_env_file()

PORT = int(os.environ.get("PORT", 5000))
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class DesiExplorerHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and disable aggressive caching for development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            key_configured = bool(os.environ.get("GROQ_API_KEY") or os.environ.get("GEMINI_API_KEY"))
            places = engine.load_places()
            self.send_json({
                "status": "ok",
                "app": "Desi Explorer",
                "version": "1.0.0",
                "provider": "groq",
                "model": "llama-3.3-70b-versatile",
                "places_count": len(places),
                "groq_configured": key_configured,
                "ai_configured": key_configured
            })
            return

        if path == "/api/places":
            qs = parse_qs(parsed.query)
            city = qs.get("city", [None])[0]
            places = engine.load_places()
            if city and city.lower() not in ["all", "sab"]:
                places = engine.filter_places(places, city)
            self.send_json({"places": places, "count": len(places)})
            return

        # Serve static files
        if path == "/" or path == "":
            file_path = os.path.join(STATIC_DIR, "index.html")
        else:
            rel_path = path.lstrip("/")
            file_path = os.path.join(STATIC_DIR, rel_path)

        # Security check: prevent directory traversal
        abs_static = os.path.abspath(STATIC_DIR)
        abs_req = os.path.abspath(file_path)
        if not abs_req.startswith(abs_static) or not os.path.exists(abs_req) or os.path.isdir(abs_req):
            file_path = os.path.join(STATIC_DIR, "index.html")

        if os.path.exists(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", f"{mime_type}; charset=utf-8" if "text" in mime_type or "javascript" in mime_type or "json" in mime_type else mime_type)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_json({"error": str(e)}, status=500)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        if path == "/api/itinerary":
            city = body.get("city", "Kurukshetra")
            time_available = body.get("time_available", "half_day")
            interests = body.get("interests", ["heritage", "spiritual"])
            budget = body.get("budget", "low")
            lang = body.get("lang", "en")
            req_key = body.get("api_key")

            itinerary = engine.generate_ai_itinerary(
                city=city,
                time_available=time_available,
                interests=interests,
                budget=budget,
                lang=lang,
                api_key=req_key
            )
            self.send_json(itinerary)
            return

        if path == "/api/chat":
            query = body.get("query", "")
            place_id = body.get("place_id")
            lang = body.get("lang", "en")
            req_key = body.get("api_key")

            res = engine.ask_local_guide(
                query=query,
                place_id=place_id,
                lang=lang,
                api_key=req_key
            )
            self.send_json(res)
            return

        if path == "/api/set-key":
            new_key = body.get("api_key", "").strip()
            if new_key:
                os.environ["GROQ_API_KEY"] = new_key
                self.send_json({"success": True, "message": "Groq API key updated for current session"})
            else:
                self.send_json({"success": False, "message": "No key provided"}, status=400)
            return

        self.send_json({"error": "Endpoint not found"}, status=404)

def run_server(port=PORT):
    # Ensure UTF-8 output on Windows consoles
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    server_address = ("127.0.0.1", port)
    httpd = http.server.ThreadingHTTPServer(server_address, DesiExplorerHandler)
    print(f"🚀 Desi Explorer Server running at http://127.0.0.1:{port}/")
    print(f"   API endpoints ready: /api/places, /api/itinerary, /api/chat, /api/health")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

