#!/usr/bin/env python3
"""Local static server: language is in the path (EN at root, RU under /ru/).

Also accepts POST /api/lead (and /site/api/lead) for contact form submissions.

Usage:
  python3 tools/serve_i18n.py                 # http://127.0.0.1:8080/site/
  BASE=/ python3 tools/serve_i18n.py          # http://127.0.0.1:8080/
  PORT=8090 python3 tools/serve_i18n.py

Serves files as-is. Content-Language follows path prefix (/ru/ → ru, else en).
"""
from __future__ import annotations

import http.server
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("PORT", "8080"))
BASE = os.environ.get("BASE", "/site").rstrip("/")
HOST = os.environ.get("HOST", "127.0.0.1")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leads_common import append_lead_log, broadcast_lead  # noqa: E402

MAX_FIELD = 4000
RATE_WINDOW_SEC = 60
RATE_MAX = 8
_rate: dict[str, list[float]] = {}


def content_language_for(path: str) -> str:
    if path == "/ru" or path.startswith("/ru/"):
        return "ru"
    return "en"


def _api_path(path: str) -> str:
    """Normalize request path for API matching (strip optional BASE /site)."""
    if BASE and (path == BASE or path.startswith(BASE + "/")):
        path = path[len(BASE):] or "/"
    elif path.startswith("/site/") or path == "/site":
        path = path[len("/site"):] or "/"
    return path


def _client_ip(handler: http.server.BaseHTTPRequestHandler) -> str:
    forwarded = handler.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip() or handler.client_address[0]
    return handler.client_address[0]


def _rate_ok(ip: str) -> bool:
    now = time.time()
    bucket = [t for t in _rate.get(ip, []) if now - t < RATE_WINDOW_SEC]
    if len(bucket) >= RATE_MAX:
        _rate[ip] = bucket
        return False
    bucket.append(now)
    _rate[ip] = bucket
    return True


class Handler(http.server.SimpleHTTPRequestHandler):
    _err_tpl = None

    @classmethod
    def _load_error_page(cls):
        if cls._err_tpl is None:
            f = ROOT / "404.html"
            try:
                cls._err_tpl = f.read_text(encoding="utf-8").replace("%", "%%")
            except Exception:
                cls._err_tpl = "<h1>%(code)d %(message)s</h1>"
        return cls._err_tpl

    def __init__(self, *args, **kwargs):
        self.error_message_format = self._load_error_page()
        self.error_content_type = "text/html;charset=utf-8"
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _site_path(self) -> str:
        path = urllib.parse.urlsplit(self.path).path
        return _api_path(path)

    def _redirect(self, location: str) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def _dir_needs_slash(self, path):
        if path.endswith('/') or '.' in path.rsplit('/', 1)[-1]:
            return None
        rel = path
        if BASE and rel.startswith(BASE):
            rel = rel[len(BASE):] or '/'
        fs = Path(ROOT) / rel.lstrip('/')
        if fs.is_dir():
            return path + '/'
        return None

    def _json_response(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_OPTIONS(self):
        path = _api_path(urllib.parse.urlsplit(self.path).path)
        if path == "/api/lead":
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            return
        self.send_error(404)

    def do_POST(self):
        path = _api_path(urllib.parse.urlsplit(self.path).path)
        if path == "/api/lead":
            return self._handle_lead()
        self.send_error(404)

    def _handle_lead(self) -> None:
        ip = _client_ip(self)
        if not _rate_ok(ip):
            return self._json_response(429, {"ok": False, "error": "too_many_requests"})

        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > 50_000:
            return self._json_response(400, {"ok": False, "error": "bad_request"})

        raw = self.rfile.read(length)
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        data: dict = {}
        try:
            if ctype == "application/json":
                parsed = json.loads(raw.decode("utf-8"))
                if isinstance(parsed, dict):
                    data = parsed
            else:
                form = urllib.parse.parse_qs(raw.decode("utf-8"), keep_blank_values=True)
                data = {k: (v[0] if v else "") for k, v in form.items()}
        except Exception:
            return self._json_response(400, {"ok": False, "error": "bad_request"})

        # Honeypot
        if (data.get("website") or data.get("company_url") or "").strip():
            return self._json_response(200, {"ok": True})

        name = str(data.get("name") or "").strip()
        contact = str(data.get("contact") or "").strip()
        message = str(data.get("message") or data.get("msg") or "").strip()
        lang = str(data.get("lang") or "").strip().lower()[:2]
        if lang not in ("ru", "en"):
            lang = ""

        if not name or not contact or not message:
            return self._json_response(400, {"ok": False, "error": "required"})
        if len(name) > 200 or len(contact) > 300 or len(message) > MAX_FIELD:
            return self._json_response(400, {"ok": False, "error": "too_long"})

        append_lead_log(
            {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "ip": ip,
                "name": name,
                "contact": contact,
                "message": message,
                "lang": lang,
            }
        )

        try:
            stats = broadcast_lead(name, contact, message, lang)
        except Exception as e:
            print(f"[lead] broadcast error: {e}", file=sys.stderr)
            return self._json_response(502, {"ok": False, "error": "delivery_failed"})

        print(
            f"[lead] from={name!r} contact={contact!r} sent={stats['sent']}/{stats['subscribers']}",
            file=sys.stderr,
        )
        return self._json_response(200, {"ok": True, "sent": stats["sent"]})

    def do_HEAD(self):
        path = urllib.parse.urlsplit(self.path).path
        if BASE and path in ("", "/", BASE):
            self.send_response(302)
            self.send_header("Location", f"{BASE}/")
            self.end_headers()
            return
        slash = self._dir_needs_slash(path)
        if slash:
            self.send_response(301)
            self.send_header("Location", slash)
            self.end_headers()
            return
        super().do_HEAD()

    def do_GET(self):
        path = urllib.parse.urlsplit(self.path).path
        if BASE:
            if path in ("", "/"):
                return self._redirect(f"{BASE}/")
            if path == BASE:
                return self._redirect(f"{BASE}/")
        slash = self._dir_needs_slash(path)
        if slash:
            q = urllib.parse.urlsplit(self.path).query
            loc = slash + (("?" + q) if q else "")
            self.send_response(301)
            self.send_header("Location", loc)
            self.end_headers()
            return
        super().do_GET()

    def translate_path(self, path: str) -> str:
        path = urllib.parse.urlsplit(path).path
        if BASE:
            if path == BASE or path.startswith(BASE + "/"):
                path = path[len(BASE):] or "/"
            elif path.startswith("/site/") or path == "/site":
                path = path[len("/site"):] or "/"
        return super().translate_path(path)

    def end_headers(self):
        site_path = self._site_path()
        self.send_header("Content-Language", content_language_for(site_path))
        path = urllib.parse.urlsplit(self.path).path
        if path.endswith("/") or path.endswith(".html") or path == BASE or path == "/site" or path == "":
            self.send_header("Cache-Control", "public, max-age=300")
        elif re.search(r"\.(css|js|png|jpg|jpeg|svg|ico|webp|woff2?)($|\?)", path):
            self.send_header("Cache-Control", "public, max-age=86400")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys_stderr = __import__("sys").stderr
        print("[%s] %s" % (self.log_date_time_string(), fmt % args), file=sys_stderr)


def main():
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    with http.server.ThreadingHTTPServer((HOST, PORT), Handler) as httpd:
        url = f"http://{HOST}:{PORT}{BASE or ''}/"
        print(f"Serving {ROOT}")
        print(f"Open {url}")
        print("Language: path-based (EN at /, RU under /ru/)")
        print(f"Lead API: POST {BASE or ''}/api/lead")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped")


if __name__ == "__main__":
    main()
