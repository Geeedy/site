#!/usr/bin/env python3
"""Local static server: language is in the path (EN at root, RU under /ru/).

Usage:
  python3 tools/serve_i18n.py                 # http://127.0.0.1:8080/site/
  BASE=/ python3 tools/serve_i18n.py          # http://127.0.0.1:8080/
  PORT=8090 python3 tools/serve_i18n.py

Serves files as-is. Content-Language follows path prefix (/ru/ → ru, else en).
"""
from __future__ import annotations

import http.server
import os
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("PORT", "8080"))
BASE = os.environ.get("BASE", "/site").rstrip("/")
HOST = os.environ.get("HOST", "127.0.0.1")


def content_language_for(path: str) -> str:
    if path == "/ru" or path.startswith("/ru/"):
        return "ru"
    return "en"


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
        if BASE:
            if path == BASE or path.startswith(BASE + "/"):
                path = path[len(BASE):] or "/"
            elif path.startswith("/site/") or path == "/site":
                path = path[len("/site"):] or "/"
        return path

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
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped")


if __name__ == "__main__":
    main()
