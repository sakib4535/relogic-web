#!/usr/bin/env python3
"""Relogic static server + intake API + lead inbox."""

from __future__ import annotations

import json
import mimetypes
import os
import secrets
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
LEADS = ROOT / "data" / "leads"
LEADS.mkdir(parents=True, exist_ok=True)
INBOX = LEADS / "inbox.jsonl"
KEY_FILE = ROOT / "data" / "admin.key"

if KEY_FILE.exists():
    ADMIN_KEY = KEY_FILE.read_text().strip() or "relogic-admin"
else:
    ADMIN_KEY = os.environ.get("RELOGIC_ADMIN_KEY", "relogic-admin")
    KEY_FILE.write_text(ADMIN_KEY + "\n")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save_lead(payload: dict) -> dict:
    lead_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
    record = {
        "id": lead_id,
        "receivedAt": now_iso(),
        "payload": payload,
    }
    (LEADS / f"{lead_id}.json").write_text(json.dumps(record, indent=2))
    with INBOX.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def list_leads() -> list:
    rows = []
    if INBOX.exists():
        for line in INBOX.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    rows.reverse()
    return rows


ADMIN_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Relogic intake inbox</title>
<style>
  body{margin:0;background:#050816;color:#f4f8fd;font-family:Inter,system-ui,sans-serif}
  main{width:min(1080px,calc(100% - 36px));margin:40px auto 80px}
  h1{font:700 36px/1.1 system-ui;letter-spacing:-.04em}
  p{color:#c5d0de}
  form{display:flex;gap:10px;margin:20px 0 28px}
  input,button{font:inherit;padding:10px 12px;border-radius:10px;border:1px solid rgba(186,210,232,.2);background:#0b1224;color:#fff}
  button{background:#67e8f9;color:#06111e;font-weight:800;border:0;cursor:pointer}
  article{border:1px solid rgba(186,210,232,.16);border-radius:18px;padding:18px 20px;margin:0 0 14px;background:#0a1222}
  article h2{margin:0 0 8px;font-size:18px}
  article pre{white-space:pre-wrap;color:#d7e3f2;font-size:13px}
  .meta{color:#9beaf7;font-size:12px;font-weight:700;margin-bottom:8px}
</style>
</head>
<body>
<main>
  <h1>Intake inbox</h1>
  <p>Submissions from the project form. Sign in with the admin key in data/admin.key.</p>
  <form method="get" action="/admin">
    <input type="password" name="key" placeholder="Admin key" required>
    <button type="submit">Open inbox</button>
  </form>
  %CONTENT%
</main>
</body>
</html>
"""


class RelogicHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path in ("/admin", "/admin/"):
            return self.admin(parse_qs(parsed.query))
        if path == "/api/leads":
            return self.api_leads(parse_qs(parsed.query))
        target = self.resolve(path)
        if target:
            qs = f"?{parsed.query}" if parsed.query else ""
            self.path = target + qs
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path.rstrip("/") == "/api/intake":
            return self.api_intake()
        self.send_error(404, "Unknown endpoint")

    def api_intake(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length > 200000:
            return self.json_response(413, {"ok": False, "error": "payload too large"})
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("object required")
        except Exception:
            return self.json_response(400, {"ok": False, "error": "invalid json"})

        name = str(payload.get("name") or "").strip()
        email = str(payload.get("email") or "").strip()
        if not name or not email or "@" not in email:
            return self.json_response(422, {"ok": False, "error": "name and email required"})

        payload["ip"] = self.client_address[0]
        payload["userAgent"] = self.headers.get("User-Agent", "")
        record = save_lead(payload)
        return self.json_response(201, {"ok": True, "id": record["id"], "receivedAt": record["receivedAt"]})

    def authorized(self, query):
        header = self.headers.get("X-Admin-Key") or self.headers.get("Authorization", "")
        token = ""
        if header.lower().startswith("bearer "):
            token = header.split(" ", 1)[1]
        elif header:
            token = header
        if not token:
            token = (query.get("key") or [""])[0]
        return token == ADMIN_KEY

    def admin(self, query):
        if not self.authorized(query):
            return self.html_response(401, ADMIN_PAGE.replace("%CONTENT%", ""))
        blocks = []
        for row in list_leads():
            payload = row.get("payload") or {}
            title = "%s · %s" % (payload.get("name") or "Unknown", payload.get("email") or "")
            blocks.append(
                "<article><div class='meta'>%s · %s</div><h2>%s</h2><pre>%s</pre></article>"
                % (
                    row.get("id"),
                    row.get("receivedAt"),
                    self._esc(title),
                    self._esc(json.dumps(payload, indent=2)),
                )
            )
        html = ADMIN_PAGE.replace("%CONTENT%", "".join(blocks) or "<p>No submissions yet.</p>")
        return self.html_response(200, html)

    def api_leads(self, query):
        if not self.authorized(query):
            return self.json_response(401, {"ok": False, "error": "unauthorized"})
        return self.json_response(200, {"ok": True, "leads": list_leads()})

    def resolve(self, path):
        if path == "/":
            return "/index.html"
        clean = path.rstrip("/")
        for cand in (
            clean + "/index.html",
            path.rstrip("/") + "/index.html",
            clean + ".html",
            path,
        ):
            fs = ROOT / cand.lstrip("/")
            if fs.is_file():
                return "/" + fs.relative_to(ROOT).as_posix()
        return None

    def json_response(self, code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def html_response(self, code, html):
        body = html.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @staticmethod
    def _esc(value):
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        SimpleHTTPRequestHandler.end_headers(self)


def main():
    mimetypes.add_type("image/svg+xml", ".svg")
    port = int(os.environ.get("PORT", "4173"))
    server = ThreadingHTTPServer(("0.0.0.0", port), RelogicHandler)
    print("Relogic at http://127.0.0.1:%s/" % port)
    print("Intake POST http://127.0.0.1:%s/api/intake" % port)
    print("Inbox      http://127.0.0.1:%s/admin?key=%s" % (port, ADMIN_KEY))
    server.serve_forever()


if __name__ == "__main__":
    main()
