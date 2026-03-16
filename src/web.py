"""Simple web server for Bank OCR."""
import http.server
import json
import os
from src.parser import parse_file
from src.checksum import is_valid
from src.formatter import classify_account


def process_ocr(ocr_text: str) -> list[dict]:
    """Process OCR text and return structured results."""
    accounts = parse_file(ocr_text)
    results = []
    for account in accounts:
        if "?" in account:
            status = "ILL"
            valid = None
        elif is_valid(account):
            status = "OK"
            valid = True
        else:
            status = "ERR"
            valid = False
        results.append({
            "account": account,
            "status": status,
            "valid": valid,
        })
    return results


class OCRHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._serve_html()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/api/parse":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            ocr_text = data.get("text", "")
            results = process_ocr(ocr_text)
            self._json_response(results)
        else:
            self.send_error(404)

    def _json_response(self, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_html(self):
        html_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
        try:
            with open(html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(500, "index.html not found")

    def log_message(self, format, *args):
        pass  # Suppress default logging


def run(port=8080):
    server = http.server.HTTPServer(("", port), OCRHandler)
    print(f"Bank OCR Web UI running at http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
