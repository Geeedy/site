#!/usr/bin/env python3
"""Local static server with same-URL language negotiation (cookie sd_lang / Accept-Language).

Usage:
  python3 tools/serve_i18n.py                 # http://127.0.0.1:8080/site/
  BASE=/ python3 tools/serve_i18n.py          # http://127.0.0.1:8080/
  PORT=8090 python3 tools/serve_i18n.py

Mirrors production: index.html (RU) vs index.en.html (EN) at the same path.
HTML responses are not cached (cookie must change language on the same URL).
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


def prefer_en(headers, cookie_header: str) -> bool:
    m = re.search(r"(?:^|;\s*)sd_lang=(ru|en)", cookie_header or "")
    if m:
        return m.group(1) == "en"
    al = (headers.get("Accept-Language") or "").lower()
    # Prefer Russian if present anywhere with reasonable q; else first tag
    parts = [p.strip() for p in al.split(",") if p.strip()]
    scored = []
    for p in parts:
        tag, *rest = p.split(";")
        tag = tag.strip().lower()
        q = 1.0
        for r in rest:
            r = r.strip()
            if r.startswith("q="):
                try:
                    q = float(r[2:])
                except ValueError:
                    q = 0.0
        scored.append((q, tag))
    scored.sort(key=lambda x: -x[0])
    for q, tag in scored:
        if tag.startswith("ru"):
            return False
        if tag.startswith("en"):
            return True
    return False  # default RU for this site


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

    def _lang_index_path(self, directory: Path) -> Path | None:
        cookie = self.headers.get("Cookie", "")
        want_en = prefer_en(self.headers, cookie)
        en_f = directory / "index.en.html"
        ru_f = directory / "index.html"
        if want_en and en_f.is_file():
            return en_f
        if ru_f.is_file():
            return ru_f
        if en_f.is_file():
            return en_f
        return None

    def _redirect(self, location: str) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def do_HEAD(self):
        path = urllib.parse.urlsplit(self.path).path
        if BASE and path in ("", "/", BASE):
            self.send_response(302)
            self.send_header("Location", f"{BASE}/")
            self.end_headers()
            return
        slash = self._dir_needs_slash(path)
        if slash:
            self.send_response(301); self.send_header("Location", slash); self.end_headers(); return
        super().do_HEAD()

    def _dir_needs_slash(self, path):
        """Путь-каталог без завершающего слэша (и не файл) → нужен 301 на path+'/'."""
        if path.endswith('/') or '.' in path.rsplit('/', 1)[-1]:
            return None
        rel = path
        if BASE and rel.startswith(BASE):
            rel = rel[len(BASE):] or '/'
        fs = Path(ROOT) / rel.lstrip('/')
        if fs.is_dir():
            return path + '/'
        return None

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
            self.send_response(301); self.send_header("Location", loc); self.end_headers(); return
        super().do_GET()

    def translate_path(self, path: str) -> str:
        path = urllib.parse.urlsplit(path).path
        # Strip cache-buster from path resolution (query already stripped by urlsplit)
        if BASE:
            if path == BASE or path.startswith(BASE + "/"):
                path = path[len(BASE):] or "/"
            elif path.startswith("/site/") or path == "/site":
                path = path[len("/site"):] or "/"
        fs = super().translate_path(path)
        p = Path(fs)
        if path.endswith("/") or p.is_dir():
            if not p.is_dir():
                return fs  # несуществующий путь: честный 404, без отката к родителю
            directory = p
            if str(directory).startswith(str(ROOT)):
                chosen = self._lang_index_path(directory)
                if chosen:
                    return str(chosen)
        if not path.endswith("/") and not p.exists():
            as_dir = Path(super().translate_path(path + "/"))
            if as_dir.is_dir():
                chosen = self._lang_index_path(as_dir)
                if chosen:
                    return str(chosen)
        return fs

    def end_headers(self):
        cookie = self.headers.get("Cookie", "")
        lang = "en" if prefer_en(self.headers, cookie) else "ru"
        self.send_header("Content-Language", lang)
        # Critical: same URL serves different HTML by cookie — never cache HTML
        path = urllib.parse.urlsplit(self.path).path
        if path.endswith("/") or path.endswith(".html") or path == BASE or path == "/site" or path == "":
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Vary", "Cookie, Accept-Language")
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
        print("Language: cookie sd_lang=ru|en (else Accept-Language; default RU)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
