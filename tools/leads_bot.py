#!/usr/bin/env python3
"""Telegram bot: password auth, then receive website leads.

Usage:
  python3 tools/leads_bot.py

Env:
  TELEGRAM_BOT_TOKEN   — bot token
  LEADS_BOT_PASSWORD   — subscription password
  LEADS_DATA_DIR       — directory for subscribers JSON (default: ./data)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from leads_common import (  # noqa: E402
    BOT_PASSWORD,
    BOT_TOKEN,
    add_subscriber,
    is_subscriber,
    remove_subscriber,
    send_message,
    tg_request,
)


MSG_ASK_PASSWORD = (
    "👋 Бот заявок Skill Dev.\n\n"
    "Введите пароль для подписки на новые заявки с сайта."
)
MSG_OK = (
    "✅ Пароль принят. Вы подписаны на заявки.\n"
    "Команда /stop — отписаться."
)
MSG_ALREADY = (
    "✅ Вы уже подписаны на заявки.\n"
    "Команда /stop — отписаться."
)
MSG_BAD = "❌ Неверный пароль. Попробуйте ещё раз или отправьте /start."
MSG_STOPPED = "Вы отписаны от заявок. Чтобы подписаться снова — /start и пароль."
MSG_NEED_AUTH = "Сначала авторизуйтесь: отправьте /start и введите пароль."


def get_updates(offset: int | None) -> list[dict]:
    payload: dict = {"timeout": 25}
    if offset is not None:
        payload["offset"] = offset
    result = tg_request("getUpdates", payload)
    if not result.get("ok"):
        desc = result.get("description", "unknown error")
        print(f"[leads_bot] getUpdates failed: {desc}", file=sys.stderr)
        time.sleep(3)
        return []
    return result.get("result") or []


def handle_message(msg: dict) -> None:
    chat = msg.get("chat") or {}
    chat_id = chat.get("id")
    if chat_id is None:
        return
    chat_id = int(chat_id)
    text = (msg.get("text") or "").strip()
    if not text:
        return

    lower = text.lower()
    if lower in ("/start", "/start@skilldev_leads_bot"):
        if is_subscriber(chat_id):
            send_message(chat_id, MSG_ALREADY)
        else:
            send_message(chat_id, MSG_ASK_PASSWORD)
        return

    if lower in ("/stop", "/unsubscribe"):
        remove_subscriber(chat_id)
        send_message(chat_id, MSG_STOPPED)
        return

    if is_subscriber(chat_id):
        send_message(
            chat_id,
            "Вы подписаны. Новые заявки с сайта приходят сюда автоматически.\n"
            "/stop — отписаться.",
        )
        return

    if text == BOT_PASSWORD:
        add_subscriber(chat_id)
        send_message(chat_id, MSG_OK)
    else:
        send_message(chat_id, MSG_BAD)


def main() -> None:
    if not BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN is empty", file=sys.stderr)
        sys.exit(1)

    me = tg_request("getMe", {})
    if not me.get("ok"):
        print(f"Bot auth failed: {me.get('description')}", file=sys.stderr)
        sys.exit(1)

    username = (me.get("result") or {}).get("username", "?")
    print(f"[leads_bot] started as @{username}")
    print(f"[leads_bot] waiting for /start + password")

    offset: int | None = None
    while True:
        try:
            updates = get_updates(offset)
            for upd in updates:
                offset = int(upd["update_id"]) + 1
                msg = upd.get("message") or upd.get("edited_message")
                if msg:
                    handle_message(msg)
        except KeyboardInterrupt:
            print("\n[leads_bot] stopped")
            break
        except Exception as e:
            print(f"[leads_bot] error: {e}", file=sys.stderr)
            time.sleep(5)


if __name__ == "__main__":
    main()
