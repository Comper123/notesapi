import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PORT = int(os.getenv("PORT", "8201"))
DATA_FILE = Path(os.getenv("DATA_FILE", "/data/notes.json"))


def load_notes(path=DATA_FILE):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def add_note(text, path=DATA_FILE):
    notes = load_notes(path)
    note = {"id": len(notes) + 1, "text": text}
    notes.append(note)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)
    return note


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "healthy", "version": "1.0.0"})
        elif self.path == "/notes":
            self.send_json(200, {"notes": load_notes()})
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/notes":
            self.send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            text = payload.get("text", "").strip()
            if not text:
                raise ValueError("field 'text' is required")
            self.send_json(201, add_note(text))
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.send_json(400, {"error": str(error)})

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}", flush=True)


if __name__ == "__main__":
    print(f"Starting Notes API on 0.0.0.0:{PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
