#!/usr/bin/env python3
"""Shared storage and Telegram helpers for website leads."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("LEADS_DATA_DIR", str(ROOT / "data")))
SUBSCRIBERS_FILE = DATA_DIR / "leads_subscribers.json"
LEADS_LOG = DATA_DIR / "leads.jsonl"

# Prefer env on the server (/etc/skilldev-site.env). No secrets in the repo.
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
BOT_PASSWORD = os.environ.get("LEADS_BOT_PASSWORD", "skill-def-get-leads").strip()
TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_subscribers() -> list[int]:
    ensure_data_dir()
    if not SUBSCRIBERS_FILE.exists():
        return []
    try:
        raw = json.loads(SUBSCRIBERS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    out: list[int] = []
    for item in raw if isinstance(raw, list) else []:
        try:
            out.append(int(item))
        except (TypeError, ValueError):
            continue
    return out


def save_subscribers(chat_ids: list[int]) -> None:
    ensure_data_dir()
    unique = sorted(set(int(x) for x in chat_ids))
    SUBSCRIBERS_FILE.write_text(
        json.dumps(unique, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def add_subscriber(chat_id: int) -> bool:
    ids = load_subscribers()
    if chat_id in ids:
        return False
    ids.append(chat_id)
    save_subscribers(ids)
    return True


def remove_subscriber(chat_id: int) -> bool:
    ids = load_subscribers()
    if chat_id not in ids:
        return False
    save_subscribers([x for x in ids if x != chat_id])
    return True


def is_subscriber(chat_id: int) -> bool:
    return chat_id in load_subscribers()


def tg_request(method: str, payload: dict) -> dict:
    if not BOT_TOKEN:
        return {"ok": False, "description": "TELEGRAM_BOT_TOKEN is not set"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{TG_API}/{method}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"ok": False, "description": body or str(e)}
    except Exception as e:
        return {"ok": False, "description": str(e)}


def send_message(chat_id: int, text: str) -> bool:
    result = tg_request(
        "sendMessage",
        {"chat_id": chat_id, "text": text, "disable_web_page_preview": True},
    )
    return bool(result.get("ok"))


def format_lead_message(name: str, contact: str, message: str, lang: str = "") -> str:
    lines = [
        "🆕 Новая заявка",
        "",
        f"Имя: {name}",
        f"Контакт: {contact}",
        "",
        "Сообщение:",
        message,
    ]
    if lang:
        lines.extend(["", f"Язык сайта: {lang}"])
    return "\n".join(lines)


def append_lead_log(payload: dict) -> None:
    ensure_data_dir()
    with LEADS_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def broadcast_lead(name: str, contact: str, message: str, lang: str = "") -> dict:
    """Send lead to all authorized chats. Returns delivery stats."""
    text = format_lead_message(name, contact, message, lang)
    subscribers = load_subscribers()
    sent = 0
    failed: list[int] = []
    for chat_id in subscribers:
        if send_message(chat_id, text):
            sent += 1
        else:
            failed.append(chat_id)
    return {
        "subscribers": len(subscribers),
        "sent": sent,
        "failed": failed,
    }
