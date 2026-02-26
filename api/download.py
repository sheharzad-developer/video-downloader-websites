"""
Vercel serverless function: POST /api/download
Calls Cobalt API and returns JSON. No Django dependency.
"""
import json
import os
from http.server import BaseHTTPRequestHandler

import requests


def get_cobalt_url():
    return os.environ.get("COBALT_API_URL", "https://api.cobalt.tools").rstrip("/")


def request_download(url: str, **options) -> dict:
    api_url = f"{get_cobalt_url()}/"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {"url": url, **options}
    try:
        r = requests.post(api_url, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        return {"status": "error", "error": {"code": "request_failed", "context": str(e)}}


def send_json(handler: BaseHTTPRequestHandler, data: dict, status: int = 200):
    body = json.dumps(data).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()
        return

    def do_GET(self):
        send_json(self, {"error": "Method not allowed. Use POST with JSON body: {\"url\": \"...\"}"}, 405)
        return

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
        try:
            data = json.loads(body or "{}")
        except (json.JSONDecodeError, TypeError):
            send_json(self, {"status": "error", "error": {"code": "invalid_json"}}, 400)
            return
        url = (data.get("url") or "").strip()
        if not url:
            send_json(self, {"status": "error", "error": {"code": "missing_url"}}, 400)
            return
        options = {k: v for k, v in data.items() if k != "url" and v is not None}
        result = request_download(url, **options)
        send_json(self, result)
        return
