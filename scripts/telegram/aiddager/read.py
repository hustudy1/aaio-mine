#!/usr/bin/env python3
"""AI따거 그룹 최근 메시지 읽기."""

import os
import json
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN_KH")
CHAT_ID = -5297628070
OFFSET_FILE = os.path.join(os.path.dirname(__file__), ".offset")


def get_offset() -> int:
    if os.path.exists(OFFSET_FILE):
        return int(open(OFFSET_FILE).read().strip())
    return 0


def save_offset(offset: int):
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))


def read(limit: int = 20, mark_read: bool = False) -> list[dict]:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN_KH 환경변수가 없습니다.")
    offset = get_offset() if mark_read else 0
    resp = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
        params={"offset": offset, "limit": limit},
        timeout=10,
    )
    resp.raise_for_status()
    updates = resp.json().get("result", [])
    messages = []
    for u in updates:
        msg = u.get("message", {})
        if msg.get("chat", {}).get("id") == CHAT_ID:
            messages.append({
                "update_id": u["update_id"],
                "from": msg.get("from", {}).get("first_name", "unknown"),
                "text": msg.get("text", ""),
                "date": msg.get("date"),
            })
    if mark_read and updates:
        save_offset(updates[-1]["update_id"] + 1)
    return messages


if __name__ == "__main__":
    msgs = read(limit=20, mark_read=False)
    if not msgs:
        print("새 메시지 없음")
    else:
        for m in msgs:
            print(f"[{m['from']}] {m['text']}")
